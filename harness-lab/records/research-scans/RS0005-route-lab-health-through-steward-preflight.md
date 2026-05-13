---
id: RS0005
record_type: research_scan
created_at: '2026-05-14T00:58:24+09:00'
status: captured
scope: harnessops-core daily steward preflight
existing_dossier: FB0035
classification:
  capability: daily_steward_orchestration
  failure_class: count_based_preflight_misses_stale_lab_health
evidence:
  local:
  - summary: Open scan found lab memory lint needs-abstraction while preflight showed only counts and generic lane triggers
    ref: harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md
  codebase:
  - summary: steward_preflight builds overlay counts and lane triggers but does not call lab memory lint
    ref: src/harnessops/core/steward.py
  - summary: lab memory lint already returns status, triggers, recommended commands, stale snapshot, and stale abstraction
    ref: src/harnessops/core/lab_memory_lint.py
  external: []
  risk:
  - summary: Putting too much analysis into preflight could turn the steward into a workflow engine instead of a deterministic intake command
    ref: docs/design-principles.md
candidates:
- title: Add lab_health to steward preflight and librarian lane trigger reasons
  relation: extends
  recommendation: propose
  next_command: hops lab new-eval-case --from FB0035
recommendation: 'propose a narrow deterministic preflight extension: include lab_health only for lab repos, reuse existing lint output, and keep downstream judgment in the librarian lane.'
---

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
