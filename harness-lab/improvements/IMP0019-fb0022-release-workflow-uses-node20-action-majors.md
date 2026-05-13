---
id: IMP0019
record_type: improvement_dossier
created_at: '2026-05-13T17:55:00+09:00'
updated_at: '2026-05-13T17:57:38+09:00'
status: adopted
source_type: external-benchmark
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0022
eval_cases:
- E0022
hypotheses:
- H0022
decisions:
- D0023
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions
investigation:
- created_at: '2026-05-13T17:55:15+09:00'
  kind: external-benchmark
  summary: GitHub's Node20 deprecation notice says runners begin using Node24 by default on 2026-06-02 and users should update workflows to latest actions that run on Node24; v0.1.4 release run already emitted this annotation.
  evidence_ref: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
links:
  issue_url:
---

# IMP0019: FB0022: Release workflow uses Node20 action majors

## Status

- status: adopted
- maturity: adopted
- source_type: external-benchmark
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0022`
- linked_records: `FB0022`, `E0022`, `H0022`, `D0023`

## Source Observation

Source: `harness-lab/records/feedback/FB0022-release-workflow-uses-node20-action-majors.md`

# FB0022: Release workflow uses Node20 action majors

## 概要

The v0.1.4 PyPI publish workflow succeeded but GitHub Actions annotated the run because actions/checkout@v4 and actions/setup-python@v5 still run on Node.js 20. GitHub plans Node24 default migration on 2026-06-02, so the release workflow should use Node24-ready action majors before this becomes release friction.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The PyPI publish workflow should use Node24-ready action majors and a regression test should guard against reintroducing Node20-era checkout/setup-python majors.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T17:55:15+09:00 [external-benchmark] GitHub's Node20 deprecation notice says runners begin using Node24 by default on 2026-06-02 and users should update workflows to latest actions that run on Node24; v0.1.4 release run already emitted this annotation. (evidence: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)

## Research Scans

research scan はまだありません。


## Evaluation

### E0022: E0022: FB0022-release-workflow-uses-node20-action-majors を評価


- source: `harness-lab/records/eval-cases/E0022-fb0022-release-workflow-uses-node20-action-majors.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0022-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0022-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=1, operator_burden=1, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Updated the PyPI publish workflow to actions/checkout@v5 and actions/setup-python@v6 while preserving the pypi environment, id-token permission, Python 3.11, build, twine check, and publish steps. Added a workflow contract test. Focused test, full pytest, ruff, doctor, and migrate all passed.


## Hypotheses

### H0022: H0022: E0022-fb0022-release-workflow-uses-node20-action-majors の仮説


Source: `harness-lab/records/hypotheses/H0022-e0022-fb0022-release-workflow-uses-node20-action-majors.md`


# H0022: E0022-fb0022-release-workflow-uses-node20-action-majors の仮説

## 仮説

Updating the PyPI publish workflow to Node24-ready GitHub action majors will remove release-time Node20 deprecation risk without changing the build or publish semantics.

## メカニズム

Use actions/checkout@v5 and actions/setup-python@v6 in .github/workflows/publish-pypi.yml while keeping the existing Python 3.11, build, twine check, and trusted publisher steps unchanged.

## 最小実装

Edit the publish workflow action majors and add a repository test that asserts checkout@v5 and setup-python@v6 are used for the PyPI publish workflow.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0022` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run the workflow contract test, full pytest, ruff, hops doctor, and hops migrate; release-time validation can later confirm that GitHub no longer emits Node20 action annotations.

## 中止基準

Reject if the workflow stops publishing via the existing pypi environment, drops id-token permission, changes Python version unintentionally, or cannot be represented by a simple contract test.


## Evidence

`harness-lab/views/eval-results/E0022-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0023: D0023: adopted H0022


Source: `harness-lab/records/decisions/D0023-adopted-h0022.md`


# D0023: adopted H0022

## 判断

adopted

## 理由

Adopted because the release workflow now uses Node24-ready action majors without changing publishing semantics.

## 証拠

pytest tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions -q; pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check.

## 回帰リスク

Low; only action major versions changed, and the contract test preserves the trusted publisher environment and id-token permission.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions
