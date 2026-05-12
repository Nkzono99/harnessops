# HarnessOps Overlay Spec

HarnessOps uses two visible overlays and one hidden metadata directory.

## Project Overlay: `harness-feedback/`

Project repositories use `harness-feedback/` for project-side observations and
outbound feedback drafts.

```text
harness-feedback/
  README.md
  records/
    failures/
    local-workarounds/
    upstream-feedback/
    meta-feedback/
  views/
    open-routing.md
    upstream-feedback.md
    exported-feedback/
```

Do not store research agenda changes, paper claim changes, experiment pivots,
raw private data, or target implementation patches here unless they are
represented as routed harness feedback.

## Lab Overlay: `harness-lab/`

Target repositories and the HarnessOps repository use `harness-lab/` for
evaluating upstream improvements.

```text
harness-lab/
  README.md
  records/
    feedback/
    eval-cases/
      fixtures/
    hypotheses/
    experiments/
    decisions/
  views/
    imported-feedback.md
    backlog.md
    score-trajectory.md
    eval-results/
```

`harness-lab/` is memory for feedback, evals, hypotheses, experiments, and
decisions. GitHub Issues remain the task tracker.

## Hidden Metadata: `.harnessops/`

```text
.harnessops/
  project.toml
  lock.json
  migrations/
  cache/
```

`lock.json` tracks generated files only. Human-authored records are not listed
in `managed_files`.

## Generated Files

Generated files include overlay READMEs and views. They contain a generated
marker and may be refreshed. If a managed file hash differs from the lock, init
or migration refuses overwrite unless `--force` is used and conflict behavior is
safe.

