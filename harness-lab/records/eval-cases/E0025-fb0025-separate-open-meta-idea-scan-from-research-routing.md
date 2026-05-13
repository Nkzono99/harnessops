---
id: E0025
record_type: eval_case
created_at: '2026-05-13T18:52:11+09:00'
status: active
capability: meta_improvement_research
failure_class: premature_research_routing
source_feedback: FB0025
---

# E0025: FB0025-separate-open-meta-idea-scan-from-research-routing を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0025-separate-open-meta-idea-scan-from-research-routing.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0025`
- observation: The broad prompt 'meta的な視点で改善案はある?' produces better divergent improvement ideas than the current hops-research-improvements skill because the skill starts with routing, evidence, and record-management constraints. HarnessOps needs a distinct invention lane that preserves open-ended structural critique before lab routing and selection.

## タスク

`meta_improvement_research` の `premature_research_routing` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Compare a normal broad meta prompt with hops-research-improvements on this repository; the broad prompt surfaces more structural design tensions, while the skill funnels toward recordable near-term candidates.

## 期待される挙動

Add a lightweight open-meta-scan skill that asks for raw divergent ideas without creating records, update hops-research-improvements to consume those raw ideas as the selection/routing lane, and guard packaged skills with contract tests.

## 合格基準

- `premature_research_routing` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0025 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `premature_research_routing` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
