---
id: IMP0026
record_type: improvement_dossier
created_at: '2026-05-13T23:23:22+09:00'
updated_at: '2026-05-13T23:23:37+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: evaluated
relation: new
promotion_level: shipped-behavior
source_feedback: FB0030
eval_cases:
- E0029
hypotheses:
- H0029
decisions:
- D0030
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: src/harnessops/core/upgrade_chain.py
investigation: []
links:
  issue_url:
---

# IMP0026: FB0030: Chain HarnessOps updates through version checkpoints

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: new
- promotion_level: shipped-behavior
- source_feedback: `FB0030`
- linked_records: `FB0030`, `E0029`, `H0029`, `D0030`

## Source Observation

Source: `harness-lab/records/feedback/FB0030-chain-harnessops-updates-through-version-checkpoints.md`

# FB0030: Chain HarnessOps updates through version checkpoints

## 概要

uvx を標準導線にしたことで、target/project repo の update-harness は最新 PyPI runtime から開始できる。古い managed artifact への互換コードを永久に持つ代わりに、lock の harnessops_version から公開済み checkpoint を計画し、必要な版を uvx で順に呼び出す更新チェーンを追加する。

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

hops update-harness が chain plan/apply の導線を提供し、update skill が通常更新と段階更新を使い分けられるようになる。

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0029: E0029: FB0030-chain-harnessops-updates-through-version-checkpoints を評価


- source: `harness-lab/records/eval-cases/E0029-fb0030-chain-harnessops-updates-through-version-checkpoints.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0029-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0029-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Implemented checkpointed uvx update chains in update-harness with --plan-upgrade and --apply-upgrade-chain, refreshed update skill/docs, and verified with ruff check ., pytest -q (93 passed), doctor --check-overlay --check-records, migrate --check, and git diff --check.


## Hypotheses

### H0029: H0029: E0029-fb0030-chain-harnessops-updates-through-version-checkpoints の仮説


Source: `harness-lab/records/hypotheses/H0029-e0029-fb0030-chain-harnessops-updates-through-version-checkpoints.md`


# H0029: E0029-fb0030-chain-harnessops-updates-through-version-checkpoints の仮説

## 仮説

A checkpointed uvx update chain lets target/project repositories move through bounded HarnessOps versions, so older migration code can be retired after the supported checkpoint horizon instead of expanding direct backward compatibility forever.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0029` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0029 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0029-manual-score.md`

## Guard

- status: implemented
- path: src/harnessops/core/upgrade_chain.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0030: D0030: adopted H0029


Source: `harness-lab/records/decisions/D0030-adopted-h0029.md`


# D0030: adopted H0029

## 判断

adopted

## 理由

uvx is now the standard downstream path, so update-harness can use the recorded HarnessOps version in lock.json to run bounded exact-version checkpoints before applying the current runtime. This reduces pressure to keep direct compatibility code forever while preserving an explicit plan/apply path.

## 証拠

ruff check .; pytest -q (93 passed); hops doctor --check-overlay --check-records; hops migrate --check; git diff --check

## 回帰リスク

Medium-low: subprocess uvx chain can fail when a checkpoint is unavailable, but normal update still falls back to direct current refresh when no intermediate checkpoint is available, and tests cover plan, explicit apply, and auto intermediate execution.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

src/harnessops/core/upgrade_chain.py
