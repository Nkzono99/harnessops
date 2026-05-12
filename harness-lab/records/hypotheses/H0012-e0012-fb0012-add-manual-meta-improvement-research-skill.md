---
id: H0012
record_type: hypothesis
created_at: '2026-05-13T01:43:56+09:00'
status: proposed
target_capability: meta_improvement_research
source_eval_case: E0012
---

# H0012: E0012-fb0012-add-manual-meta-improvement-research-skill の仮説

## 仮説

A dedicated hops-research-improvements skill will make meta-level improvement discovery deliberate and evidence-backed without overloading the short in-task meta scan.

## メカニズム

The skill separates research mode from execution mode, requiring codebase review, existing dossier checks, external primary-source comparison when useful, candidate classification, and explicit lab commands for note/capture/propose outcomes.

## 最小実装

Add repo-local and packaged hops-research-improvements skills, document when to use the manual research lane, and guard packaging through contract tests.

## 代替案: 削除または統合

Fold the behavior into hops-run-lab only, but that makes ordinary lab work heavier and blurs short meta scans with deliberate research.

## 期待される利点

Agents can intentionally search for second-order improvements, compare against external practices, and turn only high-signal findings into HarnessOps lab records.

## 想定される欠点

Another skill can add surface area if its trigger is too broad or if it encourages speculative idea spam.

## 評価計画

Verify the skill is repo-local, packaged for Codex and Claude, mirrored into agent assets, references codebase and web research, and routes outputs through hops lab investigate/classify/capture/propose.

## 中止基準

If the skill cannot be distinguished from hops-run-lab or lacks tests that keep it packaged and lab-routed, reject or merge it back into hops-run-lab.
