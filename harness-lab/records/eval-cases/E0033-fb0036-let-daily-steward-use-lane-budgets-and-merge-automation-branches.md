---
id: E0033
record_type: eval_case
created_at: '2026-05-14T01:48:55+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0036
---

# E0033: FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0033`
- observation: Daily steward currently treats max-systemic-candidates as a single global cap and the recommended prompt stops after pushing an automation branch. User feedback prefers lane-specific budgets, automatic merge when validation passes, optional develop/integration branch workflow, and no direct main push.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Document lane budgets, keep systemic candidates conservative, allow multiple metadata/backfill/read-only items, and update full automation guidance so validated automation branches can be merged into an authorized base or integration branch without direct protected-branch push.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0033 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
