---
id: RS0006
record_type: research_scan
created_at: '2026-05-18T03:16:43+09:00'
status: archived
scope: harnessops-core daily steward invention and priority lanes
existing_dossier: FB0050
classification:
  capability: daily_steward_supervision
  failure_class: autonomous_record_growth_without_selection_pressure
evidence:
  local:
  - summary: Open-meta scan for run 20260518-030245-7e9269e warned that the daily steward can reward producing records faster than retiring, merging, rejecting, or testing them
    ref: automation lane handoff
  - summary: Current queue has 25 items and lab health still reports needs-abstraction from file_count>256 after maintenance compaction
    ref: hops lab review queue --json; supervisor preflight
  codebase:
  - summary: hops-research-improvements already requires horizon/generalization and park/reject routing before new captures
    ref: .agents/skills/hops-research-improvements/SKILL.md
  - summary: FB0050 captures implicit lane contract risk; FB0045 captures missing source-preserving forgetting policy
    ref: harness-lab/records/feedback/FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md; harness-lab/records/feedback/FB0045-harness-lab-needs-forgetting-policy.md
  external: []
  risk:
  - summary: Over-correcting could make invention suppress useful raw discoveries; keep open-meta noisy and enforce consolidation only in downstream routing
    ref: open-meta counterframe
candidates:
- title: Add consolidation-first queue policy to invention/priority lanes
  relation: extends
  recommendation: propose after FB0050 dossier exists
  next_command: hops lab dossier --from FB0050
- title: Design source-preserving archive/exclude policy for stale local-only lab material
  relation: extends
  recommendation: queue behind lane contract work
  next_command: hops lab dossier --from FB0045
recommendation: Queue a bounded consolidation-first policy through existing FB0050/FB0045 records; priority lane should prefer FB0050 dossier/eval before any new capture.
retirement:
- created_at: '2026-05-20T03:23:43+09:00'
  status: archived
  reason: 'Superseded as an active queue item: FB0050 already has IMP0036/E0040/H0040/D0041 and the current run records follow-on queue pressure in RS0008 while preserving RS0006 as source evidence.'
  evidence_ref: IMP0036; RS0008; .harnessops/cache/steward-runs/20260520-030313-fdb26c1.json
---

# RS0006: Consolidation-first routing for daily steward candidates

## Scope

- scope: harnessops-core daily steward invention and priority lanes
- existing_dossier: FB0050
- capability: daily_steward_supervision
- failure_class: autonomous_record_growth_without_selection_pressure

## Evidence

### Local

- Open-meta scan for run 20260518-030245-7e9269e warned that the daily steward can reward producing records faster than retiring, merging, rejecting, or testing them (ref: automation lane handoff)
- Current queue has 25 items and lab health still reports needs-abstraction from file_count>256 after maintenance compaction (ref: hops lab review queue --json; supervisor preflight)

### Codebase

- hops-research-improvements already requires horizon/generalization and park/reject routing before new captures (ref: .agents/skills/hops-research-improvements/SKILL.md)
- FB0050 captures implicit lane contract risk; FB0045 captures missing source-preserving forgetting policy (ref: harness-lab/records/feedback/FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md; harness-lab/records/feedback/FB0045-harness-lab-needs-forgetting-policy.md)

### External

- なし

### Risk And Counterexample

- Over-correcting could make invention suppress useful raw discoveries; keep open-meta noisy and enforce consolidation only in downstream routing (ref: open-meta counterframe)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add consolidation-first queue policy to invention/priority lanes | extends | propose after FB0050 dossier exists | hops lab dossier --from FB0050 |
| Design source-preserving archive/exclude policy for stale local-only lab material | extends | queue behind lane contract work | hops lab dossier --from FB0045 |

## Recommendation

Queue a bounded consolidation-first policy through existing FB0050/FB0045 records; priority lane should prefer FB0050 dossier/eval before any new capture.

## Next Commands

- `hops lab dossier --from FB0050`
- `hops lab dossier --from FB0045`
