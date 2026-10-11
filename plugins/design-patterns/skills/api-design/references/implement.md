# Implement — follow the AIPs in code, and cite them there

Scope: turning a design into protos, OpenAPI, and server handlers that obey
the same AIP rules the design cited, with citations placed where a
maintainer will look for them. The research protocol and claim types in
[`../SKILL.md`](../SKILL.md) still bind: no AIP number goes into code unless
it is in the ledger.

## Contents

- [Start from the design](#start-from-the-design)
- [Tests first for AIP-mandated behaviour](#tests-first-for-aip-mandated-behaviour)
- [Where citations go](#where-citations-go)
- [Framework notes](#framework-notes)
- [Done means](#done-means)

## Start from the design

1. Read the design's decisions, Deviations table, and References first.
   Reuse its ledger; retrieve only behaviour the design left open (page-size
   default and maximum, token expiry, mask edge cases).
2. Do not re-decide in code. If the code cannot meet the design, stop and
   update the design or ask. **A deviation that exists only in code is a
   defect.**

## Tests first for AIP-mandated behaviour

Write a test for each behaviour the design adopted from an AIP, before the
handler. Retrieve each rule's level first; typical candidates:

- page-size handling — default, oversize, negative (AIP-158);
- output-only fields sent on input are cleared, not rejected (AIP-203);
- omitted vs `*` update masks (AIP-134); unknown mask paths (AIP-161);
- permission checked before existence (AIP-193 §Permission Denied);
- the error envelope's shape and details (AIP-193).

Name tests after the behaviour (`test_negative_page_size_is_invalid_argument`),
not the AIP — the citation lives in the handler.

## Where citations go

Signal, not noise. Cite once per decision site.

- **Handler docstring:** the behaviour contract, then one line —
  `References: AIP-132, AIP-158.`
- **Inline comment:** only where behaviour is surprising and AIP-caused —
  AIP number, level, paraphrase, no URL:
  `# AIP-158 (should): coerce an oversize page_size down instead of rejecting it.`
- **Never** annotate the obvious; a `GET` route needs no "AIP-131".
- **Deviations** use AIP-200's `aip.dev/not-precedent` convention, adapted to
  the language, and point at the design's Deviations row:
  `# (-- aip.dev/not-precedent: PUT kept for v1 clients; AIP-134 prefers PATCH. Design D1. --)`.
  Every code deviation has a design row, and every design row a code site.
- **Protos:** leading comments are published as API documentation — write
  consumer-facing text there. Rationale and non-public links go inside
  `(-- … --)` (AIP-192). The stripping of `(-- … --)` is done by Google's
  tooling, and AIP-192's own source notes it does not work outside Google:
  check your doc generator, and if it does not strip them, keep rationale in
  a non-doc comment instead.
- **api-linter suppressions** pair the rule with the reason, as the linter's
  rule docs show:
  `// (-- api-linter: core::0134::<rule-name>=disabled` /
  `//     aip.dev/not-precedent: <reason> --)`. Confirm the rule ID at
  `https://linter.aip.dev/{aip}/{rule-name}` before writing it.
- **OpenAPI:** `description` states behaviour in consumer terms; put the
  machine-readable citation in the operation's `externalDocs` (one URL) and
  an `x-aip` list. Spectral overrides carry a reason naming the deviation ID.

```python
@router.get("/v1/shelves/{shelf}/books", openapi_extra={"x-aip": [132, 158]})
async def list_books(
    shelf: str,
    page_size: Annotated[int, Query(alias="pageSize")] = 0,
    page_token: Annotated[str, Query(alias="pageToken")] = "",
) -> ListBooksResponse:
    """List books on a shelf; pageSize defaults to 50 and is capped at 1000.

    References: AIP-132, AIP-158.
    """
    if page_size < 0:
        raise InvalidArgument("pageSize must not be negative")
    # AIP-158 (should): coerce an oversize page_size down instead of rejecting it.
    size = min(page_size or DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE)
    ...
```

The sketch is illustrative; take the levels from your own retrieval.

## Framework notes

Observed on FastAPI 0.143, Starlette 1.7, and Pydantic 2.14 (2026-10-11).
The same traps exist in most routers — test them in yours.

- **Custom verbs:** a generic `GET /books/{book}` declared first captures a
  GET custom method (`GET /books/b1:summarize` arrives as
  `book="b1:summarize"`); POST verbs route correctly, an unknown verb
  returns 405, and `{name:path}` swallows `:verb` suffixes. Register a path
  convertor for resource IDs that excludes `:` — routing then no longer
  depends on declaration order, and unknown verbs return 404.
- **Output-only fields on input:** `extra="forbid"` turns a client's
  round-tripped `createTime` into a 422. Accept and drop output-only fields.
- **Validation errors:** the default 422 `{"detail": [...]}` is not the
  AIP-193 envelope; install exception handlers that emit it with the
  canonical code.
- **Casing:** alias fields to lowerCamelCase and set `populate_by_name=True`
  so both forms parse (ProtoJSON accepts both).
- **Durations:** `timedelta` serializes as ISO 8601 (`"PT3.5S"`); ProtoJSON
  uses `"3.5s"`. Pick one and record it under Wire format.

## Done means

Tests for every adopted AIP behaviour pass; the linter (api-linter for
protos, Spectral for OpenAPI) is clean or each suppression carries a reason;
every `not-precedent` comment matches a design row; and the hub's
verification checklist passes.
