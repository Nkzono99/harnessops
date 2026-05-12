---
id: RS0001
record_type: research_scan
created_at: '2026-05-13T03:35:35+09:00'
status: captured
scope: harnessops-core deliberate meta improvement research
existing_dossier: IMP0009
classification:
  capability: meta_improvement_research
  failure_class: unstructured_research_scan_results
evidence:
  local:
  - summary: IMP0009 remained active because the dry-run result had useful candidates but no structured artifact
    ref: harness-lab/improvements/IMP0009-fb0013-structure-meta-improvement-research-scan-outputs.md
  codebase:
  - summary: hops-research-improvements had Scope/Evidence/Candidates/Recommendation prose guidance but no CLI record for it
    ref: .agents/skills/hops-research-improvements/SKILL.md
  - summary: The new lab research-scan command stores candidate rows and refreshes views/research-scans.md
    ref: src/harnessops/cli/lab.py
  external:
  - summary: External investigation for IMP0009 found postmortem, experiment, and maturity-ring practices favor structured action items and learning records
    ref: https://sre.google/workbook/postmortem-culture/
  risk:
  - summary: A new record type can create meta-noise if used for every small observation
    ref: docs/design-principles.md
candidates:
- title: Add RS research_scan record and view
  relation: extends
  recommendation: propose
  next_command: hops lab new-eval-case --from FB0013
recommendation: 'adopt: use research-scan for deliberate multi-candidate meta-improvement research before routing candidates to investigate/capture/propose/park/reject.'
---

# RS0001: Structure meta improvement research scan outputs

## Scope

- scope: harnessops-core deliberate meta improvement research
- existing_dossier: IMP0009
- capability: meta_improvement_research
- failure_class: unstructured_research_scan_results

## Evidence

### Local

- IMP0009 remained active because the dry-run result had useful candidates but no structured artifact (ref: harness-lab/improvements/IMP0009-fb0013-structure-meta-improvement-research-scan-outputs.md)

### Codebase

- hops-research-improvements had Scope/Evidence/Candidates/Recommendation prose guidance but no CLI record for it (ref: .agents/skills/hops-research-improvements/SKILL.md)
- The new lab research-scan command stores candidate rows and refreshes views/research-scans.md (ref: src/harnessops/cli/lab.py)

### External

- External investigation for IMP0009 found postmortem, experiment, and maturity-ring practices favor structured action items and learning records (ref: https://sre.google/workbook/postmortem-culture/)

### Risk And Counterexample

- A new record type can create meta-noise if used for every small observation (ref: docs/design-principles.md)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add RS research_scan record and view | extends | propose | hops lab new-eval-case --from FB0013 |

## Recommendation

adopt: use research-scan for deliberate multi-candidate meta-improvement research before routing candidates to investigate/capture/propose/park/reject.

## Next Commands

- `hops lab new-eval-case --from FB0013`
