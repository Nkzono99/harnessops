# Harness Lab Knowledge

このファイルは `hops lab compact` が更新する deterministic working index です。
`records/` と `improvements/` は引き続き監査可能な正本で、この snapshot は再利用しやすい索引です。

## Compaction State

- updated_at: 2026-05-14T03:08:12+09:00
- mode: forced
- triggers: file_count>256
- file_count: 300 / threshold 256
- byte_count: 806152 / threshold 2000000
- improvement_count: 30 / threshold 50
- source_digest: `2172da30944f7a33c114f8c7bfada6bcce47e5f7b2d7ef29f005ac251e658532`

## How To Use

- 作業開始時に全dossierを読む代わりに、まず capability/failure_class の教訓、guard、open question を確認する。
- 採用判断や反例処理では、必ず source ID から正本レコードへ戻る。
- このファイルの Curator Notes は手で更新してよい。次回 compaction でも保持される。

## Capability Knowledge

### daily_steward_orchestration
#### count_based_preflight_misses_stale_lab_health
- sources: `IMP0029`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=5.0, privacy_sanitization_risk=5.0, regression_risk=2.0
- guards: IMP0029:implemented:tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
- lesson IMP0029 (adopted): Implemented a narrow deterministic preflight extension. Validation: uv run pytest -q passed 94 tests; uv run ruff check changed files passed; hops doctor --check-overlay --check-records ok; hops migrate --check reported no pending migrations. Live preflight J...

#### fragmented_improvement_loop
- sources: `IMP0023`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=5.0, impact=5.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=3.0, privacy_sanitization_risk=2.0, regression_risk=3.0
- guards: IMP0023:implemented:tests/test_agent_harness_contract.py; tests/test_cli/test_steward.py
- lesson IMP0023 (adopted): Implemented hops-daily-steward as a conductor skill rather than a monolithic improver. It includes run modes, write policy, lane trigger matrix, context-separated subagent lanes, structured lane output schema, run ledger reporting, no-op policy, remote confir...

### generated_view_management
#### stale_generated_view_repair_gap
- sources: `IMP0016`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=5.0, privacy_sanitization_risk=5.0, regression_risk=2.0
- guards: IMP0016:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0016 (adopted): Implemented lab refresh-views so it first refreshes doctor-managed overlay artifacts, then regenerates dynamic lab views with deduplicated output. Focused regression covers stale README/backlog/score-trajectory lock warnings and preserves research-scan view c...

### github_issue_import
#### unicode_decode_failure
- sources: `IMP0005`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=3.0, maintainability=5.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=5.0, privacy_sanitization_risk=1.0, regression_risk=2.0
- lesson IMP0005 (adopted): Implemented explicit UTF-8 decoding for gh issue view during feedback import, with replacement on invalid bytes and TypeError fallback handling. Regression test now imports Unicode Japanese issue body/comment and asserts encoding=utf-8 is used. Verified with...

### harness_lab_traceability
#### missing_lab_capture
- sources: `IMP0001`, `IMP0017`, `IMP0019`, `IMP0020`, `IMP0026`, `IMP0031`
- status_counts: adopted=6
- average_scores: anti_theater=4.67, evaluability=5.0, impact=4.0, maintainability=4.0, mechanism_clarity=4.5, minimality=4.17, operator_burden=1.0, privacy_sanitization_risk=0.5, regression_risk=1.5
- guards: IMP0017:implemented:tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once, IMP0019:implemented:tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions, IMP0020:implemented:tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged, IMP0026:implemented:src/harnessops/core/upgrade_chain.py, IMP0031:implemented:tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents
- lesson IMP0001 (adopted): CLI tests exercise lab capture and eval conversion. Contract tests assert bridge, packaged skills, release skill, and docs mention hops lab capture. This record captures the previously missing lab trace.
- lesson IMP0017 (adopted): Focused regression tests show stale harnessops_version emits a hops-update-harness notice once and suppresses it for update-harness itself; a real doctor run in this repository surfaced the stale 0.1.2 -> 0.1.3 lock.
- lesson IMP0019 (adopted): Updated the PyPI publish workflow to actions/checkout@v5 and actions/setup-python@v6 while preserving the pypi environment, id-token permission, Python 3.11, build, twine check, and publish steps. Added a workflow contract test. Focused test, full pytest, ruf...
- lesson IMP0020 (adopted): Broadened hops-research-improvements to HarnessOps core plus linked target/project repositories. The skill now branches by repo role: target/meta lab repos use research-scan/investigate/classify/capture/propose, while project repos use failure/feedback/export...
- lesson IMP0026 (adopted): Implemented checkpointed uvx update chains in update-harness with --plan-upgrade and --apply-upgrade-chain, refreshed update skill/docs, and verified with ruff check ., pytest -q (93 passed), doctor --check-overlay --check-records, migrate --check, and git di...
- lesson IMP0031 (adopted): Updated daily steward docs and repo-local/packaged skill copies to prefer GitHub Flow: automation feature branch, PR, and merge into protected main after validation/required checks. Added lane budgets for systemic candidates, metadata/guard backfills, and rea...

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
#### deterministic_snapshot_conflates_trigger_and_abstraction
- sources: `IMP0015`
- status_counts: adopted=1
- average_scores: anti_theater=4.0, evaluability=4.0, impact=4.0, maintainability=4.0, mechanism_clarity=5.0, minimality=0.0, operator_burden=0.0, privacy_sanitization_risk=0.0, regression_risk=0.0
- guards: IMP0015:implemented:tests/test_cli/test_mvp_flow.py
- lesson IMP0015 (adopted): Lint/prepare commands separate trigger detection from semantic abstraction; tests cover nonzero lint, warn-only lint, and input bundle generation.

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

#### premature_research_routing
- sources: `IMP0022`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=5.0, maintainability=4.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=2.0, privacy_sanitization_risk=1.0, regression_risk=2.0
- guards: IMP0022:implemented:tests/test_agent_harness_contract.py
- lesson IMP0022 (adopted): Implemented a separate open invention lane: hops-open-meta-scan now produces Raw Ideas, Counterframes, Routing Hints, and Do Not Record Yet without default lab writes; hops-research-improvements now explicitly acts as the downstream selection/routing lane. Re...

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

### repository_maintainability
#### records_module_sprawl
- sources: `IMP0028`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=5.0, mechanism_clarity=5.0, minimality=4.0, operator_burden=0.0, privacy_sanitization_risk=0.0, regression_risk=2.0
- guards: IMP0028:implemented:src/harnessops/core/improvement_dossier.py
- lesson IMP0028 (adopted): Split records.py into record_types, record_io, record_index, lab_records, and improvement_dossier while keeping records.py as a compatibility facade. Updated internal imports and record schema docs. Verified with ruff check ., pytest -q (92 passed), doctor --...

#### surface_sprawl
- sources: `IMP0027`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=4.0, maintainability=5.0, mechanism_clarity=4.0, minimality=4.0, operator_burden=1.0, privacy_sanitization_risk=0.0, regression_risk=2.0
- guards: IMP0027:implemented:src/harnessops/cli/agent.py
- lesson IMP0027 (adopted): Removed root plugin and user plugin install surfaces, moved packaged agent skills under agent_assets/skills, extracted shared markdown and managed file helpers, demoted experiments from required lab layout, and updated docs/SPEC/README. Verified with ruff che...

### unclassified
#### unclassified
- sources: `IMP0002`, `IMP0003`, `IMP0004`, `IMP0018`, `IMP0021`, `IMP0024`, `IMP0025`
- status_counts: adopted=7
- average_scores: anti_theater=4.57, evaluability=5.0, impact=4.0, maintainability=4.14, mechanism_clarity=4.57, minimality=4.14, operator_burden=2.43, privacy_sanitization_risk=1.14, regression_risk=2.14
- guards: IMP0018:implemented:tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract, IMP0021:implemented:tests/test_agent_harness_contract.py, IMP0024:implemented:tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback, IMP0025:planned:tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation
- lesson IMP0002 (adopted): Implemented conflict-aware agent bridge refresh: managed bridge hashes are stored in lock metadata; unmodified stale files update automatically, local edits produce .new files, --force-agent-bridge overwrites explicitly, and JSON/text output reports checked,...
- lesson IMP0003 (adopted): Implemented lab dossiers as a generated compatibility layer: hops lab dossier --from <FB/E/H/D> creates or updates harness-lab/improvements/IMP*.md from normalized records, refreshes views/improvements.md, preserves FB/E/H/D as the source of truth, and docume...
- lesson IMP0004 (adopted): Implemented lab-first GitHub issue promotion: hops lab issue draft/create --from <FB/E/H/D/IMP> builds a sanitized issue body from the generated dossier, writes local markdown drafts, searches duplicates, requires --confirm-create for remote creation, and wri...
- lesson IMP0018 (adopted): Packaged/generated agent assets now use uvx --from harnessops hops for missing PATH fallback; editable checkout commands remain only in HarnessOps development docs. Contract tests, targeted update-harness tests, full pytest, ruff, doctor, and migrate all pass...
- lesson IMP0021 (adopted): Implemented the anti-myopia gate directly in the hops-research-improvements skill: it now requires horizon/generalization classification before capture or issue creation, parks local-only frictions, limits promotion to one systemic candidate, and includes a c...
- lesson IMP0024 (adopted): Doctor now warns when a target repo bridge contains the stale editable fallback and the repo does not declare a local hops console script. Focused positive/negative tests, full pytest, ruff, doctor, and migrate passed.
- lesson IMP0025 (adopted): Validated role-scoped bridge behavior with focused agent bridge/update-harness tests plus full suite: ruff check ., pytest -q (90 passed), hops doctor --check-overlay --check-records, hops migrate --check.

### uvx_update_guidance
#### stale_hops_update_path
- sources: `IMP0030`
- status_counts: adopted=1
- average_scores: anti_theater=5.0, evaluability=5.0, impact=3.0, maintainability=4.0, mechanism_clarity=5.0, minimality=5.0, operator_burden=0.0, privacy_sanitization_risk=0.0, regression_risk=1.0
- guards: IMP0030:implemented:tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime
- lesson IMP0030 (adopted): Existing behavior satisfies FB0028: update_notice.py compares repo-managed, current runtime, and latest PyPI versions; CLI spec documents uvx update-harness, plan-upgrade, doctor, and migrate-check guidance; targeted guard passed with uv run pytest tests/test...

## Guard Index

- `IMP0006` improvement_loop_design/ambiguous_improvement_workflow: implemented tests/test_cli/test_mvp_flow.py
- `IMP0007` meta_hypothesis_scan/missed_second_order_observation: implemented tests/test_agent_harness_contract.py
- `IMP0008` meta_improvement_research/missing_research_skill: implemented tests/test_agent_harness_contract.py
- `IMP0009` meta_improvement_research/unstructured_research_scan_results: implemented tests/test_cli/test_mvp_flow.py
- `IMP0011` lab_record_consistency/duplicate_improvement_dossier_race: implemented tests/test_cli/test_mvp_flow.py
- `IMP0012` record_lookup/generated_view_shadowed_record_id: implemented tests/test_cli/test_mvp_flow.py
- `IMP0013` lab_evaluation_review/eval_template_noise_in_dossier: implemented tests/test_cli/test_mvp_flow.py
- `IMP0014` lab_memory_compaction/record_sprawl_without_knowledge_consolidation: implemented tests/test_cli/test_mvp_flow.py
- `IMP0015` lab_memory_compaction/deterministic_snapshot_conflates_trigger_and_abstraction: implemented tests/test_cli/test_mvp_flow.py
- `IMP0016` generated_view_management/stale_generated_view_repair_gap: implemented tests/test_cli/test_mvp_flow.py
- `IMP0017` harness_lab_traceability/missing_lab_capture: implemented tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once
- `IMP0018` unclassified/unclassified: implemented tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract
- `IMP0019` harness_lab_traceability/missing_lab_capture: implemented tests/test_agent_harness_contract.py::test_pypi_publish_workflow_uses_node24_ready_actions
- `IMP0020` harness_lab_traceability/missing_lab_capture: implemented tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged
- `IMP0021` unclassified/unclassified: implemented tests/test_agent_harness_contract.py
- `IMP0022` meta_improvement_research/premature_research_routing: implemented tests/test_agent_harness_contract.py
- `IMP0023` daily_steward_orchestration/fragmented_improvement_loop: implemented tests/test_agent_harness_contract.py; tests/test_cli/test_steward.py
- `IMP0024` unclassified/unclassified: implemented tests/test_cli/test_mvp_flow.py::test_doctor_warns_about_stale_editable_bridge_fallback
- `IMP0025` unclassified/unclassified: planned tests/test_cli/test_mvp_flow.py::test_agent_bridge_generation
- `IMP0026` harness_lab_traceability/missing_lab_capture: implemented src/harnessops/core/upgrade_chain.py
- `IMP0027` repository_maintainability/surface_sprawl: implemented src/harnessops/cli/agent.py
- `IMP0028` repository_maintainability/records_module_sprawl: implemented src/harnessops/core/improvement_dossier.py
- `IMP0029` daily_steward_orchestration/count_based_preflight_misses_stale_lab_health: implemented tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
- `IMP0030` uvx_update_guidance/stale_hops_update_path: implemented tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once; tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_when_current_runtime_is_behind_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_handles_unreleased_runtime_ahead_of_pypi; tests/test_cli/test_mvp_flow.py::test_update_notice_warns_when_repo_lock_is_newer_than_runtime
- `IMP0031` harness_lab_traceability/missing_lab_capture: implemented tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented; tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents

## Research Scans

- `RS0001` meta_improvement_research/unstructured_research_scan_results: adopt: use research-scan for deliberate multi-candidate meta-improvement research before routing candidates to investigate/capture/propose/park/reject. (1 candidates)
- `RS0002` generated_view_management/stale_generated_view_repair_gap: capture the stale generated-view repair gap before implementation; prefer one fix that makes refresh/status behavior match doctor-managed artifacts and gives operators an explicit next command. (3 candidates)
- `RS0003` release-and-agent-bridge/post-release-residual-risk: Prioritize the release workflow Node24 migration first because it has an external deadline before June 2 2026; then treat issue #9 as a residual extension of IMP0018 rather than a new broad bridge rewrite. (3 candidates)
- `RS0004` issue_lab_reconciliation/stale_external_issue_tracker: prioritize #9 residual implementation next; separately ask before closing #6/#7/#8 because remote tracker writes should be explicit (4 candidates)
- `RS0005` daily_steward_orchestration/count_based_preflight_misses_stale_lab_health: propose a narrow deterministic preflight extension: include lab_health only for lab repos, reuse existing lint output, and keep downstream judgment in the librarian lane. (1 candidates)

## External Evidence

- `IMP0006` Compared the current loop with PDSA, SRE postmortem/action-item practice, ADR decision records, issue triage, and Technology Radar maturity rings; the missing HarnessOps concepts are explicit investigation, theme classification, maturity,... (evidence: docs/design-principles.md)
- `IMP0008` Manual meta-improvement research should borrow from external practice patterns: Google SRE stresses reviewed postmortem action items and repositories of learning; Open Practice Library experiment guidance stresses explicit hypotheses, meas... (evidence: https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)
- `IMP0009` External practices suggest the research result should be more structured than a prose note: SRE postmortem tooling captures sections/tables for repository analysis; Open Practice Library experiment design requires explicit hypothesis, curr... (evidence: https://sre.google/workbook/postmortem-culture/ ; https://openpracticelibrary.com/practice/design-of-experiments/ ; https://www.thoughtworks.com/radar/faq)
- `IMP0014` Anthropic Managed Agents 'dreaming' is a scheduled process that reviews prior sessions and memory stores, extracts patterns, and curates memory; this supports a background/threshold compaction layer rather than stuffing all lab history int... (evidence: https://claude.com/blog/new-in-claude-managed-agents)
- `IMP0014` Claude memory docs frame durable memory as client-controlled files that are created, read, updated, and deleted across sessions; HarnessOps should mirror that with local mutable knowledge files under harness-lab rather than append-only sum... (evidence: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- `IMP0014` Generative Agents and Reflexion both separate episodic traces from higher-level reflections; the lab should preserve records as episodic traces and compile recurring patterns, decisions, and guards into a smaller semantic layer. (evidence: https://arxiv.org/abs/2304.03442; https://arxiv.org/abs/2303.11366)
- `IMP0014` MemGPT and recent agent-memory surveys emphasize hierarchical context, write-manage-read loops, contradiction handling, privacy, and learned forgetting; HarnessOps compaction should be deterministic, source-linked, local, and reviewable. (evidence: https://arxiv.org/abs/2310.08560; https://arxiv.org/abs/2603.07670)
- `IMP0017` pip implements its update notice as a CLI wrapper around command execution: fetch a potential prompt before the command, cache remote version state for roughly one week, skip when disabled/no-index, then emit the notice after the command b... (evidence: https://github.com/pypa/pip/blob/main/src/pip/_internal/cli/index_command.py)
- `IMP0019` GitHub's Node20 deprecation notice says runners begin using Node24 by default on 2026-06-02 and users should update workflows to latest actions that run on Node24; v0.1.4 release run already emitted this annotation. (evidence: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)

## Contradictions And Regressions

既存判断への反例やregressionは記録されていません。

## Open Questions

未判断の改善テーマはありません。

## Curator Notes
<!-- harnessops:curator-notes:start -->
ここは `hops lab compact` が保持する手編集領域です。圧縮結果への補足、反例、今後の見直し観点を短く追記できます。
<!-- harnessops:curator-notes:end -->
