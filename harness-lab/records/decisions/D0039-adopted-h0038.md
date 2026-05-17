---
id: D0039
record_type: decision
created_at: '2026-05-17T09:44:40+09:00'
status: adopted
source: H0038
evidence:
  summary: hops steward preflight --json includes hops-open-meta-scan at order 3; subagent_plan recommends open-meta-scan; focused steward and contract tests pass; ruff passes.
  guard_path: tests/test_cli/test_steward.py::test_steward_preflight_json_reports_run_ledger
---

# D0039: adopted H0038

## 判断

adopted

## 理由

The explicit lane makes open meta scanning a first-class subagent result instead of hidden work inside invention.

## 証拠

hops steward preflight --json includes hops-open-meta-scan at order 3; subagent_plan recommends open-meta-scan; focused steward and contract tests pass; ruff passes.

## 回帰リスク

Low: lane count changes from five to six, so existing consumers expecting five lanes must use supervisor_plan dynamically.

## フォローアップ

Watch the next daily steward run for raw idea quality and whether invention records too many candidates.

## 回帰ガード

tests/test_cli/test_steward.py::test_steward_preflight_json_reports_run_ledger
