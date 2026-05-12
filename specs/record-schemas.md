# Record Schemas

HarnessOps records are Markdown files with YAML frontmatter. The frontmatter is
machine-validated; the body is human-readable evidence and rationale.

## Common Rules

- `id`, `record_type`, and `created_at` are required for every record.
- ID prefixes must match record type: `F`, `LW`, `UF`, `MF`, `FB`, `E`, `H`,
  `X`, and `D`.
- Records are append-only by default. Mutation requires an explicit CLI command.
- Generated views are not records and may be overwritten.
- Record bodies must not contain unresolved `TODO` placeholders after creation
  commands that claim to create evidence-bearing artifacts.

## Required Sections

| Type | Required body sections |
|---|---|
| `failure` | Context, What happened, Why this matters, Desired behavior, Local workaround, Routing rationale |
| `upstream_feedback` | Summary, Minimal reproduction, Expected upstream improvement, Private info excluded |
| `meta_feedback` | Summary, Minimal reproduction, Expected upstream improvement, Private info excluded |
| `imported_feedback` | Summary, Reproduction, Expected upstream change |
| `eval_case` | Fixture, Task, Expected behavior, Pass criteria, Fail criteria |
| `hypothesis` | Hypothesis, Mechanism, Minimal implementation, Alternative: deletion or consolidation, Expected upside, Expected downside, Evaluation plan, Kill criteria |
| `decision` | Decision, Reason, Evidence, Regression risk, Follow-up, Regression guard |

## Evidence Discipline

A hypothesis without mechanism, evaluation plan, and kill criteria is not a real
experiment. A decision without evidence is not adoption-ready. An adopted
decision must identify a regression guard, such as a test path, eval result, or
generated check that will detect recurrence.

## Validation

`hops doctor --check-records` validates frontmatter, ID prefixes, required body
sections, dispositions, and adoption evidence. JSON schema files under
`src/harnessops/schemas/json/` document the machine-readable contract.

