---
id: D0022
record_type: decision
created_at: '2026-05-13T17:19:35+09:00'
status: adopted
source: H0021
evidence:
  summary: pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; rg confirms target-facing editable fallback is absent.
  guard_path: tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract
---

# D0022: adopted H0021

## 判断

adopted

## 理由

Adopted because packaged agent assets now match the PyPI/uvx downstream invocation model while preserving editable commands for HarnessOps development workflows.

## 証拠

pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; rg confirms target-facing editable fallback is absent.

## 回帰リスク

Low; changes are text guidance and contract assertions, with update-harness propagation verified through targeted CLI tests.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract
