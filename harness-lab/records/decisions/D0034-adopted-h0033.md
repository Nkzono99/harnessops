---
id: D0034
record_type: decision
created_at: '2026-05-14T01:51:24+09:00'
status: adopted
source: H0033
evidence:
  summary: 'docs/daily-steward-automation.md documents GitHub Flow, lane budgets, PR/merge gates, and no direct protected branch push; .agents/skills/hops-daily-steward/SKILL.md and packaged Codex/Claude copies carry the same rules; tests/test_agent_harness_contract.py asserts the prompt contract; validation: uv run pytest tests/test_agent_harness_contract.py tests/test_cli/test_mvp_flow.py -q (63 passed), uv run ruff check src tests (passed), git diff --check (passed), hops doctor --check-overlay --check-records (ok).'
  guard_path: tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents
---

# D0034: adopted H0033

## 判断

adopted

## 理由

Adopted because GitHub Flow matches the desired automation posture: branch-protected main stays protected, validated automation work can still finish through PR/merge, and lane budgets let the steward handle lightweight backfills without diluting the systemic candidate standard.

## 証拠

docs/daily-steward-automation.md documents GitHub Flow, lane budgets, PR/merge gates, and no direct protected branch push; .agents/skills/hops-daily-steward/SKILL.md and packaged Codex/Claude copies carry the same rules; tests/test_agent_harness_contract.py asserts the prompt contract; validation: uv run pytest tests/test_agent_harness_contract.py tests/test_cli/test_mvp_flow.py -q (63 passed), uv run ruff check src tests (passed), git diff --check (passed), hops doctor --check-overlay --check-records (ok).

## 回帰リスク

Medium-low: automation may still be blocked by required checks, branch protection, or PR conflicts, but the prompt requires leaving the branch/PR intact and reporting blockers. Direct main push is explicitly disallowed.

## フォローアップ

If future runs need higher throughput, raise lane budgets explicitly by run type rather than turning daily steward into an unbounded backlog processor.

## 回帰ガード

tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents
