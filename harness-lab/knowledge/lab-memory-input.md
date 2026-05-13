# Lab Memory Abstraction Input

このファイルは `hops lab memory prepare` が作る skill 入力です。
`records/` と `improvements/` が正本で、この bundle は抽象化作業の入口です。

## Lint State

- status: ok
- reason: thresholds-not-exceeded-no-sources-or-current
- source_digest: `011a809c1c52093bc69d4a3e91fcc6e815b589038e86803305338152a18ac93c`
- pressure: none
- triggers: none

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

## Abstraction Manifest Template

```yaml
schema_version: '0.1'
kind: harness_lab_memory_abstraction
updated_at: <ISO-8601 timestamp>
source_digest: 011a809c1c52093bc69d4a3e91fcc6e815b589038e86803305338152a18ac93c
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
- RS0001
outputs:
- harness-lab/knowledge/principles.md
- harness-lab/knowledge/patterns.yml
- harness-lab/knowledge/anti-patterns.md
- harness-lab/knowledge/evaluation-playbook.md
notes: Update this manifest when the skill refreshes abstract knowledge.
```
