---
id: IMP0024
record_type: improvement_dossier
created_at: '2026-05-13T22:11:13+09:00'
updated_at: '2026-05-13T22:12:24+09:00'
status: adopted
source_type: external-issue
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0027
eval_cases:
- E0027
hypotheses:
- H0027
decisions:
- D0028
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/9
---

# IMP0024: FB0027: Make generated bridge instructions provide a valid hops invocation in target repos

## Status

- status: adopted
- maturity: adopted
- source_type: external-issue
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0027`
- linked_records: `FB0027`, `E0027`, `H0027`, `D0028`

## Source Observation

Source: `harness-lab/records/feedback/FB0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos.md`

# FB0027: Make generated bridge instructions provide a valid hops invocation in target repos

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/9
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T15:32:51Z
updated_at: 2026-05-12T15:32:51Z

## Issue本文
## Context

HarnessOps bridge skills currently tell agents:

```text
PATH に `hops` がない環境では `uv run --with-editable . hops <command>` を使います。
```

This is only correct when the current repository is the HarnessOps checkout. In a linked target repository such as runops, `uv run --with-editable . hops ...` tries to install/run the target project, which does not provide the `hops` console script. During the runops update work, `hops` was not on PATH, so the usable command was instead:

```bash
uv run --with-editable [local HarnessOps checkout path] hops <command>
```

That path knowledge was available to the human/session, but not represented in the project bridge metadata or skill instructions.

## Proposal

Make HarnessOps agent bridge instructions and/or project metadata provide a reliable way to invoke `hops` from target repositories.

Possible approaches:

- Record a `hops_command` or `hops_source` hint in `.harnessops/project.toml` or a generated bridge file.
- Generate bridge skill text that distinguishes between:
  - `hops` installed on PATH
  - HarnessOps checkout available at a known path
  - no local HarnessOps checkout, requiring installation guidance
- Provide a command such as `hops doctor --print-invocation` or `hops bridge command` that emits the recommended invocation for agents.
- Avoid suggesting `uv run --with-editable . hops` in target repositories unless the target actually declares/provides `hops`.

## Why this matters

The bridge is supposed to make target-side agents delegate HarnessOps operations to the CLI. If the fallback invocation is wrong, agents either fail early or bypass HOPS with direct file edits/manual GitHub commands.

## Acceptance criteria

- A linked target repo's generated bridge skill contains a valid fallback command for running HOPS.
- `hops doctor --check-overlay` can detect and warn when the bridge fallback command is not valid for the target repo.
- Tests cover a target repo that does not provide the `hops` console script.

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

### E0027: E0027: FB0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos を評価


- source: `harness-lab/records/eval-cases/E0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0027-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0027-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=4, maintainability=4, privacy_sanitization_risk=2
- notes: Doctor now warns when a target repo bridge contains the stale editable fallback and the repo does not declare a local hops console script. Focused positive/negative tests, full pytest, ruff, doctor, and migrate passed.


## Hypotheses

### H0027: H0027: E0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos の仮説


Source: `harness-lab/records/hypotheses/H0027-e0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos.md`


# H0027: E0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos の仮説

## 仮説

Doctor should warn when a linked repo-local HarnessOps bridge tells agents to run an editable local hops fallback that the current target repo cannot provide.

## メカニズム

Scan generated HarnessOps bridge skill files during doctor, detect the stale editable fallback string, and compare it with the current repo's pyproject console scripts so target repos without a hops entrypoint get an actionable warning.

## 最小実装

Add a validation helper for stale bridge fallback text, wire it into doctor warnings, and cover a linked target fixture that lacks a hops console script.

## 代替案: 削除または統合

Do not add a new invocation command yet; the generated bridge already uses uvx, so the residual need is stale/invalid fallback detection.

## 期待される利点

Agents in target/project repos are steered back to update-harness or uvx instead of bypassing HOPS after an invalid fallback command.

## 想定される欠点

Doctor gains another text-based bridge check that must avoid false positives for HarnessOps development docs.

## 評価計画

Run a focused CLI test that rewrites a generated target bridge to the stale editable fallback and confirms doctor warns, plus contract tests and full repo validation.

## 中止基準

Reject if doctor warns on normal generated uvx bridge files or requires private local HarnessOps checkout paths to pass.


## Evidence

`harness-lab/views/eval-results/E0027-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/9

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0028: D0028: adopted H0027


Source: `harness-lab/records/decisions/D0028-adopted-h0027.md`


# D0028: adopted H0027

## 判断

adopted

## 理由

Adopted because doctor now detects stale editable HarnessOps bridge fallback text in target repos that cannot provide a local hops console script, while leaving generated uvx bridge guidance and local hops providers alone.

## 証拠

pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; focused doctor bridge fallback tests passed.

## 回帰リスク

Low; the change is a warning-only validation hook scoped to repo-local harnessops-bridge skill files and guarded by positive/negative CLI tests.

## フォローアップ

Remote issue #9 remains open because automation was not authorized to comment or close GitHub issues.

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback
