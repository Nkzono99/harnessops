---
id: IMP0035
record_type: improvement_dossier
created_at: '2026-05-18T03:08:59+09:00'
updated_at: '2026-05-18T03:10:01+09:00'
status: adopted
source_type: github-issue
scope: harnessops-core
maturity: implemented
relation: extends
promotion_level: target-lab-case
source_feedback: FB0052
eval_cases:
- E0039
hypotheses:
- H0039
decisions:
- D0040
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/29
---

# IMP0035: FB0052: Support squash/rebase merge methods in github-flow merge

## Status

- status: adopted
- maturity: implemented
- source_type: github-issue
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0052`
- linked_records: `FB0052`, `E0039`, `H0039`, `D0040`

## Source Observation

Source: `harness-lab/records/feedback/FB0052-support-squash-rebase-merge-methods-in-github-flow-merge.md`

# FB0052: Support squash/rebase merge methods in github-flow merge

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/29
author: Nkzono99
labels: bug, enhancement
created_at: 2026-05-17T00:29:32Z
updated_at: 2026-05-17T00:29:32Z

## Issue本文
## Summary

`hops github-flow merge --require-checks` currently invokes `gh pr merge --merge`. This blocks automation in repositories that intentionally disable merge commits but allow squash or rebase merges.

## Observed

During the paperops daily steward run on 2026-05-17, validation passed and PR #38 was clean:

- Target repo: https://github.com/Nkzono99/paperops
- PR: https://github.com/Nkzono99/paperops/pull/38
- Branch: `codex/steward/20260517-daily`
- Required check: `Smoke / smoke` passed
- `hops github-flow merge --require-checks` failed because the repository disallows merge commits
- Manual workaround: `gh pr merge 38 --repo Nkzono99/paperops --squash --delete-branch`

## Expected

`hops github-flow merge` should support repositories whose allowed merge method is squash or rebase.

Possible shape:

- Add `--method merge|squash|rebase|auto` to `hops github-flow merge`
- Default to `auto` or read the repository's allowed merge methods before choosing
- Preserve `--require-checks` behavior before merging
- Keep protected-branch direct pushes forbidden

## Acceptance criteria

- A repo with merge commits disabled and squash enabled can be merged by HOPS after required checks pass
- A repo with rebase-only policy can be merged by HOPS after required checks pass
- Failure output clearly names the attempted method and the repo policy mismatch
- Existing merge-commit-enabled repos keep working

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

### E0039: E0039: FB0052-support-squash-rebase-merge-methods-in-github-flow-merge を評価


- source: `harness-lab/records/eval-cases/E0039-fb0052-support-squash-rebase-merge-methods-in-github-flow-merge.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0039-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0039-manual-score.md`
- scores: impact=4, mechanism_clarity=0, evaluability=0, minimality=0, regression_risk=0, operator_burden=0, anti_theater=4, maintainability=0, privacy_sanitization_risk=0
- notes: Implemented github-flow merge --method auto|merge|squash|rebase, preserved required-check gating, and added focused CLI tests covering squash auto-selection, explicit rebase, and clear merge-method failure reporting.


## Hypotheses

### H0039: H0039: E0039-fb0052-support-squash-rebase-merge-methods-in-github-flow-merge の仮説


Source: `harness-lab/records/hypotheses/H0039-e0039-fb0052-support-squash-rebase-merge-methods-in-github-flow-merge.md`


# H0039: E0039-fb0052-support-squash-rebase-merge-methods-in-github-flow-merge の仮説

## 仮説

Allow github-flow merge to select merge, squash, or rebase methods while preserving required-check gating and clear failure reporting.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0039` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops lab eval --case E0039 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0039-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/29

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0040: D0040: adopted H0039


Source: `harness-lab/records/decisions/D0040-adopted-h0039.md`


# D0040: adopted H0039

## 判断

adopted

## 理由

github-flow merge can now choose repository-compatible merge methods while preserving required-check and conflict gates.

## 証拠

uv run pytest tests/test_cli/test_mvp_flow.py; uv run ruff check src/harnessops/cli/github_flow.py tests/test_cli/test_mvp_flow.py

## 回帰リスク

Low: command behavior remains gated by gh pr view/checks and existing merge repositories are handled through auto selecting merge when allowed.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
