---
id: E0017
record_type: eval_case
created_at: '2026-05-13T03:25:20+09:00'
status: active
capability: meta_improvement_research
failure_class: unstructured_research_scan_results
source_feedback: FB0013
---

# E0017: FB0013-structure-meta-improvement-research-scan-outputs を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0013-structure-meta-improvement-research-scan-outputs.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0017`
- observation: Dry-running the manual meta improvement research skill produced useful candidates, but the result exists only as prose in the agent response or as free-form investigation summaries. HarnessOps lacks a structured research-scan artifact or view for candidate, evidence, relation, recommendation, and next command.

## タスク

`meta_improvement_research` の `unstructured_research_scan_results` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Run hops-research-improvements against the current repository. The skill instructs the agent to output Scope, Evidence, Candidates, and Recommendation, but CLI support stops at lab investigate/classify/capture/propose.

## 期待される挙動

Add a lightweight structured research-scan record or command, for example a lab research/scan artifact that can hold candidates with evidence refs, relation, recommended action, and optional conversion to investigate/capture/propose.

## 合格基準

- `unstructured_research_scan_results` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0017 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `unstructured_research_scan_results` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
