---
id: IMP0041
record_type: improvement_dossier
created_at: '2026-05-22T03:18:30+09:00'
updated_at: '2026-05-22T03:18:43+09:00'
status: adopted
source_type: github-issue
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0056
eval_cases:
- E0045
hypotheses:
- H0045
decisions:
- D0046
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_github_flow_merge_auto_uses_squash_when_merge_commits_disabled
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/40
---

# IMP0041: FB0056: hops github-flow merge --json should include post-merge state

## Status

- status: adopted
- maturity: adopted
- source_type: github-issue
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0056`
- linked_records: `FB0056`, `E0045`, `H0045`, `D0046`

## Source Observation

Source: `harness-lab/records/feedback/FB0056-hops-github-flow-merge-json-should-include-post-merge-state.md`

# FB0056: hops github-flow merge --json should include post-merge state

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/40
author: Nkzono99
labels: enhancement
created_at: 2026-05-20T01:08:49Z
updated_at: 2026-05-20T01:08:49Z

## Issue本文
## Summary

Transferred from runops issue #88: https://github.com/Nkzono99/runops/issues/88

`hops github-flow merge --json` has returned PR information captured before merge, so `pr.state` can remain `OPEN` even when the merge command itself succeeded. Finalization lanes then need an extra `gh pr view --json state,mergedAt,mergeCommit` call to build a reliable final report.

The merge command should return machine-readable post-merge state directly.

## Expected JSON fields

Possible fields:

- `merged: true|false`
- `pr.number`, `pr.url`, `pr.state`
- `mergedAt`
- `mergeCommit.oid`
- `headRefName`, `baseRefName`
- `deletedBranch: true|false`
- `checksSummary`
- if both snapshots are useful, distinguish them as `pre_merge_pr` and `post_merge_pr`

## Acceptance criteria

- After a successful merge, JSON indicates `state=MERGED` or `merged=true`.
- Merge commit SHA is available from JSON.
- Branch deletion success/failure is available from JSON.
- Pre-merge and post-merge snapshots are not mixed under ambiguous field names.
- Automation can produce its final report without a second `gh pr view` call.

## Evidence from target repo

During a runops steward run, `hops github-flow merge 83 --require-checks --delete-branch --json` succeeded, but returned `pr.state` from the pre-merge snapshot. The runops lab records track this as `FB0014` / `E0014` / `H0014` / `IMP0014`, with decision `D0014` currently `needs-more-evidence`.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0045: E0045: FB0056-hops-github-flow-merge-json-should-include-post-merge-state を評価


- source: `harness-lab/records/eval-cases/E0045-fb0056-hops-github-flow-merge-json-should-include-post-merge-state.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0045-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0045-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=4, operator_burden=4, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: Implemented post-merge PR lookup for github-flow merge JSON. Focused validation passed: uv run pytest tests/test_cli/test_mvp_flow.py -k github_flow_merge -q (5 passed); uv run ruff check src tests passed.


## Hypotheses

### H0045: H0045: E0045-fb0056-hops-github-flow-merge-json-should-include-post-merge-state の仮説


Source: `harness-lab/records/hypotheses/H0045-e0045-fb0056-hops-github-flow-merge-json-should-include-post-merge-state.md`


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


## Evidence

`harness-lab/views/eval-results/E0045-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_github_flow_merge_auto_uses_squash_when_merge_commits_disabled

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/40

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0046: D0046: adopted H0045


Source: `harness-lab/records/decisions/D0046-adopted-h0045.md`


# D0046: adopted H0045

## 判断

adopted

## 理由

Implemented unambiguous post-merge JSON for github-flow merge.

## 証拠

Focused validation passed: uv run pytest tests/test_cli/test_mvp_flow.py -k github_flow_merge -q (5 passed); uv run ruff check src tests passed. Output now keeps pre_merge_pr separate, updates pr/post_merge_pr after successful merge, exposes merged/mergedAt/mergeCommit, and checks deletedBranch.

## 回帰リスク

Low: behavior is scoped to successful merge JSON assembly after existing draft/conflict/check gates and merge method selection.

## フォローアップ

Finalize should include Closes #40 in the PR body after full validation.

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_github_flow_merge_auto_uses_squash_when_merge_commits_disabled
