---
id: E0022
record_type: eval_case
created_at: '2026-05-13T17:55:00+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0022
---

# E0022: FB0022-release-workflow-uses-node20-action-majors を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0022-release-workflow-uses-node20-action-majors.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0022`
- observation: The v0.1.4 PyPI publish workflow succeeded but GitHub Actions annotated the run because actions/checkout@v4 and actions/setup-python@v5 still run on Node.js 20. GitHub plans Node24 default migration on 2026-06-02, so the release workflow should use Node24-ready action majors before this becomes release friction.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

The PyPI publish workflow should use Node24-ready action majors and a regression test should guard against reintroducing Node20-era checkout/setup-python majors.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0022 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
