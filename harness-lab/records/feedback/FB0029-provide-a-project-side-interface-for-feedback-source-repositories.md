---
id: FB0029
record_type: imported_feedback
created_at: '2026-05-13T22:53:07+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-12
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 12
    url: https://github.com/Nkzono99/harnessops/issues/12
    title: Provide a project-side interface for feedback-source repositories
    author: Nkzono99
    labels: []
    created_at: '2026-05-13T13:41:49Z'
    updated_at: '2026-05-13T13:41:49Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/12
---

# FB0029: Provide a project-side interface for feedback-source repositories

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/12
author: Nkzono99
labels: なし
created_at: 2026-05-13T13:41:49Z
updated_at: 2026-05-13T13:41:49Z

## Issue本文
## Context

HarnessOps lab record `FB0003` was promoted to a GitHub Issue draft.

Source dossier: `harness-lab/improvements/IMP0003-fb0003-project-side-feedback-source-repositories-need-a-role-scoped-interface.md`

## Proposal

# IMP0003: FB0003: Project-side feedback-source repositories need a role-scoped interface

## Status

- status: active
- maturity: raw
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0003`
- linked_records: `FB0003`

## Source Observation

Source: `harness-lab/records/feedback/FB0003-project-side-feedback-source-repositories-need-a-role-scoped-interface.md`

# FB0003: Project-side feedback-source repositories need a role-scoped interface

## 概要

runops project directories initialize HarnessOps with profile=runops-project, which is feedback-source mode and writes harness-feedback/. In that role agents mainly need feedback capture/export plus lifecycle checks, but the generic agent bridge exposes broader harness-lab/eval/propose commands that belong to target or meta repositories. This blurs the boundary between project-side private feedback capture and upstream adoption decisions.

## 再現

In runops, runo init delegates to hops init --profile runops-project --with-agent-bridge. The runops-project profile is mode=feedback-source with path=harness-feedback, while the generated HarnessOps bridge lists lab capture/dossier/investigate/classify/new-eval-case/propose/eval/decide commands as general guidance.

## 期待する上流変更

HarnessOps should provide a project-side minimal interface or role-scoped bridge for feedback-source repositories, exposing init/doctor/update-harness/migrate and feedback commands while keeping lab/eval/propose/decide guidance scoped to upstream-lab or meta-lab repositories.

## Target Capability

- capability: role_scoped_agent_bridge
- failure_class: project_feedback_interface_too_broad

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: not-defined
- path: None

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。

## Safety

This body was sanitized by HarnessOps before issue creation.


## 除外した非公開情報

- 非公開情報を除外
- 送信元プロジェクトを匿名化
- ローカルパスを伏せ字化

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
