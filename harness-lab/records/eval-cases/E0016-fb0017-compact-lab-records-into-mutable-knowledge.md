---
id: E0016
record_type: eval_case
created_at: '2026-05-13T02:52:59+09:00'
status: active
capability: lab_memory_compaction
failure_class: record_sprawl_without_knowledge_consolidation
source_feedback: FB0017
---

# E0016: FB0017-compact-lab-records-into-mutable-knowledge を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0017-compact-lab-records-into-mutable-knowledge.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0016`
- observation: As harness-lab grows, append-only records and generated dossiers will become too large to scan. The lab needs a compaction path that preserves canonical records while updating a smaller knowledge layer for reusable lessons, contradictions, guards, and promotion patterns.

## タスク

`lab_memory_compaction` の `record_sprawl_without_knowledge_consolidation` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Accumulate feedback, eval cases, hypotheses, decisions, manual scores, and dossiers until reviewing harness-lab requires reading many files instead of consulting a compiled knowledge surface.

## 期待される挙動

Provide a first-class lab compaction command that checks size thresholds, compiles source-linked mutable knowledge files, and leaves canonical records intact for audit and regeneration.

## 合格基準

- `record_sprawl_without_knowledge_consolidation` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0016 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `record_sprawl_without_knowledge_consolidation` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
