# Harness Lab Evaluation Playbook

Updated: 2026-05-14T01:10:08+09:00
Source digest: `b52b8f6c8c026009c5e0cef42f497c2e8e85d0ab89754ea9da3298b6b2f7d823`

This playbook captures evaluation habits that survived across adopted improvements. It guides new evaluations, but source records remain authoritative.

## Core Axes

- Score impact, mechanism clarity, evaluability, minimality, regression risk, operator burden, anti-theater value, maintainability, and privacy/sanitization risk.
- Sources: `IMP0001`, `IMP0002`, `IMP0003`, `IMP0004`, `IMP0005`, `IMP0006`, `IMP0007`, `IMP0008`, `IMP0009`, `IMP0011`, `IMP0012`, `IMP0013`, `IMP0014`, `IMP0015`, `IMP0016`
- Use high mechanism clarity as a requirement for adoption: the change should name the failure mechanism and show how the implementation closes it.
- Use anti-theater as a real axis: a change should prevent misleading records, stale success, unreviewable noise, or performative process.

## Evidence Path

- Start with source feedback or a research scan, then create an eval case, hypothesis, manual evaluation, decision, and guard.
- Sources: `IMP0001`, `IMP0006`, `IMP0009`, `RS0001`
- For deliberate research, require local/codebase evidence, external evidence when useful, candidate relation, recommendation, and next command before promotion.
- For compact memory, require lint/prepare output, source IDs, and a matching source digest before updating abstract knowledge.

## Holdouts To Reuse

- Stale managed bridge file with no local edits should update automatically; locally edited managed file should produce `.new` instead of being overwritten. Source: `IMP0002`
- Unicode GitHub issue body/comment on Windows should import via UTF-8 decoding without crashing. Source: `IMP0005`
- Concurrent lab dossier/classify/investigate calls for the same feedback should not create duplicate improvement dossiers. Source: `IMP0011`
- Record lookup by ID should prefer canonical record directories over generated views. Source: `IMP0012`
- Generated dossiers should not embed full generic eval-case template bodies when manual eval summaries carry the signal. Source: `IMP0013`
- Lab memory lint/prepare should expose stale or missing abstraction state without treating deterministic snapshots as semantic memory. Sources: `IMP0014`, `IMP0015`
- Steward preflight should expose lab-health triggers for lab repositories and skip harness-lab memory probing in project repositories. Source: `IMP0029`
- Research scans should stay deliberate and structured rather than becoming a record for every small idea. Sources: `IMP0008`, `IMP0009`, `RS0001`
- `hops lab refresh-views` should clear doctor-managed lab generated-view warnings for README, backlog, dynamic lab views, research scans, and score trajectory without losing dynamic view content. Sources: `RS0002`, `IMP0016`

## Adoption Criteria

- Adopt when the source failure is reproducible, the mechanism is explicit, the implementation is minimal enough to maintain, and a regression guard exists or the risk is intentionally low.
- Sources: `IMP0005`, `IMP0006`, `IMP0011`, `IMP0012`, `IMP0013`, `IMP0014`, `IMP0015`, `IMP0016`
- Promote beyond target-lab-case only when the lesson affects protocol, cross-project behavior, memory design, agent skills, or reusable evaluation workflow.
- Sources: `IMP0006`, `IMP0007`, `IMP0008`, `IMP0009`, `IMP0014`

## Kill Criteria

- Reject or merge back if a new skill cannot be distinguished from an existing skill, lacks packaging tests, or does not route durable outputs through the lab. Source: `IMP0008`
- Reject or narrow if trigger checks do not produce actionable next steps or encourage unsourced abstraction. Source: `IMP0015`
- Reject remote promotion if sanitation or duplicate detection cannot be made explicit. Source: `IMP0004`
- Reject generated review surfaces that add more template text than decision signal. Sources: `IMP0003`, `IMP0013`
- Reject generated-view repair changes that leave doctor warnings after the advertised refresh command. Sources: `RS0002`, `IMP0016`
- Reject compaction changes that erase canonical source links, source digests, or contradiction/guard context. Sources: `IMP0014`, `IMP0015`
- Reject steward/preflight changes that write lab memory, perform semantic abstraction, or create `harness-lab/` behavior in project repositories. Sources: `IMP0023`, `IMP0029`, `RS0005`

## Guard Catalogue

- `tests/test_cli/test_mvp_flow.py`: guards improvement loop, research scans, dossier creation consistency, canonical lookup, dossier evaluation summaries, lab compaction, memory lint/prepare, and generated-view refresh repair. Sources: `IMP0006`, `IMP0009`, `IMP0011`, `IMP0012`, `IMP0013`, `IMP0014`, `IMP0015`, `IMP0016`
- `tests/test_agent_harness_contract.py`: guards packaged skills and bridge guidance for meta scan, research skill, and memory abstraction. Sources: `IMP0007`, `IMP0008`, `IMP0015`
- `tests/test_cli/test_steward.py`: guards pull-first safety, finalize behavior, project-repo lab-health skip, and stale lab-health routing to librarian. Sources: `IMP0023`, `IMP0029`
- Full `hops doctor --check-overlay --check-records` and `hops migrate --check` remain release-level checks for layout and managed-artifact consistency. Sources: `IMP0001`, `IMP0002`, `IMP0004`, `IMP0005`, `IMP0006`

## Reading Rules

- Read compact memory first for orientation, then return to source records before adopting, rejecting, or changing behavior. Sources: `IMP0014`, `IMP0015`
- Prefer manual eval summaries over empty eval templates when judging current state. Source: `IMP0013`
- Treat external benchmarks as design context, not as proof that the local implementation works. Sources: `IMP0006`, `IMP0008`, `IMP0009`, `IMP0014`
