# HarnessOps

HarnessOps is a feedback routing and improvement experiment OS for
AI-assisted harness projects.

It exists to keep self-improvement loops evidence-backed. AI can generate
candidate changes, but HarnessOps records failures, routes feedback, creates
eval cases, captures hypotheses, persists scorecards, and records adoption or
rejection decisions.

## Core Model

HarnessOps separates three repository roles:

| Layer | Overlay | Responsibility |
|---|---|---|
| project repository | `harness-feedback/` | Observe failures, record local workarounds, export sanitized feedback. |
| target repository | `harness-lab/` | Import feedback, create eval cases, evaluate hypotheses, record decisions. |
| HarnessOps repository | `harness-lab/` | Improve schemas, CLI, migrations, profiles, adapters, and plugin workflow. |

Project evolution belongs in `research/` or `notes/`, not in
`harness-feedback/`. Target/meta promotion must pass through routing and
sanitization.

## Minimal Loop

```bash
hops init --profile runops-project
hops add-failure --title "Harness friction" --target runops
hops route --record F0001
hops feedback export --sanitize
```

On the target side:

```bash
hops init --profile runops-upstream
hops feedback import path/to/UF0001-runops-feedback.md
hops lab new-eval-case --from FB0001
hops propose --from E0001
hops eval --case E0001 --manual --score impact=4 --score anti-theater=5
hops decide --from H0001 --status parked
```

Adopted decisions require evidence, regression risk, and a guard path:

```bash
hops decide --from H0001 --status adopted \
  --reason "Eval passed with a smaller profile change" \
  --evidence "harness-lab/views/eval-results/E0001-manual-score.yml" \
  --regression-risk "Low; fixture covers the failure class" \
  --guard-path "tests/test_cli/test_mvp_flow.py"
```

## Privacy

Project-side visibility defaults to `private-until-sanitized`.
`hops feedback export` refuses unsanitized output unless `--allow-private` is
explicit. Sanitization redacts local paths, configured private terms, protected
paths, and source project identity before outbound feedback is written.

Optional project config:

```yaml
# .harnessops/sanitize.yml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - secret-method-name
```

## Agent Plugins

Codex and Claude plugin packages live under `plugins/`. They are thin workflow
wrappers. They must call `hops` for state changes and must not directly
restructure `.harnessops/`, `harness-feedback/`, or `harness-lab/`.

Repo bridge:

```bash
hops agent bridge --codex
```

User plugin install:

```bash
hops agent install --codex --scope user
```

## Development

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uvx --from . harnessops --help
uv run --with-editable . hops doctor --check-overlay --check-records
```

Current MVP coverage verifies detection, init, doctor, migration checks,
failure creation, routing, feedback export/import, eval case creation,
hypothesis/decision records, scorecard output, sanitization, and overwrite
safety.

