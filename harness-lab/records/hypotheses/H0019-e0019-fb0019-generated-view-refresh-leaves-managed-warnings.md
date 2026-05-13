---
id: H0019
record_type: hypothesis
created_at: '2026-05-13T11:45:44+09:00'
status: proposed
target_capability: generated_view_management
source_eval_case: E0019
---

# H0019: E0019-fb0019-generated-view-refresh-leaves-managed-warnings の仮説

## 仮説

If lab refresh-views regenerates every lab artifact that doctor validates as managed, then operators can clear stale generated-view warnings with the obvious lab repair command instead of learning to ignore warnings.

## メカニズム

doctor warns by comparing lock managed_file hashes. The lab refresh command currently updates only dynamic views and their hashes, leaving static/generated lab artifacts under old hashes. Reusing the managed overlay refresh path, then dynamic view refresh, will align the command with the full managed set.

## 最小実装

Change hops lab refresh-views to refresh managed overlay files for the current lab overlay before regenerating dynamic views, then keep lock hashes current. Add a regression test where README/backlog/score-trajectory are stale and lab refresh-views clears doctor warnings.

## 代替案: 削除または統合

Add a new top-level hops views refresh/status command and leave lab refresh-views as-is, but this adds surface area before the existing command is made honest.

## 期待される利点

A single lab command repairs all doctor-managed generated lab artifacts and reduces warning fatigue.

## 想定される欠点

Refreshing managed files can overwrite generated static text if it is not locally edited; conflict behavior must preserve edited managed files via existing .new behavior.

## 評価計画

In a fixture repo, stale README/backlog/score-trajectory and run hops lab refresh-views; doctor --check-overlay --check-records should produce no generated-view warnings. Existing dynamic view refresh behavior should still include research scans and improvements.

## 中止基準

Reject this path if it overwrites locally edited managed files without a .new conflict copy, or if it requires a broader views command before the lab-specific repair works.
