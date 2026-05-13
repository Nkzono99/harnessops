---
id: E0031
record_type: eval_case
created_at: '2026-05-14T00:10:36+09:00'
status: active
capability: repository_maintainability
failure_class: records_module_sprawl
source_feedback: FB0032
---

# E0031: FB0032-split-record-core-modules-by-responsibility を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0032-split-record-core-modules-by-responsibility.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0031`
- observation: records.py has become the central maintainability hotspot: it mixes record type constants, frontmatter IO, ID/path indexing, feedback/eval/hypothesis/decision creation, research scan parsing, and improvement dossier aggregation/mutation. Split these responsibilities into focused modules while keeping harnessops.core.records as a compatibility facade.

## タスク

`repository_maintainability` の `records_module_sprawl` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Introduce record_types.py, record_io.py, record_index.py, lab_records.py, and improvement_dossier.py; preserve current imports and behavior; update tests/docs only where the new structure needs a contract.

## 合格基準

- `records_module_sprawl` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0031 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `records_module_sprawl` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
