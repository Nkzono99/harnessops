---
id: E0046
record_type: eval_case
created_at: '2026-05-22T03:39:16+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0044
---

# E0046: FB0044-steward-run-ledger-and-lane-result-validation を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0044-steward-run-ledger-and-lane-result-validation.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0046`
- observation: The redesigned daily automation now emits a supervisor_plan, but actual lane execution state still lives in agent prose. The supervisor can skip, repeat, or trust malformed lane reports without a durable machine-readable run ledger or lane result validation.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Add HOPS CLI support for starting a steward run ledger, recording lane results against the supervisor_plan contract, validating lane result JSON, and ending a run with auditable status.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0046 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
