---
id: E0033
record_type: eval_case
created_at: '2026-05-14T01:27:31+09:00'
status: active
capability: uvx_update_guidance
failure_class: stale_hops_update_path
source_feedback: FB0028
---

# E0033: FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0028-make-update-notices-guide-uvx-based-harnessops-upgrades.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0033`
- observation: Target and project repositories need a single update path when repo-managed HarnessOps artifacts, the currently running hops runtime, and the latest PyPI release differ. The existing notice only compares the repo lock with the current runtime and still points agents at the hops-update-harness skill or bare hops command.

## タスク

`uvx_update_guidance` の `stale_hops_update_path` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Update the CLI notice so ordinary hops usage in linked repos compares recorded, current, and latest PyPI HarnessOps versions when available, emits uvx --refresh-package harnessops --from harnessops hops update-harness guidance, and keeps migration application behind an explicit follow-up check.

## 合格基準

- `stale_hops_update_path` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0033 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `stale_hops_update_path` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
