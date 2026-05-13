---
id: FB0024
record_type: imported_feedback
created_at: '2026-05-13T18:22:23+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-11
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 11
    url: https://github.com/Nkzono99/harnessops/issues/11
    title: Make hops-research-improvements less myopic
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-13T09:17:09Z'
    updated_at: '2026-05-13T09:17:09Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/11
---

# FB0024: Make hops-research-improvements less myopic

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/11
author: Nkzono99
labels: enhancement
created_at: 2026-05-13T09:17:09Z
updated_at: 2026-05-13T09:17:09Z

## Issue本文
## Problem

The `hops-research-improvements` workflow currently tends to select very local, near-term improvement candidates. In recent target-repo use it quickly promoted concrete friction such as individual CLI traceback handling or update-harness edge cases. Those can be useful, but the workflow is too eager to turn the latest observed annoyance into a lab record or issue.

This makes the skill feel myopic: it captures symptoms before stepping back to ask whether the observation is part of a broader capability gap, a repeated cross-project pattern, or just a small local bug that should be parked.

## Expected behavior

Before creating `hops lab capture`, `research-scan`, or a GitHub issue, the skill should do an explicit strategy pass:

- Group observations by horizon: immediate bugfix, workflow design, evaluation methodology, cross-project harness principle.
- Prefer systemic improvements over one-off local fixes unless the local fix is a guardrail for a broader failure class.
- Require a short generalization check: what capability does this improve, which failure class does it represent, and would it matter in at least two target/project repos?
- Add a "park/reject as local" path for observations that are real but too narrow.
- Encourage synthesis across several small frictions before proposing a new improvement dossier.

## Possible implementation

Update the `hops-research-improvements` skill with a mandatory pre-capture section such as:

1. List candidate observations.
2. Mark each as `local-only`, `repeated-pattern`, `cross-project`, or `strategic`.
3. Choose at most one systemic candidate.
4. Park narrow candidates unless they are evidence for the systemic one.
5. Only then run `hops lab capture`, `hops lab research-scan`, or `hops lab investigate/classify`.

The workflow could also add wording like: "Do not create a new record for the newest friction unless it reveals a broader mechanism or evaluation gap."

## Evaluation idea

Create an eval case with several local frictions, for example:

- a CLI command prints a traceback for invalid input
- update-harness emits a confusing `.new` file
- a target skill lacks context about repo role

The expected output should not be three separate improvement issues. It should synthesize a broader candidate, such as "research-improvement candidate selection needs a horizon/generalization guard", and park the narrow fixes as evidence.

## Acceptance criteria

- The skill contains an explicit anti-myopia / horizon-scan step before capture or issue creation.
- The output format includes a `park` or `local-only` recommendation path.
- A test or fixture verifies that multiple narrow observations are synthesized into one broader improvement instead of being promoted independently.
- Existing useful behavior remains: truly urgent guardrail bugs can still be captured when they protect a wider failure class.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
