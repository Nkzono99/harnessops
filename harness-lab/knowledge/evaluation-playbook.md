# Harness Lab Evaluation Playbook

Updated: 2026-05-16T03:11:28+09:00
Source digest: `c32879ff67e15871ff60297ed65310ce07a3a037068063e801f01e0b02fa445d`

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
- Update notices should cover recorded/current/latest HarnessOps version drift, point to `uvx --refresh-package harnessops --from harnessops hops update-harness`, and keep migration application explicit. Source: `IMP0030`
- Daily steward remote completion should push only an automation branch, open or update a PR, and merge only after validation, target freshness, required checks, and branch protection allow it. Source: `IMP0031`
- No-argument issue triage should inspect open issues, report priority buckets, evidence, missing information, recommended HOPS action, and remote-action authorization before importing, closing, or implementing. Source: `IMP0032`
- Daily steward should not return status-only no-op on clean runs until it has processed reactive work, advanced queue work, run proactive discovery, or exhausted explicit budget. Source: `FB0037`
- HarnessOps latest/update-harness work should be signal-driven, and init/link/update-harness should maintain `.gitignore` hygiene for `.harnessops/cache/*` without hiding canonical `.harnessops` state. Source: `FB0038`
- GitHub Flow merge diagnostics should distinguish missing required checks from failing or pending checks, and PR CI should provide a concrete required-check target before branch protection is tightened. Source: `FB0041`
- Generated AGENTS.md/CLAUDE.md and update-harness guidance should expose the minimal HarnessOps invocation plus role-specific routing for target/meta versus project repositories. Source: `FB0042`
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
- Reject update guidance that cannot name the safe uvx refresh path or that auto-applies migrations during ordinary command use. Source: `IMP0030`
- Reject automation merge guidance that bypasses branch protection, merges without validation/checks, or turns daily steward into an unbounded systemic backlog processor. Source: `IMP0031`
- Reject issue-triage guidance that closes, comments on, labels, or imports issues without explicit remote-action authority and a HOPS-owned record path. Source: `IMP0032`
- Reject steward guidance that applies implementation-level validation/guard gates to record-only discovery, or that restores a single global systemic-candidate cap as the main throughput control. Source: `FB0037`
- Reject update-lane guidance that updates HarnessOps to latest at the start of every daily run, or `.gitignore` hygiene that ignores canonical `.harnessops/project.toml`, lock, migrations, feedback, or lab records. Source: `FB0038`
- Reject GitHub Flow automation that treats missing required checks as ordinary failures or has no PR workflow that branch protection can require. Source: `FB0041`
- Reject agent conduit guidance that omits the invocation path or lets project repositories create lab state instead of feedback/export records. Source: `FB0042`

## Guard Catalogue

- `tests/test_cli/test_mvp_flow.py`: guards improvement loop, research scans, dossier creation consistency, canonical lookup, dossier evaluation summaries, lab compaction, memory lint/prepare, and generated-view refresh repair. Sources: `IMP0006`, `IMP0009`, `IMP0011`, `IMP0012`, `IMP0013`, `IMP0014`, `IMP0015`, `IMP0016`
- `tests/test_agent_harness_contract.py`: guards packaged skills and bridge guidance for meta scan, research skill, and memory abstraction. Sources: `IMP0007`, `IMP0008`, `IMP0015`
- `tests/test_cli/test_steward.py`: guards pull-first safety, finalize behavior, project-repo lab-health skip, and stale lab-health routing to librarian. Sources: `IMP0023`, `IMP0029`
- `tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once` and adjacent update-notice tests: guard recorded/current/latest version notice behavior and uvx update guidance. Source: `IMP0030`
- `tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented` and `tests/test_agent_harness_contract.py::test_daily_steward_skill_is_packaged_for_agents`: guard lane budgets plus branch/PR/merge automation guidance. Source: `IMP0031`
- `tests/test_agent_harness_contract.py`: guards no-argument issue triage reporting, remote-action authority boundaries, and daily steward delegation to `hops-issue-triage`. Source: `IMP0032`
- `tests/test_agent_harness_contract.py::test_daily_steward_automation_prompt_is_documented` and `tests/test_agent_harness_contract.py::test_meta_improvement_research_skill_is_packaged`: guard no-idle daily automation, risk-tier budgets, and ranked candidate queue wording. Source: `FB0037`
- `tests/test_cli/test_mvp_flow.py::test_init_doctor_migrate_project` and `tests/test_cli/test_mvp_flow.py::test_update_harness_repairs_harnessops_gitignore_block`: guard HarnessOps `.gitignore` cache hygiene. Source: `FB0038`
- `.github/workflows/pr-ci.yml`, `src/harnessops/cli/github_flow.py`, and related CLI tests: guard required-check-aware GitHub Flow diagnostics. Source: `FB0041`
- `tests/test_agent_harness_contract.py` and packaged update-harness skill assets: guard compact role-aware agent conduit guidance. Source: `FB0042`
- Full `hops doctor --check-overlay --check-records` and `hops migrate --check` remain release-level checks for layout and managed-artifact consistency. Sources: `IMP0001`, `IMP0002`, `IMP0004`, `IMP0005`, `IMP0006`

## Reading Rules

- Read compact memory first for orientation, then return to source records before adopting, rejecting, or changing behavior. Sources: `IMP0014`, `IMP0015`
- Prefer manual eval summaries over empty eval templates when judging current state. Source: `IMP0013`
- Treat external benchmarks as design context, not as proof that the local implementation works. Sources: `IMP0006`, `IMP0008`, `IMP0009`, `IMP0014`
