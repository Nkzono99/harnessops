---
id: D0024
record_type: decision
created_at: '2026-05-13T18:05:26+09:00'
status: adopted
source: H0023
evidence:
  summary: tests/test_agent_harness_contract.py; pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check.
  guard_path: tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged
---

# D0024: adopted H0023

## 判断

adopted

## 理由

Adopted because repo-local research improvements should be usable wherever HarnessOps is installed, with role-aware routing to lab or feedback workflows.

## 証拠

tests/test_agent_harness_contract.py; pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check.

## 回帰リスク

Medium-low; this broadens instructions, but contract tests preserve packaged skill equality and explicitly guard the project-repo no-harness-lab rule.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged
