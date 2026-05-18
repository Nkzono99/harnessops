---
id: RS0004
record_type: research_scan
created_at: '2026-05-13T18:17:28+09:00'
status: archived
scope: harnessops-core issue tracker and lab-state reconciliation
existing_dossier: IMP0002/IMP0003/IMP0004/IMP0018
classification:
  capability: issue_lab_reconciliation
  failure_class: stale_external_issue_tracker
evidence:
  local:
  - summary: 'Open issues #6, #7, and #8 still appear in GitHub even though their linked lab dossiers are adopted.'
    ref: gh issue list --state open --limit 20
  - summary: 'Issue #9 remains open and overlaps IMP0018, but still includes residual acceptance criteria for doctor fallback validation or an invocation-reporting command.'
    ref: https://github.com/Nkzono99/harnessops/issues/9
  - summary: lab memory lint is ok, but snapshot and abstraction are stale after v0.1.5, so post-release readers may need either issue reconciliation or an explicit memory compaction pass later.
    ref: uv run --with-editable . hops lab memory lint --warn-only
  codebase:
  - summary: IMP0002 records conflict-aware update-harness behavior as adopted, with tests covering unmodified refresh, local edit conflict, forced overwrite, and count/path output.
    ref: harness-lab/improvements/IMP0002-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md
  - summary: IMP0003 records per-improvement dossier support as adopted, with docs and tests for low-friction dossier creation and generated views.
    ref: harness-lab/improvements/IMP0003-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md
  - summary: IMP0004 records lab-first GitHub issue draft/create as adopted, including sanitized body creation, duplicate search, confirm-create, and URL writeback.
    ref: harness-lab/improvements/IMP0004-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md
  - summary: Current bridge assets use uvx --from harnessops hops fallback and contract tests block generated target skills from mentioning editable checkout fallback.
    ref: src/harnessops/core/agent_bridge.py; tests/test_agent_harness_contract.py
  external: []
  risk:
  - summary: Closing or commenting on remote GitHub issues is an external write; keep this scan local until the user explicitly asks to reconcile issues.
    ref:
  - summary: 'Closing #9 now would lose the remaining doctor validation / print-invocation requirement; treat it as an implementation candidate, not a stale issue.'
    ref:
candidates:
- title: 'Prepare closure comments for issues #6, #7, and #8'
  relation: new
  recommendation: ask-user-then-close
  next_command: 'gh issue close 6 --comment <adopted in IMP0002/v0.1.x evidence>; repeat for #7/#8'
- title: 'Finish issue #9 residual invocation diagnostics'
  relation: extends
  recommendation: capture-or-propose
  next_command: hops feedback import --issue 9 --repo Nkzono99/harnessops, then connect the residual to IMP0018 or create a new eval case
- title: 'Defer #5 until the broader improve-harness workflow is explicitly mapped'
  relation: parks
  recommendation: investigate
  next_command: 'compare #5 body against IMP0006/IMP0008/IMP0009 and decide whether it is superseded or still an umbrella issue'
- title: Refresh semantic lab memory after issue reconciliation
  relation: extends
  recommendation: defer
  next_command: hops lab memory prepare --force followed by hops-compact-lab-memory if stale context becomes a real friction
recommendation: 'prioritize #9 residual implementation next; separately ask before closing #6/#7/#8 because remote tracker writes should be explicit'
retirement:
- created_at: '2026-05-19T03:32:32+09:00'
  status: archived
  reason: 'remote issue close candidates are stale because issues #5-#9 are already closed; keep scan as audit evidence only'
  evidence_ref: issue-execution lane found no open issues; gh issue list --repo Nkzono99/harnessops --state all --limit 20
---

# RS0004: Reconcile post-v0.1.5 open issues with lab decisions

## Scope

- scope: harnessops-core issue tracker and lab-state reconciliation
- existing_dossier: IMP0002/IMP0003/IMP0004/IMP0018
- capability: issue_lab_reconciliation
- failure_class: stale_external_issue_tracker

## Evidence

### Local

- Open issues #6, #7, and #8 still appear in GitHub even though their linked lab dossiers are adopted. (ref: gh issue list --state open --limit 20)
- Issue #9 remains open and overlaps IMP0018, but still includes residual acceptance criteria for doctor fallback validation or an invocation-reporting command. (ref: https://github.com/Nkzono99/harnessops/issues/9)
- lab memory lint is ok, but snapshot and abstraction are stale after v0.1.5, so post-release readers may need either issue reconciliation or an explicit memory compaction pass later. (ref: uv run --with-editable . hops lab memory lint --warn-only)

### Codebase

- IMP0002 records conflict-aware update-harness behavior as adopted, with tests covering unmodified refresh, local edit conflict, forced overwrite, and count/path output. (ref: harness-lab/improvements/IMP0002-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md)
- IMP0003 records per-improvement dossier support as adopted, with docs and tests for low-friction dossier creation and generated views. (ref: harness-lab/improvements/IMP0003-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md)
- IMP0004 records lab-first GitHub issue draft/create as adopted, including sanitized body creation, duplicate search, confirm-create, and URL writeback. (ref: harness-lab/improvements/IMP0004-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md)
- Current bridge assets use uvx --from harnessops hops fallback and contract tests block generated target skills from mentioning editable checkout fallback. (ref: src/harnessops/core/agent_bridge.py; tests/test_agent_harness_contract.py)

### External

- なし

### Risk And Counterexample

- Closing or commenting on remote GitHub issues is an external write; keep this scan local until the user explicitly asks to reconcile issues.
- Closing #9 now would lose the remaining doctor validation / print-invocation requirement; treat it as an implementation candidate, not a stale issue.

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Prepare closure comments for issues #6, #7, and #8 | new | ask-user-then-close | gh issue close 6 --comment <adopted in IMP0002/v0.1.x evidence>; repeat for #7/#8 |
| Finish issue #9 residual invocation diagnostics | extends | capture-or-propose | hops feedback import --issue 9 --repo Nkzono99/harnessops, then connect the residual to IMP0018 or create a new eval case |
| Defer #5 until the broader improve-harness workflow is explicitly mapped | parks | investigate | compare #5 body against IMP0006/IMP0008/IMP0009 and decide whether it is superseded or still an umbrella issue |
| Refresh semantic lab memory after issue reconciliation | extends | defer | hops lab memory prepare --force followed by hops-compact-lab-memory if stale context becomes a real friction |

## Recommendation

prioritize #9 residual implementation next; separately ask before closing #6/#7/#8 because remote tracker writes should be explicit

## Next Commands

- `gh issue close 6 --comment <adopted in IMP0002/v0.1.x evidence>; repeat for #7/#8`
- `hops feedback import --issue 9 --repo Nkzono99/harnessops, then connect the residual to IMP0018 or create a new eval case`
- `compare #5 body against IMP0006/IMP0008/IMP0009 and decide whether it is superseded or still an umbrella issue`
- `hops lab memory prepare --force followed by hops-compact-lab-memory if stale context becomes a real friction`
