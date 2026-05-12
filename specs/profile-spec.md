# Profile Spec

Profiles describe how HarnessOps should detect, initialize, validate, route, and
sanitize a repository.

## Required Fields

```yaml
id: runops-project
version: 0.1.0
adapter: runops_project
mode: feedback-source
root_markers:
  - campaign.toml
feedback:
  path: harness-feedback
capabilities:
  - manifest_integrity
failure_classes:
  - manifest_provenance_gap
```

Recommended fields:

- `repository_kind`: project, target, or HarnessOps repository category.
- `provider`: upstream harness provider.
- `project_evolution`: roots where object-level project changes belong.
- `state_roots`: project state paths used by doctor or future context tools.
- `quality_commands`: provider commands that can be run by humans or CI.
- `protected_paths`: paths that must not be copied into public feedback.
- `private_paths`: paths that sanitizer should redact.
- `upstream_targets`: target harnesses and meta-harness destinations.

## Resolution Order

```text
local override > harness-owned entry point > built-in profile
```

The lockfile stores the resolved profile id, source, version, and fingerprint so
future migrations can detect profile drift.

## Built-in Profiles

HarnessOps ships:

- `generic-code`
- `python-package`
- `target-harness`
- `runops-project`
- `runops-upstream`
- `paper-harness-project`
- `paper-harness-upstream`
- `harnessops-core`

## Guardrails

Profiles must distinguish project evolution roots from harness feedback roots.
If a paper claim pivot belongs in `notes/`, the profile should make that clear
so routing does not pollute upstream templates.

