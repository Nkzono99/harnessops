---
id: D0029
record_type: decision
created_at: '2026-05-13T23:01:42+09:00'
status: adopted
source: H0028
evidence:
  summary: ruff check .; pytest -q (90 passed); hops doctor --check-overlay --check-records; hops migrate --check; harness-lab/views/eval-results/E0028-manual-score.yml
  guard_path: tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation; tests/test_cli/test_mvp_flow.py::test_update_harness_retires_project_side_lab_agent_skills; tests/test_agent_harness_contract.py::test_generated_bridge_scopes_feedback_source_interface
---

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
