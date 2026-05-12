---
id: IMP0012
record_type: improvement_dossier
created_at: '2026-05-13T02:23:36+09:00'
updated_at: '2026-05-13T02:27:16+09:00'
status: adopted
source_type: implementation-followup
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0015
eval_cases:
- E0014
hypotheses:
- H0014
decisions:
- D0015
classification:
  capability: record_lookup
  failure_class: generated_view_shadowed_record_id
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation: []
links:
  issue_url:
---

# IMP0012: FB0015: Prefer canonical records over generated views in record lookup

## Status

- status: adopted
- maturity: adopted
- source_type: implementation-followup
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0015`
- linked_records: `FB0015`, `E0014`, `H0014`, `D0015`

## Source Observation

Source: `harness-lab/records/feedback/FB0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`

# FB0015: Prefer canonical records over generated views in record lookup

## 概要

After a manual eval result exists, rerunning hops eval --case E0013 can resolve E0013 to harness-lab/views/eval-results/E0013-manual-score.md instead of the canonical records/eval-cases/E0013 record.

## 再現

Create a manual eval result for E0013, then run hops eval --case E0013 again. find_record scans overlay markdown files broadly and can return the generated eval result view whose record_type is manual_eval_result.

## 期待する上流変更

Make find_record prefer the canonical record directory implied by the ID prefix before falling back to broad overlay lookup, so generated views do not shadow FB/E/H/D/IMP records.

## Target Capability

- capability: record_lookup
- failure_class: generated_view_shadowed_record_id

## Investigation

調査メモはまだありません。

## Evaluation

### E0014: E0014: FB0015-prefer-canonical-records-over-generated-views-in-record-lookup を評価


Source: `harness-lab/records/eval-cases/E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`


# E0014: FB0015-prefer-canonical-records-over-generated-views-in-record-lookup を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0014`。

## タスク

この失敗を防ぐべき挙動を記述してください。

## 期待される挙動

ターゲットハーネスが、非公開プロジェクト文脈を漏らさずに失敗クラスを扱います。

## 合格基準

- 失敗条件が検出または防止される。
- 提案される挙動が上流メンテナにとって実行可能である。
- 非公開プロジェクト詳細を必要としない。

## 不合格基準

- 失敗を見逃す。
- 再現に非公開文脈が必要になる。


## Hypotheses

### H0014: H0014: E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup の仮説


Source: `harness-lab/records/hypotheses/H0014-e0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`


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


## Evidence

`harness-lab/views/eval-results/E0014-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0015: D0015: adopted H0014


Source: `harness-lab/records/decisions/D0015-adopted-h0014.md`


# D0015: adopted H0014

## 判断

adopted

## 理由

Generated views can share ID prefixes with canonical records, so prefix-directed lookup is needed to keep ordinary commands like hops eval --case E0013 stable after views exist.

## 証拠

tests/test_cli/test_mvp_flow.py reruns eval by ID after E0001-manual-score.md exists; uv run pytest tests/test_cli/test_mvp_flow.py -q

## 回帰リスク

Low: path-based lookup still works first, and prefix routing falls back to broad overlay lookup when no canonical record exists.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
