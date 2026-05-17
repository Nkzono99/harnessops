---
id: H0038
record_type: hypothesis
created_at: '2026-05-17T09:44:18+09:00'
status: proposed
target_capability: daily_steward_orchestration
source_eval_case: E0038
---

# H0038: E0038-fb0049-daily-steward-should-delegate-open-meta-scan の仮説

## 仮説

Daily steward will preserve divergent meta discovery better if open-meta-scan is an explicit supervisor lane before invention.

## メカニズム

Add hops-open-meta-scan to supervisor_plan.lanes so the daily supervisor spawns a dedicated subagent, then make invention review that prior lane's raw ideas and record selected candidates for priority-improvement.

## 最小実装

Insert the open-meta-scan lane, update steward tests, and update repo-local/packaged lane skills plus docs to describe the raw-idea handoff.

## 代替案: 削除または統合

Keep open-meta-scan nested inside hops-invention-steward and rely on that lane to remember to run it.

## 期待される利点

Raw ideas become visible in the steward ledger, invention has an explicit review input, and priority-improvement receives recorded candidates instead of ad hoc summaries.

## 想定される欠点

One more daily steward subagent lane adds latency and one more ledger result to record.

## 評価計画

Check steward preflight JSON includes hops-open-meta-scan at order 3, subagent recommendations include open-meta-scan, packaged skill copies match, and focused steward/contract tests pass.

## 中止基準

Reject if the new lane blocks clean runs, records raw ideas directly without review, or lets priority-improvement depend on unreviewed raw text.
