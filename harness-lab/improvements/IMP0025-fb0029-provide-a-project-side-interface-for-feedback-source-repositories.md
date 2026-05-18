---
id: IMP0025
record_type: improvement_dossier
created_at: '2026-05-13T22:57:22+09:00'
updated_at: '2026-05-19T03:36:30+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: investigated
relation: new
promotion_level: target-lab-case
source_feedback: FB0029
eval_cases:
- E0028
hypotheses:
- H0028
decisions:
- D0029
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation
investigation:
- created_at: '2026-05-13T23:00:57+09:00'
  kind: implementation
  summary: Implemented role-scoped repo-local bridge generation. feedback-source/local-and-feedback repos now receive a project-side bridge and only feedback/lifecycle skills; upstream/meta lab repos keep lab/eval/propose guidance. update-harness retires unedited managed skills that no longer belong to the repo role and reports retained edited retired files.
  evidence_ref:
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/12
---

# IMP0025: FB0029: Provide a project-side interface for feedback-source repositories

## Status

- status: adopted
- maturity: investigated
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0029`
- linked_records: `FB0029`, `E0028`, `H0028`, `D0029`

## Source Observation

Source: `harness-lab/records/feedback/FB0029-provide-a-project-side-interface-for-feedback-source-repositories.md`

# FB0029: Provide a project-side interface for feedback-source repositories

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/12
author: Nkzono99
labels: なし
created_at: 2026-05-13T13:41:49Z
updated_at: 2026-05-13T13:41:49Z

## Issue本文
## Context

HarnessOps lab record `FB0003` was promoted to a GitHub Issue draft.

Source dossier: `harness-lab/improvements/IMP0003-fb0003-project-side-feedback-source-repositories-need-a-role-scoped-interface.md`

## Proposal

# IMP0003: FB0003: Project-side feedback-source repositories need a role-scoped interface

## Status

- status: active
- maturity: raw
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0003`
- linked_records: `FB0003`

## Source Observation

Source: `harness-lab/records/feedback/FB0003-project-side-feedback-source-repositories-need-a-role-scoped-interface.md`

# FB0003: Project-side feedback-source repositories need a role-scoped interface

## 概要

runops project directories initialize HarnessOps with profile=runops-project, which is feedback-source mode and writes harness-feedback/. In that role agents mainly need feedback capture/export plus lifecycle checks, but the generic agent bridge exposes broader harness-lab/eval/propose commands that belong to target or meta repositories. This blurs the boundary between project-side private feedback capture and upstream adoption decisions.

## 再現

In runops, runo init delegates to hops init --profile runops-project --with-agent-bridge. The runops-project profile is mode=feedback-source with path=harness-feedback, while the generated HarnessOps bridge lists lab capture/dossier/investigate/classify/new-eval-case/propose/eval/decide commands as general guidance.

## 期待する上流変更

HarnessOps should provide a project-side minimal interface or role-scoped bridge for feedback-source repositories, exposing init/doctor/update-harness/migrate and feedback commands while keeping lab/eval/propose/decide guidance scoped to upstream-lab or meta-lab repositories.

## Target Capability

- capability: role_scoped_agent_bridge
- failure_class: project_feedback_interface_too_broad

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: not-defined
- path: None

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。

## Safety

This body was sanitized by HarnessOps before issue creation.


## 除外した非公開情報

- 非公開情報を除外
- 送信元プロジェクトを匿名化
- ローカルパスを伏せ字化

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

- 2026-05-13T23:00:57+09:00 [implementation] Implemented role-scoped repo-local bridge generation. feedback-source/local-and-feedback repos now receive a project-side bridge and only feedback/lifecycle skills; upstream/meta lab repos keep lab/eval/propose guidance. update-harness retires unedited managed skills that no longer belong to the repo role and reports retained edited retired files.

## Research Scans

research scan はまだありません。


## Evaluation

### E0028: E0028: FB0029-provide-a-project-side-interface-for-feedback-source-repositories を評価


- source: `harness-lab/records/eval-cases/E0028-fb0029-provide-a-project-side-interface-for-feedback-source-repositories.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0028-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0028-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=1, operator_burden=0, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Validated role-scoped bridge behavior with focused agent bridge/update-harness tests plus full suite: ruff check ., pytest -q (90 passed), hops doctor --check-overlay --check-records, hops migrate --check.


## Hypotheses

### H0028: H0028: E0028-fb0029-provide-a-project-side-interface-for-feedback-source-repositories の仮説


Source: `harness-lab/records/hypotheses/H0028-e0028-fb0029-provide-a-project-side-interface-for-feedback-source-repositories.md`


# H0028: E0028-fb0029-provide-a-project-side-interface-for-feedback-source-repositories の仮説

## 仮説

評価ケースを失敗させた最小の上流挙動を変更し、`E0028` の `unclassified` を改善する。

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0028` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops eval --case E0028 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0028-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/12

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0029: D0029: adopted H0028


Source: `harness-lab/records/decisions/D0029-adopted-h0028.md`


# D0029: adopted H0028

## 判断

adopted

## 理由

Role-scoped bridge generation directly addresses issue #12 by separating project-side feedback capture from lab/eval/propose/decision workflows.

## 証拠

ruff check .; pytest -q (90 passed); hops doctor --check-overlay --check-records; hops migrate --check; harness-lab/views/eval-results/E0028-manual-score.yml

## 回帰リスク

Medium-low: project repos no longer receive lab-oriented generated skills; update-harness retires only unchanged managed retired files and reports edited ones.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation; tests/test_cli/test_mvp_flow.py::test_update_harness_retires_project_side_lab_agent_skills; tests/test_agent_harness_contract.py::test_generated_bridge_scopes_feedback_source_interface
