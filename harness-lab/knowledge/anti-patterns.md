# Harness Lab Anti-Patterns

Updated: 2026-05-20T03:06:25+09:00
Source digest: `e755a800c8a0910e2e60dddae2f014a96211f47860e6e7278f9302a007ec36a3`

These are reusable failure shapes to avoid. Each item names source IDs so decisions can return to canonical records.

## Reporting Success While Leaving State Stale

- Avoid when: an update or doctor path says `ok` but leaves stale managed files, duplicate dossiers, stale generated views, or shadowed record IDs unresolved.
- Sources: `IMP0002`, `IMP0011`, `IMP0012`, `IMP0015`, `RS0002`, `IMP0016`, `IMP0029`, `IMP0030`
- Why it fails: operators trust the tool and stop looking, while the next agent inherits obsolete guidance or resolves an ID to the wrong artifact.
- Guard: report updated/unchanged/conflicted/stale counts, prefer canonical ID lookup, add doctor checks for duplicate canonical mappings, keep memory stale state visible, make repair commands cover the same generated artifacts that doctor validates, and keep update notices pointed at the recorded/current/latest version mismatch plus the uvx refresh path.

## Treating Counts As Health

- Avoid when: a steward, dashboard, or automation preflight reports only record counts and generic lane triggers while hiding stale memory, stale generated views, missing abstraction, guard gaps, or pending migration state.
- Sources: `IMP0023`, `IMP0029`, `RS0005`, `IMP0015`, `IMP0031`, `IMP0036`, `RS0006`
- Why it fails: counts prove that records exist, not that the lab is usable today; the next agent may skip librarian work even though the source digest has moved.
- Guard: expose read-only health signals such as `lab_health.status`, pressure triggers, stale snapshot/abstraction flags, recommended commands, and structured lane artifact contracts, then delegate compaction, abstraction, or consolidation to the proper lane; keep remote completion gates separate from intake and require validation/checks before merge.

## Ending Validated Automation At A Pushed Branch

- Avoid when: a scheduled run validates changes, pushes an automation branch, and then stops even though the prompt authorized PR creation and merge through the normal protected-branch path.
- Sources: `IMP0031`, `FB0037`, `FB0041`, `IMP0035`
- Why it fails: the work is neither merged nor clearly blocked, so the next run may repeat or stop on its own dirty/branch state instead of advancing a reviewed change; a merge method mismatch can strand an otherwise clean PR.
- Guard: after validation, fetch, confirm the merge target freshness, finalize onto the automation branch, push only that branch, open or update the PR, wait for required checks, choose a repository-compatible merge/squash/rebase method, merge only when allowed, and report whether the blocker is missing checks, failing checks, pending checks, conflicts, merge policy, or branch protection.

## Leaving Agent Handoff Paths Implicit

- Avoid when: AGENTS.md, CLAUDE.md, bridge skills, or update-harness output assume agents already know the valid `hops` invocation, repo role, and write path.
- Sources: `FB0042`, `IMP0030`, `FB0038`, `IMP0037`
- Why it fails: each target or project repo grows local conventions, agents may create lab state in project repos, and stale runtime/update guidance can mask the intended HarnessOps conduit.
- Guard: keep a compact role-scoped conduit in generated agent guidance, name the `hops` or `uvx --from harnessops hops` path, point stale-version work to explicit update/doctor/migrate commands, preserve canonical HarnessOps state while ignoring only transient cache files, and use global/local storage for ordinary repositories that should not commit HarnessOps working state.

## Treating No-Op As Daily Success

- Avoid when: a clean autonomous run with remote authority reports only preflight/doctor state because no obvious reactive work was waiting.
- Sources: `FB0037`, `FB0038`, `IMP0034`, `FB0050`, `IMP0036`, `RS0006`
- Why it fails: healthy repositories slowly train the automation into status polling, and hidden or prose-only open scans make raw ideas disappear before invention can review or record them; unbounded creation of new records raises lab pressure without retiring work.
- Guard: make proactive discovery mandatory when reactive work and queue are thin, keep `hops-open-meta-scan` as its own supervisor lane, preserve raw ideas as structured lane artifacts, split record/implementation/merge gates, handle latest/update-harness only when stale state is signaled, prefer consolidation through existing records before new captures, and reserve no-op for blockers, failed validation, exhausted budget, or explicit discovery failure.

## Dirtying Ordinary Repositories With Local HarnessOps State

- Avoid when: a repository only needs local development feedback or shared agent state, but HarnessOps writes `.harnessops`, `harness-feedback`, or `harness-lab` files into that project.
- Sources: `IMP0037`
- Why it fails: normal repositories inherit dirty-worktree blockers and may accidentally publish local-only feedback or lab context.
- Guard: use the global registry, `storage=local`, HOPS_HOME-backed exports, and the packaged global Codex plugin for local share-state workflows; keep repo-local overlays for repos that explicitly opt into canonical HarnessOps state.

## Tracking Runtime Cache As Project State

- Avoid when: transient files under `.harnessops/cache/` or future HarnessOps tmp paths are left to appear as normal untracked project changes.
- Sources: `FB0038`
- Why it fails: cache churn can stop dirty-worktree automation and hides the difference between canonical HarnessOps state and local runtime state.
- Guard: init/link/update-harness should maintain a marker-managed `.gitignore` block that ignores cache contents while preserving `.harnessops/cache/.gitkeep`.

## Manual Packaged Skill Sync

- Avoid when: repo-local HOPS skills are edited and then copied by hand into packaged Codex/Claude asset directories.
- Sources: `IMP0039`
- Why it fails: one host or a retired skill can drift silently, and tests that touch only one packaged host may still pass.
- Guard: use `hops agent sync-packaged-skills --check` before validation and normal `hops agent sync-packaged-skills` to update both packaged hosts.

## Compacting Without Reducing Active Memory

- Avoid when: lab memory lint stays under file-count pressure after deterministic snapshot and semantic abstraction are fresh.
- Sources: `IMP0038`, `RS0006`
- Why it fails: another abstraction pass can update the digest while leaving stale or superseded material in the active queue and working memory.
- Guard: use source-preserving retirement or active-memory exclusion for stale local-only or superseded records, and prefer consolidation through existing FB/IMP/RS items before creating more queue roots.

## Treating Boilerplate As Evidence

- Avoid when: generated dossier sections embed unfilled eval-case templates, generic headings, or thin scaffolding as if they were review signal.
- Sources: `IMP0003`, `IMP0013`
- Why it fails: the real manual evaluation and decision are buried, and reviewers learn to ignore lab records.
- Guard: summarize eval records and manual scores; keep full templates in canonical records only when they add source-specific content.

## Letting Meta Work Become Idea Spam

- Avoid when: every interesting thought becomes a new scan, feedback item, skill, or memory rule without a trigger, source, candidate recommendation, or next command.
- Sources: `IMP0007`, `IMP0008`, `IMP0009`, `RS0001`, `IMP0014`, `IMP0015`
- Why it fails: the lab becomes larger without becoming more predictive or easier to act on.
- Guard: separate bounded in-task meta scans from deliberate research scans, record candidate relation/recommendation, and compact only to source-linked abstractions.

## Promoting Local Context Remotely Without Sanitation

- Avoid when: lab-first records, issue imports, external evidence, or feedback bundles are copied into remote issues without explicit sanitation and encoding checks.
- Sources: `IMP0004`, `IMP0005`, `IMP0008`, `IMP0014`
- Why it fails: private paths or research context can leak, and Unicode can be corrupted before the record is even parsed.
- Guard: use UTF-8 subprocess decoding, run sanitizer paths before external sharing, require explicit remote-create confirmation, and keep privacy risk visible in evaluation.

## Acting On Issues Without Authority Or Record Routing

- Avoid when: an agent closes, comments on, labels, imports, or implements from GitHub issues before checking remote-action authority and deciding which HOPS record path owns the work.
- Sources: `IMP0032`, `IMP0023`, `IMP0004`
- Why it fails: issue triage becomes target-specific operational behavior instead of audited HarnessOps memory, and remote changes can bypass the prompt's authority boundary.
- Guard: default no-argument triage to a read/report step, include `remote_action_allowed` in the triage report, import or capture durable work before implementation, and close issues only with validation plus related PR/commit evidence.

## Replacing Canonical Records With Summaries

- Avoid when: compact memory, generated dossiers, or research summaries are treated as adoption evidence instead of pointers back to source records.
- Sources: `IMP0012`, `IMP0014`, `IMP0015`
- Why it fails: source digest, contradictions, and low-level guards disappear, so future decisions cannot audit how an abstraction was formed.
- Guard: keep source IDs on every abstraction, keep `lab-memory-abstraction.yml` aligned to the input digest, and use canonical lookup before broad overlay scans.

## Solving Workflow Gaps With Force Modes Only

- Avoid when: the only answer to stale managed files, migration friction, or generated output drift is an unconditional overwrite.
- Sources: `IMP0002`, `IMP0006`
- Why it fails: force can refresh packaged state, but it cannot distinguish unmodified stale content from meaningful local edits or explain the migration path.
- Guard: add conflict-aware refresh behavior, explicit migration/update commands, and test-visible output that names what changed.
