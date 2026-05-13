---
id: IMP0031
record_type: improvement_dossier
created_at: '2026-05-14T01:51:33+09:00'
updated_at: '2026-05-14T01:59:45+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0036
eval_cases:
- E0034
hypotheses:
- H0034
decisions:
- D0035
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents
investigation: []
links:
  issue_url:
---

# IMP0031: FB0036: Let daily steward use lane budgets and merge automation branches

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0036`
- linked_records: `FB0036`, `E0034`, `H0034`, `D0035`

## Source Observation

Source: `harness-lab/records/feedback/FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`

# FB0036: Let daily steward use lane budgets and merge automation branches

## 概要

Daily steward currently treats max-systemic-candidates as a single global cap and the recommended prompt stops after pushing an automation branch. User feedback prefers lane-specific budgets, automatic merge when validation passes, optional develop/integration branch workflow, and no direct main push.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Document lane budgets, keep systemic candidates conservative, allow multiple metadata/backfill/read-only items, and update full automation guidance so validated automation branches can be merged into an authorized base or integration branch without direct protected-branch push.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0034: E0034: FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches を評価


- source: `harness-lab/records/eval-cases/E0034-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0034-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0034-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Updated daily steward docs and repo-local/packaged skill copies to prefer GitHub Flow: automation feature branch, PR, and merge into protected main after validation/required checks. Added lane budgets for systemic candidates, metadata/guard backfills, and read-only park/reject decisions. Updated contract tests to assert the new automation prompt shape. Validation so far: uv run pytest tests/test_agent_harness_contract.py tests/test_cli/test_mvp_flow.py -q (63 passed), uv run ruff check src tests (passed), git diff --check (passed), hops doctor --check-overlay --check-records (ok).


## Hypotheses

### H0034: H0034: E0034-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches の仮説


Source: `harness-lab/records/hypotheses/H0034-e0034-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`


# H0034: E0034-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches の仮説

## 仮説

Daily steward automation should use GitHub Flow by default: commit validated work to an automation feature branch, open or update a PR, and merge into protected main when checks pass, while using lane-specific work budgets to avoid diluting evidence quality.

## メカニズム

The automation prompt and steward skill separate systemic candidates from metadata/guard backfills and read-only decisions, then treat merge as a prompt-authorized remote action outside steward finalize. This preserves branch protection, keeps main direct push disabled, and lets small backfills move without pretending they are systemic candidates.

## 最小実装

Update daily-steward automation docs, agent guide/design principle references, and repo-local plus packaged hops-daily-steward skill copies. Do not change CLI finalize behavior.

## 代替案: 削除または統合

Keep branch-only output or adopt Git Flow develop as the default. Branch-only leaves routine validated work unmerged; Git Flow adds an integration branch the user does not prefer. Keep develop only as an opt-in merge target.

## 期待される利点

Fully automated runs can finish useful validated changes through PR/merge, while lane budgets keep daily runs bounded and reviewable.

## 想定される欠点

Automatic PR merge can still be blocked by branch protection or required checks; automation must report those blockers and leave the branch/PR intact.

## 評価計画

Verify docs and skill text, run ruff/tests as appropriate, and run hops doctor --check-overlay --check-records plus hops migrate --check.

## 中止基準

Revert or revise if automation starts direct-pushing to protected main, merges without validation/checks, or treats multiple systemic candidates as a bulk queue without item-level evidence.


## Evidence

`harness-lab/views/eval-results/E0034-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0035: D0035: adopted H0034


Source: `harness-lab/records/decisions/D0035-adopted-h0034.md`


# D0035: adopted H0034

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
