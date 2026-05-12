---
name: hops-run-lab
description: Use when working in harness-lab on eval cases, hypotheses, and decisions.
---

Run `hops doctor --check-overlay`. Use `hops lab new-eval-case`,
`hops propose --manual-template`, `hops eval --manual`, and `hops decide`.

Guardrails:

- Do not recommend adoption without eval evidence.
- Hypotheses must include mechanism, evaluation plan, and kill criteria.
- Prefer deletion or consolidation before adding new workflow surface.
- Adopted decisions must include evidence, regression risk, and a guard path.
- Do not expose holdout cases or private project context.
