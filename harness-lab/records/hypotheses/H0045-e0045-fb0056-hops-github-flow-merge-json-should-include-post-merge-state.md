---
id: H0045
record_type: hypothesis
created_at: '2026-05-22T03:13:45+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0045
---

# H0045: E0045-fb0056-hops-github-flow-merge-json-should-include-post-merge-state の仮説

## 仮説

After a successful github-flow merge, HOPS can query the PR again and expose an unambiguous post-merge snapshot while preserving the existing pre-merge gating fields.

## メカニズム

Keep the existing pre-merge view for draft/conflict/check gating, store it as pre_merge_pr, then after gh pr merge succeeds run gh pr view with state,mergedAt,mergeCommit,headRefName,baseRefName,url,number and expose post_merge_pr plus top-level merged and deletedBranch fields.

## 最小実装

Update github_flow merge JSON assembly and add focused CLI tests with fake gh responses.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0045` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run the focused github_flow_merge test subset plus HOPS doctor and migrate checks.

## 中止基準

Reject if merge can report success without a post-merge query, if failed merges lose the PR URL/reason, or if required-check gating is weakened.
