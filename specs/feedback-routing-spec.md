# Feedback Routing Spec

Routing prevents upstream pollution by separating project evolution, local
process issues, target-harness gaps, HarnessOps meta gaps, protocol gaps,
external-system issues, and private records.

## Dispositions

| Disposition | Meaning | Default destination |
|---|---|---|
| `project-evolution` | Research/paper/project content changed. | `research/` or `notes/` |
| `project-local-process` | Project-specific process or workaround. | Local notes or workaround record |
| `target-upstream-candidate` | Target harness should consider a change. | runops, paper-harness, etc. |
| `meta-harness-candidate` | HarnessOps schema, CLI, routing, migration, or plugin gap. | HarnessOps |
| `protocol-candidate` | Common `.harness/manifest` or shared CLI convention gap. | HarnessOps protocol/spec |
| `external-candidate` | Cluster, simulator, journal, or other external system. | External tracker or note |
| `do-not-upstream` | Explicitly local/private. | No upstream export |

## Event Splitting

One observed event may produce multiple records. A research pivot belongs in
`research/decisions/`, while a missing pivot workflow in runops can become
`harness-feedback/records/upstream-feedback/`, and a routing ambiguity can
become `meta-feedback`.

## Routing Evidence

`hops route --record <id>` persists a disposition. Human reviewers should check:

- Is this object-level project evolution?
- Is there an upstream tool gap independent of project details?
- Can the issue be reproduced after sanitization?
- Does it reveal a HarnessOps schema/routing/process gap?
- Would upstreaming this leak private or project-specific context?

## Current Implementation

The MVP uses deterministic heuristics plus explicit `--target` and
`--disposition` overrides. Adapter-specific routing should expand from these
rules without bypassing the same record schema.

