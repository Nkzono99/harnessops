---
id: E0038
record_type: eval_case
created_at: '2026-05-17T09:44:04+09:00'
status: active
capability: daily_steward_orchestration
failure_class: nested_open_scan_not_delegated
source_feedback: FB0049
---

# E0038: FB0049-daily-steward-should-delegate-open-meta-scan を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0049-daily-steward-should-delegate-open-meta-scan.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0038`
- observation: Daily steward supervisor currently lists invention as one lane; hops-open-meta-scan is only nested inside invention guidance, so the supervisor does not spawn a dedicated open-meta-scan subagent or make its raw ideas an explicit handoff into routing and priority work.

## タスク

`daily_steward_orchestration` の `nested_open_scan_not_delegated` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Run hops steward preflight --json and inspect supervisor_plan.lanes: hops-open-meta-scan is not a lane even though hops-invention-steward mentions it.

## 期待される挙動

Add an explicit open-meta-scan supervisor lane using hops-open-meta-scan, then make invention review the raw ideas and record selected candidates so priority-improvement-steward can pick them up.

## 合格基準

- `nested_open_scan_not_delegated` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0038 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `nested_open_scan_not_delegated` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
