# REST and OpenAPI — rendering proto-first AIPs over HTTP/JSON

Scope: applying AIPs to REST-only or OpenAPI APIs, and to transcoded gRPC
APIs, where most of the friction lives — the points where a REST habit and an
AIP disagree, or where AIPs are silent and a wire spec decides. Each row names
the source to retrieve and the decision to record; levels come from your own
retrieval.

## Contents

- [Model first, then render](#model-first-then-render)
- [Translation table](#translation-table)
- [Linting OpenAPI](#linting-openapi)

## Model first, then render

AIPs are written for protocol buffers; google.aip.dev's
[FAQ](https://google.aip.dev/faq) tells non-proto users to follow the spirit
of the guidance. So model the API in AIP terms first — resources, names,
standard methods — then render it to HTTP with AIP-127 and to JSON with the
[ProtoJSON mapping](https://protobuf.dev/programming-guides/json/). Wire
facts AIPs leave to that mapping are **[SPEC]** claims, never **[AIP]** ones.

## Translation table

| Concern                       | Retrieve                                             | Rendering to decide and record                                                                                                                                  |
| ----------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JSON field casing             | [SPEC] ProtoJSON; AIP-140 (proto names); AIP-127 (`json_name`) | ProtoJSON emits lowerCamelCase keys and parsers accept the proto name too. AIP-140's casing rule governs proto definitions, not JSON. Emit camelCase; accept both |
| Query parameters              | AIP-127, AIP-133, AIP-134, AIP-158                   | AIP-127 notes clients send query names in camelCase (`?bookId=`). Fields outside the path and body become query parameters: `pageSize`, `pageToken`, `updateMask`, the Create ID |
| Resource names in paths       | AIP-122, AIP-127                                     | A path variable for a resource name covers the whole name (`{name=shelves/*/books/*}`). OpenAPI parameters cannot hold `/`, so render one parameter per ID segment and document the name format — record it as **[JUDGMENT]** |
| Custom verbs                  | AIP-136; [SPEC] `google/api/http.proto`              | A literal `:verb` suffix on the path. Check the GET-vs-POST rule and verb casing in AIP-136, and test your router ([`implement.md`](implement.md#framework-notes)) |
| Partial update                | AIP-134, AIP-161; [SPEC] ProtoJSON                   | `PATCH` with an optional field mask; in JSON the mask is one comma-separated string of lowerCamelCase paths. JSON merge-patch is not the AIP model — a Deviations row if chosen |
| Timestamps and durations      | AIP-142 (types); [SPEC] ProtoJSON                    | Timestamps are RFC 3339, `Z`-normalized. Durations are `"3.5s"`, not ISO 8601 `"PT3.5S"`                                                                         |
| Enums, 64-bit integers, bytes | AIP-126; [SPEC] ProtoJSON                            | Enum names as strings (parsers also accept numbers); 64-bit integers as decimal strings; bytes as standard base64                                               |
| Field behaviour               | AIP-203                                              | Output-only maps to `readOnly: true` — the server clears it on input and does not error. Input-only maps to `writeOnly`, required to `required`. Immutable has no OpenAPI keyword: describe it or use an extension |
| Error body                    | AIP-193 § HTTP/1.1+JSON; [SPEC] `google/rpc/code.proto` | `{"error": {"code", "message", "status", "details"}}` — `code` is the HTTP status, `status` the canonical code name. RFC 9457 problem+json is a **[TEAM]** choice and a Deviations row |
| Success status codes          | AIP-135; [SPEC] `code.proto`                         | AIPs are silent on 201 and 204; `code.proto` maps OK to 200. Delete's response type (Empty, so `{}` in JSON, or the resource for soft delete) comes from AIP-135 and AIP-164. 201/204 are **[TEAM]** choices |
| Long-running work             | AIP-151; [SPEC] `google/longrunning/operations.proto` | Polling is `GET /v1/{name=operations/**}`, cancel is `POST …:cancel`; `WaitOperation` has no HTTP binding                                                       |
| Versioning                    | AIP-185, AIP-184                                     | AIP-185 puts the major version first in the REST path. AIP-184's identifiers are dates (`YYYY-MM-DD`, with optional variant prefix and decorator) in a Google-named header or query parameter (**G**) — translate the name, keep the format. AIP-185's opening Guidance requires the path major version and its IBV section does not lift that; a free-form version header is not interface-based versioning |
| Pagination                    | AIP-158, AIP-132                                     | Results field first, `nextPageToken` empty only at the end, optional `totalSize`. A bare JSON array cannot gain a token later                                    |

## Linting OpenAPI

There is no Google-official AIP ruleset for OpenAPI: `linter.aip.dev` lints
protocol buffers only. Two workable routes:

1. **Generic plus review.** Run Spectral's `spectral:oas` ruleset and check
   AIP conformance by review against the AIPs you retrieved.
2. **AEP ruleset, corrected.** [`@aep_dev/aep-openapi-linter`](https://github.com/aep-dev/aep-openapi-linter)
   (MIT) encodes AEP, a 2023 community fork of the AIPs whose defaults differ
   from Google's in places. Run it with those rules off, each with the AIP
   that governs:

```yaml
extends:
  - "@aep_dev/aep-openapi-linter"
rules:
  aep-122-resource-path-field: off      # AIP-122 identifies resources by `name`
  aep-133-id-parameter: off             # AIP-133 names the Create ID `{resource}_id`
  aep-134-content-type: off             # AIP-134 uses PATCH with a field mask
  aep-135-response-204: off             # AIP-135 returns Empty (or the resource)
  aep-140-uri-property-naming: off      # AIP-140 keeps `url` for URL-only fields
  aep-158-max-page-size-parameter: off  # AIP-158 calls it `page_size`
  aep-158-page-token-parameter: off               # expects page_token; REST renders pageToken
  aep-158-response-next-page-token-property: off  # ProtoJSON emits nextPageToken
  aep-122-collection-identifier-format: off       # bans uppercase; AIP-122 collection IDs are camelCase
```

Retrieve each AIP before trusting its comment; the rule names were read from
the ruleset on 2026-10-11 (npm 0.5.3). The list is not exhaustive: triage
any other rule that assumes AEP's snake_case JSON the same way. AEP is an aid for OpenAPI mechanics —
how to express a `:verb` path, a list schema, or operation polling in OAS. It
never justifies a design, and where it and an AIP differ, the AIP wins and the
output says so.

| Topic             | AEP default                         | Google AIP                                   |
| ----------------- | ----------------------------------- | -------------------------------------------- |
| JSON field names  | lower_snake_case (AEP-140)          | lowerCamelCase — [SPEC] ProtoJSON, linked by AIP-127 |
| Resource ID field | `path` (AEP-122)                    | `name` (AIP-122)                             |
| Page size         | `max_page_size` (AEP-158)           | `page_size` (AIP-158)                        |
| Partial update    | JSON merge-patch content type       | `PATCH` with a field mask (AIP-134)          |
| Delete response   | 204 No Content (AEP-135)            | Empty, or the resource on soft delete        |
| Create ID         | `id` parameter                      | `{resource}_id` (AIP-133)                    |

Freshness: ProtoJSON, googleapis protos, and the AEP ruleset read on
2026-10-11.
