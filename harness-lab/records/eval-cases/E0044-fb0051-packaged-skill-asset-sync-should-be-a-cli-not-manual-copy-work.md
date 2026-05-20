---
id: E0044
record_type: eval_case
created_at: '2026-05-21T03:31:54+09:00'
status: active
capability: agent_asset_packaging
failure_class: manual_packaged_skill_sync_drift
source_feedback: FB0051
---

# E0044: FB0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0051-packaged-skill-asset-sync-should-be-a-cli-not-manual-copy-work.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0044`
- observation: Updating repo-local HOPS skills requires keeping packaged Codex and Claude assets in lockstep. Manual copy work already left Claude assets drifted, so routine sync and CI-style drift detection should be owned by a HOPS CLI command.

## タスク

`agent_asset_packaging` の `manual_packaged_skill_sync_drift` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Edit a repo-local skill, run the old manual copy workflow, and observe that one host can drift. The new hops agent sync-packaged-skills --check detects the drift.

## 期待される挙動

Provide a command that syncs .agents/skills/hops-* into packaged agent assets for codex and claude, with a --check mode that detects missing, drifted, or retired skills without writing.

## 合格基準

- `manual_packaged_skill_sync_drift` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0044 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `manual_packaged_skill_sync_drift` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
