---
id: IMP0039
record_type: improvement_dossier
created_at: '2026-05-19T03:23:04+09:00'
updated_at: '2026-05-19T03:23:27+09:00'
status: active
source_type: codebase
scope: harnessops-core
maturity: investigated
relation: extends
promotion_level: target-lab-case
source_feedback: FB0051
eval_cases: []
hypotheses: []
decisions: []
research_scans: []
classification:
  capability: agent_asset_packaging
  failure_class: manual_packaged_skill_sync_drift
guard:
  status: not-defined
  path:
investigation:
- created_at: '2026-05-19T03:23:27+09:00'
  kind: codebase
  summary: The CLI surface now has hops agent sync-packaged-skills with --codex, --claude, --check, and --json options; a read-only check over current Codex and Claude packaged HOPS skills returned ok=true with no missing, drifted, retired, or updated assets. This makes FB0051 a validation-standardization candidate rather than a manual copy task.
  evidence_ref: uv run --with-editable . hops agent sync-packaged-skills --help; uv run --with-editable . hops agent sync-packaged-skills --check --json
links:
  issue_url:
---

# IMP0039: FB0051: Packaged skill asset sync should be a CLI, not manual copy work

## Status

- status: active
- maturity: investigated
- source_type: codebase
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0051`
- linked_records: `FB0051`

## Source Observation

Source: `harness-lab/records/feedback/FB0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md`

# FB0051: Packaged skill asset sync should be a CLI, not manual copy work

## 概要

Updating repo-local HOPS skills requires keeping packaged Codex and Claude assets in lockstep. Manual copy work already left Claude assets drifted, so routine sync and CI-style drift detection should be owned by a HOPS CLI command.

## 再現

Edit a repo-local skill, run the old manual copy workflow, and observe that one host can drift. The new hops agent sync-packaged-skills --check detects the drift.

## 期待する上流変更

Provide a command that syncs .agents/skills/hops-* into packaged agent assets for codex and claude, with a --check mode that detects missing, drifted, or retired skills without writing.

## Target Capability

- capability: agent_asset_packaging
- failure_class: manual_packaged_skill_sync_drift

## Investigation

- 2026-05-19T03:23:27+09:00 [codebase] The CLI surface now has hops agent sync-packaged-skills with --codex, --claude, --check, and --json options; a read-only check over current Codex and Claude packaged HOPS skills returned ok=true with no missing, drifted, retired, or updated assets. This makes FB0051 a validation-standardization candidate rather than a manual copy task. (evidence: uv run --with-editable . hops agent sync-packaged-skills --help; uv run --with-editable . hops agent sync-packaged-skills --check --json)

## Research Scans

research scan はまだありません。


## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: not-defined
- path: None

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。
