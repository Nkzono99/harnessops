---
id: E0023
record_type: eval_case
created_at: '2026-05-13T17:59:46+09:00'
status: active
capability: harness_lab_traceability
failure_class: missing_lab_capture
source_feedback: FB0023
---

# E0023: FB0023-research-skill-scope-excludes-linked-target-and-project-repos を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0023-research-skill-scope-excludes-linked-target-and-project-repos.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0023`
- observation: The hops-research-improvements skill description says it is for HarnessOps meta improvements, which makes it sound like a HarnessOps-core-only tool even though repo-local skills are also deployed into linked target and project repositories. Agents in those repositories should be able to use the same research workflow for target/project harness improvements while preserving the correct lab versus feedback routing.

## タスク

`harness_lab_traceability` の `missing_lab_capture` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

The skill and packaged copies should explicitly support HarnessOps core, target repositories with harness-lab, and project repositories with harness-feedback, with guidance for routing research outputs through the right HOPS commands.

## 合格基準

- `missing_lab_capture` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0023 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `missing_lab_capture` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
