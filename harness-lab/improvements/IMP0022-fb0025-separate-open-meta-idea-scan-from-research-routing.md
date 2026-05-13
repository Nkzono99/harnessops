---
id: IMP0022
record_type: improvement_dossier
created_at: '2026-05-13T18:53:09+09:00'
updated_at: '2026-05-13T18:53:20+09:00'
status: adopted
source_type: user-strategy
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0025
eval_cases:
- E0025
hypotheses:
- H0025
decisions:
- D0026
research_scans: []
classification:
  capability: meta_improvement_research
  failure_class: premature_research_routing
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py
investigation: []
links:
  issue_url:
---

# IMP0022: FB0025: Separate open meta idea scan from research routing

## Status

- status: adopted
- maturity: adopted
- source_type: user-strategy
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0025`
- linked_records: `FB0025`, `E0025`, `H0025`, `D0026`

## Source Observation

Source: `harness-lab/records/feedback/FB0025-separate-open-meta-idea-scan-from-research-routing.md`

# FB0025: Separate open meta idea scan from research routing

## 概要

The broad prompt 'meta的な視点で改善案はある?' produces better divergent improvement ideas than the current hops-research-improvements skill because the skill starts with routing, evidence, and record-management constraints. HarnessOps needs a distinct invention lane that preserves open-ended structural critique before lab routing and selection.

## 再現

Compare a normal broad meta prompt with hops-research-improvements on this repository; the broad prompt surfaces more structural design tensions, while the skill funnels toward recordable near-term candidates.

## 期待する上流変更

Add a lightweight open-meta-scan skill that asks for raw divergent ideas without creating records, update hops-research-improvements to consume those raw ideas as the selection/routing lane, and guard packaged skills with contract tests.

## Target Capability

- capability: meta_improvement_research
- failure_class: premature_research_routing

## Investigation

調査メモはまだありません。

## Research Scans

research scan はまだありません。


## Evaluation

### E0025: E0025: FB0025-separate-open-meta-idea-scan-from-research-routing を評価


- source: `harness-lab/records/eval-cases/E0025-fb0025-separate-open-meta-idea-scan-from-research-routing.md`

- capability: meta_improvement_research

- failure_class: premature_research_routing

- manual_eval_yml: `harness-lab/views/eval-results/E0025-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0025-manual-score.md`
- scores: impact=5, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=2, anti_theater=5, maintainability=4, privacy_sanitization_risk=1
- notes: Implemented a separate open invention lane: hops-open-meta-scan now produces Raw Ideas, Counterframes, Routing Hints, and Do Not Record Yet without default lab writes; hops-research-improvements now explicitly acts as the downstream selection/routing lane. Repo-local, Codex/Claude plugin, and packaged asset copies are synchronized and guarded by contract tests.


## Hypotheses

### H0025: H0025: E0025-fb0025-separate-open-meta-idea-scan-from-research-routing の仮説


Source: `harness-lab/records/hypotheses/H0025-e0025-fb0025-separate-open-meta-idea-scan-from-research-routing.md`


# H0025: E0025-fb0025-separate-open-meta-idea-scan-from-research-routing の仮説

## 仮説

Separating open divergent idea generation from research routing will preserve broad structural critique while keeping HarnessOps evidence, privacy, and lab-selection discipline in the downstream lane.

## メカニズム

A lightweight hops-open-meta-scan skill produces Raw Ideas and Counterframes without creating records, while hops-research-improvements explicitly consumes those ideas later for evidence, relation, park/reject, and lab workflow routing.

## 最小実装

Add repo-local and packaged hops-open-meta-scan skills; update hops-research-improvements to reference open scan as the pre-routing invention lane; add contract tests and docs for the separation.

## 代替案: 削除または統合

Keep one combined research skill, but that repeats the failure mode: management constraints shape the first-pass ideas. Folding into hops-run-lab would make ordinary lab work heavier.

## 期待される利点

Agents can get the broad-prompt advantage before HarnessOps narrows candidates into records, reducing premature routing and improving novelty/diversity of meta-improvement ideas.

## 想定される欠点

Another skill adds surface area, and agents may overuse open scans if triggers are too broad.

## 評価計画

Verify repo-local, plugin, and packaged asset skills are in sync; assert the open skill does not default to lab capture; assert research skill points to open scan and selection/routing lane; run contract tests, ruff, doctor, and migrate.

## 中止基準

Reject or merge back if the open skill starts creating records by default, duplicates research routing behavior, or lacks packaging guards.


## Evidence

`harness-lab/views/eval-results/E0025-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0026: D0026: adopted H0025


Source: `harness-lab/records/decisions/D0026-adopted-h0025.md`


# D0026: adopted H0025

## 判断

adopted

## 理由

The implementation separates divergent meta-idea generation from evidence/routing workflow while preserving HarnessOps safety and packaging guarantees.

## 証拠

Added hops-open-meta-scan across repo-local, Codex/Claude plugins, and packaged assets; updated hops-research-improvements and docs; uv run pytest tests/test_agent_harness_contract.py; uv run ruff check tests/test_agent_harness_contract.py; hops doctor --check-overlay --check-records; manual eval E0025.

## 回帰リスク

Low to moderate. A new skill adds trigger surface, but it explicitly avoids default lab writes and is paired with downstream research routing.

## フォローアップ

Forward-test the open scan against a broad meta-improvement prompt and compare novelty/diversity with the research routing skill.

## 回帰ガード

tests/test_agent_harness_contract.py
