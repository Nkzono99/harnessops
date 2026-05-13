---
id: E0030
record_type: eval_case
created_at: '2026-05-13T23:51:09+09:00'
status: active
capability: repository_maintainability
failure_class: surface_sprawl
source_feedback: FB0031
---

# E0030: FB0031-simplify-harnessops-repository-surfaces を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0031-simplify-harnessops-repository-surfaces.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0030`
- observation: HarnessOps has grown through feature work: root plugin artifacts may no longer be part of the standard path, core modules mix workflow logic with small utility boundaries, harness-lab contains directories with weak or missing workflows, and docs/SPEC/README may not reflect recent CLI and uvx update-chain behavior. Clean up repo surfaces and improve maintainability without changing core behavior.

## タスク

`repository_maintainability` の `surface_sprawl` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Remove or retire obsolete plugin surfaces, add low-risk code organization boundaries, document current standard workflows, and record any lab layout cleanup as a deliberate migration path rather than ad hoc file moves.

## 合格基準

- `surface_sprawl` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0030 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `surface_sprawl` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
