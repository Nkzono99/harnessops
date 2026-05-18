---
id: RS0007
record_type: research_scan
created_at: '2026-05-19T03:22:54+09:00'
status: archived
scope: harnessops-core lab memory and queue retirement
existing_dossier: FB0045/IMP0014/IMP0015/RS0004
classification:
  capability: lab_memory_compaction
  failure_class: source_preserving_queue_retirement_gap
evidence:
  local:
  - summary: Maintenance refreshed snapshot and semantic abstraction, but memory lint still reports needs-abstraction because file_count>256
    ref: harness-lab/knowledge/lab-memory.yml
  - summary: 'Issue lane found no open issues; current issue list shows #5-#9 closed, making RS0004 remote-close candidates stale'
    ref: gh issue list --repo Nkzono99/harnessops --state all --limit 20
  codebase:
  - summary: IMP0014 and IMP0015 already adopted deterministic compaction and trigger/abstraction separation, so the remaining pressure is active-set retirement rather than compaction mechanics
    ref: harness-lab/improvements/IMP0014-fb0017-compact-lab-records-into-mutable-knowledge.md; harness-lab/improvements/IMP0015-fb0018-separate-lab-memory-triggers-from-abstraction.md
  external: []
  risk:
  - summary: Premature deletion would destroy auditability; policy should archive, supersede, or exclude from active memory while preserving canonical records
    ref:
candidates:
- title: Evaluate FB0045 forgetting policy
  relation: extends
  recommendation: selected_for_execution
  next_command: hops lab eval-case create --from FB0045
- title: Treat RS0004 remote issue close actions as stale evidence
  relation: parks
  recommendation: park
  next_command:
recommendation: Route managed-pressure and stale research candidates into FB0045/IMP0038; priority lane should design an eval case for source-preserving active-memory retirement before adding new queue mechanics.
retirement:
- created_at: '2026-05-19T03:32:42+09:00'
  status: archived
  reason: FB0045 candidate advanced to E0041/H0041 and implementation guard; keep scan as source evidence without repeated queue command
  evidence_ref: E0041; H0041; tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
---

# RS0007: Route lab pressure to forgetting policy

## Scope

- scope: harnessops-core lab memory and queue retirement
- existing_dossier: FB0045/IMP0014/IMP0015/RS0004
- capability: lab_memory_compaction
- failure_class: source_preserving_queue_retirement_gap

## Evidence

### Local

- Maintenance refreshed snapshot and semantic abstraction, but memory lint still reports needs-abstraction because file_count>256 (ref: harness-lab/knowledge/lab-memory.yml)
- Issue lane found no open issues; current issue list shows #5-#9 closed, making RS0004 remote-close candidates stale (ref: gh issue list --repo Nkzono99/harnessops --state all --limit 20)

### Codebase

- IMP0014 and IMP0015 already adopted deterministic compaction and trigger/abstraction separation, so the remaining pressure is active-set retirement rather than compaction mechanics (ref: harness-lab/improvements/IMP0014-fb0017-compact-lab-records-into-mutable-knowledge.md; harness-lab/improvements/IMP0015-fb0018-separate-lab-memory-triggers-from-abstraction.md)

### External

- なし

### Risk And Counterexample

- Premature deletion would destroy auditability; policy should archive, supersede, or exclude from active memory while preserving canonical records

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Evaluate FB0045 forgetting policy | extends | selected_for_execution | hops lab eval-case create --from FB0045 |
| Treat RS0004 remote issue close actions as stale evidence | parks | park |  |

## Recommendation

Route managed-pressure and stale research candidates into FB0045/IMP0038; priority lane should design an eval case for source-preserving active-memory retirement before adding new queue mechanics.

## Next Commands

- `hops lab eval-case create --from FB0045`
