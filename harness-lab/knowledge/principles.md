# Harness Lab Principles

Updated: 2026-05-20T03:06:25+09:00
Source digest: `e755a800c8a0910e2e60dddae2f014a96211f47860e6e7278f9302a007ec36a3`

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
- Sources: `IMP0002`, `IMP0011`, `IMP0016`, `RS0002`, `IMP0030`, `FB0038`, `IMP0039`
- Applies when: refreshing agent bridge files, generated records, generated views, update guidance, or any managed file that users may edit.
- Counterexamples: reporting `ok` while leaving stale skills in place; concurrent lab commands creating duplicate dossiers for one source feedback; a repair command that refreshes only dynamic generated views while doctor still warns on other managed artifacts; an update notice that compares only one version pair and omits the recommended `uvx --refresh-package` path; generated cache files appearing as untracked repo noise; manually copying repo-local skills to packaged agent assets and missing one host.
- Guard: store packaged hashes or source-feedback locks where needed, write `.new` on local conflicts, have doctor detect duplicate canonical mappings, make refresh commands cover the same managed artifact set that doctor validates, keep update notices tied to recorded/current/latest version checks plus explicit migrate/doctor follow-up, maintain a marker-managed `.gitignore` block for HarnessOps transient paths, and provide `--check` commands for repeated package-sync work.

## Remote And External Paths Must Be Encoding-Safe And Sanitized

- Principle: remote issue import/export and external evidence workflows must preserve Unicode, minimize private context leakage, and make sanitation explicit before remote creation.
- Sources: `IMP0004`, `IMP0005`, `IMP0008`, `IMP0014`
- Applies when: importing GitHub issues, drafting lab-first issues, creating remote issues, citing external benchmarks, or exporting project feedback.
- Counterexamples: Windows console decoding can corrupt `gh` JSON; lab-first issue creation can leak unsanitized body text if the remote path bypasses the sanitizer.
- Guard: decode `gh` JSON as UTF-8, require confirmation for remote issue creation, keep privacy risk as an evaluation axis, and retain evidence refs without copying private project context into knowledge files.

## Issue Triage Needs Explicit Intake, Routing, And Authority

- Principle: issue triage should be a reusable HarnessOps lane that discovers open issues when no issue is named, reports priority and missing information, routes durable work through lab or feedback records, and performs remote actions only when the prompt or human explicitly authorizes them.
- Sources: `IMP0023`, `IMP0032`, `IMP0004`, `IMP0005`
- Applies when: daily steward runs without a specific issue, importing GitHub issues, deciding whether to close spam/unrelated items, or replacing repo-local triage prompts in target repositories.
- Counterexamples: target-specific triage prompts drift from HarnessOps guidance; a no-argument run that skips open issue discovery; closing or commenting on issues because a skill suggested it but the run lacks remote-action authority.
- Guard: `hops-issue-triage` reports priority buckets, evidence, missing info, recommended HOPS action, and remote-action authorization; issue changes flow through `hops feedback import` or project feedback export/import paths before implementation; close comments name validation and related PR/commit evidence.

## Memory Compaction Separates Triggering From Abstraction

- Principle: cheap deterministic snapshots should answer whether and where to compact; agent-guided abstraction should decide what durable principle, pattern, anti-pattern, or evaluation rule survives.
- Sources: `IMP0014`, `IMP0015`, `IMP0038`
- Applies when: lab size grows, source digest changes, targets are missing or stale, or a human manually asks for memory compaction.
- Counterexamples: replacing deterministic snapshots with free-form skill memory loses digest checks; treating snapshots as semantic memory loses contradiction handling; repeatedly refreshing abstraction does not reduce active file-count pressure when old low-signal records should be retired or excluded from working memory.
- Guard: run lint/prepare, read the input bundle and source records, update abstract outputs with source IDs, then set `lab-memory-abstraction.yml` to the input source digest; when pressure remains after fresh abstraction, route source-preserving retirement or active-memory exclusion instead of deleting records.

## Deterministic Intake Should Surface Actionable Health, Not Decide The Work

- Principle: scheduled or recurring intake commands should expose read-only health signals that affect routing, while leaving synthesis, abstraction, and implementation to the appropriate lane or skill.
- Sources: `IMP0023`, `IMP0029`, `RS0005`, `IMP0015`, `IMP0031`, `IMP0036`, `RS0006`
- Applies when: adding daily steward preflight fields, lane triggers, lab health summaries, stale memory checks, automation run ledgers, or branch/merge completion rules.
- Counterexamples: overlay counts alone can trigger a vague librarian lane while hiding stale snapshot or semantic-memory state; a preflight that writes memory or ranks every candidate would turn deterministic intake into a workflow engine; a scheduled run that pushes a branch but never attempts the authorized PR/merge path leaves validated work half-finished; prose-only lane artifacts make downstream lanes infer result shape from wording.
- Guard: keep preflight read-only, include source-linked `lab_health` status and recommended commands for lab repos, skip lab memory probing in project repos, route `needs-abstraction` to `hops-compact-lab-memory`, expose machine-checkable lane artifact contracts where downstream lanes consume them, prefer consolidation through existing records before new captures, and require validation plus protected-branch checks before automation merges.

## Automation Should Finish Through Reviewable Branch Paths

- Principle: unattended steward work should use explicit lane budgets and complete validated changes through an automation branch and PR/merge path, not direct protected-branch pushes or unbounded backlog processing.
- Sources: `IMP0023`, `IMP0031`, `FB0037`, `FB0041`, `IMP0035`
- Applies when: daily steward prompts, repo-local skills, packaged skills, or automation docs describe remote writes, branch targets, PR updates, merges, or lane scope.
- Counterexamples: treating `max-systemic-candidates` as the only cap ignores lightweight metadata/read-only work; stopping after push leaves completed work pending forever; direct main pushes bypass branch protection; merging logic that cannot distinguish missing required checks from failing checks gives operators no actionable branch-protection path; assuming merge commits are allowed blocks repositories that intentionally require squash or rebase.
- Guard: separate systemic candidates, metadata/guard backfills, and read-only decisions; push only the automation branch; confirm validation, target freshness, required checks, branch protection, and repository-compatible merge method before merge; keep a real PR CI workflow available for branch protection; report missing-check and failing-check blockers separately without force-pushing.

## Agent Guidance Should Encode The Minimal Role-Specific HarnessOps Path

- Principle: generated agent instructions should give agents the shortest valid `hops` invocation and route writes by repository role, so a target/meta repo uses lab/GitHub Flow while a project repo uses feedback export/import paths.
- Sources: `FB0042`, `IMP0030`, `FB0038`, `IMP0037`
- Applies when: updating AGENTS.md, CLAUDE.md, packaged skills, bridge instructions, or update-harness diagnostics that tell agents how to operate in linked repositories.
- Counterexamples: a bridge skill mentions HarnessOps but omits the actual `hops` or `uvx --from harnessops hops` path; project-repo guidance implies creating `harness-lab/`; broad ignore/update guidance hides canonical `.harnessops` state; ordinary repositories get dirtied by local HarnessOps development state when a global/local storage path would preserve the workflow.
- Guard: keep the conduit compact, role-aware, and contract-tested; preserve canonical `.harnessops` files while ignoring only transient cache state; route local-only project state through the global registry and HOPS_HOME storage when appropriate; pair update notices with explicit doctor/migrate follow-up rather than implicit migration.

## Steward Automation Needs Discovery Pressure

- Principle: a clean autonomous steward run should create or advance a queue instead of treating status-only no-op as success.
- Sources: `FB0037`, `FB0038`, `IMP0023`, `IMP0031`, `IMP0034`, `FB0050`, `IMP0036`, `RS0006`
- Applies when: configuring daily automation, deciding whether to run `hops-open-meta-scan`, splitting record/implementation/merge gates, setting work-packet budgets, or handling update-harness/latest-version work.
- Counterexamples: gating open invention to rare triggers leaves healthy repositories in preflight/doctor/no-op loops; hiding open meta scan inside invention makes raw ideas invisible to the supervisor ledger; leaving raw ideas in prose-only lane results makes downstream invention depend on formatting; requiring implementation-level guards before research-scan or classify prevents queue creation; rewarding new records faster than retiring, merging, rejecting, or testing them increases lab pressure.
- Guard: use global, record, implementation, and merge gates separately; run proactive discovery when reactive work and queue are thin; make `open-meta-scan` an explicit lane whose raw ideas are reviewed by invention before priority work; preserve raw ideas as structured lane artifacts; treat HarnessOps latest/update-harness as signal-driven work instead of a mandatory start step; control execution by risk tier and work-packet budget rather than one systemic-candidate cap; route invention through consolidation-first review of existing FB/IMP/RS items before capturing new work.
