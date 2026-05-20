---
id: H0044
record_type: hypothesis
created_at: '2026-05-21T03:32:06+09:00'
status: proposed
target_capability: agent_asset_packaging
source_eval_case: E0044
---

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
