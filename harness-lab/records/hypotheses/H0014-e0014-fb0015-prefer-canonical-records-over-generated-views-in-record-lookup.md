---
id: H0014
record_type: hypothesis
created_at: '2026-05-13T02:23:56+09:00'
status: proposed
target_capability: record_lookup
source_eval_case: E0014
---

# H0014: E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup の仮説

## 仮説

Record lookup should prefer canonical record directories for known ID prefixes, preventing generated views from shadowing FB/E/H/D/IMP records.

## メカニズム

find_record can derive a likely record directory from the ID prefix, search that directory first, and only fall back to broad overlay lookup if no canonical record matches.

## 最小実装

Update find_record prefix search order and add a regression test that reruns hops eval --case after a manual eval result exists.

## 代替案: 削除または統合

Require callers to pass full record paths after generated views exist, but that makes ordinary CLI usage brittle.

## 期待される利点

CLI commands remain stable even after generated views and eval results are created.

## 想定される欠点

Prefix-based lookup adds a small amount of special-case routing to the generic record finder.

## 評価計画

Run a test that evaluates E0001 twice by ID, plus the full CLI test suite.

## 中止基準

If prefix routing breaks path-based lookup or nonstandard record IDs, revert to exact frontmatter-id lookup with deterministic sorting.
