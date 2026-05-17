---
id: FB0051
record_type: imported_feedback
created_at: '2026-05-17T12:15:33+09:00'
status: triaged
source:
  type: local-capture
  original_id: routine-cli-request
  source_project: harnessops
classification:
  capability: agent_asset_packaging
  failure_class: manual_packaged_skill_sync_drift
links:
  eval_case:
  issue_url:
---

# FB0051: Packaged skill asset sync should be a CLI, not manual copy work

## 概要

Updating repo-local HOPS skills requires keeping packaged Codex and Claude assets in lockstep. Manual copy work already left Claude assets drifted, so routine sync and CI-style drift detection should be owned by a HOPS CLI command.

## 再現

Edit a repo-local skill, run the old manual copy workflow, and observe that one host can drift. The new hops agent sync-packaged-skills --check detects the drift.

## 期待する上流変更

Provide a command that syncs .agents/skills/hops-* into packaged agent assets for codex and claude, with a --check mode that detects missing, drifted, or retired skills without writing.
