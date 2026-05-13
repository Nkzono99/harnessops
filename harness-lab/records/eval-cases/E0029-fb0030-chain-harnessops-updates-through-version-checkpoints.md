---
id: E0029
record_type: eval_case
created_at: '2026-05-13T23:20:47+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0030
---

# E0029: FB0030-chain-harnessops-updates-through-version-checkpoints を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0030-chain-harnessops-updates-through-version-checkpoints.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0029`
- observation: uvx を標準導線にしたことで、target/project repo の update-harness は最新 PyPI runtime から開始できる。古い managed artifact への互換コードを永久に持つ代わりに、lock の harnessops_version から公開済み checkpoint を計画し、必要な版を uvx で順に呼び出す更新チェーンを追加する。

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

hops update-harness が chain plan/apply の導線を提供し、update skill が通常更新と段階更新を使い分けられるようになる。

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0029 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
