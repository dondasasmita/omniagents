# Design doc — the API section

Scope: the shape of the API section of a design doc or RFC, the calibration
tiers that decide how much Google ceremony it carries, and the References and
attribution block that closes it. Claim types (**[AIP]**, **[SPEC]**,
**[PRECEDENT]**, **[TEAM]**, **[JUDGMENT]**, **[AIP-DRAFT]**) are defined in
[`../SKILL.md`](../SKILL.md#claims-and-citations).

## Contents

- [Template rules](#template-rules)
- [Calibration tiers](#calibration-tiers)
- [Template](#template)
- [Worked rows](#worked-rows)
- [References and attribution](#references-and-attribution)

## Template rules

- **REQUIRED** slots always appear. **CONDITIONAL** slots appear with a
  one-line `N/A — <reason>` when they do not apply; never delete them
  silently, because an absent slot reads as an omission.
- Every decision table has a **Basis** column holding the claim type and its
  citation. A decision with no Google source is **[JUDGMENT]** with a reason,
  not a stretched AIP link.
- Company-neutral: no product, organization, or team names in reusable
  text; neutral example resources. Permissions follow the org's own scheme —
  Google IAM strings are Google-specific.
- Every `[unverified]` item and every unresolved conflict lands in Open
  questions.
- **Scale prose to the tier, not the slot count.** At T1, sections 3, 5, 8,
  9, and 10 may each be a single line; the slot still has to be there.

## Calibration tiers

**At every tier, adopt now** — each is breaking to add later: resource-
oriented paths and stable IDs; standard methods before custom ones; the
major version in the path; List responses paginated from day one; one error
envelope; per method, a fixed choice between a synchronous response and an
operation; one JSON casing and one time encoding. Retrieve the owning AIP for
each before citing it.

**Defer what is additive,** listing each deferred item under Future additive
options with its AIP:

| Decision                         | T1 single-team internal               | T2 internal platform                          | T3 external or declarative                                |
| -------------------------------- | ------------------------------------- | --------------------------------------------- | --------------------------------------------------------- |
| Hierarchy depth                  | Flat collections unless real ownership | Parent is the tenancy boundary                | Whatever the domain's ownership requires                  |
| Location in resource names       | No                                    | Only if region is part of identity            | Same rule; residency often makes it identity              |
| Etags (154)                      | Defer                                 | Where concurrent edits matter                 | Retrieve 128 and 154 — declarative clients depend on them |
| Request IDs (155)                | Defer                                 | Creates with costly side effects              | Mutations clients will retry                              |
| Filtering and ordering (160, 132) | Defer                                | When a named consumer needs it                | When a named consumer needs it                            |
| Soft delete (164)                | Defer                                 | When recovery is a requirement                | When recovery or retention policy requires it             |
| Batch methods (231–235)          | Defer                                 | When chattiness is measured                   | When chattiness is measured                               |
| Revisions (162, draft)           | Defer                                 | Defer; cite as **[AIP-DRAFT]**                | Cite as **[AIP-DRAFT]**                                   |

Long-running work is not a tier choice: retrieve AIP-151 and apply its
latency guidance to each method. Add a hierarchy level only for ownership,
tenancy, or lifecycle — each level brings parent fields, cascading-delete
rules (AIP-135), and cross-collection reads (AIP-159, AIP-217).

## Template

~~~markdown
## API design: <API name>

### 0. Anchors (REQUIRED)
Surface (proto / REST / both) · release status and stability level ·
consumers and tier (T1/T2/T3) · local standard (link or "none found") ·
non-goals.

### 1. Resources (REQUIRED)
| Resource | Name pattern | Parent | Key fields | Basis |

### 2. Methods (REQUIRED)
| Method | HTTP verb and path | Request | Response | Idempotency / concurrency | Basis |

### 3. Wire format (REQUIRED for REST and transcoded APIs)
Casing, timestamps, durations, enums, 64-bit integers, field masks —
each with its [SPEC] source.

### 4. Examples (REQUIRED)
JSON request and response for the main calls. Every example parses and
matches the tables above.

### 5. Errors (REQUIRED)
| Condition | Canonical code | HTTP status | ErrorInfo reason | Basis |

### 6. Pagination, filtering, ordering (CONDITIONAL: any List)
Page size default and maximum, token behaviour, filter and order support.

### 7. Long-running work (CONDITIONAL: any method past AIP-151's guidance)
Which methods return operations, polling path, cancellation, metadata.

### 8. Versioning and compatibility (REQUIRED)
Versioning strategy, stability level, and for each change: additive or
breaking, with the migration path.

### 9. Authorization (REQUIRED)
| Method | Permission (org scheme) | Behaviour without access |

### 10. Future additive options (REQUIRED; "none" with a reason is valid)
| Option | AIP | Trigger that would justify it |

### 11. Deviations and conflicts (REQUIRED; empty is valid)
| ID | Rule (level) | Choice | Basis | Who decided | Cost to reverse |

### 12. Open questions (REQUIRED)
Every [unverified] claim and every unresolved conflict.

### 13. References (REQUIRED)
| Source | Title | URL | State | Retrieved |
<attribution line>
~~~

## Worked rows

A cited decision, in a Methods table:

| Method      | HTTP verb and path                    | Response            | Basis                                                                              |
| ----------- | ------------------------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| `ListBooks` | `GET /v1/shelves/{shelf}/books`       | `ListBooksResponse` | **[AIP]** [AIP-132](https://google.aip.dev/132), [AIP-158](https://google.aip.dev/158): pagination present from day one (levels as retrieved) |

A judgment, phrased so it cannot pass for a rule:

> **[JUDGMENT]** Shelves stay top-level rather than under a `libraries/*`
> parent: no consumer needs per-library isolation, and AIPs are silent on
> when to add a level.

A deviation:

| ID | Rule (level)                                  | Choice                                   | Basis                                                     | Who decided | Cost to reverse                        |
| -- | --------------------------------------------- | ---------------------------------------- | --------------------------------------------------------- | ----------- | -------------------------------------- |
| D1 | [AIP-134](https://google.aip.dev/134) (should: PATCH) | Keep `PUT` for existing v1 clients | **[AIP]** live-API compatibility outranks it ([AIP-180](https://google.aip.dev/180)); add `PATCH` alongside | API owners  | Remove `PUT` at the next major version |

## References and attribution

One row per source in the ledger — the AIP number or page name, its title,
the canonical URL, its state (approved, draft, reviewing), and the retrieval
date. [SPEC] and [PRECEDENT] sources get rows too.

Close with this line, adapted from the notice Google's
[licensing page](https://google.aip.dev/licensing) asks for on modified
versions:

> Portions of this document are modifications based on work created and
> shared by Google and used according to terms described in the
> [Creative Commons 4.0 Attribution License](https://creativecommons.org/licenses/by/4.0/).
> Changes: paraphrased, condensed, and applied to this design. Code samples
> adapted from AIP pages are licensed under Apache 2.0.

Freshness: template and tiers settled 2026-10-11; the attribution wording
follows google.aip.dev/licensing as read that day.
