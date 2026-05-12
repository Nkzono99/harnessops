---
id: H0010
record_type: hypothesis
created_at: '2026-05-13T00:50:34+09:00'
status: proposed
target_capability: improvement_loop_design
source_eval_case: E0010
---

# H0010: E0010-fb0010-redesign-standard-improvement-loop-around-investigation-and-themes の仮説

## 仮説

A theme-centered loop with explicit investigation, classification/routing, guard, and promotion semantics will make HarnessOps improvements easier to run consistently and easier to learn from later.

## メカニズム

Add structured dossier fields and CLI commands for recording investigation notes and classification metadata, revise the design principles to define each loop stage, and surface a theme view so agents see status, maturity, relations, guards, and promotion level as part of ordinary lab work.

## 最小実装

Add lab classify/investigate commands that update improvement dossiers, extend dossier frontmatter/body with source/maturity/relation/promotion/guard metadata, and update docs/specs/tests.

## 代替案: 削除または統合

Only rewrite docs/design-principles.md without changing CLI, leaving agents to remember the workflow manually.

## 期待される利点

The harness nudges agents from raw observations toward investigated themes, evaluated hypotheses, guarded adoption, and later benchmarkable experience instead of loose notes.

## 想定される欠点

More metadata can become process overhead if it is mandatory too early or if the dossier becomes the only source of truth.

## 評価計画

Create a lab record, generate a dossier, classify and investigate it, then verify docs, views, tests, doctor, and migrate all pass.

## 中止基準

If the commands duplicate existing FB/E/H/D source-of-truth records or make simple lab capture significantly heavier, keep only the docs change and reject the CLI layer.
