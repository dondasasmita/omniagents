# AIP map — where each rule lives

Scope: routing from a design topic, a spec token, or a user's phrase to the
AIP that owns it, plus the facts about Google's sources that change how you
retrieve and cite them. The **Decides** column names the question an AIP
answers, never its answer — retrieve the page for that, per the research
protocol in [`../SKILL.md`](../SKILL.md#research-protocol--retrieve-what-you-cite-cite-what-you-retrieved).

## Contents

- [Topic map](#topic-map)
- [Vocabulary bridge](#vocabulary-bridge)
- [Stale priors](#stale-priors)
- [Source mechanics](#source-mechanics)
- [Second-tier sources](#second-tier-sources)

## Topic map

General AIPs live at `https://google.aip.dev/{n}`. Flags: **G** Google-specific
— translate to the org's equivalent, never copy · **P** proto-only · **D**
Draft · **R** Reviewing (cite with the state, never as a requirement).

| Topic                                | Spec tokens you will see                                                       | AIP                         | Decides                                                                              | Flags |
| ------------------------------------ | ------------------------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------------------------------ | ----- |
| Resource model                       | collection paths, `parent`, child collections                                 | 121, 124                    | What counts as a resource; how resources reference each other                        |       |
| Resource names and IDs               | `name`, `{resource}_id`, `uid`, path segments                                  | 122                         | Name format, collection IDs, user-settable IDs, referencing other resources          |       |
| Resource types                       | `google.api.resource`, type strings                                            | 123                         | How a resource type is declared and named                                            | P, G  |
| Planes                               | `:predict`, uploads, streaming data paths                                      | 111                         | Management vs data plane — changes consistency and ID rules in other AIPs            |       |
| Declarative-friendly resources       | IaC consumers, server-set fields, defaults                                     | 128, 129                    | Whether resources must suit declarative clients; how server-modified values behave   |       |
| Singletons                           | `…/settings`, `…/config`, one per parent                                       | 156                         | Which methods a resource without an ID may have                                      |       |
| Methods overview                     | —                                                                              | 130                         | Standard vs custom; method categories                                                |       |
| Standard methods                     | `GET /…/{id}`, `POST /…`, `PATCH`, `DELETE`                                    | 131, 132, 133, 134, 135     | Request and response shape, verb, body, and required fields for Get/List/Create/Update/Delete |  |
| Custom methods                       | `:verb` suffix, `POST …:cancel`, stateless calls such as predict               | 136                         | When a custom method is justified; its naming, verb, and body                        |       |
| HTTP and JSON mapping                | `google.api.http`, query parameters, request body                              | 127                         | How methods map to verbs, paths, and bodies; JSON encoding of bodies                 |       |
| Batch methods                        | `:batchGet`, `:batchCreate`, `:batchUpdate`, `:batchDelete`                    | 231, 233, 234, 235          | Batch shapes; atomic vs partial success. There is no AIP-232                         |       |
| Long-running operations              | `Operation`, `done`, `operations/…`                                            | 151                         | When a method returns an operation; where failures go                                |       |
| Jobs                                 | `…/jobs/{job}`, `:run`                                                         | 152                         | Configured, re-runnable work modelled as a resource                                  |       |
| Import and export                    | `:import`, `:export`                                                           | 153                         | Bulk data in and out                                                                 |       |
| Field names                          | casing, `uri` vs `url`, abbreviations, `is_` prefixes                          | 140                         | Naming of proto fields (JSON casing is [SPEC])                                       |       |
| Naming conventions                   | message, method, and enum names                                                | 190                         | Naming of definitions; method name shape                                             |       |
| Field behaviour                      | `REQUIRED`, `OUTPUT_ONLY`, `IMMUTABLE`, OpenAPI `readOnly`                     | 203                         | Which behaviours are declared and what each promises                                 | P     |
| Field formats                        | UUID, IP address, email strings                                                | 202                         | Format annotations on string fields                                                  | P     |
| Standard fields                      | `create_time`, `update_time`, `display_name`, `etag`, `uid`                    | 148                         | What standard fields mean when present                                               |       |
| Quantities                           | units, `_bytes`, `_seconds` suffixes                                           | 141                         | Units and numeric types                                                              |       |
| Time and duration                    | `*_time`, `*_duration`, epoch integers                                         | 142                         | Types for instants and spans                                                         |       |
| Standardized codes                   | language, region, currency codes                                               | 143                         | Which code systems to use                                                            |       |
| Repeated fields                      | arrays inside resources                                                        | 144                         | Naming and update semantics of lists                                                 |       |
| Ranges                               | start/end pairs                                                                | 145                         | Range representation                                                                 |       |
| Generic fields                       | `Struct`, `Any`, maps                                                          | 146                         | When untyped fields are acceptable                                                   |       |
| Sensitive fields                     | secrets, credentials, personal data                                            | 147                         | Handling sensitive values in requests and responses                                  |       |
| Unset values                         | `optional`, zero values, presence                                              | 149                         | Distinguishing unset from default                                                    |       |
| Enums and lifecycle states           | enum values, `state`, `*_UNSPECIFIED`                                          | 126, 216                    | Enum design; state fields and how transitions happen                                 |       |
| Unicode                              | string length limits, normalization                                            | 210                         | How string sizes and normalization are defined                                       |       |
| Pagination                           | `page_size`, `page_token`, `next_page_token`, `total_size`, `page`, `limit`    | 158, 132                    | The pagination contract — and when it must exist                                     |       |
| Filtering and ordering               | `filter`, `order_by`                                                           | 160, 132                    | Filter grammar; ordering syntax                                                      |       |
| Reading across collections           | `-` wildcard parent, `unreachable`                                             | 159, 217                    | Listing across parents; reporting unreachable locations                              |       |
| Partial update                       | `update_mask`, `PATCH`, `allow_missing` (upsert)                               | 134, 161                    | Update semantics and field-mask rules                                                |       |
| Partial responses                    | `view`, `read_mask`, sparse fieldsets                                          | 157                         | Returning a subset of a resource                                                     | G     |
| Optimistic concurrency               | `etag`, `If-Match`                                                             | 154                         | Freshness validation and the error it raises                                         |       |
| Idempotency                          | `request_id`, idempotency keys                                                 | 155                         | Request identification for safe retries                                              |       |
| Revisions                            | resource versions, history, snapshots                                          | 162                         | Revision sub-collections                                                             | D     |
| Validate-only                        | `validate_only`, dry run                                                       | 163                         | Validating a change without side effects                                             |       |
| Soft delete                          | `delete_time`, `purge_time`, `:undelete`, `:expunge`, `show_deleted`           | 164                         | Soft delete, undelete, and expunge                                                   |       |
| Criteria-based delete                | `:purge` with `filter`                                                         | 165                         | Deleting by filter                                                                   |       |
| Expiration                           | `expire_time`, `ttl`                                                           | 214                         | Resource time-to-live                                                                |       |
| Authorization                        | permission checks, 403 vs 404                                                  | 211, 193                    | What a method checks, and in which order                                             | G     |
| Policy preview                       | —                                                                              | 236                         | Previewing policy changes                                                            | G     |
| Errors                               | `error.code`, `status`, `details`, `ErrorInfo`                                 | 193                         | The error model, required details, and the HTTP/JSON envelope                        |       |
| Retry configuration                  | retryable codes                                                                | 194                         | Which codes clients may retry automatically                                          | G     |
| Backwards compatibility              | renames, removals, type changes, defaults                                      | 180                         | What counts as breaking                                                              |       |
| Stability levels                     | alpha, beta, preview, GA                                                       | 181                         | What each stability level promises                                                   |       |
| Versioning                           | `/v1/`, `v1beta1`, channel- vs interface-based                                 | 185                         | Versioning strategies; where the version goes                                        |       |
| Version identifiers                  | date versions, version headers                                                 | 184                         | Format and transport of interface-based version identifiers                          | G     |
| Beta-blocking changes                | —                                                                              | 205                         | Changes that must land before beta                                                   | G     |
| External software dependencies       | —                                                                              | 182                         | Depending on external software                                                       | R     |
| Documentation                        | proto comments, `(-- … --)` internal comments                                  | 192                         | What comments say; internal vs public text                                           | P     |
| File and package layout              | proto packages, file names, options                                            | 191                         | Proto syntax, packaging, and file layout                                             | P, G  |
| Common components                    | shared protos, `google.type.*`                                                 | 213, 215                    | Common vs API-specific protos                                                        | P     |
| Client libraries                     | method signatures, auto-pagination, resource-name parsing                      | 4210–4290                   | Generator expectations — at `https://google.aip.dev/client-libraries/{n}`            | G     |
| Precedent and deviations             | `aip.dev/not-precedent`                                                        | 200                         | How a deviation is recorded; local consistency                                       |       |
| How AIPs work                        | states, requirement keywords, glossary                                         | 1, 8, 9                     | AIP states; keyword typesetting; terms                                               |       |
| Design review process                | —                                                                              | 100                         | Google's API review FAQ                                                              | G     |
| Cloud project identifiers            | `projects/{project}`                                                           | 2510                        | Project IDs vs numbers — at `https://google.aip.dev/cloud/2510`                      | G     |

The Cloud API Design Guide keeps only its introduction, its changelog, and
[Directory structure](https://docs.cloud.google.com/apis/design/directory_structure)
(googleapis repository layout — **G**) as first-party pages; every former
chapter redirects to an AIP. Skip the guide unless asked about the guide
itself.

## Vocabulary bridge

Users rarely say the AIP term. Translate before searching.

| The user says                                    | AIP term                              | AIP      |
| ------------------------------------------------ | ------------------------------------- | -------- |
| versions, history, snapshots of a resource       | revisions                             | 162 (D)  |
| archive, trash, restore                          | soft delete, undelete                 | 164      |
| settings, config, preferences — one per parent   | singleton                             | 156      |
| partial results, a region is down                | unreachable                           | 217, 159 |
| list across all parents                          | reading across collections            | 159      |
| bulk                                             | batch methods                         | 231–235  |
| background task, polling                         | long-running operation, job           | 151, 152 |
| upsert                                           | `allow_missing`                       | 134      |
| optimistic locking, `If-Match`                   | etag, freshness validation            | 154      |
| idempotency key                                  | request identification, `request_id`  | 155      |
| sparse fields                                    | partial responses                     | 157      |
| dry run                                          | change validation, `validate_only`    | 163      |
| TTL                                              | expiration                            | 214      |
| delete by filter                                 | criteria-based delete                 | 165      |
| control plane vs data plane, predictions         | planes                                | 111      |
| a documented exception to a standard             | not-precedent                         | 200      |
| header or date-based versions                    | interface-based versioning, identifiers | 185, 184 |

## Stale priors

Each entry is a prompt to retrieve, not a rule to cite. Wording was checked
against the AIP source on 2026-10-11; re-verify before relying on it.

- **Versioning (AIP-184, AIP-185).** Prior: version only through `v1` /
  `v1beta` in the path. Since 2026-08-17 AIP-185 adds interface-based
  versioning and AIP-184 defines date-based version identifiers sent by
  header or query parameter. The two disagree on a request that omits the
  identifier — cite both and flag it.
- **Custom-method verbs (AIP-136).** Since 2026-06-09 a retrieval method may
  use `POST` when its payload could overflow a URL; `GET` remains the rule
  for retrieval.
- **Soft delete (AIP-164).** An `Expunge` custom method was added 2026-04-28,
  with its own permission requirement.
- **Field behaviour (AIP-203).** The annotation applies to every request
  field; since June 2026 a resource's `etag` and `oneof` fields are carved
  out. Output-only input is cleared, never rejected.
- **Errors (AIP-193).** `ErrorInfo` has been required on every error since
  2023-05-10, with dynamic message parts in its metadata; the 2024-10-18
  restructure renamed most anchors. Permission is checked before existence
  (§Permission Denied).
- **Partial update (AIP-134).** The update mask is optional, an omitted mask
  has defined semantics, and `*` means full replacement. `PUT` is limited to
  full-replacement-only methods.
- **Batch atomicity (AIP-233–235).** Since 2025-03-06 batch methods may be
  atomic or partial-success, with constraints tied to sync vs async.
- **Resource IDs (AIP-122, AIP-133).** The ban on UUID-looking user IDs was
  dropped 2025-03-10. Whether Create needs a `{resource}_id` depends on the
  plane (AIP-111).
- **Read masks (AIP-157).** A read mask as a request field is deprecated for
  Google APIs in favour of a system parameter (**G**).
- **Naming (AIP-140, AIP-190).** `uri` vs `url` guidance changed 2025-09-15;
  AIP-190 (2025-06-10) replaced the guide's naming page.
- **Etag mismatch (AIP-154).** The error is `ABORTED`, not
  `FAILED_PRECONDITION`.
- **Parents with children (AIP-135).** Deleting a parent that still has
  children, without `force`, has a prescribed failure.
- **LRO failures (AIP-151).** A failure to start and a failure during
  execution surface in different places.
- **Compatibility (AIP-180).** Changes dated 2025-10-21 treat several
  format and default changes as breaking.
- **Proto syntax (AIP-191).** Proto3 syntax is required; Editions are not
  mentioned.

Summaries reliably corrupt these — check the source sentence itself:

- AIP-121's strong-consistency rule is scoped to management-plane methods.
- AIP-148 constrains what standard fields mean when present; declarative-
  friendly resources **should** include several of them. It does not require
  them everywhere.
- AIP-122 says a field referencing another resource should hold its name,
  not embed its message — except in internal-only APIs with tight lifecycle
  relationships *and* inherited permissions, and in AIP-162 revisions.
- AIP-158's warning on base64 page tokens is a bolded *Warning*, not a
  requirement keyword.
- AIP-217's `return_partial_success` flag is how an *existing* API adopts
  the `unreachable` pattern; it is not required of new APIs.
- AIP-132 makes `page_size` and `page_token` **must** on List requests;
  AIP-158 says **should**. Cite both levels.
- Google product behaviour is [PRECEDENT], never [AIP]. Vertex AI's
  `:predict` is a custom-method pattern under AIP-136, and its `endpoint`
  field name itself departs from AIP-136's naming.

## Source mechanics

- **Canonical URLs.** General: `https://google.aip.dev/{n}`. Scoped:
  `https://google.aip.dev/{scope}/{n}` (`client-libraries`, `auth`, `cloud`,
  `apps`, `aog`). Cite these, never raw or GitHub URLs.
- **Redirects your fetch tool will not follow.** `aip.dev/{n}` and
  `cloud.google.com/apis/design/*` redirect across hosts; `google.aip.dev/4221`
  (a scoped AIP without its scope), `/0158`, and `/not-precedent` are
  meta-refresh stubs. Re-fetch the target URL the tool reports.
- **Raw markdown.** `https://raw.githubusercontent.com/aip-dev/google.aip.dev/master/aip/general/{NNNN}.md`
  (branch `master`, four digits); scoped: `…/aip/{scope}/{n}.md`. Front matter
  carries `state` and `created`.
- **Change history.** The rendered "Updated" date equals "Created" and is
  unreliable; per-AIP Changelog sections are incomplete; the Design Guide
  changelog tracks only the guide. The authoritative feed is
  `https://github.com/aip-dev/google.aip.dev/commits/master/aip/general/{NNNN}.md`.
  Pin a citation with a commit permalink if the reader needs a fixed text.
- **Anchors.** Heading slugs (duplicates get `_1`), regenerated when headings
  change — AIP-193's 2024 rewrite renamed most of its anchors. Use one only
  after seeing it in retrieved text.
- **Keywords.** AIPs use must, must not, should, should not, and may,
  lowercase and bold ([AIP-8](https://google.aip.dev/8#requirement-keywords)).
  Rationale and History sections carry no requirements. An unbolded "must"
  inside Guidance: report it as unbolded and do not silently upgrade or
  downgrade it.
- **Org AIPs.** [google.aip.dev/adopting](https://google.aip.dev/adopting)
  reserves AIP-9000 to 9999 for an organization's internal AIPs — cite those
  as [TEAM].
- **Status.** Only AIP-162 (Draft) and AIP-182 (Reviewing) are non-approved
  in the general scope as of 2026-10-11; AIP-1 tells producers to rely
  primarily on approved AIPs.
- **Licensing.** Text CC BY 4.0, code samples Apache 2.0
  ([licensing](https://google.aip.dev/licensing)); the attribution line is in
  [`design-doc.md`](design-doc.md#references-and-attribution).

## Second-tier sources

AIPs delegate wire details; these carry them. Cite as [SPEC] or [PRECEDENT],
never as an AIP rule.

- **[SPEC]** [ProtoJSON mapping](https://protobuf.dev/programming-guides/json/)
  — JSON casing and the encodings of Timestamp, Duration, FieldMask, enums,
  and 64-bit integers.
- **[SPEC]** googleapis
  [`google/rpc/code.proto`](https://raw.githubusercontent.com/googleapis/googleapis/master/google/rpc/code.proto)
  (canonical codes and their HTTP mapping),
  [`google/longrunning/operations.proto`](https://raw.githubusercontent.com/googleapis/googleapis/master/google/longrunning/operations.proto)
  (operation polling paths),
  [`google/api/http.proto`](https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/http.proto)
  (path template and `:verb` grammar),
  [`google/api/field_behavior.proto`](https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/field_behavior.proto).
- **[PRECEDENT]** A product's protos in `googleapis/googleapis` on raw GitHub
  answer binding, return-type, and field-behaviour questions in one fetch —
  for example `google/cloud/aiplatform/v1/prediction_service.proto`. Only
  beta and GA APIs set precedent (AIP-200). The rendered
  docs.cloud.google.com REST reference pages bury content behind roughly
  100k characters of navigation; prefer the protos, and search
  docs.cloud.google.com only to learn which product does X.
- **AEP** (`aep.dev`, a 2023 community fork of the AIPs) is an aid for
  OpenAPI mechanics only and diverges from AIPs on several defaults — see
  [`rest-and-openapi.md`](rest-and-openapi.md#linting-openapi). Never cite it
  to justify a design.

Freshness: verified against `google.aip.dev` (upstream commit `615875b`,
2026-10-07) on 2026-10-11.
