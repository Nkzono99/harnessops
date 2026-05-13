---
id: H0025
record_type: hypothesis
created_at: '2026-05-13T18:52:24+09:00'
status: proposed
target_capability: meta_improvement_research
source_eval_case: E0025
---

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
