# API design skill — source dossier

- **Date:** 2026-10-11
- **Status:** applied; verification in §6; release pending (`make release`)
- **Trigger:** The maintainer drafted an "API Design (Google AIP style,
  researched and cited)" skill and asked for it to be improved: clear
  direction to web-search whenever unsure, proper citation when a design doc
  justifies a choice from Google's guidance, and the same discipline when
  implementing. Three parallel audits ran against the draft — sources,
  skill architecture, and a red team that executed it. This dossier is the
  source of truth for the skill's stances; Google facts live in the companion
  canon, [`../research/2026-10-11-aip-canon.md`](../research/2026-10-11-aip-canon.md).
  Change a stance here, or a fact there, before changing the skill.

## 1. Evidence

**Source audit** (full results in the canon). Fourteen corrections to the
draft, most consequentially: AIP-184 (API version identifiers) and
interface-based versioning in AIP-185 landed 2026-08-17 and were missing;
`:predict` is Vertex AI precedent, not an AIP, and its `endpoint` field
departs from AIP-136; every Cloud Design Guide chapter now redirects to an
AIP except Introduction, Directory structure, and Changelog, and the guide's
changelog does not track AIP changes; the only OpenAPI ruleset in reach
(AEP's) conflicts with AIPs on six rules; AIP text is CC BY 4.0 but code
samples are Apache 2.0, and Google asks for a specific modified-versions
notice.

**Skill-architecture audit.**

- The draft had no frontmatter, so it could never auto-trigger — and
  `claude plugin validate` passes it with only a warning.
- The validator does not enforce the agentskills spec (name vs directory,
  description length); a separate check is needed.
- `paths` frontmatter is inert for plugin skills in Claude Code 2.1.296 and
  hides skills in skill-directory installs until a matching file is touched
  — harmful for a skill whose main use is a design doc with no spec open.
- Review severity keyed to must/should can mandate a breaking change on a
  live API.

**Red team** — the draft executed for real on an ML-platform design (REST,
FastAPI), a review of a deliberately non-AIP OpenAPI spec, an implement task,
and niche lookups.

- Cost: 36 fetches and 4 searches for one design; 20 used, 7 partly, 9 not
  at all. The sources actually needed for REST (ProtoJSON,
  `google/rpc/code.proto`, `google/longrunning/operations.proto`, product
  protos) were not sanctioned by the draft.
- Fidelity: ten defects between a summary and the AIP source, for example
  AIP-148 summarized as requiring `create_time` on every resource (it
  constrains meaning if present), AIP-121's strong consistency stripped of
  its management-plane scope, AIP-122's embedding exceptions dropped, a
  bolded Warning in AIP-158 inflated to "must not", and search summaries
  deflating AIP-156's "must not" to "should not".
- Search: domain-filtered queries leaked off-domain results; user vocabulary
  ("settings", "model versions") missed the AIP terms (singleton, revisions);
  bare "AIP" matched other products.
- REST pitfalls observed on FastAPI 0.143 / Starlette 1.7 / Pydantic 2.14:
  a generic `GET /x/{id}` captures `/x/a:verb`; `extra="forbid"` rejects
  round-tripped output-only fields with 422; validation errors are not the
  AIP-193 envelope; `timedelta` serializes as ISO 8601, not ProtoJSON's
  `"3.5s"`.

## 2. Diagnosis

1. **Undeliverable.** No frontmatter, no triggers.
2. **Fetched was treated as verified.** Summaries corrupt levels,
   conditions, and exceptions; "keep the requirement level" cannot hold when
   the retrieval itself loses it.
3. **Every Google statement was an AIP rule.** With no claim taxonomy and no
   sanctioned wire-spec sources, the agent omits wire details, states them
   from memory, or launders them under an unrelated AIP.
4. **Thoroughness meant fetching everything** — two indexes and a fixed core
   on every task, no depth by task size, no ledger reuse.
5. **Missing modes.** No implement mode (the user's explicit third ask), no
   evolve mode, no quick-question mode; review severity unsafe on live APIs.
6. **No calibration.** Nothing stops `projects/*/locations/*`, LROs, etags,
   and request IDs being copied onto a small internal API.
7. **Incomplete precedence.** "Team standard wins" had no safety floor, no
   existing-surface tier, and no rule for AIP-vs-AIP conflicts.

## 3. Stances (what the skill encodes)

1. **Research director, hybrid genre.** Freeze only what this repo decides —
   claim types, citation format, template slots, severity mapping, where
   citations go in code, routing, calibration. Retrieve everything Google
   decides. The citation list is the fetch list.
2. **Retrieval ladder:** context7 `/aip-dev/google.aip.dev` (verbatim), raw
   AIP markdown with a keyword grep (exact), the rendered page with a
   per-rule extraction prompt, and search for discovery only. Never cite a
   search summary; never guess a URL or an anchor.
3. **Observable triggers replace "when unsure".** Eight predicates (about to
   state a Google-attributed specific not in the ledger, recalled-but-
   unretrieved AIP, unmapped topic, disagreement, non-proto surface,
   non-approved or stale AIP, load-bearing claim, unseen anchor), plus a
   vocabulary bridge for search.
4. **Six claim types; only [AIP] says must, should, or may.** [AIP-DRAFT],
   [SPEC], [PRECEDENT], [TEAM], and [JUDGMENT] carry their own phrasing, and
   "AIPs are silent on X" is a valid claim.
5. **Precedence with a floor.** Correctness, security, and data integrity
   are never silently overridden; then the user's instruction, live-API
   compatibility (AIP-180), local consistency (AIP-200), the team standard,
   approved AIPs, [SPEC], [PRECEDENT], drafts, judgment.
6. **Calibration:** adopt now what is breaking to add later; defer what is
   additive; copy no Google infrastructure; T1/T2/T3 tiers decide the
   optional machinery.
7. **Review severity follows impact,** on the reviewer's BLOCKER /
   IMPORTANT / SUGGESTION scale; never an in-place rename on a live API.
8. **Implement mode:** tests first for adopted AIP behaviour; citations at
   decision sites only; deviations through AIP-200's `not-precedent`
   convention, mirrored in the design's Deviations table; the `(-- … --)`
   internal-comment stripping is Google tooling, so check the doc generator.
9. **REST is modelled, then rendered:** AIP-127 for HTTP, ProtoJSON as
   [SPEC] for JSON; AEP is an OpenAPI-mechanics aid with its conflicting
   rules disabled, never a justification.
10. **Attribution** follows Google's licensing page: the modified-versions
    notice, the CC BY 4.0 link, the changes made, and Apache 2.0 for code.

## 4. What this is not

- Not a digest of AIP rules — the stale-priors list is prompts to retrieve,
  dated, never citations.
- Not channel choice, reliability mechanics, client SDKs, GraphQL,
  AsyncAPI, or AuthN/AuthZ mechanisms; the hub's NOT-covered list routes
  each.

## 5. Edit map (applied)

| File | Change |
| --- | --- |
| `plugins/design-patterns/skills/api-design/SKILL.md` | New hub: anchors, research protocol, triggers, claim types, precedence, calibration, red flags, routing, verification, boundaries |
| `…/api-design/references/aip-map.md` | Topic-to-AIP map with spec tokens and G/P/D/R flags, vocabulary bridge, stale priors, source mechanics, second-tier sources |
| `…/api-design/references/design-doc.md` | Template with REQUIRED/CONDITIONAL slots, calibration tiers, worked rows, References and attribution |
| `…/api-design/references/review.md` | Release-status gate, finding shape, impact-based severity, evolving a live API |
| `…/api-design/references/implement.md` | Tests first, citation placement, framework notes, done criteria |
| `…/api-design/references/rest-and-openapi.md` | Translation table, OpenAPI linting with the corrected AEP ruleset |
| `plugins/design-patterns/skills/system/SKILL.md` | NOT-covered bullet routing API contract questions to `api-design` |
| `plugins/design-patterns/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Descriptions and keywords |
| `README.md`, `CHANGELOG.md` | Catalogue row; `[Unreleased]` entries |
| `.agents/plugins/marketplace.json`, `plugins/*/.codex-plugin/plugin.json` | Regenerated by `make sync-codex` |

## 6. Verification

- Spec, budget, TOC, link, and anchor check (scratch script mirroring the
  audit's F9 gap): exit 0; name equals directory; listing 777 characters
  (description 442 + when_to_use 334), under the ~800 house target; hub 301
  lines, about 4.6k tokens.
- `markdownlint` 0.34.0 with `.markdownlint.json`: only MD013 on table rows,
  which the house tolerates.
- `claude plugin validate ./plugins/design-patterns` and `make validate`:
  passed.
- Every concrete URL in the skill returned 200, as did instantiated forms of
  the six placeholder patterns; the two anchors used were seen in the live
  HTML.
- The YAML ruleset parses; the Python sketch passes `ast.parse`.
- `make sync-codex`: the Codex `plugin.json` is byte-identical to the Claude
  one; `.agents/` changed only in the design-patterns entry.
- Listing budget: shipped total rises from 21,174 to 21,951 characters at
  release, already over the ~15,000 default (audit F1, pre-existing).
- Not run: a live trigger eval. `claude --plugin-dir` needs the installed
  copy disabled first to avoid a duplicate plugin name.
- **Red-team recheck of the built skill** (same agent that executed the
  draft; evidence reused, nothing re-fetched): 13 of its 16 findings fixed,
  3 partly fixed. It found 7 factual errors, 4 self-inconsistencies, and 6
  review-mode ambiguities, and each was confirmed at source before applying.
  Applied:
  - the inverted AIP-122 embedding rule;
  - ErrorInfo's 2023-05-10 date;
  - three more AEP overrides;
  - the WebFetch verbatim claim;
  - the FastAPI capture example;
  - client-library range 4210–4290;
  - the Design Guide's three first-party pages;
  - a [SPEC] label on JSON casing;
  - the org-AIP block moved to the map with its source;
  - a REST path in the worked row;
  - one basis label per deviation row;
  - review defaults for unknown release status and in-place correctness
    fixes;
  - severity rows for [SPEC] departures and live structural defects;
  - the IBV date format;
  - a T1 compact-form rule;
  - a calibration item in the verification checklist.
  `allowed-tools` gained `WebSearch` and `raw.githubusercontent.com` so the
  top-ranked retrieval routes do not stall on permission prompts. Its S2 dry
  run then produced the right severities, remediations, basis labels, and top
  three. All gates re-run green after the edits; 19 concrete URLs return 200.

## 7. Rejected alternatives

- **A new `omniagents-api` plugin.** Moving a skill later renames it, a
  major bump; justified only if two or more API-family skills are planned.
- **Naming it `api-and-interface-design`.** The curated `workflow` import
  references that name, but "interface" collides with `codebase-design` and
  the name invites a collision if the upstream skill is ever imported.
- **`paths` frontmatter.** Inert for plugin skills, harmful in skill dirs.
- **A bundled extraction script.** context7 plus a one-line raw grep cover
  exact wording without code to maintain.
- **Mandatory index and Design Guide fetches on every task.** The index is
  read once per design or review session; the guide only for its own pages.
- **Must-fix / nice-to-have severity.** Replaced by impact-based severity on
  the reviewer scale.
- **Preloading into reviewer agents.** They have no web tools, so the
  research protocol could not run.

## 8. Open items

- Run a trigger eval (three should-trigger, three should-not prompts) before
  release.
- AIP-184 and AIP-185 disagree on a request that omits a version
  identifier; the sources do not resolve it, so the skill cites both.
- Re-verify the map when it is six months old or the index lists AIPs the
  map lacks.
- Maintainer decisions outside this change: the repo-wide `paths` cleanup
  (15 skills), committing the spec-check script under `scripts/`, and the
  frontmatter-defaults conflict between audit P5 and the lua dossier §6
  (this skill follows §6).
