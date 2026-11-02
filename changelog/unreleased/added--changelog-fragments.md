- **Changelog fragments** — feature PRs record release notes as files under
  `changelog/unreleased/` (`<section>--<slug>.md`) instead of editing
  `CHANGELOG.md`, whose `[Unreleased]` anchor was the recurring conflict of
  the gap-closure PR series. `scripts/changelog_fragments.py` validates
  fragments (`make check-changelog`, wired into VALIDATE) and
  `scripts/release.sh` folds them into `[Unreleased]` before stamping the
  version, so `CHANGELOG.md` has exactly one writer: the release itself.
