---
id: IMP0038
record_type: improvement_dossier
created_at: '2026-05-19T03:22:20+09:00'
updated_at: '2026-05-20T03:23:17+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: shipped-behavior
source_feedback: FB0045
eval_cases:
- E0041
hypotheses:
- H0041
decisions:
- D0042
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
investigation:
- created_at: '2026-05-19T03:22:41+09:00'
  kind: codebase
  summary: Today's daily steward has fresh snapshot and semantic memory, but lab memory lint still reports needs-abstraction from file_count>256; issue discovery also found no open GitHub issues while RS0004 still carries old remote-close candidates. Treat this as source-preserving active-memory and queue-retirement pressure, not another snapshot compaction pass.
  evidence_ref: harness-lab/knowledge/lab-memory.yml; uv run --with-editable . hops lab memory lint --warn-only; gh issue list --repo Nkzono99/harnessops --state all --limit 20
- created_at: '2026-05-20T03:23:16+09:00'
  kind: codebase
  summary: 'Run 20260520-030313 shows the remaining lab-health pressure is split: maintenance refreshed memory, later issue work made semantic memory stale again, and file_count remains above threshold. Because IMP0038 already guards source-preserving active queue and memory exclusion, the follow-on should distinguish physical file-count pressure from an active-memory budget before adding new compaction mechanics.'
  evidence_ref: .harnessops/cache/steward-runs/20260520-030313-fdb26c1.json; harness-lab/knowledge/lab-memory-input.yml; tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
links:
  issue_url:
---

# IMP0038: FB0045: Harness lab needs forgetting policy

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: shipped-behavior
- source_feedback: `FB0045`
- linked_records: `FB0045`, `E0041`, `H0041`, `D0042`

## Source Observation

Source: `harness-lab/records/feedback/FB0045-harness-lab-needs-forgetting-policy.md`

# FB0045: Harness lab needs forgetting policy

## 概要

Harness-lab currently supports recording, deterministic compaction, semantic abstraction, and source-linked extraction, but growth pressure will keep increasing because old low-signal records are never retired, archived, summarized away, or marked out of working memory.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Design a source-preserving forgetting lane that can mark stale local-only or superseded lab material as archived or excluded from active memory without destroying auditability.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-19T03:22:41+09:00 [codebase] Today's daily steward has fresh snapshot and semantic memory, but lab memory lint still reports needs-abstraction from file_count>256; issue discovery also found no open GitHub issues while RS0004 still carries old remote-close candidates. Treat this as source-preserving active-memory and queue-retirement pressure, not another snapshot compaction pass. (evidence: harness-lab/knowledge/lab-memory.yml; uv run --with-editable . hops lab memory lint --warn-only; gh issue list --repo Nkzono99/harnessops --state all --limit 20)
- 2026-05-20T03:23:16+09:00 [codebase] Run 20260520-030313 shows the remaining lab-health pressure is split: maintenance refreshed memory, later issue work made semantic memory stale again, and file_count remains above threshold. Because IMP0038 already guards source-preserving active queue and memory exclusion, the follow-on should distinguish physical file-count pressure from an active-memory budget before adding new compaction mechanics. (evidence: .harnessops/cache/steward-runs/20260520-030313-fdb26c1.json; harness-lab/knowledge/lab-memory-input.yml; tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory)

## Research Scans

research scan はまだありません。


## Evaluation

### E0041: E0041: FB0045-harness-lab-needs-forgetting-policy を評価


- source: `harness-lab/records/eval-cases/E0041-fb0045-harness-lab-needs-forgetting-policy.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0041-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0041-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=4, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: Implemented a narrow source-preserving retire command. The guard creates a research scan with a stale next command, retires it, confirms the source file and reason remain, verifies active queue exclusion with include-closed visibility, and verifies memory abstraction input excludes the retired source.


## Hypotheses

### H0041: H0041: E0041-fb0045-harness-lab-needs-forgetting-policy の仮説


Source: `harness-lab/records/hypotheses/H0041-e0041-fb0045-harness-lab-needs-forgetting-policy.md`


# H0041: E0041-fb0045-harness-lab-needs-forgetting-policy の仮説

## 仮説

A source-preserving lab retire command can remove stale research candidates from active priority and memory inputs while preserving the canonical record.

## メカニズム

Update record frontmatter with archived or superseded status plus retirement metadata, then make queue and abstraction-source collectors treat retired records as closed unless explicitly requested.

## 最小実装

Add a narrow hops lab retire command for existing lab records, skip retired records in review queue and abstraction input by default, and guard it with a CLI fixture test.

## 代替案: 削除または統合

Only document a forgetting policy or manually edit records, but that leaves no repeatable guard and keeps stale next commands in the queue.

## 期待される利点

Priority lanes can retire stale local-only or superseded items without deleting audit records, reducing repeated queue pressure.

## 想定される欠点

A too-broad retire primitive could hide useful counterexamples, so the command must preserve reason and evidence metadata and avoid deleting files.

## 評価計画

Create a research scan with a next command, retire it, verify the file remains, queue omits it, and abstraction input sources omit it while doctor and migrate still pass.

## 中止基準

Reject or park if retirement deletes records, hides adopted guards, bypasses source feedback links, or requires direct manual edits to harness-lab.


## Evidence

`harness-lab/views/eval-results/E0041-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0042: D0042: adopted H0041


Source: `harness-lab/records/decisions/D0042-adopted-h0041.md`


# D0042: adopted H0041

## 判断

adopted

## 理由

Adopt the narrow retire primitive because it solves the active queue and semantic memory part of FB0045 without deleting records or adding a broad cleanup lane.

## 証拠

Focused pytest passed for tests/test_cli/test_lab_usage.py, covering preserved source record, retirement metadata, active queue exclusion, include-closed visibility, and memory abstraction input exclusion.

## 回帰リスク

Low to medium: retired records may be hidden from default active context, mitigated by preserving the source file, retirement metadata, and --include-closed queue visibility.

## フォローアップ

Use retire only for stale or superseded queue records with explicit evidence; physical deletion remains release-gated archive work.

## 回帰ガード

tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
