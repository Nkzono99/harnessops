# Lab Memory Abstraction Input

このファイルは `hops lab memory prepare` が作る skill 入力です。
`records/` と `improvements/` が正本で、この bundle は抽象化作業の入口です。

## Lint State

- status: needs-abstraction
- reason: triggers-present
- source_digest: `2172da30944f7a33c114f8c7bfada6bcce47e5f7b2d7ef29f005ac251e658532`
- pressure: file_count>256
- triggers: file_count>256, semantic_memory_stale

## Skill Instructions

- `hops-compact-lab-memory` skill でこの bundle を読み、抽象知を更新する。
- deterministic snapshot は索引として扱い、採用判断の証拠にはしない。
- すべての原則、パターン、アンチパターン、評価則に source ID を付ける。
- 反例や失敗条件を消さず、適用条件または中止基準として残す。
- 更新後に `lab-memory-abstraction.yml` の `source_digest` をこの値に合わせる。

## Abstraction Targets

- `harness-lab/knowledge/principles.md`: 採用/却下を越えて残った設計原則を source ID 付きで保つ。
- `harness-lab/knowledge/patterns.yml`: 再利用可能な改善パターン、適用条件、反例、ガードを構造化する。
- `harness-lab/knowledge/anti-patterns.md`: 繰り返し避けるべき改善劇場、過剰一般化、失敗クラスをまとめる。
- `harness-lab/knowledge/evaluation-playbook.md`: 評価軸、holdout、判断基準、kill criteria の経験をまとめる。

## Sources

### `IMP0001` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0001-fb0001-harnessops-improvements-lacked-lab-trace.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0001: FB0001: HarnessOps improvements lacked lab trace

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0001`
- linked_records: `FB0001`, `E0001`, `H0001`, `D0001`

## Source Observation

Source: `harness-lab/records/feedback/FB0001-harnessops-improvements-lacked-lab-trace.md`

# FB0001: HarnessOps improvements lacked lab trace

## 概要

HarnessOps CLI and skill improvements could be implemented, committed, released, and published without any harness-lab record.

## 再現

Run a nontrivial HarnessOps improvement from local conversation without an upstream feedback bundle or GitHub issue. Existing hops-run-lab guidance assumed an FB record already existed.

## 期待する上流変更

Provide a first-class lab capture command and update agent, release, and lab skills so local HarnessOps improvements start with a harness-lab record.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

調査メモはまだありません。

## Evaluation

### E0001: E0001: FB0001-harnessops-improvements-lacked-lab-trace を評価


- source: `harness-lab/records/eval-cases/E0001-fb0001-harnessops-improvements-lacked-lab-trace.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0001-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0001-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=0, operator_burden=0, anti_theater=4, maintainability=4, privacy_sanitization_risk=0
- notes: CLI tests exercise lab capture and eval conversion. Contract tests assert bridge, packaged skills, release skill, and...

### `IMP0002` unclassified/unclassified
- path: `harness-lab/improvements/IMP0002-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0002: FB0006: Make update-harness conflict-aware for agent bridge files

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0006`
- linked_records: `FB0006`, `E0006`, `H0006`, `D0007`

## Source Observation

Source: `harness-lab/records/feedback/FB0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`

# FB0006: Make update-harness conflict-aware for agent bridge files

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/6
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:53:22Z
updated_at: 2026-05-12T14:53:22Z

## Issue本文
## Context

While updating runops' HarnessOps bridge, `.agents/skills/hops-export-feedback/SKILL.md` was stale. Running:

```bash
hops update-harness --agent-bridge --codex
```

reported `ok` and `agent bridge: checked 9 paths`, but the stale skill file was not updated because existing skill directories are skipped unless `--force-agent-bridge` is used.

Using `--force-agent-bridge` did update the file, but that is a blunt overwrite mode. It does not distinguish between an unmodified managed file that should be refreshed and a locally edited file that should be preserved.

## Proposal

Make `hops update-harness` conflict-aware for agent bridge files, similar to the behavior expected from `runo update-harness`:

- If a managed file has not been changed locally, overwrite it with the current packaged version.
- If a managed file has local edits, preserve it and write `<path>.new` for the updated packaged version.
- `--force-agent-bridge` should remain available for explicit overwrite.
- JSON and text output should report exact counts and paths for `updated`, `unchanged`, `conflicted`, an...

### `IMP0003` unclassified/unclassified
- path: `harness-lab/improvements/IMP0003-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0003: FB0007: Simplify harness-lab around per-improvement dossiers

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0007`
- linked_records: `FB0007`, `E0007`, `H0007`, `D0008`

## Source Observation

Source: `harness-lab/records/feedback/FB0007-simplify-harness-lab-around-per-improvement-dossiers.md`

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
- The capture path exists, but the...

### `IMP0004` unclassified/unclassified
- path: `harness-lab/improvements/IMP0004-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0004: FB0008: Add GitHub issue workflow for lab-first improvement records

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0008`
- linked_records: `FB0008`, `E0008`, `H0008`, `D0009`

## Source Observation

Source: `harness-lab/records/feedback/FB0008-add-github-issue-workflow-for-lab-first-improvement-records.md`

# FB0008: Add GitHub issue workflow for lab-first improvement records

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/8
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:54:12Z
updated_at: 2026-05-12T14:54:12Z

## Issue本文
## Context

HarnessOps now has `hops feedback issue create` for sanitized exported feedback bundles. That is useful for project-side feedback records.

However, in the current runops workflow we captured a HarnessOps improvement directly via:

```bash
hops lab capture ...
hops lab new-eval-case --from FB0001
hops propose --from E0001
```

When asked to create a GitHub issue from that lab-first record, `hops feedback export --target harnessops --sanitize --format github-issue` did not find a matching project-side feedback bundle. We had to create the GitHub issue manually with `gh issue create`.

This is a gap for the lab-first improvement workflow proposed in #5.

## Proposal

Add a first-class path from `harness-lab` records to GitHub Issue drafts/creation.

Possible command shapes:

```bash
hops lab issue draft --from FB0001
hops lab issue create --from FB0001 --repo owner/repo --confirm-create
```

or:

```bash
hops feedback issue create --from-lab FB0001 --repo owner/repo --confirm-create
```

Expected behavior:

- Build an issue title/body from a lab record or improvement do...

### `IMP0005` github_issue_import/unicode_decode_failure
- path: `harness-lab/improvements/IMP0005-fb0009-github-issue-import-fails-on-windows-console-decoding.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0005: FB0009: GitHub issue import fails on Windows console decoding

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0009`
- linked_records: `FB0009`, `E0009`, `H0009`, `D0010`

## Source Observation

Source: `harness-lab/records/feedback/FB0009-github-issue-import-fails-on-windows-console-decoding.md`

# FB0009: GitHub issue import fails on Windows console decoding

## 概要

hops feedback import --issue 7 --repo Nkzono99/harnessops crashed on Windows cp932 decoding while reading gh JSON for a Unicode issue body; setting PYTHONUTF8=1 allowed the import to complete.

## 再現

On Windows PowerShell with the default cp932 locale, run uv run --with-editable . hops feedback import --issue 7 --repo Nkzono99/harnessops. The subprocess reader raises UnicodeDecodeError and json.loads receives None.

## 期待する上流変更

Decode gh issue JSON as UTF-8 explicitly, or capture bytes and decode UTF-8, then add coverage for Unicode issue bodies on Windows.

## Target Capability

- capability: github_issue_import
- failure_class: unicode_decode_failure

## Investigation

調査メモはまだありません。

## Evaluation

### E0009: E0009: FB0009-github-issue-import-fails-on-windows-console-decoding を評価


- source: `harness-lab/records/eval-cases/E0009-fb0009-github-issue-import-fails-on-windows-console-decoding.md`

- capability: github_issue_import

- failure_class: unicode_decode_failure

- manual_eval_yml: `harness-lab/views/eval-results/E0009-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0009-manual-score.md`
- scores: impact=3, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=2, operator_burden=5, anti_theater=5, maintainability=5, privacy_sani...

### `IMP0006` improvement_loop_design/ambiguous_improvement_workflow
- path: `harness-lab/improvements/IMP0006-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes.md`
- status: adopted
- maturity: adopted
- relation: extends

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

- 2026-05-13T00:56:19+09:00 [external-benchmark] Compared the current loop with PDSA, SRE postmortem/action-item practice, ADR decision records, issue triage, and Technology Radar maturity rings; the missing HarnessOps concepts are explicit investigation, theme classification, maturity, guard status, and p...

### `IMP0007` meta_hypothesis_scan/missed_second_order_observation
- path: `harness-lab/improvements/IMP0007-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0007: FB0011: Add meta-hypothesis scan harness for autonomous second-order observations

## Status

- status: adopted
- maturity: adopted
- source_type: extension
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0011`
- linked_records: `FB0011`, `E0011`, `H0011`, `D0012`

## Source Observation

Source: `harness-lab/records/feedback/FB0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`

# FB0011: Add meta-hypothesis scan harness for autonomous second-order observations

## 概要

HarnessOps should help agents notice second-order improvement hypotheses during work, not only when the user explicitly names them. Signals include user interruptions, cross-cutting design principles, repeated friction, migration/compatibility choices, external analogies, and moments where a local idea appears reusable elsewhere.

## 再現

During the standard improvement loop redesign, the user supplied a meta-level compatibility principle mid-work. The agent applied it, but did not autonomously create a separate hypothesis about detecting such second-order observations.

## 期待する上流変更

Define and document a lightweight meta-hypothesis scan harness with trigger signals, checkpoint timing, capture thresholds, outputs, and anti-spam guardrails; update agent lab guidance so the scan runs naturally during substantial work.

## Target Capability

- capability: meta_hypothesis_scan
- failure_class: missed_second_order_observation

## Investigation

- 2026-05-13T01:34:21+09:00 [design] The scan should be event-triggered and checkpoint-triggered, but bounded: record only high-signal second-order observations that affect future agent behavior, migration policy, evaluation design, or cross-project promotion. (evidence:...

### `IMP0008` meta_improvement_research/missing_research_skill
- path: `harness-lab/improvements/IMP0008-fb0012-add-manual-meta-improvement-research-skill.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0008: FB0012: Add manual meta improvement research skill

## Status

- status: adopted
- maturity: adopted
- source_type: extension
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0012`
- linked_records: `FB0012`, `E0012`, `H0012`, `D0013`

## Source Observation

Source: `harness-lab/records/feedback/FB0012-add-manual-meta-improvement-research-skill.md`

# FB0012: Add manual meta improvement research skill

## 概要

HarnessOps needs a deliberate research skill for meta-level improvement discovery, separate from in-task meta-hypothesis scan. The skill should guide agents through codebase investigation, external web research, comparison, classification, and conversion into lab notes or hypotheses.

## 再現

The user asked for a skill that can be manually triggered to investigate meta-level improvement ideas, including codebase and web research, while still allowing future non-periodic autonomous triggering.

## 期待する上流変更

Add a packaged and repo-local HOPS skill for meta improvement research, with workflow steps, web/source requirements, output thresholds, and lab integration commands.

## Target Capability

- capability: meta_improvement_research
- failure_class: missing_research_skill

## Investigation

- 2026-05-13T01:43:56+09:00 [external-benchmark] Manual meta-improvement research should borrow from external practice patterns: Google SRE stresses reviewed postmortem action items and repositories of learning; Open Practice Library experiment guidance stresses explicit hypotheses, measures, pass criteria, and learning; Technology Radar style maturity rings provide a useful model for non-binary promotion status. (evidence: https://sre.google/sre-book/postmortem-culture/ ; https://openpracticelibrary.com/practice...

### `IMP0009` meta_improvement_research/unstructured_research_scan_results
- path: `harness-lab/improvements/IMP0009-fb0013-structure-meta-improvement-research-scan-outputs.md`
- status: adopted
- maturity: adopted
- relation: extends

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

- 2026-05-13T02:03:24+09:00 [external-benchmark] External practices suggest the research result should be more structured than a prose note: SRE postmortem tooling captures sections/tables for repository analysis; Open Practice Library experiment design requires explicit hypothesis, current condition, target condition, pass, measures, and learning; Technology Radar use...

### `IMP0011` lab_record_consistency/duplicate_improvement_dossier_race
- path: `harness-lab/improvements/IMP0011-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0011: FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## Status

- status: adopted
- maturity: adopted
- source_type: failure
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0014`
- linked_records: `FB0014`, `E0013`, `H0013`, `D0014`

## Source Observation

Source: `harness-lab/records/feedback/FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`

# FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## 概要

Running lab dossier, lab classify, and lab investigate concurrently for the same source feedback created two improvement dossiers for FB0013. Doctor did not detect the duplicate source_feedback mapping.

## 再現

Invoke multiple hops lab commands for a new FB in parallel, such as dossier/classify/investigate. Each command can call create_or_update_improvement_dossier before another command's new dossier is visible, causing duplicate IMP records.

## 期待する上流変更

Make improvement dossier creation idempotent under concurrent calls or add doctor validation that detects duplicate IMP source_feedback values and tells the operator how to repair them.

## Target Capability

- capability: lab_record_consistency
- failure_class: duplicate_improvement_dossier_race

## Investigation

- 2026-05-13T02:05:22+09:00 [codebase] create_or_update_improvement_dossier first scans existing IMP files by source_feedback and otherwise allocates next_id from the directory. Without locking or duplicate validation, concurrent commands can both miss the existing dossier and allocate different IMP IDs. Current doctor validates individual records but not uniqueness of source_feedback across improvement dossiers. (evidence: src/harnessops/core/records.py::_find_existing...

### `IMP0012` record_lookup/generated_view_shadowed_record_id
- path: `harness-lab/improvements/IMP0012-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0012: FB0015: Prefer canonical records over generated views in record lookup

## Status

- status: adopted
- maturity: adopted
- source_type: implementation-followup
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0015`
- linked_records: `FB0015`, `E0014`, `H0014`, `D0015`

## Source Observation

Source: `harness-lab/records/feedback/FB0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`

# FB0015: Prefer canonical records over generated views in record lookup

## 概要

After a manual eval result exists, rerunning hops eval --case E0013 can resolve E0013 to harness-lab/views/eval-results/E0013-manual-score.md instead of the canonical records/eval-cases/E0013 record.

## 再現

Create a manual eval result for E0013, then run hops eval --case E0013 again. find_record scans overlay markdown files broadly and can return the generated eval result view whose record_type is manual_eval_result.

## 期待する上流変更

Make find_record prefer the canonical record directory implied by the ID prefix before falling back to broad overlay lookup, so generated views do not shadow FB/E/H/D/IMP records.

## Target Capability

- capability: record_lookup
- failure_class: generated_view_shadowed_record_id

## Investigation

調査メモはまだありません。

## Evaluation

### E0014: E0014: FB0015-prefer-canonical-records-over-generated-views-in-record-lookup を評価


- source: `harness-lab/records/eval-cases/E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`

- capability: record_lookup

- failure_class: generated_view_shadowed_record_id

- manual_eval_yml: `harness-lab/views/eval-results/E0014-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0014-manual-score.md`
- scores: impact=4, mechanism_clarity=5...

### `IMP0013` lab_evaluation_review/eval_template_noise_in_dossier
- path: `harness-lab/improvements/IMP0013-fb0016-remove-unused-eval-case-template-noise-from-dossiers.md`
- status: adopted
- maturity: adopted
- relation: new

# IMP0013: FB0016: Remove unused eval-case template noise from dossiers

## Status

- status: adopted
- maturity: adopted
- source_type: user-review
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0016`
- linked_records: `FB0016`, `E0015`, `H0015`, `D0016`

## Source Observation

Source: `harness-lab/records/feedback/FB0016-remove-unused-eval-case-template-noise-from-dossiers.md`

# FB0016: Remove unused eval-case template noise from dossiers

## 概要

Improvement dossiers render the full eval_case record body under ## Evaluation, so readers see generic sections like fixtures, task, expected behavior, pass/fail criteria that often remain template text. Manual eval yml results are the part that actually functions.

## 再現

Open harness-lab/improvements/IMP*.md and inspect ## Evaluation. It embeds # E000*: ## フィクスチャ, ## タスク, ## 期待される挙動 and similar sections even when they are template text.

## 期待する上流変更

Either make eval cases meaningful in the flow or stop rendering template bodies into dossiers. Prefer summarizing eval records and manual score outputs in dossiers, and generate more source-specific eval case text for new cases.

## Target Capability

- capability: lab_evaluation_review
- failure_class: eval_template_noise_in_dossier

## Investigation

調査メモはまだありません。

## Evaluation

### E0015: E0015: FB0016-remove-unused-eval-case-template-noise-from-dossiers を評価


- source: `harness-lab/records/eval-cases/E0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers.md`

- capability: lab_evaluation_review

- failure_class: eval_template_noise_in_dossier

- manual_eval_yml: `harness-lab/views/eval-results/E0015-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0015-manual-score.md`
- scores: impact=4, m...

### `IMP0014` lab_memory_compaction/record_sprawl_without_knowledge_consolidation
- path: `harness-lab/improvements/IMP0014-fb0017-compact-lab-records-into-mutable-knowledge.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0014: FB0017: Compact lab records into mutable knowledge

## Status

- status: adopted
- maturity: adopted
- source_type: external-benchmark
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0017`
- linked_records: `FB0017`, `E0016`, `H0016`, `D0017`

## Source Observation

Source: `harness-lab/records/feedback/FB0017-compact-lab-records-into-mutable-knowledge.md`

# FB0017: Compact lab records into mutable knowledge

## 概要

As harness-lab grows, append-only records and generated dossiers will become too large to scan. The lab needs a compaction path that preserves canonical records while updating a smaller knowledge layer for reusable lessons, contradictions, guards, and promotion patterns.

## 再現

Accumulate feedback, eval cases, hypotheses, decisions, manual scores, and dossiers until reviewing harness-lab requires reading many files instead of consulting a compiled knowledge surface.

## 期待する上流変更

Provide a first-class lab compaction command that checks size thresholds, compiles source-linked mutable knowledge files, and leaves canonical records intact for audit and regeneration.

## Target Capability

- capability: lab_memory_compaction
- failure_class: record_sprawl_without_knowledge_consolidation

## Investigation

- 2026-05-13T02:53:41+09:00 [external-benchmark] Anthropic Managed Agents 'dreaming' is a scheduled process that reviews prior sessions and memory stores, extracts patterns, and curates memory; this supports a background/threshold compaction layer rather than stuffing all lab history into context. (evidence: https://claude.com/blog/new-in-claude-managed-agents)
- 2026-05-13T02:53:53+09:00 [external-benchmark] Claude memory docs frame durable memory as client-controlled files that are created...

### `IMP0015` lab_memory_compaction/deterministic_snapshot_conflates_trigger_and_abstraction
- path: `harness-lab/improvements/IMP0015-fb0018-separate-lab-memory-triggers-from-abstraction.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0015: FB0018: Separate lab memory triggers from abstraction

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: project-pattern
- source_feedback: `FB0018`
- linked_records: `FB0018`, `E0018`, `H0018`, `D0019`

## Source Observation

Source: `harness-lab/records/feedback/FB0018-separate-lab-memory-triggers-from-abstraction.md`

# FB0018: Separate lab memory triggers from abstraction

## 概要

Current lab compaction is a deterministic aggregation snapshot, but the desired dream-like behavior needs lint-style trigger checks and a skill-guided abstraction workflow.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Keep source-linked deterministic snapshots as an index, add lint/prepare commands for compaction triggers, and provide an agent skill that performs higher-level lab memory abstraction with source traceability.

## Target Capability

- capability: lab_memory_compaction
- failure_class: deterministic_snapshot_conflates_trigger_and_abstraction

## Investigation

- 2026-05-13T09:19:14+09:00 [codebase] Existing compact_lab provides deterministic metrics and source-linked lab-memory outputs. Keep it as an index/snapshot, then add memory lint/prepare commands for trigger detection and input bundling while moving higher-level abstraction into an agent skill. (evidence: src/harnessops/core/lab_compaction.py)

## Research Scans

research scan はまだありません。


## Evaluation

### E0018: E0018: FB0018-separate-lab-memory-triggers-from-abstraction を評価


- source: `harness-lab/records/eval-cases/E0018-fb0018-separate-lab-memory-triggers-from-abstraction.md`

- capability: lab_memory_compaction

- failure_class: deterministic_snapshot_conflates_trigger_and_abstraction

- manual_eval_yml: `harness-lab/views/ev...

### `IMP0016` generated_view_management/stale_generated_view_repair_gap
- path: `harness-lab/improvements/IMP0016-fb0019-generated-view-refresh-leaves-managed-warnings.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0016: FB0019: Generated view refresh leaves managed warnings

## Status

- status: adopted
- maturity: adopted
- source_type: research-scan
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0019`
- linked_records: `FB0019`, `E0019`, `H0019`, `D0020`

## Source Observation

Source: `harness-lab/records/feedback/FB0019-generated-view-refresh-leaves-managed-warnings.md`

# FB0019: Generated view refresh leaves managed warnings

## 概要

The current lab refresh-views command refreshes dynamic lab views but leaves some doctor-managed generated artifacts stale, so doctor remains ok with generated-view warnings after the apparent repair command.

## 再現

Run hops doctor --check-overlay --check-records, then hops lab refresh-views, then doctor again; README, backlog, and score-trajectory warnings remain.

## 期待する上流変更

Provide a refresh path that updates every doctor-managed lab generated artifact or clearly reports the next repair action, so operators do not learn to ignore stale generated-view warnings.

## Target Capability

- capability: generated_view_management
- failure_class: stale_generated_view_repair_gap

## Investigation

- 2026-05-13T11:45:19+09:00 [codebase] RS0002 and code inspection show refresh_views only regenerates imported-feedback, improvements, and research-scans for lab overlays, while doctor validates the lock hashes for README, backlog, imported-feedback, improvements, research-scans, and score-trajectory. A temporary-copy reproduction confirmed lab refresh-views leaves README, backlog, and score-trajectory warnings after refreshing dynamic views. (evidence: RS0002; src/harnessops/core/render.py; src/harnessops/core/validation.py; src/harnessops/core/overlay.py)

## Research Scans

research scan はまだあ...

### `IMP0017` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0017-fb0020-hops-usage-should-surface-stale-harnessops-managed-files.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0017: FB0020: hops usage should surface stale HarnessOps managed files

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0020`
- linked_records: `FB0020`, `E0020`, `H0020`, `D0021`

## Source Observation

Source: `harness-lab/records/feedback/FB0020-hops-usage-should-surface-stale-harnessops-managed-files.md`

# FB0020: hops usage should surface stale HarnessOps managed files

## 概要

After a HarnessOps release, linked repositories can keep older generated skills or managed artifacts until update-harness runs. Users may keep using hops without noticing that update-harness should be applied.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

When a linked repository is used with a newer hops version than the recorded lock state, hops should emit a low-noise notice that points the user or agent to the hops-update-harness skill / hops update-harness.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T17:01:51+09:00 [external-benchmark] pip implements its update notice as a CLI wrapper around command execution: fetch a potential prompt before the command, cache remote version state for roughly one week, skip when disabled/no-index, then emit the notice after the command body without failing the command if the check errors. (evidence: https://github.com/pypa/pip/blob/main/src/pip/_internal/cli/index_command.py)

## Research Scans

research scan はまだありません。


## Evaluation

### E0020: E0020: FB0020-hops-usage-should-surface-stale-harnessops-managed-files を評価


- source: `harness-lab/records/eval-cases/E0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files.md`

- capabili...

### `IMP0018` unclassified/unclassified
- path: `harness-lab/improvements/IMP0018-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0018: FB0021: Packaged agent SKILL assets still document editable hops fallback

## Status

- status: adopted
- maturity: adopted
- source_type: external-issue
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0021`
- linked_records: `FB0021`, `E0021`, `H0021`, `D0022`

## Source Observation

Source: `harness-lab/records/feedback/FB0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`

# FB0021: Packaged agent SKILL assets still document editable hops fallback

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/10
author: Nkzono99
labels: なし
created_at: 2026-05-13T08:01:45Z
updated_at: 2026-05-13T08:01:45Z

## Issue本文
## Summary

The packaged HarnessOps agent assets still tell agents to use an editable local checkout fallback:

```text
uv run --with-editable . hops <command>
```

Current HarnessOps docs for target/project integration already assume the PyPI package path, so linked downstream repositories should be guided toward the PyPI-installed CLI instead, for example:

```text
uvx --from harnessops hops <command>
```

## Observed from downstream update

While updating a linked downstream repository with PyPI `harnessops==0.1.3`, the repo-local agent SKILL copies had to be adjusted from editable fallback to PyPI/`uvx` fallback.

## Affected upstream assets

`rg "uv run --with-editable|with-editable"` shows at least:

- `src/harnessops/core/agent_bridge.py`
- `src/harnessops/agent_assets/plugins/codex/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/codex/harnessops/README.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/READ...

### `IMP0019` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0019-fb0022-release-workflow-uses-node20-action-majors.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0019: FB0022: Release workflow uses Node20 action majors

## Status

- status: adopted
- maturity: adopted
- source_type: external-benchmark
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0022`
- linked_records: `FB0022`, `E0022`, `H0022`, `D0023`

## Source Observation

Source: `harness-lab/records/feedback/FB0022-release-workflow-uses-node20-action-majors.md`

# FB0022: Release workflow uses Node20 action majors

## 概要

The v0.1.4 PyPI publish workflow succeeded but GitHub Actions annotated the run because actions/checkout@v4 and actions/setup-python@v5 still run on Node.js 20. GitHub plans Node24 default migration on 2026-06-02, so the release workflow should use Node24-ready action majors before this becomes release friction.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The PyPI publish workflow should use Node24-ready action majors and a regression test should guard against reintroducing Node20-era checkout/setup-python majors.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T17:55:15+09:00 [external-benchmark] GitHub's Node20 deprecation notice says runners begin using Node24 by default on 2026-06-02 and users should update workflows to latest actions that run on Node24; v0.1.4 release run already emitted this annotation. (evidence: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)

## Research Scans

research scan はまだありません。


## Evaluation

### E0022: E0022: FB0022-release-workflow-uses-node20-action-majors を評価


- source: `harness-lab/records/eval-cases/E0022-fb0022-release-workflow-uses-node20-action-majors.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture...

### `IMP0020` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0020-fb0023-research-skill-scope-excludes-linked-target-and-project-repos.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0020: FB0023: Research skill scope excludes linked target and project repos

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0023`
- linked_records: `FB0023`, `E0023`, `H0023`, `D0024`

## Source Observation

Source: `harness-lab/records/feedback/FB0023-research-skill-scope-excludes-linked-target-and-project-repos.md`

# FB0023: Research skill scope excludes linked target and project repos

## 概要

The hops-research-improvements skill description says it is for HarnessOps meta improvements, which makes it sound like a HarnessOps-core-only tool even though repo-local skills are also deployed into linked target and project repositories. Agents in those repositories should be able to use the same research workflow for target/project harness improvements while preserving the correct lab versus feedback routing.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The skill and packaged copies should explicitly support HarnessOps core, target repositories with harness-lab, and project repositories with harness-feedback, with guidance for routing research outputs through the right HOPS commands.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T18:00:01+09:00 [codebase] Repo-local skills are packaged for target/project repositories, but hops-research-improvements currently frames itself as HarnessOps meta improvement research and assumes harness-lab commands. Project repositories should instead record observed failures through harness-feedback and route/export sanitized feedback, while target or meta repositories can use harness-lab research-scan/eval/propose directly. (evidence: .ag...

### `IMP0021` unclassified/unclassified
- path: `harness-lab/improvements/IMP0021-fb0024-make-hops-research-improvements-less-myopic.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0021: FB0024: Make hops-research-improvements less myopic

## Status

- status: adopted
- maturity: adopted
- source_type: github-issue
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0024`
- linked_records: `FB0024`, `E0024`, `H0024`, `D0025`

## Source Observation

Source: `harness-lab/records/feedback/FB0024-make-hops-research-improvements-less-myopic.md`

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
- Require a short generalization check: what capability does this improve, which failure class does it represent, and would it matter in a...

### `IMP0022` meta_improvement_research/premature_research_routing
- path: `harness-lab/improvements/IMP0022-fb0025-separate-open-meta-idea-scan-from-research-routing.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0022: FB0025: Separate open meta idea scan from research routing

## Status

- status: adopted
- maturity: adopted
- source_type: user-strategy
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0025`
- linked_records: `FB0025`, `E0025`, `H0025`, `D0026`

## Source Observation

Source: `harness-lab/records/feedback/FB0025-separate-open-meta-idea-scan-from-research-routing.md`

# FB0025: Separate open meta idea scan from research routing

## 概要

The broad prompt 'meta的な視点で改善案はある?' produces better divergent improvement ideas than the current hops-research-improvements skill because the skill starts with routing, evidence, and record-management constraints. HarnessOps needs a distinct invention lane that preserves open-ended structural critique before lab routing and selection.

## 再現

Compare a normal broad meta prompt with hops-research-improvements on this repository; the broad prompt surfaces more structural design tensions, while the skill funnels toward recordable near-term candidates.

## 期待する上流変更

Add a lightweight open-meta-scan skill that asks for raw divergent ideas without creating records, update hops-research-improvements to consume those raw ideas as the selection/routing lane, and guard packaged skills with contract tests.

## Target Capability

- capability: meta_improvement_research
- failure_class: premature_research_routing

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0025: E0025: FB0025-separate-open-meta-idea-scan-from-research-routing を評価


- source: `harness-lab/records/eval-cases/E0025-fb0025-separate-open-meta-idea-scan-from-research-routing.md`

- capability: meta_improvement_research

- failure_class: premature_research_routing

- m...

### `IMP0023` daily_steward_orchestration/fragmented_improvement_loop
- path: `harness-lab/improvements/IMP0023-fb0026-add-daily-steward-orchestration-skill.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0023: FB0026: Add daily steward orchestration skill

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0026`
- linked_records: `FB0026`, `E0026`, `H0026`, `D0027`

## Source Observation

Source: `harness-lab/records/feedback/FB0026-add-daily-steward-orchestration-skill.md`

# FB0026: Add daily steward orchestration skill

## 概要

HarnessOps needs a recurring conductor workflow that can read operational issues, feedback, lab state, doctor/update state, run divergent invention lanes, route candidates, advance eval/hypothesis/guard work, and inspect the improvement loop itself across HarnessOps core, target repositories, and project repositories. External review supported the conductor design but requested explicit write policy, lane triggers, subagent I/O schemas, idempotency, and null-action handling; the Advance lane remains intentionally included for full automation.

## 再現

A daily run over open operational issues currently requires manually choosing between issue triage, open meta scan, research routing, lab advancement, update-harness, and loop-audit skills. Without a conductor, the loop either stays manual or collapses into one over-scaffolded skill.

## 期待する上流変更

Add a packaged hops-daily-steward skill that orchestrates issue triage, open meta scan, librarian, critic, maintainer, evaluator, and advance lanes with explicit run modes, write gates, subagent output schema, no-op policy, and report/ledger sections while delegating state changes to hops CLI.

## Target Capability

- capability: daily_steward_orchestration
- failure_class: fragmented_improvement_loop

## Investigation

- 2026-05-13T19:23:30+09:00 [implementation-note] Code...

### `IMP0024` unclassified/unclassified
- path: `harness-lab/improvements/IMP0024-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos.md`
- status: adopted
- maturity: adopted
- relation: extends

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
- Generate bridge skill text that distinguish...

### `IMP0025` unclassified/unclassified
- path: `harness-lab/improvements/IMP0025-fb0029-provide-a-project-side-interface-for-feedback-source-repositories.md`
- status: adopted
- maturity: investigated
- relation: new

# IMP0025: FB0029: Provide a project-side interface for feedback-source repositories

## Status

- status: adopted
- maturity: investigated
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0029`
- linked_records: `FB0029`, `E0028`, `H0028`, `D0029`

## Source Observation

Source: `harness-lab/records/feedback/FB0029-provide-a-project-side-interface-for-feedback-source-repositories.md`

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

runops project directories initialize HarnessOps with profile=runops-project, which is feedback-source mode and writes harness-feedback/. In that role agents mainly need feedback capture/export plus lifecycle checks, but the generic agent bridge exposes broader harness-lab/eval/propose commands that belong to target or meta...

### `IMP0026` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0026-fb0030-chain-harnessops-updates-through-version-checkpoints.md`
- status: adopted
- maturity: evaluated
- relation: new

# IMP0026: FB0030: Chain HarnessOps updates through version checkpoints

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: new
- promotion_level: shipped-behavior
- source_feedback: `FB0030`
- linked_records: `FB0030`, `E0029`, `H0029`, `D0030`

## Source Observation

Source: `harness-lab/records/feedback/FB0030-chain-harnessops-updates-through-version-checkpoints.md`

# FB0030: Chain HarnessOps updates through version checkpoints

## 概要

uvx を標準導線にしたことで、target/project repo の update-harness は最新 PyPI runtime から開始できる。古い managed artifact への互換コードを永久に持つ代わりに、lock の harnessops_version から公開済み checkpoint を計画し、必要な版を uvx で順に呼び出す更新チェーンを追加する。

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

hops update-harness が chain plan/apply の導線を提供し、update skill が通常更新と段階更新を使い分けられるようになる。

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0029: E0029: FB0030-chain-harnessops-updates-through-version-checkpoints を評価


- source: `harness-lab/records/eval-cases/E0029-fb0030-chain-harnessops-updates-through-version-checkpoints.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0029-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0029-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: Implemented checkpointed uvx update chains in update-harness with --plan-upgrade and --apply-upgrade-chain, refreshed update skill/docs, and verified with ruff check ., pytest -q (9...

### `IMP0027` repository_maintainability/surface_sprawl
- path: `harness-lab/improvements/IMP0027-fb0031-simplify-harnessops-repository-surfaces.md`
- status: adopted
- maturity: evaluated
- relation: extends

# IMP0027: FB0031: Simplify HarnessOps repository surfaces

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0031`
- linked_records: `FB0031`, `E0030`, `H0030`, `D0031`

## Source Observation

Source: `harness-lab/records/feedback/FB0031-simplify-harnessops-repository-surfaces.md`

# FB0031: Simplify HarnessOps repository surfaces

## 概要

HarnessOps has grown through feature work: root plugin artifacts may no longer be part of the standard path, core modules mix workflow logic with small utility boundaries, harness-lab contains directories with weak or missing workflows, and docs/SPEC/README may not reflect recent CLI and uvx update-chain behavior. Clean up repo surfaces and improve maintainability without changing core behavior.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Remove or retire obsolete plugin surfaces, add low-risk code organization boundaries, document current standard workflows, and record any lab layout cleanup as a deliberate migration path rather than ad hoc file moves.

## Target Capability

- capability: repository_maintainability
- failure_class: surface_sprawl

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0030: E0030: FB0031-simplify-harnessops-repository-surfaces を評価


- source: `harness-lab/records/eval-cases/E0030-fb0031-simplify-harnessops-repository-surfaces.md`

- capability: repository_maintainability

- failure_class: surface_sprawl

- manual_eval_yml: `harness-lab/views/eval-results/E0030-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0030-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=2, o...

### `IMP0028` repository_maintainability/records_module_sprawl
- path: `harness-lab/improvements/IMP0028-fb0032-split-record-core-modules-by-responsibility.md`
- status: adopted
- maturity: evaluated
- relation: extends

# IMP0028: FB0032: Split record core modules by responsibility

## Status

- status: adopted
- maturity: evaluated
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0032`
- linked_records: `FB0032`, `E0031`, `H0031`, `D0032`

## Source Observation

Source: `harness-lab/records/feedback/FB0032-split-record-core-modules-by-responsibility.md`

# FB0032: Split record core modules by responsibility

## 概要

records.py has become the central maintainability hotspot: it mixes record type constants, frontmatter IO, ID/path indexing, feedback/eval/hypothesis/decision creation, research scan parsing, and improvement dossier aggregation/mutation. Split these responsibilities into focused modules while keeping harnessops.core.records as a compatibility facade.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Introduce record_types.py, record_io.py, record_index.py, lab_records.py, and improvement_dossier.py; preserve current imports and behavior; update tests/docs only where the new structure needs a contract.

## Target Capability

- capability: repository_maintainability
- failure_class: records_module_sprawl

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0031: E0031: FB0032-split-record-core-modules-by-responsibility を評価


- source: `harness-lab/records/eval-cases/E0031-fb0032-split-record-core-modules-by-responsibility.md`

- capability: repository_maintainability

- failure_class: records_module_sprawl

- manual_eval_yml: `harness-lab/views/eval-results/E0031-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0031-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=0, anti_th...

### `IMP0029` daily_steward_orchestration/count_based_preflight_misses_stale_lab_health
- path: `harness-lab/improvements/IMP0029-fb0035-expose-lab-health-in-steward-preflight.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0029: FB0035: Expose lab health in steward preflight

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0035`
- linked_records: `FB0035`, `RS0005`, `E0032`, `H0032`, `D0033`

## Source Observation

Source: `harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md`

# FB0035: Expose lab health in steward preflight

## 概要

hops steward preflight reports overlay counts and lane triggers, but it does not surface lab memory pressure or stale snapshot/semantic memory state as actionable daily steward input.

## 再現

Run hops steward preflight --json in a meta-lab repository where hops lab memory lint --warn-only reports needs-abstraction; the preflight JSON only shows counts and generic librarian trigger information.

## 期待する上流変更

Steward preflight should include source-linked lab health status and trigger reasons so daily runs can route stale memory or lab pressure to the librarian lane without relying on manual follow-up commands.

## Target Capability

- capability: daily_steward_orchestration
- failure_class: count_based_preflight_misses_stale_lab_health

## Investigation

- 2026-05-14T01:04:35+09:00 [implementation-note] Implemented lab_health in steward_preflight by reusing the existing non-writing lab memory lint result for upstream/meta lab repos. The JSON now includes status, pressure, triggers, stale snapshot/abstraction state, and recommended commands; the librarian lane reason names needs-abstraction triggers. Feedback-source project repos report lab_health unavailable instead of probing harness-lab memory. (evidence: src/harnessops/core/steward.py; tests/test_cli/test_steward.py)

## Research Scans

### RS0005:...

### `IMP0030` uvx_update_guidance/stale_hops_update_path
- path: `harness-lab/improvements/IMP0030-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0030: FB0028: Make update notices guide uvx-based HarnessOps upgrades

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0028`
- linked_records: `FB0028`, `E0033`, `H0033`, `D0034`

## Source Observation

Source: `harness-lab/records/feedback/FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`

# FB0028: Make update notices guide uvx-based HarnessOps upgrades

## 概要

Target and project repositories need a single update path when repo-managed HarnessOps artifacts, the currently running hops runtime, and the latest PyPI release differ. The existing notice only compares the repo lock with the current runtime and still points agents at the hops-update-harness skill or bare hops command.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Update the CLI notice so ordinary hops usage in linked repos compares recorded, current, and latest PyPI HarnessOps versions when available, emits uvx --refresh-package harnessops --from harnessops hops update-harness guidance, and keeps migration application behind an explicit follow-up check.

## Target Capability

- capability: uvx_update_guidance
- failure_class: stale_hops_update_path

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0033: E0033: FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades を評価


- source: `harness-lab/records/eval-cases/E0033-fb0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`

- capability: uvx_update_guidance

- failure_class: stale_hops_update_path

- manual_eval_yml: `harness-lab/views/eval-results/E0033-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0033-manual-score.md`
- scores: i...

### `IMP0031` harness_lab_traceability/missing_lab_capture
- path: `harness-lab/improvements/IMP0031-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`
- status: adopted
- maturity: adopted
- relation: extends

# IMP0031: FB0036: Let daily steward use lane budgets and merge automation branches

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0036`
- linked_records: `FB0036`, `E0034`, `H0034`, `D0035`

## Source Observation

Source: `harness-lab/records/feedback/FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`

# FB0036: Let daily steward use lane budgets and merge automation branches

## 概要

Daily steward currently treats max-systemic-candidates as a single global cap and the recommended prompt stops after pushing an automation branch. User feedback prefers lane-specific budgets, automatic merge when validation passes, optional develop/integration branch workflow, and no direct main push.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Document lane budgets, keep systemic candidates conservative, allow multiple metadata/backfill/read-only items, and update full automation guidance so validated automation branches can be merged into an authorized base or integration branch without direct protected-branch push.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0034: E0034: FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches を評価


- source: `harness-lab/records/eval-cases/E0034-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0034-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0034-manual-score...

### `RS0001` meta_improvement_research/unstructured_research_scan_results
- path: `harness-lab/records/research-scans/RS0001-structure-meta-improvement-research-scan-outputs.md`
- status: captured

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

### `RS0002` generated_view_management/stale_generated_view_repair_gap
- path: `harness-lab/records/research-scans/RS0002-clarify-generated-view-refresh-and-stale-warning-repair.md`
- status: captured

# RS0002: Clarify generated view refresh and stale warning repair

## Scope

- scope: harnessops-core generated view management
- existing_dossier: 未設定
- capability: generated_view_management
- failure_class: stale_generated_view_repair_gap

## Evidence

### Local

- Doctor currently reports stale generated-view warnings for README, backlog, imported-feedback, improvements, research-scans, and score-trajectory in this repo (ref: uv run --with-editable . hops doctor --check-overlay --check-records)

### Codebase

- refresh_views rewrites only imported-feedback, improvements, and research-scans for lab overlays (ref: src/harnessops/core/render.py)
- doctor compares every lock managed_file hash and emits a generic generated-view warning without a next command (ref: src/harnessops/core/validation.py)
- generated_overlay_files registers lab README, backlog, imported-feedback, improvements, research-scans, and score-trajectory as managed files (ref: src/harnessops/core/overlay.py)
- roadmap names hops views refresh/status, while the implemented command is hops lab refresh-views (ref: docs/roadmap.md ; src/harnessops/cli/lab.py)

### External

- なし

### Risk And Counterexample

- A refresh command that updates only some managed views can leave doctor ok with warnings, training operators to ignore generated-view staleness (ref: temporary copy run: doctor -> lab refresh-views -> doctor)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Make lab refresh-views cover all doctor-managed lab artifacts | extends | capture | hops lab capture --title Generated-view-refresh-leaves-managed-warnings --capability generated_view_management --failure-class stale_generated_view_repair_gap |
| Add doctor next-action guidance for stale generated views...

### `RS0003` release-and-agent-bridge/post-release-residual-risk
- path: `harness-lab/records/research-scans/RS0003-post-release-residual-improvement-candidates-after-v0-1-4.md`
- status: captured

# RS0003: Post-release residual improvement candidates after v0.1.4

## Scope

- scope: harnessops-core
- existing_dossier: IMP0018
- capability: release-and-agent-bridge
- failure_class: post-release-residual-risk

## Evidence

### Local

- v0.1.4 release succeeded, but GitHub release run emitted Node.js 20 action deprecation annotations (ref: gh run 25787498566)

### Codebase

- Publish workflow still uses actions/checkout@v4 and actions/setup-python@v5 (ref: .github/workflows/publish-pypi.yml)
- Issue #9 remains open; #10 fixed generated/packaged fallback text but did not add doctor validation or print-invocation command (ref: https://github.com/Nkzono99/harnessops/issues/9)
- lab memory lint reports status ok while snapshot and abstraction are stale, which can make post-release knowledge freshness ambiguous (ref: uv run --with-editable . hops lab memory lint --warn-only)

### External

- GitHub says runners begin using Node24 by default on June 2 2026 and users should update workflows to latest actions that run on Node24 (ref: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)
- actions/checkout v5 and actions/setup-python v6 document Node24 runtime support (ref: https://github.com/actions/checkout https://github.com/actions/setup-python)

### Risk And Counterexample

- The release workflow still passes today, but the deprecation window is short and warnings may turn into release friction after GitHub runner defaults change (ref: .github/workflows/publish-pypi.yml)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Migrate release workflow actions to Node24-ready majors | new | capture/propose | hops lab capture --title 'Release workflow uses Node20 action majors' |
| Finish issue #9...

### `RS0004` issue_lab_reconciliation/stale_external_issue_tracker
- path: `harness-lab/records/research-scans/RS0004-reconcile-post-v0-1-5-open-issues-with-lab-decisions.md`
- status: captured

# RS0004: Reconcile post-v0.1.5 open issues with lab decisions

## Scope

- scope: harnessops-core issue tracker and lab-state reconciliation
- existing_dossier: IMP0002/IMP0003/IMP0004/IMP0018
- capability: issue_lab_reconciliation
- failure_class: stale_external_issue_tracker

## Evidence

### Local

- Open issues #6, #7, and #8 still appear in GitHub even though their linked lab dossiers are adopted. (ref: gh issue list --state open --limit 20)
- Issue #9 remains open and overlaps IMP0018, but still includes residual acceptance criteria for doctor fallback validation or an invocation-reporting command. (ref: https://github.com/Nkzono99/harnessops/issues/9)
- lab memory lint is ok, but snapshot and abstraction are stale after v0.1.5, so post-release readers may need either issue reconciliation or an explicit memory compaction pass later. (ref: uv run --with-editable . hops lab memory lint --warn-only)

### Codebase

- IMP0002 records conflict-aware update-harness behavior as adopted, with tests covering unmodified refresh, local edit conflict, forced overwrite, and count/path output. (ref: harness-lab/improvements/IMP0002-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md)
- IMP0003 records per-improvement dossier support as adopted, with docs and tests for low-friction dossier creation and generated views. (ref: harness-lab/improvements/IMP0003-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md)
- IMP0004 records lab-first GitHub issue draft/create as adopted, including sanitized body creation, duplicate search, confirm-create, and URL writeback. (ref: harness-lab/improvements/IMP0004-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md)
- Current bridge assets use uvx --from harnessops hops fallback and contract tests b...

### `RS0005` daily_steward_orchestration/count_based_preflight_misses_stale_lab_health
- path: `harness-lab/records/research-scans/RS0005-route-lab-health-through-steward-preflight.md`
- status: captured

# RS0005: Route lab health through steward preflight

## Scope

- scope: harnessops-core daily steward preflight
- existing_dossier: FB0035
- capability: daily_steward_orchestration
- failure_class: count_based_preflight_misses_stale_lab_health

## Evidence

### Local

- Open scan found lab memory lint needs-abstraction while preflight showed only counts and generic lane triggers (ref: harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md)

### Codebase

- steward_preflight builds overlay counts and lane triggers but does not call lab memory lint (ref: src/harnessops/core/steward.py)
- lab memory lint already returns status, triggers, recommended commands, stale snapshot, and stale abstraction (ref: src/harnessops/core/lab_memory_lint.py)

### External

- なし

### Risk And Counterexample

- Putting too much analysis into preflight could turn the steward into a workflow engine instead of a deterministic intake command (ref: docs/design-principles.md)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add lab_health to steward preflight and librarian lane trigger reasons | extends | propose | hops lab new-eval-case --from FB0035 |

## Recommendation

propose a narrow deterministic preflight extension: include lab_health only for lab repos, reuse existing lint output, and keep downstream judgment in the librarian lane.

## Next Commands

- `hops lab new-eval-case --from FB0035`

## Abstraction Manifest Template

```yaml
schema_version: '0.1'
kind: harness_lab_memory_abstraction
updated_at: <ISO-8601 timestamp>
source_digest: 2172da30944f7a33c114f8c7bfada6bcce47e5f7b2d7ef29f005ac251e658532
sources:
- IMP0001
- IMP0002
- IMP0003
- IMP0004
- IMP0005
- IMP0006
- IMP0007
- IMP0008
- IMP0009
- IMP0011
- IMP0012
- IMP0013
- IMP0014
- IMP0015
- IMP0016
- IMP0017
- IMP0018
- IMP0019
- IMP0020
- IMP0021
- IMP0022
- IMP0023
- IMP0024
- IMP0025
- IMP0026
- IMP0027
- IMP0028
- IMP0029
- IMP0030
- IMP0031
- RS0001
- RS0002
- RS0003
- RS0004
- RS0005
outputs:
- harness-lab/knowledge/principles.md
- harness-lab/knowledge/patterns.yml
- harness-lab/knowledge/anti-patterns.md
- harness-lab/knowledge/evaluation-playbook.md
notes: Update this manifest when the skill refreshes abstract knowledge.
```
