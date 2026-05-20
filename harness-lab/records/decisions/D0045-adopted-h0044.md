---
id: D0045
record_type: decision
created_at: '2026-05-21T03:33:05+09:00'
status: adopted
source: H0044
evidence:
  summary: hops agent sync-packaged-skills --check --json ok=true with no missing/drifted/retired assets; uv run pytest tests/test_cli/test_agent.py -q passed; uv run pytest tests/test_agent_harness_contract.py -k packaged_agent_assets_match_repo_local_skills -q passed; manual eval harness-lab/views/eval-results/E0044-manual-score.yml.
  guard_path: tests/test_cli/test_agent.py::test_agent_sync_packaged_skills_cli_check_reports_drift;tests/test_agent_harness_contract.py::test_packaged_agent_assets_match_repo_local_skills
---

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
