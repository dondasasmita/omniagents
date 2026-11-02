- **Series PR workflow** — the fork-based PR series now merges as a local
  branch stack: each branch rebases onto its predecessor, PRs target `main`
  and merge strictly in stack order, and after every merge
  `git rebase --update-refs origin/main` from the stack tip updates the whole
  chain in one pass. README → *Versioning and releases* documents the
  discipline.
