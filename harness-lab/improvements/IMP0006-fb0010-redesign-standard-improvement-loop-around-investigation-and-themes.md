---
id: IMP0006
record_type: improvement_dossier
created_at: '2026-05-13T00:56:17+09:00'
updated_at: '2026-05-13T02:42:06+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0010
eval_cases:
- E0010
hypotheses:
- H0010
decisions:
- D0011
classification:
  capability: improvement_loop_design
  failure_class: ambiguous_improvement_workflow
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T00:56:19+09:00'
  kind: external-benchmark
  summary: Compared the current loop with PDSA, SRE postmortem/action-item practice, ADR decision records, issue triage, and Technology Radar maturity rings; the missing HarnessOps concepts are explicit investigation, theme classification, maturity, guard status, and promotion level.
  evidence_ref: docs/design-principles.md
links:
  issue_url:
---

# IMP0006: FB0010: Redesign standard improvement loop around investigation and themes

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0010`
- linked_records: `FB0010`, `E0010`, `H0010`, `D0011`

## Source Observation

Source: `harness-lab/records/feedback/FB0010-redesign-standard-improvement-loop-around-investigation-and-themes.md`

# FB0010: Redesign standard improvement loop around investigation and themes

## 概要

The current design-principles standard improvement loop is too abstract: observation, routing, guard, and promotion are unclear, and it does not explicitly include investigation, external comparison, improvement classification, theme maturity, or later contradictory/extension observations.

## 再現

While reviewing docs/design-principles.md, the loop leaves agents unsure whether observation includes issues/friction/external research, whether routing means periodic review or classification, what guard means, and how promotion should be designed.

## 期待する上流変更

Define a concrete improvement-loop vocabulary and add lightweight harness support so agents naturally capture observations, investigation notes, classification, theme status, relations, guards, and promotion levels before implementation and review.

## Target Capability

- capability: improvement_loop_design
- failure_class: ambiguous_improvement_workflow

## Investigation

- 2026-05-13T00:56:19+09:00 [external-benchmark] Compared the current loop with PDSA, SRE postmortem/action-item practice, ADR decision records, issue triage, and Technology Radar maturity rings; the missing HarnessOps concepts are explicit investigation, theme classification, maturity, guard status, and promotion level. (evidence: docs/design-principles.md)

## Evaluation

### E0010: E0010: FB0010-redesign-standard-improvement-loop-around-investigation-and-themes を評価


- source: `harness-lab/records/eval-cases/E0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes.md`

- capability: improvement_loop_design

- failure_class: ambiguous_improvement_workflow

- manual_eval_yml: `harness-lab/views/eval-results/E0010-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0010-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=3, operator_burden=4, anti_theater=4, maintainability=4, privacy_sanitization_risk=1
- notes: Redesigned the standard improvement loop around explicit observation, investigation, recording, classification/routing, hypothesis, evaluation design, decision, application, guard, and promotion. Added improvement theme metadata plus lab investigate/classify commands, extended dossier rendering and views, updated agent skills so the flow is natural, and documented that backward compatibility can be cut when migrate/update-harness provides a migration path. Verified with focused tests, full pytest, doctor, and migrate.


## Hypotheses

### H0010: H0010: E0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes の仮説


Source: `harness-lab/records/hypotheses/H0010-e0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes.md`


# H0010: E0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes の仮説

## 仮説

A theme-centered loop with explicit investigation, classification/routing, guard, and promotion semantics will make HarnessOps improvements easier to run consistently and easier to learn from later.

## メカニズム

Add structured dossier fields and CLI commands for recording investigation notes and classification metadata, revise the design principles to define each loop stage, and surface a theme view so agents see status, maturity, relations, guards, and promotion level as part of ordinary lab work.

## 最小実装

Add lab classify/investigate commands that update improvement dossiers, extend dossier frontmatter/body with source/maturity/relation/promotion/guard metadata, and update docs/specs/tests.

## 代替案: 削除または統合

Only rewrite docs/design-principles.md without changing CLI, leaving agents to remember the workflow manually.

## 期待される利点

The harness nudges agents from raw observations toward investigated themes, evaluated hypotheses, guarded adoption, and later benchmarkable experience instead of loose notes.

## 想定される欠点

More metadata can become process overhead if it is mandatory too early or if the dossier becomes the only source of truth.

## 評価計画

Create a lab record, generate a dossier, classify and investigate it, then verify docs, views, tests, doctor, and migrate all pass.

## 中止基準

If the commands duplicate existing FB/E/H/D source-of-truth records or make simple lab capture significantly heavier, keep only the docs change and reject the CLI layer.


## Evidence

`harness-lab/views/eval-results/E0010-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0011: D0011: adopted H0010


Source: `harness-lab/records/decisions/D0011-adopted-h0010.md`


# D0011: adopted H0010

## 判断

adopted

## 理由

H0010 の最小実装を採用。標準改善ループを調査・分類・テーマ成熟度・ガード・昇格まで具体化し、CLI と agent skill が自然にその流れを促すようにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/validation.py src/harnessops/core/agent_bridge.py tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0010-manual-score.yml

## 回帰リスク

Moderate-low. The new metadata is optional and generated into dossiers, while FB/E/H/D records remain the source of truth. AGENTS.md explicitly allows layout cleanup when migrate/update-harness can carry users forward.

## フォローアップ

Consider adding a dedicated migration if future releases make improvement dossier metadata mandatory or remove older lab structures.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
