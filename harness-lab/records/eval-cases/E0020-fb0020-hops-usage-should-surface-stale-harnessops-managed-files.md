---
id: E0020
record_type: eval_case
created_at: '2026-05-13T17:01:41+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0020
---

# E0020: FB0020-hops-usage-should-surface-stale-harnessops-managed-files を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0020-hops-usage-should-surface-stale-harnessops-managed-files.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0020`
- observation: After a HarnessOps release, linked repositories can keep older generated skills or managed artifacts until update-harness runs. Users may keep using hops without noticing that update-harness should be applied.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

When a linked repository is used with a newer hops version than the recorded lock state, hops should emit a low-noise notice that points the user or agent to the hops-update-harness skill / hops update-harness.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0020 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
