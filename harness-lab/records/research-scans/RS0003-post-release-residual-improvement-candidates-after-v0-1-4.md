---
id: RS0003
record_type: research_scan
created_at: '2026-05-13T17:47:43+09:00'
status: captured
scope: harnessops-core
existing_dossier: IMP0018
classification:
  capability: release-and-agent-bridge
  failure_class: post-release-residual-risk
evidence:
  local:
  - summary: v0.1.4 release succeeded, but GitHub release run emitted Node.js 20 action deprecation annotations
    ref: gh run 25787498566
  codebase:
  - summary: Publish workflow still uses actions/checkout@v4 and actions/setup-python@v5
    ref: .github/workflows/publish-pypi.yml
  - summary: 'Issue #9 remains open; #10 fixed generated/packaged fallback text but did not add doctor validation or print-invocation command'
    ref: https://github.com/Nkzono99/harnessops/issues/9
  - summary: lab memory lint reports status ok while snapshot and abstraction are stale, which can make post-release knowledge freshness ambiguous
    ref: uv run --with-editable . hops lab memory lint --warn-only
  external:
  - summary: GitHub says runners begin using Node24 by default on June 2 2026 and users should update workflows to latest actions that run on Node24
    ref: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
  - summary: actions/checkout v5 and actions/setup-python v6 document Node24 runtime support
    ref: https://github.com/actions/checkout https://github.com/actions/setup-python
  risk:
  - summary: The release workflow still passes today, but the deprecation window is short and warnings may turn into release friction after GitHub runner defaults change
    ref: .github/workflows/publish-pypi.yml
candidates:
- title: Migrate release workflow actions to Node24-ready majors
  relation: new
  recommendation: capture/propose
  next_command: hops lab capture --title 'Release workflow uses Node20 action majors'
- title: 'Finish issue #9 residual doctor/invocation acceptance criteria'
  relation: extends IMP0018
  recommendation: 'investigate or import issue #9'
  next_command: hops feedback import --issue 9 --repo Nkzono99/harnessops
- title: Clarify memory lint stale-but-ok output after releases
  relation: new
  recommendation: park unless repeated confusion
  next_command: hops lab research-scan or capture after another instance
recommendation: 'Prioritize the release workflow Node24 migration first because it has an external deadline before June 2 2026; then treat issue #9 as a residual extension of IMP0018 rather than a new broad bridge rewrite.'
---

# RS0003: Post-release residual improvement candidates after v0.1.4

## Scope

- scope: harnessops-core
- existing_dossier: IMP0018
- capability: release-and-agent-bridge
- failure_class: post-release-residual-risk

## Evidence

### Local

- v0.1.4 release succeeded, but GitHub release run emitted Node.js 20 action deprecation annotations (ref: gh run 25787498566)

### Codebase

- Publish workflow still uses actions/checkout@v4 and actions/setup-python@v5 (ref: .github/workflows/publish-pypi.yml)
- Issue #9 remains open; #10 fixed generated/packaged fallback text but did not add doctor validation or print-invocation command (ref: https://github.com/Nkzono99/harnessops/issues/9)
- lab memory lint reports status ok while snapshot and abstraction are stale, which can make post-release knowledge freshness ambiguous (ref: uv run --with-editable . hops lab memory lint --warn-only)

### External

- GitHub says runners begin using Node24 by default on June 2 2026 and users should update workflows to latest actions that run on Node24 (ref: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)
- actions/checkout v5 and actions/setup-python v6 document Node24 runtime support (ref: https://github.com/actions/checkout https://github.com/actions/setup-python)

### Risk And Counterexample

- The release workflow still passes today, but the deprecation window is short and warnings may turn into release friction after GitHub runner defaults change (ref: .github/workflows/publish-pypi.yml)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Migrate release workflow actions to Node24-ready majors | new | capture/propose | hops lab capture --title 'Release workflow uses Node20 action majors' |
| Finish issue #9 residual doctor/invocation acceptance criteria | extends IMP0018 | investigate or import issue #9 | hops feedback import --issue 9 --repo Nkzono99/harnessops |
| Clarify memory lint stale-but-ok output after releases | new | park unless repeated confusion | hops lab research-scan or capture after another instance |

## Recommendation

Prioritize the release workflow Node24 migration first because it has an external deadline before June 2 2026; then treat issue #9 as a residual extension of IMP0018 rather than a new broad bridge rewrite.

## Next Commands

- `hops lab capture --title 'Release workflow uses Node20 action majors'`
- `hops feedback import --issue 9 --repo Nkzono99/harnessops`
- `hops lab research-scan or capture after another instance`
