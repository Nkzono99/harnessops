# Harness Lab Anti-Patterns

Updated: 2026-05-13T11:52:44+09:00
Source digest: `a475562f28434dcb0ec9f3111fd1eab187caea0298d9b946a45447809f089e4b`

These are reusable failure shapes to avoid. Each item names source IDs so decisions can return to canonical records.

## Reporting Success While Leaving State Stale

- Avoid when: an update or doctor path says `ok` but leaves stale managed files, duplicate dossiers, stale generated views, or shadowed record IDs unresolved.
- Sources: `IMP0002`, `IMP0011`, `IMP0012`, `IMP0015`, `RS0002`, `IMP0016`
- Why it fails: operators trust the tool and stop looking, while the next agent inherits obsolete guidance or resolves an ID to the wrong artifact.
- Guard: report updated/unchanged/conflicted/stale counts, prefer canonical ID lookup, add doctor checks for duplicate canonical mappings, keep memory stale state visible, and make repair commands cover the same generated artifacts that doctor validates.

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
