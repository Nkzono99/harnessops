---
id: IMP0009
record_type: improvement_dossier
created_at: '2026-05-13T02:03:24+09:00'
updated_at: '2026-05-13T02:42:10+09:00'
status: active
source_type: dry-run
scope: harnessops-core
maturity: investigated
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0013
eval_cases: []
hypotheses: []
decisions: []
classification:
  capability: meta_improvement_research
  failure_class: unstructured_research_scan_results
guard:
  status: planned
  path: tests/test_agent_harness_contract.py
investigation:
- created_at: '2026-05-13T02:03:24+09:00'
  kind: external-benchmark
  summary: 'External practices suggest the research result should be more structured than a prose note: SRE postmortem tooling captures sections/tables for repository analysis; Open Practice Library experiment design requires explicit hypothesis, current condition, target condition, pass, measures, and learning; Technology Radar uses visible maturity rings that can move over time.'
  evidence_ref: https://sre.google/workbook/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq
links:
  issue_url:
---

# IMP0009: FB0013: Structure meta improvement research scan outputs

## Status

- status: active
- maturity: investigated
- source_type: dry-run
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0013`
- linked_records: `FB0013`

## Source Observation

Source: `harness-lab/records/feedback/FB0013-structure-meta-improvement-research-scan-outputs.md`

# FB0013: Structure meta improvement research scan outputs

## 概要

Dry-running the manual meta improvement research skill produced useful candidates, but the result exists only as prose in the agent response or as free-form investigation summaries. HarnessOps lacks a structured research-scan artifact or view for candidate, evidence, relation, recommendation, and next command.

## 再現

Run hops-research-improvements against the current repository. The skill instructs the agent to output Scope, Evidence, Candidates, and Recommendation, but CLI support stops at lab investigate/classify/capture/propose.

## 期待する上流変更

Add a lightweight structured research-scan record or command, for example a lab research/scan artifact that can hold candidates with evidence refs, relation, recommended action, and optional conversion to investigate/capture/propose.

## Target Capability

- capability: meta_improvement_research
- failure_class: unstructured_research_scan_results

## Investigation

- 2026-05-13T02:03:24+09:00 [external-benchmark] External practices suggest the research result should be more structured than a prose note: SRE postmortem tooling captures sections/tables for repository analysis; Open Practice Library experiment design requires explicit hypothesis, current condition, target condition, pass, measures, and learning; Technology Radar uses visible maturity rings that can move over time. (evidence: https://sre.google/workbook/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)

## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: planned
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。
