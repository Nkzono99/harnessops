# CLI Spec

`hops` is the primary command alias and `harnessops` is the explicit long
alias. Both entry points call `harnessops.cli.main:app`.

The CLI is the authoritative state engine. Plugins, skills, and agents may
guide a workflow, but managed state is mutated through CLI commands.

## Command Groups

| Command | Mutates state | Purpose |
|---|---:|---|
| `hops version` | no | Print package version. |
| `hops profiles list/show` | no | Inspect built-in profiles and profile fingerprints. |
| `hops detect` | no | Infer repository kind and recommended profile. |
| `hops init --profile <id>` | yes | Create `.harness/`, `.harnessops/`, and the profile overlay. |
| `hops link --profile <id>` | yes | Alias for linking an existing repository to HarnessOps. |
| `hops doctor` | no | Validate project link, overlay, lock, and records. |
| `hops migrate --check/--apply` | yes for apply | Check or apply schema/layout migrations. |
| `hops add-failure` | yes | Create a project-side failure record. |
| `hops add-feedback --from <Fid>` | yes | Create a private upstream/meta feedback draft. |
| `hops route --record <id>` | yes | Classify and persist a record disposition. |
| `hops feedback export --sanitize` | yes | Write sanitized outbound bundles under generated views. |
| `hops feedback import <bundle>` | yes | Import a sanitized bundle into `harness-lab`. |
| `hops lab new-eval-case --from <FBid>` | yes | Convert imported feedback to an eval case. |
| `hops propose --from <Eid>` | yes | Scaffold a hypothesis with mechanism and kill criteria sections. |
| `hops eval --case <Eid> --manual` | yes | Persist a multi-axis manual scorecard. |
| `hops decide --from <id> --status <status>` | yes | Record adoption, rejection, or deferral. |
| `hops agent bridge/install/verify` | yes for bridge/install | Manage thin agent entry points. |

## Safety Rules

1. No command creates GitHub issues, pull requests, or remote changes.
2. `feedback export` refuses unsanitized output unless `--allow-private` is explicit.
3. `init` writes generated files only. If a generated file was edited and lock
   hashes do not match, the command refuses overwrite or writes a conflict copy.
4. Records under `records/` are human-authored history and are not regenerated
   by view refreshes.
5. Adopted decisions require evidence, regression risk, and a guard path.

## Exit Codes

| Code | Meaning |
|---:|---|
| 0 | Success. |
| 1 | Validation or usage error. |
| 2 | Unsafe overwrite or install conflict prevented. |
| 3 | Profile not found. |

## Acceptance Commands

```bash
hops --help
hops profiles list
hops detect --json
hops init --profile runops-project
hops doctor --check-overlay --check-records
hops migrate --check
hops add-failure --title "Harness friction" --target runops
hops route --record F0001 --json
hops feedback export --sanitize
```

