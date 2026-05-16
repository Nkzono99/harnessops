# Harness Lab Anti-Patterns

Updated: 2026-05-17T04:09:04+09:00
Source digest: `af9f230bf6b55e4f02ef4ba21d14c3914e0d519cfa33809ca0a9f8599de63f38`

These are reusable failure shapes to avoid. Each item names source IDs so decisions can return to canonical records.

## Reporting Success While Leaving State Stale

- Avoid when: an update or doctor path says `ok` but leaves stale managed files, duplicate dossiers, stale generated views, or shadowed record IDs unresolved.
- Sources: `IMP0002`, `IMP0011`, `IMP0012`, `IMP0015`, `RS0002`, `IMP0016`, `IMP0029`, `IMP0030`
- Why it fails: operators trust the tool and stop looking, while the next agent inherits obsolete guidance or resolves an ID to the wrong artifact.
- Guard: report updated/unchanged/conflicted/stale counts, prefer canonical ID lookup, add doctor checks for duplicate canonical mappings, keep memory stale state visible, make repair commands cover the same generated artifacts that doctor validates, and keep update notices pointed at the recorded/current/latest version mismatch plus the uvx refresh path.

## Treating Counts As Health

- Avoid when: a steward, dashboard, or automation preflight reports only record counts and generic lane triggers while hiding stale memory, stale generated views, missing abstraction, guard gaps, or pending migration state.
- Sources: `IMP0023`, `IMP0029`, `RS0005`, `IMP0015`, `IMP0031`
- Why it fails: counts prove that records exist, not that the lab is usable today; the next agent may skip librarian work even though the source digest has moved.
- Guard: expose read-only health signals such as `lab_health.status`, pressure triggers, stale snapshot/abstraction flags, and recommended commands, then delegate compaction or abstraction to the librarian lane; keep remote completion gates separate from intake and require validation/checks before merge.

## Ending Validated Automation At A Pushed Branch

- Avoid when: a scheduled run validates changes, pushes an automation branch, and then stops even though the prompt authorized PR creation and merge through the normal protected-branch path.
- Sources: `IMP0031`, `FB0037`, `FB0041`
- Why it fails: the work is neither merged nor clearly blocked, so the next run may repeat or stop on its own dirty/branch state instead of advancing a reviewed change.
- Guard: after validation, fetch, confirm the merge target freshness, finalize onto the automation branch, push only that branch, open or update the PR, wait for required checks, merge only when allowed, and report whether the blocker is missing checks, failing checks, pending checks, conflicts, or branch protection.

## Leaving Agent Handoff Paths Implicit

- Avoid when: AGENTS.md, CLAUDE.md, bridge skills, or update-harness output assume agents already know the valid `hops` invocation, repo role, and write path.
- Sources: `FB0042`, `IMP0030`, `FB0038`
- Why it fails: each target or project repo grows local conventions, agents may create lab state in project repos, and stale runtime/update guidance can mask the intended HarnessOps conduit.
- Guard: keep a compact role-scoped conduit in generated agent guidance, name the `hops` or `uvx --from harnessops hops` path, point stale-version work to explicit update/doctor/migrate commands, and preserve canonical HarnessOps state while ignoring only transient cache files.

## Treating No-Op As Daily Success

- Avoid when: a clean autonomous run with remote authority reports only preflight/doctor state because no obvious reactive work was waiting.
- Sources: `FB0037`, `FB0038`
- Why it fails: healthy repositories slowly train the automation into status polling, so queue discovery, record-only work, small guards, and safe cleanup never start.
- Guard: make proactive discovery mandatory when reactive work and queue are thin, split record/implementation/merge gates, handle latest/update-harness only when stale state is signaled, and reserve no-op for blockers, failed validation, exhausted budget, or explicit discovery failure.

## Tracking Runtime Cache As Project State

- Avoid when: transient files under `.harnessops/cache/` or future HarnessOps tmp paths are left to appear as normal untracked project changes.
- Sources: `FB0038`
- Why it fails: cache churn can stop dirty-worktree automation and hides the difference between canonical HarnessOps state and local runtime state.
- Guard: init/link/update-harness should maintain a marker-managed `.gitignore` block that ignores cache contents while preserving `.harnessops/cache/.gitkeep`.

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
