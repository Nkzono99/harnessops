---
id: IMP0028
record_type: improvement_dossier
created_at: '2026-05-14T00:11:31+09:00'
updated_at: '2026-05-14T00:11:44+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: evaluated
relation: extends
promotion_level: shipped-behavior
source_feedback: FB0032
eval_cases:
- E0031
hypotheses:
- H0031
decisions:
- D0032
research_scans: []
classification:
  capability: repository_maintainability
  failure_class: records_module_sprawl
guard:
  status: implemented
  path: src/harnessops/core/improvement_dossier.py
investigation: []
links:
  issue_url:
---

# IMP0028: FB0032: Split record core modules by responsibility

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0032`
- linked_records: `FB0032`, `E0031`, `H0031`, `D0032`

## Source Observation

Source: `harness-lab/records/feedback/FB0032-split-record-core-modules-by-responsibility.md`

# FB0032: Split record core modules by responsibility

## 概要

records.py has become the central maintainability hotspot: it mixes record type constants, frontmatter IO, ID/path indexing, feedback/eval/hypothesis/decision creation, research scan parsing, and improvement dossier aggregation/mutation. Split these responsibilities into focused modules while keeping harnessops.core.records as a compatibility facade.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Introduce record_types.py, record_io.py, record_index.py, lab_records.py, and improvement_dossier.py; preserve current imports and behavior; update tests/docs only where the new structure needs a contract.

## Target Capability

- capability: repository_maintainability
- failure_class: records_module_sprawl

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0031: E0031: FB0032-split-record-core-modules-by-responsibility を評価


- source: `harness-lab/records/eval-cases/E0031-fb0032-split-record-core-modules-by-responsibility.md`

- capability: repository_maintainability

- failure_class: records_module_sprawl

- manual_eval_yml: `harness-lab/views/eval-results/E0031-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0031-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=0, anti_theater=5, maintainability=5, privacy_sanitization_risk=0
- notes: Split records.py into record_types, record_io, record_index, lab_records, and improvement_dossier while keeping records.py as a compatibility facade. Updated internal imports and record schema docs. Verified with ruff check ., pytest -q (92 passed), doctor --check-overlay --check-records, and migrate --check.


## Hypotheses

### H0031: H0031: E0031-fb0032-split-record-core-modules-by-responsibility の仮説


Source: `harness-lab/records/hypotheses/H0031-e0031-fb0032-split-record-core-modules-by-responsibility.md`


# H0031: E0031-fb0032-split-record-core-modules-by-responsibility の仮説

## 仮説

Splitting records.py into focused record type, IO, lookup, creation, and dossier modules reduces the central maintenance hotspot while keeping harnessops.core.records as a compatibility facade for existing callers.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0031` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0031 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0031-manual-score.md`

## Guard

- status: implemented
- path: src/harnessops/core/improvement_dossier.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0032: D0032: adopted H0031


Source: `harness-lab/records/decisions/D0032-adopted-h0031.md`


# D0032: adopted H0031

## 判断

adopted

## 理由

The old records.py module mixed record schemas, IO, indexing, creators, and dossier aggregation. Focused modules make future changes easier to review while retaining the previous import surface through harnessops.core.records.

## 証拠

ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check

## 回帰リスク

Low-medium: behavior was moved mechanically and the facade preserves old imports; full CLI and record tests passed, but future follow-up should add smaller unit tests for the new modules.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/core/improvement_dossier.py
