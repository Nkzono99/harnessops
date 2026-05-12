---
id: FB0007
record_type: imported_feedback
created_at: '2026-05-13T00:00:03+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-7
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 7
    url: https://github.com/Nkzono99/harnessops/issues/7
    title: Simplify harness-lab around per-improvement dossiers
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-12T14:53:47Z'
    updated_at: '2026-05-12T14:53:47Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/7
---

# FB0007: Simplify harness-lab around per-improvement dossiers

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/7
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:53:47Z
updated_at: 2026-05-12T14:53:47Z

## Issue本文
## Context

`harness-lab/` has a good theory: GitHub Issues remain the task tracker, while the lab keeps evaluation memory, hypotheses, experiments, and decisions.

In actual use, the current structure feels too heavy for the common case. A single improvement can quickly spread across multiple thin files and directories:

- `records/feedback/FB0001-...md`
- `records/eval-cases/E0001-...md`
- `records/hypotheses/H0001-...md`
- `records/experiments/`
- `records/decisions/D0001-...md`
- generated views under `views/`

The individual files are often mostly boilerplate at the moment they are created. More importantly, the workflow for recording an improvement and later using that record during implementation/review is not yet obvious enough.

## Concern

For day-to-day harness improvement, this may create more bookkeeping than memory:

- The directory structure is cognitively expensive.
- The relationship between feedback, eval case, hypothesis, experiment, and decision is hard to scan.
- The content starts thin, so agents/users may create records but not return to them.
- The capture path exists, but the “use this while improving the harness” path is underdeveloped.
- It is unclear which file is the living source of truth for one improvement.

## Proposal

Consider making the ordinary workflow centered on one mutable improvement dossier per improvement, for example:

```text
harness-lab/improvements/IMP0001-promote-improve-harness-workflow.md
```

A dossier could contain sections such as:

- status and current decision
- source observation / feedback
- target capability or failure class
- hypothesis and mechanism
- eval plan and acceptance criteria
- experiments and evidence
- links to GitHub issues / PRs / commits
- open questions and next action
- decision log / changelog

Generated views can then be derived from these dossiers: backlog, active improvements, decisions, score trajectory, and open eval gaps.

The current typed records (`FB`, `E`, `H`, `X`, `D`) could remain as an advanced or normalized layer, but should not be mandatory for the common “record and improve one thing” flow.

## Acceptance criteria

- There is a low-friction command to create or update one improvement dossier.
- A user or agent can open one file and understand the full improvement history.
- Generated views still support triage and review.
- Existing `harness-lab/records/*` layouts have a migration or compatibility story.
- The docs explain when to use a simple dossier versus the normalized multi-record flow.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
