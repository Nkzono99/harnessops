---
id: D0023
record_type: decision
created_at: '2026-05-13T17:57:38+09:00'
status: adopted
source: H0022
evidence:
  summary: pytest tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions -q; pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check.
  guard_path: tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions
---

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
