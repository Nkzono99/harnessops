---
id: RS0002
record_type: research_scan
created_at: '2026-05-13T11:43:08+09:00'
status: captured
scope: harnessops-core generated view management
existing_dossier:
classification:
  capability: generated_view_management
  failure_class: stale_generated_view_repair_gap
evidence:
  local:
  - summary: Doctor currently reports stale generated-view warnings for README, backlog, imported-feedback, improvements, research-scans, and score-trajectory in this repo
    ref: uv run --with-editable . hops doctor --check-overlay --check-records
  codebase:
  - summary: refresh_views rewrites only imported-feedback, improvements, and research-scans for lab overlays
    ref: src/harnessops/core/render.py
  - summary: doctor compares every lock managed_file hash and emits a generic generated-view warning without a next command
    ref: src/harnessops/core/validation.py
  - summary: generated_overlay_files registers lab README, backlog, imported-feedback, improvements, research-scans, and score-trajectory as managed files
    ref: src/harnessops/core/overlay.py
  - summary: roadmap names hops views refresh/status, while the implemented command is hops lab refresh-views
    ref: docs/roadmap.md ; src/harnessops/cli/lab.py
  external: []
  risk:
  - summary: A refresh command that updates only some managed views can leave doctor ok with warnings, training operators to ignore generated-view staleness
    ref: 'temporary copy run: doctor -> lab refresh-views -> doctor'
candidates:
- title: Make lab refresh-views cover all doctor-managed lab artifacts
  relation: extends
  recommendation: capture
  next_command: hops lab capture --title Generated-view-refresh-leaves-managed-warnings --capability generated_view_management --failure-class stale_generated_view_repair_gap
- title: Add doctor next-action guidance for stale generated views
  relation: extends
  recommendation: capture
  next_command: hops lab capture --title Doctor-stale-view-warnings-need-repair-commands --capability generated_view_management --failure-class stale_generated_view_repair_gap
- title: Align roadmap and CLI around views refresh/status
  relation: extends
  recommendation: note
  next_command: hops lab investigate --from <future-IMP> --kind codebase --summary Roadmap-and-CLI-expose-different-generated-view-command-shapes
recommendation: capture the stale generated-view repair gap before implementation; prefer one fix that makes refresh/status behavior match doctor-managed artifacts and gives operators an explicit next command.
---

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
| Add doctor next-action guidance for stale generated views | extends | capture | hops lab capture --title Doctor-stale-view-warnings-need-repair-commands --capability generated_view_management --failure-class stale_generated_view_repair_gap |
| Align roadmap and CLI around views refresh/status | extends | note | hops lab investigate --from <future-IMP> --kind codebase --summary Roadmap-and-CLI-expose-different-generated-view-command-shapes |

## Recommendation

capture the stale generated-view repair gap before implementation; prefer one fix that makes refresh/status behavior match doctor-managed artifacts and gives operators an explicit next command.

## Next Commands

- `hops lab capture --title Generated-view-refresh-leaves-managed-warnings --capability generated_view_management --failure-class stale_generated_view_repair_gap`
- `hops lab capture --title Doctor-stale-view-warnings-need-repair-commands --capability generated_view_management --failure-class stale_generated_view_repair_gap`
- `hops lab investigate --from <future-IMP> --kind codebase --summary Roadmap-and-CLI-expose-different-generated-view-command-shapes`
