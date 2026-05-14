---
id: FB0039
record_type: imported_feedback
created_at: '2026-05-14T11:10:05+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-18
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 18
    url: https://github.com/Nkzono99/harnessops/issues/18
    title: Consolidate repo-local issue triage into HOPS daily steward
    author: Nkzono99
    labels: []
    created_at: '2026-05-14T02:03:28Z'
    updated_at: '2026-05-14T02:03:28Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/18
---

# FB0039: Consolidate repo-local issue triage into HOPS daily steward

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/18
author: Nkzono99
labels: なし
created_at: 2026-05-14T02:03:28Z
updated_at: 2026-05-14T02:03:28Z

## Issue本文
## 背景

runops 側にあった repo-local `triage` skill と `runops-issue-triage-and-run` automation prompt を削除し、issue triage / unattended daily loop は HarnessOps 側の `hops-daily-steward` と `hops-issue-triage` に統一する方針にした。

runops 側の `triage` skill が持っていた汎用機能のうち、HarnessOps 側に寄せるべきものをこの issue で追跡したい。

## 移譲したい機能

- open issue を優先度つきで分類する報告形式を持つ
  - 対応推奨 (高)
  - 対応推奨 (中)
  - 保留 / 要議論
  - close 推奨
- spam / malicious / unrelated issue の close 候補判定を明文化する
- issue close は人間または automation prompt の明示権限がある場合だけ行う、という安全ルールを HOPS daily / issue triage 側へ寄せる
- 対応完了時の issue close 作法を HOPS 側に持つ
  - commit message の `Closes #N`
  - 手動 close コメント
  - won't fix コメント
- `gh issue view` / GitHub connector で本文・コメント・ラベル・再現情報を確認し、不足情報を triage 報告に含める

## 完了条件

- `hops-issue-triage` または `hops-daily-steward` の skill / docs が上記の汎用 issue triage 作法をカバーしている
- repo-local な `triage` skill がなくても、target repository の daily run で issue triage の判断と報告が迷子にならない
- remote actions は automation prompt の権限に従う、という境界が明記されている

## 関連

- runops 側では `.agents/skills/triage`, `.claude/skills/triage`, `.codex/automation-prompts/runops-issue-triage-and-run.md` を削除予定
- runops は target repository として HarnessOps の `hops-daily-steward` に寄せる

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
