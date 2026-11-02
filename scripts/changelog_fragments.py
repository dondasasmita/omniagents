#!/usr/bin/env python3
"""Changelog fragments: per-PR note files assembled into CHANGELOG.md at release.

A fragment is changelog/unreleased/<section>--<slug>.md holding the exact
bullet lines that belong under the matching "### <Section>" heading of
[Unreleased]. Feature PRs add fragments and never edit CHANGELOG.md;
scripts/release.sh folds pending fragments into [Unreleased] right before
stamping the version.

Usage:
  changelog_fragments.py check   [fragment_dir]
  changelog_fragments.py assemble [CHANGELOG.md] [fragment_dir]
"""

import re
import sys
from pathlib import Path

SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")
NAME_RE = re.compile(
    r"^(added|changed|deprecated|removed|fixed|security)"
    r"--[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
UNRELEASED_RE = re.compile(r"^## \[Unreleased\]\s*$")
H2_RE = re.compile(r"^## ")


def collect_fragments(fragment_dir):
    by_section, errors = {}, []
    if not fragment_dir.is_dir():
        return by_section, errors
    for path in sorted(fragment_dir.iterdir()):
        if not path.is_file():
            continue
        match = NAME_RE.match(path.name)
        if not match:
            errors.append(
                f"{path.name}: name must be <section>--<slug>.md with section "
                "one of " + ", ".join(s.lower() for s in SECTIONS)
            )
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        while lines and not lines[-1].strip():
            lines.pop()
        content = [ln for ln in lines if ln.strip()]
        if not content or not content[0].startswith("- "):
            errors.append(f"{path.name}: content must start with a '- ' bullet")
            continue
        by_section.setdefault(match.group(1), []).append((path, lines))
    return by_section, errors


def assemble(changelog_path, fragment_dir):
    by_section, errors = collect_fragments(fragment_dir)
    for err in errors:
        print(f"error: {err}", file=sys.stderr)
    if errors:
        return 1
    if not by_section:
        return 0

    lines = changelog_path.read_text(encoding="utf-8").splitlines()
    head = next((i for i, ln in enumerate(lines) if UNRELEASED_RE.match(ln)), None)
    if head is None:
        print(
            f"error: {changelog_path} has no '## [Unreleased]' heading",
            file=sys.stderr,
        )
        return 1
    end = head + 1
    while end < len(lines) and not H2_RE.match(lines[end]):
        end += 1
    block = lines[head + 1 : end]

    segments = []
    index = {}

    def absorb(title, body):
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        if title is None and not body:
            return
        if title in index:
            existing = segments[index[title]][1]
            if existing and body:
                existing.append("")
            existing.extend(body)
            return
        index[title] = len(segments)
        segments.append([title, body])

    title, body = None, []
    for ln in block:
        if ln.startswith("### "):
            absorb(title, body)
            title, body = ln[4:].strip(), []
        else:
            body.append(ln)
    absorb(title, body)

    consumed = []
    for section in SECTIONS:
        entries = by_section.get(section.lower())
        if not entries:
            continue
        bullets = []
        for path, entry_lines in entries:
            bullets.extend(entry_lines)
            consumed.append(path)
        if section in index:
            segments[index[section]][1].extend(bullets)
        else:
            index[section] = len(segments)
            segments.append([section, bullets])

    new_block = []
    for t, b in segments:
        if t is None:
            chunk = b
        else:
            chunk = [f"### {t}", ""] + b
        if not chunk:
            continue
        if new_block:
            new_block.append("")
        new_block.extend(chunk)

    new_lines = lines[: head + 1] + [""] + new_block + [""] + lines[end:]
    changelog_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    for path in consumed:
        path.unlink()
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("check", "assemble"):
        print("usage: changelog_fragments.py check|assemble [...]", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parent.parent
    if argv[1] == "check":
        fragment_dir = Path(argv[2]) if len(argv) > 2 else root / "changelog/unreleased"
        by_section, errors = collect_fragments(fragment_dir)
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        if errors:
            return 1
        count = sum(len(v) for v in by_section.values())
        print(f"ok: {count} fragment(s) well-formed" if count else "ok: no fragments pending")
        return 0
    changelog_path = Path(argv[2]) if len(argv) > 2 else root / "CHANGELOG.md"
    fragment_dir = Path(argv[3]) if len(argv) > 3 else root / "changelog/unreleased"
    return assemble(changelog_path, fragment_dir)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
