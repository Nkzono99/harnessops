---
id: H0027
record_type: hypothesis
created_at: '2026-05-13T22:07:37+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0027
---

# H0027: E0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos の仮説

## 仮説

Doctor should warn when a linked repo-local HarnessOps bridge tells agents to run an editable local hops fallback that the current target repo cannot provide.

## メカニズム

Scan generated HarnessOps bridge skill files during doctor, detect the stale editable fallback string, and compare it with the current repo's pyproject console scripts so target repos without a hops entrypoint get an actionable warning.

## 最小実装

Add a validation helper for stale bridge fallback text, wire it into doctor warnings, and cover a linked target fixture that lacks a hops console script.

## 代替案: 削除または統合

Do not add a new invocation command yet; the generated bridge already uses uvx, so the residual need is stale/invalid fallback detection.

## 期待される利点

Agents in target/project repos are steered back to update-harness or uvx instead of bypassing HOPS after an invalid fallback command.

## 想定される欠点

Doctor gains another text-based bridge check that must avoid false positives for HarnessOps development docs.

## 評価計画

Run a focused CLI test that rewrites a generated target bridge to the stale editable fallback and confirms doctor warns, plus contract tests and full repo validation.

## 中止基準

Reject if doctor warns on normal generated uvx bridge files or requires private local HarnessOps checkout paths to pass.
