---
id: H0001
record_type: hypothesis
created_at: '2026-05-12T13:55:13+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0001
---

# H0001: E0001-fb0001-harnessops-improvements-lacked-lab-trace の仮説

## 仮説

A first-class lab capture command plus agent and release guidance will make local HarnessOps improvements traceable before release.

## メカニズム

The command creates an FB record directly from local observations without requiring an external issue or sanitized bundle, and the skills/docs remind agents to use it.

## 最小実装

Add hops lab capture, tests, documentation, repo-local skill guidance, and release-skill checks.

## 代替案: 削除または統合

Require a GitHub issue or manual record creation before every HarnessOps improvement.

## 期待される利点

Nontrivial HarnessOps changes have an explicit feedback, eval, hypothesis, and decision trail.

## 想定される欠点

Small changes may feel like they carry extra record-keeping overhead.

## 評価計画

Exercise lab capture in CLI tests, assert skill/docs mention it, run full pytest and doctor with record validation.

## 中止基準

If agents still bypass lab records or the command creates low-value noise, simplify the trigger rule or add a stronger release gate.
