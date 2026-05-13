---
id: H0034
record_type: hypothesis
created_at: '2026-05-14T01:49:12+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0034
---

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
