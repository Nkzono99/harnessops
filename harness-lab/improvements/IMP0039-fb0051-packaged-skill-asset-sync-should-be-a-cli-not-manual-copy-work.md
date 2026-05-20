---
id: IMP0039
record_type: improvement_dossier
created_at: '2026-05-19T03:23:04+09:00'
updated_at: '2026-05-21T03:33:17+09:00'
status: adopted
source_type: codebase
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0051
eval_cases:
- E0044
hypotheses:
- H0044
decisions:
- D0045
research_scans: []
classification:
  capability: agent_asset_packaging
  failure_class: manual_packaged_skill_sync_drift
guard:
  status: implemented
  path: tests/test_cli/test_agent.py::test_agent_sync_packaged_skills_cli_check_reports_drift;tests/test_agent_harness_contract.py::test_packaged_agent_assets_match_repo_local_skills
investigation:
- created_at: '2026-05-19T03:23:27+09:00'
  kind: codebase
  summary: The CLI surface now has hops agent sync-packaged-skills with --codex, --claude, --check, and --json options; a read-only check over current Codex and Claude packaged HOPS skills returned ok=true with no missing, drifted, retired, or updated assets. This makes FB0051 a validation-standardization candidate rather than a manual copy task.
  evidence_ref: uv run --with-editable . hops agent sync-packaged-skills --help; uv run --with-editable . hops agent sync-packaged-skills --check --json
- created_at: '2026-05-21T03:27:11+09:00'
  kind: codebase
  summary: The packaged skill sync concern from open-meta is already owned by IMP0039. Current queue still exposes IMP0039 as active and evaluation-design-needed, so route distribution-smell work to an eval case or guard for hops agent sync-packaged-skills --check instead of opening another sync record.
  evidence_ref: harness-lab/improvements/IMP0039-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md; uv run --with-editable . hops lab review queue --json
links:
  issue_url:
---

# IMP0039: FB0051: Packaged skill asset sync should be a CLI, not manual copy work

## Status

- status: adopted
- maturity: adopted
- source_type: codebase
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0051`
- linked_records: `FB0051`, `E0044`, `H0044`, `D0045`

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
- 2026-05-21T03:27:11+09:00 [codebase] The packaged skill sync concern from open-meta is already owned by IMP0039. Current queue still exposes IMP0039 as active and evaluation-design-needed, so route distribution-smell work to an eval case or guard for hops agent sync-packaged-skills --check instead of opening another sync record. (evidence: harness-lab/improvements/IMP0039-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md; uv run --with-editable . hops lab review queue --json)

## Research Scans

research scan はまだありません。


## Evaluation

### E0044: E0044: FB0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work を評価


- source: `harness-lab/records/eval-cases/E0044-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md`

- capability: agent_asset_packaging

- failure_class: manual_packaged_skill_sync_drift

- manual_eval_yml: `harness-lab/views/eval-results/E0044-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0044-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=2, operator_burden=1, anti_theater=5, maintainability=4, privacy_sanitization_risk=0
- notes: hops agent sync-packaged-skills --check --json returned ok=true with no missing, drifted, or retired Codex/Claude assets; tests/test_cli/test_agent.py passed 2 tests; tests/test_agent_harness_contract.py -k packaged_agent_assets_match_repo_local_skills passed 1 test.


## Hypotheses

### H0044: H0044: E0044-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work の仮説


Source: `harness-lab/records/hypotheses/H0044-e0044-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md`


# H0044: E0044-fb0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work の仮説

## 仮説

Treat packaged HOPS skill sync as a first-class CLI validation path so Codex and Claude packaged assets cannot silently drift from repo-local skills.

## メカニズム

Use hops agent sync-packaged-skills to derive desired packaged assets from .agents/skills/hops-* and compare or write both host asset trees with missing, drifted, and retired paths reported as machine-readable JSON.

## 最小実装

Keep the existing sync-packaged-skills CLI and assert --check --json reports drift without writing, while the repo contract test verifies packaged assets match repo-local skills.

## 代替案: 削除または統合

Continue manual copy plus broad package asset tests, but that leaves routine updates dependent on human memory and makes host-specific drift easy to miss until release.

## 期待される利点

Routine steward and release validation can detect packaged skill drift with one command and point directly at affected host assets.

## 想定される欠点

The sync command adds another release-time check and can fail on intentional package-only experiments unless they are moved out of the hops-* repo-local skill set.

## 評価計画

Run hops agent sync-packaged-skills --check --json, pytest tests/test_cli/test_agent.py, and pytest tests/test_agent_harness_contract.py -k packaged_agent_assets_match_repo_local_skills, then record manual scores for E0044.

## 中止基準

Reject if --check writes files, fails to report host-specific drift, or the contract test cannot prove Codex and Claude assets match repo-local skills.


## Evidence

`harness-lab/views/eval-results/E0044-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_agent.py::test_agent_sync_packaged_skills_cli_check_reports_drift;tests/test_agent_harness_contract.py::test_packaged_agent_assets_match_repo_local_skills

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0045: D0045: adopted H0044


Source: `harness-lab/records/decisions/D0045-adopted-h0044.md`


# D0045: adopted H0044

## 判断

adopted

## 理由

The existing sync-packaged-skills CLI gives this packet the requested non-writing drift detector and write path for Codex and Claude packaged skill assets.

## 証拠

hops agent sync-packaged-skills --check --json ok=true with no missing/drifted/retired assets; uv run pytest tests/test_cli/test_agent.py -q passed; uv run pytest tests/test_agent_harness_contract.py -k packaged_agent_assets_match_repo_local_skills -q passed; manual eval harness-lab/views/eval-results/E0044-manual-score.yml.

## 回帰リスク

Low-to-moderate: the command only derives packaged hops-* assets from repo-local skills; intentional package-only experiments must not live under the mirrored hops-* asset tree.

## フォローアップ

Keep hops agent sync-packaged-skills --check --json in release/finalize validation so packaged Codex and Claude skills cannot drift silently.

## 回帰ガード

tests/test_cli/test_agent.py::test_agent_sync_packaged_skills_cli_check_reports_drift;tests/test_agent_harness_contract.py::test_packaged_agent_assets_match_repo_local_skills
