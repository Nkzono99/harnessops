---
id: FB0050
record_type: imported_feedback
created_at: '2026-05-17T12:02:21+09:00'
status: triaged
source:
  type: local-capture
  original_id: review-after-PR30
  source_project: harnessops
classification:
  capability: daily_steward_supervision
  failure_class: implicit_lane_contract
links:
  eval_case:
  issue_url:
---

# FB0050: Daily steward lane results need structured artifacts and lane-aligned recommendations

## 概要

Code review found that open-meta-scan results were only described by handoff prose, while subagent spawn recommendations used signal names that did not always match supervisor lane names. This can make downstream invention/priority agents depend on implicit formatting or nonexistent lane identifiers.

## 再現

Review merged PR #30 and inspect src/harnessops/core/steward.py plus daily steward preflight JSON.

## 期待する上流変更

Steward run preflight should expose optional structured lane artifacts for open-meta-scan raw ideas/counterframes/routing hints, and subagent spawn recommendations should align with actual supervisor lanes while keeping signal detail available separately.
