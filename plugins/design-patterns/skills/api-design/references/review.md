# Review — grade a contract against the AIPs

Scope: reviewing an existing `.proto`, OpenAPI spec, or endpoint list, and
evolving a live API without breaking its callers. Severity uses the reviewer
plugin's scale (BLOCKER / IMPORTANT / SUGGESTION) but follows **impact, not
requirement level**.

## Contents

- [Release-status gate](#release-status-gate)
- [Finding shape](#finding-shape)
- [Severity](#severity)
- [Output](#output)
- [Evolving a live API](#evolving-a-live-api)

## Release-status gate

Before the first finding, establish whether the surface is live and at what
stability level. On a live API, "fix this must violation" can itself be the
breaking change — the remediation changes, not the finding. If the status is
unknown, treat the surface as live, say so, and ask once. A fix that changes
only error behaviour is still a behaviour change (AIP-180): offer it in place
only if the owners accept that.

Scan the spec for tokens (the map's middle column), retrieve one AIP per
finding category present, and reuse the ledger. Before reporting a finding,
try to falsify it: is it explained by the team standard, local consistency
(AIP-200), the method's plane, or the rule's own condition?

## Finding shape

Each finding carries: location (`path:line` or `METHOD /path`) · issue ·
basis (claim type, citation, level) · impact (correctness /
breaking-to-fix-later / consistency / style) · remediation · severity.

Remediation is one of:

- **In place** — unreleased surfaces, or a live correctness fix the owners
  accept as a behaviour change.
- **Additive, then deprecate** — add the conformant form alongside the old
  one and retire the old one on the deprecation path (AIP-180, AIP-185).
- **New major version.**
- **Documented deviation** — a Deviations row and a `not-precedent` comment.
  When the review has no design doc to hold the row, list the deviation in
  the review's own output and recommend where it should live.

## Severity

| Severity       | Use when                                                                                                                                       |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **BLOCKER**    | Correctness, security, or data-integrity defect in the contract (errors returned as 2xx, verb semantics broken); a change that breaks existing callers; an unreleased structural choice that is breaking to fix later (a List with no page token, or a bare-array response) |
| **IMPORTANT**  | Departs from an approved AIP or a [SPEC] wire convention with a named cost — consistency, client friction, a future breaking change. On a live API, remediate additively or record a deviation; a live structural defect whose only fix breaks callers lands here, with a next-major plan |
| **SUGGESTION** | Style and polish; may-level guidance; should-level guidance with no named cost                                                                  |

A should-level rule with a correctness impact is a BLOCKER; a must-level
rule whose only fix breaks live callers is IMPORTANT with a deviation and a
next-major plan. Never propose an in-place rename on a live API.

## Output

Findings table → top three by impact (correctness, then breaking-to-fix-later,
then consistency, then style) → a short "already right" list → References
with the attribution line from
[`design-doc.md`](design-doc.md#references-and-attribution). No findings is a
valid result; say so plainly.

## Evolving a live API

1. Retrieve AIP-180 and AIP-185 (plus AIP-184 for date- or header-based
   versions) and the AIPs of whatever changes.
2. Classify every change as additive or breaking, citing AIP-180's category.
3. Breaking changes get a new major version, or an additive path plus
   deprecation; never a silent in-place change.
4. Keep local consistency (AIP-200) over the global standard inside one
   surface; record every exception with `not-precedent`.
