---
id: IMP0027
record_type: improvement_dossier
created_at: '2026-05-13T23:52:02+09:00'
updated_at: '2026-05-13T23:52:18+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: evaluated
relation: extends
promotion_level: shipped-behavior
source_feedback: FB0031
eval_cases:
- E0030
hypotheses:
- H0030
decisions:
- D0031
research_scans: []
classification:
  capability: repository_maintainability
  failure_class: surface_sprawl
guard:
  status: implemented
  path: src/harnessops/cli/agent.py
investigation: []
links:
  issue_url:
---

# IMP0027: FB0031: Simplify HarnessOps repository surfaces

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0031`
- linked_records: `FB0031`, `E0030`, `H0030`, `D0031`

## Source Observation

Source: `harness-lab/records/feedback/FB0031-simplify-harnessops-repository-surfaces.md`

# FB0031: Simplify HarnessOps repository surfaces

## 概要

HarnessOps has grown through feature work: root plugin artifacts may no longer be part of the standard path, core modules mix workflow logic with small utility boundaries, harness-lab contains directories with weak or missing workflows, and docs/SPEC/README may not reflect recent CLI and uvx update-chain behavior. Clean up repo surfaces and improve maintainability without changing core behavior.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Remove or retire obsolete plugin surfaces, add low-risk code organization boundaries, document current standard workflows, and record any lab layout cleanup as a deliberate migration path rather than ad hoc file moves.

## Target Capability

- capability: repository_maintainability
- failure_class: surface_sprawl

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0030: E0030: FB0031-simplify-harnessops-repository-surfaces を評価


- source: `harness-lab/records/eval-cases/E0030-fb0031-simplify-harnessops-repository-surfaces.md`

- capability: repository_maintainability

- failure_class: surface_sprawl

- manual_eval_yml: `harness-lab/views/eval-results/E0030-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0030-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=5, maintainability=5, privacy_sanitization_risk=0
- notes: Removed root plugin and user plugin install surfaces, moved packaged agent skills under agent_assets/skills, extracted shared markdown and managed file helpers, demoted experiments from required lab layout, and updated docs/SPEC/README. Verified with ruff check ., pytest -q (92 passed), doctor, and migrate.


## Hypotheses

### H0030: H0030: E0030-fb0031-simplify-harnessops-repository-surfaces の仮説


Source: `harness-lab/records/hypotheses/H0030-e0030-fb0031-simplify-harnessops-repository-surfaces.md`


# H0030: E0030-fb0031-simplify-harnessops-repository-surfaces の仮説

## 仮説

Removing obsolete root plugin surfaces, keeping repo-local skills as the only agent distribution path, and extracting small shared helpers reduces maintenance drift while preserving CLI-centered behavior.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0030` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0030 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0030-manual-score.md`

## Guard

- status: implemented
- path: src/harnessops/cli/agent.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0031: D0031: adopted H0030


Source: `harness-lab/records/decisions/D0031-adopted-h0030.md`


# D0031: adopted H0030

## 判断

adopted

## 理由

Repo-local skills are now the standard agent path, so root plugin mirrors and user plugin install support add maintenance surface without improving the current workflow. Small shared helpers reduce duplication without changing record or managed-file behavior.

## 証拠

ruff check .; pytest -q (92 passed); hops doctor --check-overlay --check-records; hops migrate --check

## 回帰リスク

Medium-low: removes optional plugin UX, but repo-local skill generation and packaged skill assets remain covered by tests; experiment record reading remains compatible but experiments are no longer required in the default lab layout.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/cli/agent.py
