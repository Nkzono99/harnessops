---
id: E0041
record_type: eval_case
created_at: '2026-05-19T03:27:31+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0045
---

# E0041: FB0045-harness-lab-needs-forgetting-policy を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0045-harness-lab-needs-forgetting-policy.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0041`
- observation: Harness-lab currently supports recording, deterministic compaction, semantic abstraction, and source-linked extraction, but growth pressure will keep increasing because old low-signal records are never retired, archived, summarized away, or marked out of working memory.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Design a source-preserving forgetting lane that can mark stale local-only or superseded lab material as archived or excluded from active memory without destroying auditability.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0041 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
