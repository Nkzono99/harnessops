---
id: IMP0037
record_type: improvement_dossier
created_at: '2026-05-18T14:21:56+09:00'
updated_at: '2026-05-18T15:07:04+09:00'
status: active
source_type: friction
scope: harnessops-core
maturity: investigated
relation: implements FB0053 global local-state workflow
promotion_level: strategic
source_feedback: FB0053
eval_cases: []
hypotheses: []
decisions: []
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_project_link_storage_local_keeps_repo_clean;tests/test_cli/test_mvp_flow.py::test_agent_user_install_writes_global_codex_plugin;tests/test_agent_harness_contract.py::test_global_plugin_is_packaged_without_root_plugin_surface
investigation:
- created_at: '2026-05-18T14:22:05+09:00'
  kind: codebase
  summary: Implemented a shared Project abstraction with separate repo root and storage root, a global registry under HOPS_HOME/default ~/.harnessops, storage=local project link/resolve, local pack/import/merge commands, and a packaged HarnessOps Global Codex plugin installed via agent install --scope user --codex. Existing repo-local init/link remains storage=repo and shares the same record/render paths through Project.overlay_dir.
  evidence_ref: src/harnessops/core/registry.py;src/harnessops/core/project.py;src/harnessops/cli/project.py;src/harnessops/cli/local.py;src/harnessops/core/agent_plugin.py;tests/test_cli/test_mvp_flow.py
- created_at: '2026-05-18T15:07:04+09:00'
  kind: code-review
  summary: Added the global share-state Codex skill and moved the default local pack output to HOPS_HOME exports so pack does not dirty ordinary repositories.
  evidence_ref: src/harnessops/cli/local.py;src/harnessops/agent_assets/plugins/codex/harnessops-global/skills/hops-global-share-state/SKILL.md;tests/test_cli/test_mvp_flow.py
links:
  issue_url:
---

# IMP0037: FB0053: Global local HarnessOps usage without repository files

## Status

- status: active
- maturity: investigated
- source_type: friction
- scope: harnessops-core
- relation: implements FB0053 global local-state workflow
- promotion_level: strategic
- source_feedback: `FB0053`
- linked_records: `FB0053`

## Source Observation

Source: `harness-lab/records/feedback/FB0053-global-local-harnessops-usage-without-repository-files.md`

# FB0053: Global local HarnessOps usage without repository files

## 概要

Support a global registry and local state storage so ordinary repositories can use HarnessOps during development without committing .harnessops, harness-feedback, or harness-lab. Agents should access the same flow through a global Codex plugin that delegates all state changes to uvx --from harnessops hops.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add a global project registry, storage=local overlay resolution, project resolve/link commands, and a packaged/global plugin surface while keeping existing repo-local target/project usage working.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-18T14:22:05+09:00 [codebase] Implemented a shared Project abstraction with separate repo root and storage root, a global registry under HOPS_HOME/default ~/.harnessops, storage=local project link/resolve, local pack/import/merge commands, and a packaged HarnessOps Global Codex plugin installed via agent install --scope user --codex. Existing repo-local init/link remains storage=repo and shares the same record/render paths through Project.overlay_dir. (evidence: src/harnessops/core/registry.py;src/harnessops/core/project.py;src/harnessops/cli/project.py;src/harnessops/cli/local.py;src/harnessops/core/agent_plugin.py;tests/test_cli/test_mvp_flow.py)
- 2026-05-18T15:07:04+09:00 [code-review] Added the global share-state Codex skill and moved the default local pack output to HOPS_HOME exports so pack does not dirty ordinary repositories. (evidence: src/harnessops/cli/local.py;src/harnessops/agent_assets/plugins/codex/harnessops-global/skills/hops-global-share-state/SKILL.md;tests/test_cli/test_mvp_flow.py)

## Research Scans

research scan はまだありません。


## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_project_link_storage_local_keeps_repo_clean;tests/test_cli/test_mvp_flow.py::test_agent_user_install_writes_global_codex_plugin;tests/test_agent_harness_contract.py::test_global_plugin_is_packaged_without_root_plugin_surface

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。
