---
id: FB0057
record_type: imported_feedback
created_at: '2026-06-02T15:18:57+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-release-prep
  source_project: harnessops
classification:
  capability: external_overlay_paths
  failure_class: path_resolution
links:
  eval_case:
  issue_url:
---

# FB0057: Support external overlay paths

## 概要

Overlay path handling should work when a project chooses an overlay directory outside the repository root, including relative ../ paths and absolute paths. Existing path joins and relative_to(root) display logic break doctor/update/refresh flows for those overlays.

## 再現

Run hops init --profile harnessops-core --path ../outside-harness-lab, then run hops doctor --check-overlay --check-records, hops lab refresh-views, and hops update-harness --json.

## 期待する上流変更

Resolve overlay filesystem paths relative to the project root only when needed, preserve configured overlay path strings in generated metadata, and display files inside external overlays using the configured overlay path.
