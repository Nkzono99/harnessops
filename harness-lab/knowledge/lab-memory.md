# Harness Lab Knowledge

このファイルは `hops lab compact` が更新する mutable working memory です。
`records/` と `improvements/` は引き続き監査可能な正本で、この知識層は再利用しやすい要約です。

## Compaction State

- updated_at: 2026-05-13T03:38:14+09:00
- mode: forced
- triggers: forced-or-none
- file_count: 152 / threshold 256
- byte_count: 253630 / threshold 2000000
- improvement_count: 13 / threshold 50
- source_digest: `23d26796b16ad6759d1f087546bebe4132d5d7ed77d88ec1c06eca01973b2d65`

## How To Use

- 作業開始時に全dossierを読む代わりに、まず capability/failure_class の教訓、guard、open question を確認する。
- 採用判断や反例処理では、必ず source ID から正本レコードへ戻る。
- このファイルの Curator Notes は手で更新してよい。次回 compaction でも保持される。

## Capability Knowledge

### github_issue_import
#### unicode_decode_failure
- sources: `IMP0005`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=3.0, maintainability=5.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=5.0, privacy_sanitization_risk=1.0, regression_risk=2.0
- lesson IMP0005 (adopted): Implemented explicit UTF-8 decoding for gh issue view during feedback import, with replacement on invalid bytes and TypeError fallback handling. Regression test now imports Unicode Japanese issue body/comment and asserts encoding=utf-8 is used. Verified with...

### harness_lab_traceability
#### missing_lab_capture
- sources: `IMP0001`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=4.0, minimality=4.0, operator_burden=0.0, privacy_sanitization_risk=0.0, regression_risk=0.0
- lesson IMP0001 (adopted): CLI tests exercise lab capture and eval conversion. Contract tests assert bridge, packaged skills, release skill, and docs mention hops lab capture. This record captures the previously missing lab trace.

### improvement_loop_design
#### ambiguous_improvement_workflow
- sources: `IMP0006`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=4.0, privacy_sanitization_risk=1.0, regression_risk=3.0
- guards: IMP0006:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0006 (adopted): Redesigned the standard improvement loop around explicit observation, investigation, recording, classification/routing, hypothesis, evaluation design, decision, application, guard, and promotion. Added improvement theme metadata plus lab investigate/classify...

### lab_evaluation_review
#### eval_template_noise_in_dossier
- sources: `IMP0013`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=5.0, privacy_sanitization_risk=5.0, regression_risk=2.0
- guards: IMP0013:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0013 (adopted): Dossiers now summarize eval records and manual eval yml/md instead of embedding full eval-case template bodies. New eval cases are seeded from source feedback summary, reproduction, and expected change. Manual eval markdown no longer includes a full eval case...

### lab_memory_compaction
#### record_sprawl_without_knowledge_consolidation
- sources: `IMP0014`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=4.0, privacy_sanitization_risk=5.0, regression_risk=3.0
- guards: IMP0014:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0014 (adopted): Compaction is deterministic, source-linked, and guarded by CLI tests. It preserves canonical records and keeps manual Curator Notes mutable, so it reduces review load without turning summaries into adoption evidence.

### lab_record_consistency
#### duplicate_improvement_dossier_race
- sources: `IMP0011`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=4.0, privacy_sanitization_risk=5.0, regression_risk=3.0
- guards: IMP0011:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0011 (adopted): Implemented source_feedback-level locking for dossier creation, doctor validation for duplicate improvement dossier source_feedback values, visible evidence_ref rendering for investigation notes, LF-stable generated records, and canonical record lookup so gen...

### meta_hypothesis_scan
#### missed_second_order_observation
- sources: `IMP0007`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=4.0, impact=5.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=4.0, privacy_sanitization_risk=1.0, regression_risk=3.0
- guards: IMP0007:implemented:tests/test_agent_harness_contract.py
- lesson IMP0007 (adopted): Designed the meta-hypothesis scan harness: trigger signals, task checkpoints, output levels, capture thresholds, and anti-spam guardrails are documented in design-principles; run-lab skills now instruct agents to run a bounded scan during interruptions, repea...

### meta_improvement_research
#### missing_research_skill
- sources: `IMP0008`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=4.0, impact=4.0, maintainability=4.0, mechanism_clarity=4.0, minimality=4.0, operator_burden=3.0, privacy_sanitization_risk=4.0, regression_risk=3.0
- guards: IMP0008:implemented:tests/test_agent_harness_contract.py
- lesson IMP0008 (adopted): The skill is distinct from the in-task meta scan, lab-routed, package-tested, and privacy-aware. Risk is moderate skill surface area, guarded by explicit trigger criteria and packaging contract tests.

#### unstructured_research_scan_results
- sources: `IMP0009`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=4.0, privacy_sanitization_risk=5.0, regression_risk=3.0
- guards: IMP0009:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0009 (adopted): Research scans now persist deliberate meta-improvement research as RS records with structured evidence, candidates, relation, recommendation, next command, and a generated view. The implementation keeps existing investigate/capture/propose actions as downstre...

### record_lookup
#### generated_view_shadowed_record_id
- sources: `IMP0012`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=5.0, privacy_sanitization_risk=5.0, regression_risk=2.0
- guards: IMP0012:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0012 (adopted): find_record now searches the canonical record directory implied by known ID prefixes before broad overlay lookup. Regression test reruns eval by ID after an eval result view exists.

### unclassified
#### unclassified
- sources: `IMP0002`, `IMP0003`, `IMP0004`
- status_counts: adopted=3
- average_scores: anti_theater=4.67, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=4.33, minimality=4.0, operator_burden=4.33, privacy_sanitization_risk=1.33, regression_risk=3.0
- lesson IMP0002 (adopted): Implemented conflict-aware agent bridge refresh: managed bridge hashes are stored in lock metadata; unmodified stale files update automatically, local edits produce .new files, --force-agent-bridge overwrites explicitly, and JSON/text output reports checked,...
- lesson IMP0003 (adopted): Implemented lab dossiers as a generated compatibility layer: hops lab dossier --from <FB/E/H/D> creates or updates harness-lab/improvements/IMP*.md from normalized records, refreshes views/improvements.md, preserves FB/E/H/D as the source of truth, and docume...
- lesson IMP0004 (adopted): Implemented lab-first GitHub issue promotion: hops lab issue draft/create --from <FB/E/H/D/IMP> builds a sanitized issue body from the generated dossier, writes local markdown drafts, searches duplicates, requires --confirm-create for remote creation, and wri...

## Guard Index

- `IMP0006` improvement_loop_design/ambiguous_improvement_workflow: implemented tests/test_cli/test_mvp_flow.py
- `IMP0007` meta_hypothesis_scan/missed_second_order_observation: implemented tests/test_agent_harness_contract.py
- `IMP0008` meta_improvement_research/missing_research_skill: implemented tests/test_agent_harness_contract.py
- `IMP0009` meta_improvement_research/unstructured_research_scan_results: implemented tests/test_cli/test_mvp_flow.py
- `IMP0011` lab_record_consistency/duplicate_improvement_dossier_race: implemented tests/test_cli/test_mvp_flow.py
- `IMP0012` record_lookup/generated_view_shadowed_record_id: implemented tests/test_cli/test_mvp_flow.py
- `IMP0013` lab_evaluation_review/eval_template_noise_in_dossier: implemented tests/test_cli/test_mvp_flow.py
- `IMP0014` lab_memory_compaction/record_sprawl_without_knowledge_consolidation: implemented tests/test_cli/test_mvp_flow.py

## Research Scans

- `RS0001` meta_improvement_research/unstructured_research_scan_results: adopt: use research-scan for deliberate multi-candidate meta-improvement research before routing candidates to investigate/capture/propose/park/reject. (1 candidates)

## External Evidence

- `IMP0006` Compared the current loop with PDSA, SRE postmortem/action-item practice, ADR decision records, issue triage, and Technology Radar maturity rings; the missing HarnessOps concepts are explicit investigation, theme classification, maturity,... (evidence: docs/design-principles.md)
- `IMP0008` Manual meta-improvement research should borrow from external practice patterns: Google SRE stresses reviewed postmortem action items and repositories of learning; Open Practice Library experiment guidance stresses explicit hypotheses, meas... (evidence: https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)
- `IMP0009` External practices suggest the research result should be more structured than a prose note: SRE postmortem tooling captures sections/tables for repository analysis; Open Practice Library experiment design requires explicit hypothesis, curr... (evidence: https://sre.google/workbook/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)
- `IMP0014` Anthropic Managed Agents 'dreaming' is a scheduled process that reviews prior sessions and memory stores, extracts patterns, and curates memory; this supports a background/threshold compaction layer rather than stuffing all lab history int... (evidence: https://claude.com/blog/new-in-claude-managed-agents)
- `IMP0014` Claude memory docs frame durable memory as client-controlled files that are created, read, updated, and deleted across sessions; HarnessOps should mirror that with local mutable knowledge files under harness-lab rather than append-only sum... (evidence: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- `IMP0014` Generative Agents and Reflexion both separate episodic traces from higher-level reflections; the lab should preserve records as episodic traces and compile recurring patterns, decisions, and guards into a smaller semantic layer. (evidence: https://arxiv.org/abs/2304.03442; https://arxiv.org/abs/2303.11366)
- `IMP0014` MemGPT and recent agent-memory surveys emphasize hierarchical context, write-manage-read loops, contradiction handling, privacy, and learned forgetting; HarnessOps compaction should be deterministic, source-linked, local, and reviewable. (evidence: https://arxiv.org/abs/2310.08560; https://arxiv.org/abs/2603.07670)

## Contradictions And Regressions

既存判断への反例やregressionは記録されていません。

## Open Questions

未判断の改善テーマはありません。

## Curator Notes
<!-- harnessops:curator-notes:start -->
ここは `hops lab compact` が保持する手編集領域です。圧縮結果への補足、反例、今後の見直し観点を短く追記できます。
<!-- harnessops:curator-notes:end -->
