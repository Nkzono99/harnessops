---
id: H0042
record_type: hypothesis
created_at: '2026-05-20T03:12:44+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0042
---

# H0042: E0042-fb0054-support-squash-rebase-merge-methods-in-github-flow-merge の仮説

## 仮説

github-flow merge auto-selects an allowed GitHub merge method while preserving required-check gating.

## メカニズム

Resolve --method auto from gh repo view merge policy and pass the selected --merge/--squash/--rebase flag to gh pr merge; allow explicit methods for policy-specific repositories.

## 最小実装

Keep merge prechecks unchanged, add method selection coverage for squash-only and rebase requests, and report the attempted method on merge failure.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

Daily steward finalization can merge target repositories that disable merge commits but allow squash or rebase.

## 想定される欠点

Auto policy lookup adds one gh repo view call before merge.

## 評価計画

Run focused github_flow_merge tests and HOPS doctor/migrate checks.

## 中止基準

Reject if required checks can be bypassed or protected base branches can be direct-pushed.
