---
id: IMP0009
record_type: improvement_dossier
created_at: '2026-05-13T02:03:24+09:00'
updated_at: '2026-05-13T03:38:03+09:00'
status: adopted
source_type: dry-run
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0013
eval_cases:
- E0017
hypotheses:
- H0017
decisions:
- D0018
research_scans:
- RS0001
classification:
  capability: meta_improvement_research
  failure_class: unstructured_research_scan_results
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
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

- status: adopted
- maturity: adopted
- source_type: dry-run
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0013`
- linked_records: `FB0013`, `RS0001`, `E0017`, `H0017`, `D0018`

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

## Research Scans

### RS0001: RS0001: Structure meta improvement research scan outputs


Source: `harness-lab/records/research-scans/RS0001-structure-meta-improvement-research-scan-outputs.md`


# RS0001: Structure meta improvement research scan outputs

## Scope

- scope: harnessops-core deliberate meta improvement research
- existing_dossier: IMP0009
- capability: meta_improvement_research
- failure_class: unstructured_research_scan_results

## Evidence

### Local

- IMP0009 remained active because the dry-run result had useful candidates but no structured artifact (ref: harness-lab/improvements/IMP0009-fb0013-structure-meta-improvement-research-scan-outputs.md)

### Codebase

- hops-research-improvements had Scope/Evidence/Candidates/Recommendation prose guidance but no CLI record for it (ref: .agents/skills/hops-research-improvements/SKILL.md)
- The new lab research-scan command stores candidate rows and refreshes views/research-scans.md (ref: src/harnessops/cli/lab.py)

### External

- External investigation for IMP0009 found postmortem, experiment, and maturity-ring practices favor structured action items and learning records (ref: https://sre.google/workbook/postmortem-culture/)

### Risk And Counterexample

- A new record type can create meta-noise if used for every small observation (ref: docs/design-principles.md)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add RS research_scan record and view | extends | propose | hops lab new-eval-case --from FB0013 |

## Recommendation

adopt: use research-scan for deliberate multi-candidate meta-improvement research before routing candidates to investigate/capture/propose/park/reject.

## Next Commands

- `hops lab new-eval-case --from FB0013`


## Evaluation

### E0017: E0017: FB0013-structure-meta-improvement-research-scan-outputs を評価


- source: `harness-lab/records/eval-cases/E0017-fb0013-structure-meta-improvement-research-scan-outputs.md`

- capability: meta_improvement_research

- failure_class: unstructured_research_scan_results

- manual_eval_yml: `harness-lab/views/eval-results/E0017-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0017-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=3, operator_burden=4, anti_theater=4, maintainability=4, privacy_sanitization_risk=5
- notes: Research scans now persist deliberate meta-improvement research as RS records with structured evidence, candidates, relation, recommendation, next command, and a generated view. The implementation keeps existing investigate/capture/propose actions as downstream routing rather than replacing them.


## Hypotheses

### H0017: H0017: E0017-fb0013-structure-meta-improvement-research-scan-outputs の仮説


Source: `harness-lab/records/hypotheses/H0017-e0017-fb0013-structure-meta-improvement-research-scan-outputs.md`


# H0017: E0017-fb0013-structure-meta-improvement-research-scan-outputs の仮説

## 仮説

A hops lab research-scan record can turn meta-improvement research output into a structured, source-linked artifact before agents decide whether to investigate, capture, propose, park, or reject candidates.

## メカニズム

The command stores scope, evidence groups, candidate rows, relations, recommendations, and next commands in a canonical RS record plus a generated summary view, so research results stop living only in chat prose or free-form investigation notes.

## 最小実装

Add a research_scan record type, a hops lab research-scan CLI command, generated view support, validation, docs, packaged skill guidance, and tests that assert structured candidates and evidence are recorded.

## 代替案: 削除または統合

Keep using free-form hops lab investigate summaries only, but that loses candidate boundaries and makes later routing or compaction harder.

## 期待される利点

Meta-improvement research can be reviewed, routed, compacted, and converted into lab actions without rereading chat history.

## 想定される欠点

Another record type can add surface area, so keep it lightweight and only use it for deliberate research scans rather than every small observation.

## 評価計画

Create a research scan in a fixture repo, assert RS frontmatter/body/view capture evidence and candidates, then run contract tests for packaged skills and full validation.

## 中止基準

Reject if the command bypasses existing lab flow, cannot link back to evidence, or encourages speculative candidate spam without recommendations or next commands.


## Evidence

`harness-lab/views/eval-results/E0017-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0018: D0018: adopted H0017


Source: `harness-lab/records/decisions/D0018-adopted-h0017.md`


# D0018: adopted H0017

## 判断

adopted

## 理由

The RS record path makes meta-improvement research reviewable and routable before converting candidates into lab actions.

## 証拠

tests/test_cli/test_mvp_flow.py records a research scan and asserts structured frontmatter, candidate next_command, generated view, and doctor compatibility; tests/test_agent_harness_contract.py keeps packaged research skill guidance aligned.

## 回帰リスク

Moderate: a new record type could add meta-noise, mitigated by deliberate skill trigger criteria, candidate recommendations, and not replacing existing investigate/capture/propose commands.

## フォローアップ

Use research-scan for deliberate multi-candidate meta improvement research; avoid it for one-off notes that fit existing dossier investigate/classify.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
