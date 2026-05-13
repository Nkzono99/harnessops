---
id: D0033
record_type: decision
created_at: '2026-05-14T01:04:49+09:00'
status: adopted
source: H0032
evidence:
  summary: 'Implemented lab_health in steward_preflight; added steward tests for stale lab health and project-repo skip behavior; updated daily steward docs and packaged skills; validation passed: uv run pytest -q, uv run ruff check changed files, hops doctor --check-overlay --check-records, hops migrate --check.'
  guard_path: tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
---

# D0033: adopted H0032

## 判断

adopted

## 理由

The change keeps steward preflight deterministic while surfacing an existing non-writing lab memory signal that daily runs already need for routing.

## 証拠

Implemented lab_health in steward_preflight; added steward tests for stale lab health and project-repo skip behavior; updated daily steward docs and packaged skills; validation passed: uv run pytest -q, uv run ruff check changed files, hops doctor --check-overlay --check-records, hops migrate --check.

## 回帰リスク

Low to moderate. Preflight JSON grows and now calls lab memory lint for lab repos, but the lint path is read-only and project repos explicitly skip lab health.

## フォローアップ

Consider a later ranking view that orders triggered lanes by lab_health, guard gaps, and stale adopted decisions; keep it out of deterministic preflight until evidence justifies it.

## 回帰ガード

tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
