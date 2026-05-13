# Harness Lab Principles

Updated: 2026-05-14T01:10:08+09:00
Source digest: `b52b8f6c8c026009c5e0cef42f497c2e8e85d0ab89754ea9da3298b6b2f7d823`

This file is mutable abstract knowledge. It is not adoption evidence. For decisions, return to the source records and dossiers named below.

## Canonical Records Stay Authoritative

- Principle: generated views, dossiers, snapshots, and memory files are navigation and working-memory layers; the canonical records remain the audit path for feedback, evaluation, hypotheses, decisions, and research scans.
- Sources: `IMP0003`, `IMP0012`, `IMP0014`, `IMP0015`
- Applies when: adding generated views, lookup helpers, compact memory, summaries, or convenience workflows.
- Counterexamples: a generated eval-result view shadowed canonical eval-case lookup; deterministic snapshots can look authoritative if the semantic-abstraction boundary is unclear.
- Guard: prefer canonical record directories for ID lookup, keep source digests on memory artifacts, and treat compact memory as an index back to source IDs.

## Nontrivial HarnessOps Changes Need A Lab Trail

- Principle: substantial HarnessOps behavior changes should start or quickly converge on captured feedback, an evaluation case, a hypothesis, a decision, and an explicit guard.
- Sources: `IMP0001`, `IMP0006`
- Applies when: changing CLI behavior, bridge behavior, skill guidance, release behavior, lab schema, or protocol-level workflow.
- Counterexamples: small mechanical edits or generated refreshes may not need new source records unless they change behavior or reveal a reusable failure class.
- Guard: release and agent guidance should keep `hops lab capture` visible, and tests should exercise capture/eval conversion for the core loop.

## Improvement Work Needs Investigation, Classification, And Promotion State

- Principle: observations become useful memory only after the loop names the failure class, investigates mechanisms, classifies relation/maturity, evaluates a hypothesis, records a decision, and states promotion level.
- Sources: `IMP0006`, `IMP0007`, `IMP0008`, `IMP0009`, `RS0001`
- Applies when: an idea may generalize across repositories, skills, migration policy, evaluation design, or HarnessOps protocol.
- Counterexamples: overly broad triggers turn improvement work into speculative idea spam; free-form research results become hard to route.
- Guard: use bounded meta-scan checkpoints for in-task observations, and use research-scan records for deliberate multi-candidate research before routing candidates downstream.

## Readers Should See Signal Before Boilerplate

- Principle: review surfaces should summarize the current decision, source observation, evaluation result, evidence, and guard before exposing record scaffolding.
- Sources: `IMP0003`, `IMP0013`, `IMP0014`
- Applies when: rendering dossiers, score views, generated docs, or memory bundles.
- Counterexamples: embedding full eval-case templates in dossiers makes the real manual score harder to find; spreading one improvement across many thin files raises bookkeeping cost.
- Guard: keep generated dossiers and memory files concise, source-linked, and regenerable while preserving the canonical record trail.

## Managed Artifacts Must Be Honest About Staleness And Local Edits

- Principle: update commands for managed bridge or generated artifacts must distinguish unchanged, updated, conflicted, stale, and locally edited states.
- Sources: `IMP0002`, `IMP0011`, `IMP0016`, `RS0002`
- Applies when: refreshing agent bridge files, generated records, generated views, or any managed file that users may edit.
- Counterexamples: reporting `ok` while leaving stale skills in place; concurrent lab commands creating duplicate dossiers for one source feedback; a repair command that refreshes only dynamic generated views while doctor still warns on other managed artifacts.
- Guard: store packaged hashes or source-feedback locks where needed, write `.new` on local conflicts, have doctor detect duplicate canonical mappings, and make refresh commands cover the same managed artifact set that doctor validates.

## Remote And External Paths Must Be Encoding-Safe And Sanitized

- Principle: remote issue import/export and external evidence workflows must preserve Unicode, minimize private context leakage, and make sanitation explicit before remote creation.
- Sources: `IMP0004`, `IMP0005`, `IMP0008`, `IMP0014`
- Applies when: importing GitHub issues, drafting lab-first issues, creating remote issues, citing external benchmarks, or exporting project feedback.
- Counterexamples: Windows console decoding can corrupt `gh` JSON; lab-first issue creation can leak unsanitized body text if the remote path bypasses the sanitizer.
- Guard: decode `gh` JSON as UTF-8, require confirmation for remote issue creation, keep privacy risk as an evaluation axis, and retain evidence refs without copying private project context into knowledge files.

## Memory Compaction Separates Triggering From Abstraction

- Principle: cheap deterministic snapshots should answer whether and where to compact; agent-guided abstraction should decide what durable principle, pattern, anti-pattern, or evaluation rule survives.
- Sources: `IMP0014`, `IMP0015`
- Applies when: lab size grows, source digest changes, targets are missing or stale, or a human manually asks for memory compaction.
- Counterexamples: replacing deterministic snapshots with free-form skill memory loses digest checks; treating snapshots as semantic memory loses contradiction handling.
- Guard: run lint/prepare, read the input bundle and source records, update abstract outputs with source IDs, then set `lab-memory-abstraction.yml` to the input source digest.

## Deterministic Intake Should Surface Actionable Health, Not Decide The Work

- Principle: scheduled or recurring intake commands should expose read-only health signals that affect routing, while leaving synthesis, abstraction, and implementation to the appropriate lane or skill.
- Sources: `IMP0023`, `IMP0029`, `RS0005`, `IMP0015`
- Applies when: adding daily steward preflight fields, lane triggers, lab health summaries, stale memory checks, or automation run ledgers.
- Counterexamples: overlay counts alone can trigger a vague librarian lane while hiding stale snapshot or semantic-memory state; a preflight that writes memory or ranks every candidate would turn deterministic intake into a workflow engine.
- Guard: keep preflight read-only, include source-linked `lab_health` status and recommended commands for lab repos, skip lab memory probing in project repos, and route `needs-abstraction` to `hops-compact-lab-memory`.
