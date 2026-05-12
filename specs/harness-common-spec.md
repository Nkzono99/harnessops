# Harness Common Spec

`.harness/manifest.toml` is a provider-neutral marker file. HarnessOps uses it
for detection and profile hints, but the file is not HarnessOps-specific.

## Required Shape

```toml
schema_version = "0.1"

[harness]
provider = "runops"
kind = "generated-project"
version = "0.9.0"

[commands]
doctor = "runo doctor"
update = "runo update-harness"
migrate = "runo migrate"
feedback = "runo feedback"
version = "runo version"

[harnessops]
recommended_profile = "runops-project"
```

## Semantics

| Field | Required | Meaning |
|---|---:|---|
| `schema_version` | yes | Common manifest schema version. |
| `harness.provider` | yes | Upstream harness or tool name. |
| `harness.kind` | yes | `generated-project`, `paper-project`, `upstream`, `core`, etc. |
| `harness.version` | recommended | Provider version. |
| `commands.*` | optional | Provider command contract. |
| `harnessops.recommended_profile` | optional | HarnessOps detection hint. |

## Detection Priority

`hops detect` resolves repository identity in this order:

1. `.harnessops/project.toml`
2. `.harness/manifest.toml`
3. provider-specific markers
4. generic repository markers

