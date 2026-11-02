import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from changelog_fragments import assemble, collect_fragments

HEADER = "# Changelog\n\nIntro.\n\n## [Unreleased]\n\n## [1.0.0] - 2026-01-01\n\n### Added\n\n- Old thing.\n"


def write_fragment(tmp_path, name, text):
    frag_dir = tmp_path / "changelog" / "unreleased"
    frag_dir.mkdir(parents=True, exist_ok=True)
    path = frag_dir / name
    path.write_text(text, encoding="utf-8")
    return frag_dir


def test_collect_valid(tmp_path):
    frag_dir = write_fragment(tmp_path, "fixed--catalogue-hygiene.md", "- **A** — fixed.\n  Second line.\n")
    by_section, errors = collect_fragments(frag_dir)
    assert errors == []
    assert by_section == {
        "fixed": [(frag_dir / "fixed--catalogue-hygiene.md", ["- **A** — fixed.", "  Second line."])]
    }


def test_collect_rejects_bad_section_name(tmp_path):
    frag_dir = write_fragment(tmp_path, "notes--typo.md", "- entry\n")
    _, errors = collect_fragments(frag_dir)
    assert len(errors) == 1
    assert "notes--typo.md" in errors[0]


def test_collect_rejects_non_bullet_content(tmp_path):
    frag_dir = write_fragment(tmp_path, "added--prose.md", "Just prose.\n")
    _, errors = collect_fragments(frag_dir)
    assert len(errors) == 1
    assert "added--prose.md" in errors[0]


def test_collect_rejects_empty_fragment(tmp_path):
    frag_dir = write_fragment(tmp_path, "added--empty.md", "\n \n")
    _, errors = collect_fragments(frag_dir)
    assert len(errors) == 1


def test_collect_missing_dir_is_noop(tmp_path):
    by_section, errors = collect_fragments(tmp_path / "changelog" / "unreleased")
    assert by_section == {}
    assert errors == []


def test_assemble_creates_sections_in_canonical_order(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(HEADER, encoding="utf-8")
    frag_dir = write_fragment(tmp_path, "fixed--b.md", "- **B** — fixed.\n")
    write_fragment(tmp_path, "added--a.md", "- **A** — added.\n")

    assert assemble(changelog, frag_dir) == 0
    assert changelog.read_text(encoding="utf-8") == (
        "# Changelog\n"
        "\n"
        "Intro.\n"
        "\n"
        "## [Unreleased]\n"
        "\n"
        "### Added\n"
        "\n"
        "- **A** — added.\n"
        "\n"
        "### Fixed\n"
        "\n"
        "- **B** — fixed.\n"
        "\n"
        "## [1.0.0] - 2026-01-01\n"
        "\n"
        "### Added\n"
        "\n"
        "- Old thing.\n"
    )
    assert not list(frag_dir.glob("*.md"))


def test_assemble_appends_without_reordering(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        HEADER.replace(
            "## [Unreleased]\n",
            "## [Unreleased]\n\n### Fixed\n\n- Existing fix.\n\n### Added\n\n- Existing add.\n",
        ),
        encoding="utf-8",
    )
    frag_dir = write_fragment(tmp_path, "fixed--new.md", "- **New** — fix.\n")
    write_fragment(tmp_path, "changed--new.md", "- **New** — change.\n")

    assert assemble(changelog, frag_dir) == 0
    unreleased = changelog.read_text(encoding="utf-8").split("## [1.0.0]")[0]
    assert unreleased.endswith(
        "### Fixed\n\n- Existing fix.\n- **New** — fix.\n\n### Added\n\n- Existing add.\n\n### Changed\n\n- **New** — change.\n\n"
    )


def test_assemble_noop_without_fragments_leaves_file_untouched(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(HEADER, encoding="utf-8")
    assert assemble(changelog, tmp_path / "changelog" / "unreleased") == 0
    assert changelog.read_text(encoding="utf-8") == HEADER


def test_assemble_requires_unreleased_heading(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.0.0] - 2026-01-01\n", encoding="utf-8")
    frag_dir = write_fragment(tmp_path, "fixed--x.md", "- x\n")
    assert assemble(changelog, frag_dir) == 1


def test_assemble_aborts_on_invalid_fragment(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    original = HEADER
    changelog.write_text(original, encoding="utf-8")
    frag_dir = write_fragment(tmp_path, "bogus.md", "- x\n")

    assert assemble(changelog, frag_dir) == 1
    assert changelog.read_text(encoding="utf-8") == original
    assert (frag_dir / "bogus.md").exists()


def test_assemble_merges_duplicate_section_headings(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        HEADER.replace(
            "## [Unreleased]\n",
            "## [Unreleased]\n\n### Changed\n\n- First change.\n\n### Changed\n\n- Second change.\n",
        ),
        encoding="utf-8",
    )
    frag_dir = write_fragment(tmp_path, "changed--third.md", "- **Third** — change.\n")

    assert assemble(changelog, frag_dir) == 0
    unreleased = changelog.read_text(encoding="utf-8").split("## [1.0.0]")[0]
    assert unreleased.count("### Changed") == 1
    assert unreleased.endswith(
        "### Changed\n\n- First change.\n\n- Second change.\n- **Third** — change.\n\n"
    )


def test_assemble_keeps_multiline_entries_verbatim(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(HEADER, encoding="utf-8")
    frag_dir = write_fragment(
        tmp_path,
        "added--multi.md",
        "- **Long** — first line\n  wraps with a two-space indent.\n- second bullet\n",
    )

    assert assemble(changelog, frag_dir) == 0
    body = changelog.read_text(encoding="utf-8")
    assert "- **Long** — first line\n  wraps with a two-space indent.\n- second bullet\n" in body
