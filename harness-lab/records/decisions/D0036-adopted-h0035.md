---
id: D0036
record_type: decision
created_at: '2026-05-14T11:12:43+09:00'
status: adopted
source: H0035
evidence:
  summary: Updated hops-issue-triage and hops-daily-steward skills; synchronized packaged Codex/Claude assets; uv run pytest tests/test_agent_harness_contract.py -q; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; hops migrate --check; manual eval E0035.
  guard_path: tests/test_agent_harness_contract.py
---

# D0036: adopted H0035

## 判断

adopted

## 理由

The issue triage workflow now covers target-repo open issue intake without relying on repo-local triage skills, while preserving HarnessOps record routing and remote-action authorization boundaries.

## 証拠

Updated hops-issue-triage and hops-daily-steward skills; synchronized packaged Codex/Claude assets; uv run pytest tests/test_agent_harness_contract.py -q; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; hops migrate --check; manual eval E0035.

## 回帰リスク

Low. The change is skill/documentation guidance and contract tests; risk is over-triaging unrelated issues, mitigated by close-candidate and remote-action authority rules.

## フォローアップ

Consider a future CLI helper that emits the open issue triage report from gh/GitHub connector data.

## 回帰ガード

tests/test_agent_harness_contract.py
