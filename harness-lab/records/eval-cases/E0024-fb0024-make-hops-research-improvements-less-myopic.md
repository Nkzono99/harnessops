---
id: E0024
record_type: eval_case
created_at: '2026-05-13T18:22:30+09:00'
status: active
capability: unclassified
failure_class: unclassified
source_feedback: FB0024
---

# E0024: FB0024-make-hops-research-improvements-less-myopic を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0024-make-hops-research-improvements-less-myopic.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0024`
- observation: GitHub issue: https://github.com/Nkzono99/harnessops/issues/11
author: Nkzono99
labels: enhancement
created_at: 2026-05-13T09:17:09Z
updated_at: 2026-05-13T09:17:09Z

## タスク

`unclassified` の `unclassified` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

送信元フィードバックバンドルを参照してください。

## 期待される挙動

送信元フィードバックバンドルを参照してください。

## 合格基準

- `unclassified` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0024 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `unclassified` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
