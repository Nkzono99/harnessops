# HarnessOps 実装仕様書

Version: 0.1-draft  
作成日: 2026-05-11  
想定リポジトリ名: `HarnessOps`  
Python package: `harnessops`  
CLI entry points: `harnessops`, `hops`

---

## 0. 目的

HarnessOps は、AI 支援開発・研究運用・論文執筆ハーネスに対して、**改善を実験として管理する横断基盤**である。

通常の自己改善ループは、改善案の生成はできても、改善案の選別・評価・履歴化・上流還元が弱く、次のような失敗を起こしやすい。

- 新しい rule / skill / docs を追加するが、実際の能力が上がらない。
- project 固有の問題を upstream template に混ぜる。
- issue は上がるが、eval case や再発防止に変換されない。
- project の研究判断、target harness の改善、meta-level の改善が混ざる。
- AI が自分の改善案を甘く評価する。

HarnessOps はこれを、以下の型で解決する。

```text
failure / feedback observation
  -> routing / disposition
  -> upstream or meta feedback
  -> eval case
  -> improvement hypothesis
  -> experiment
  -> decision
  -> adoption / rejection / migration / report
```

---

## 1. 中核設計

### 1.1 三層モデル

HarnessOps が扱うリポジトリは三層に分かれる。

```text
1. HarnessOps repository
   改善実験 OS。CLI、schema、plugin、migration、profile、adapter を提供する。

2. target-repository
   runops や paper-harness のような upstream harness/tool。
   自分自身も改善対象であり、project-repository を生成する。

3. project-repository
   runops init / paper-harness init などで生成される実利用プロジェクト。
   実験・論文・研究運用の現場。
```

### 1.2 役割分担

| 層 | 例 | 主な責務 | 標準 overlay |
|---|---|---|---|
| HarnessOps repository | `HarnessOps` | 改善方法、schema、CLI、plugin、migration | `harness-lab/` |
| target-repository | `runops`, `paper-harness` | upstream harness の実装・評価・改善 | `harness-lab/` |
| project-repository | `my-simulation-project`, `my-paper-project` | 実プロジェクトの状態、観測、feedback | `harness-feedback/` |

### 1.3 ディレクトリ命名

`improvement/` は採用しない。理由は、研究方針の進化、実験計画、upstream 改善、meta 改善が混ざりやすいためである。

採用する標準名は以下。

```text
harness-feedback/
  project-repository に置く。
  現場で観測された harness / upstream / meta への feedback を記録する。

harness-lab/
  target-repository と HarnessOps repository に置く。
  upstream 改善を評価・実験・採用判断する。

.harnessops/
  HarnessOps の link / lock / migration / cache を置く hidden metadata。

.harness/
  harness provider 非依存の共通 manifest を置く。
```

---

## 2. 非目標

HarnessOps は次をしない。

- project の研究内容・論文主張・実験方向性そのものを決める。
- target-repository のドメイン固有設計を肩代わりする。
- GitHub Issues を完全に置き換える。
- すべての project evolution を `harness-feedback/` に集約する。
- AI による自動 PR 作成や issue 起票をユーザー確認なしに行う。

Project の中身の進化は、各 project の `research/`、`notes/`、`manuscript/` などに残す。HarnessOps は、それらから発生した harness feedback を構造化し、target/meta へ送る。

---

## 3. Repository layout

### 3.1 HarnessOps repository

```text
HarnessOps/
  pyproject.toml
  README.md
  LICENSE
  AGENTS.md
  CLAUDE.md

  src/harnessops/
    __init__.py
    cli/
      __init__.py
      main.py
      init.py
      link.py
      detect.py
      doctor.py
      migrate.py
      profiles.py
      add_failure.py
      add_feedback.py
      feedback.py
      lab.py
      eval.py
      propose.py
      decide.py
      report.py
      agent.py
    core/
      __init__.py
      paths.py
      project.py
      manifest.py
      overlay.py
      lock.py
      migration.py
      records.py
      routing.py
      sanitize.py
      render.py
      validation.py
    profiles/
      __init__.py
      registry.py
      loader.py
      builtins/
        generic-code.yml
        python-package.yml
        target-harness.yml
        runops-upstream.yml
        runops-project.yml
        paper-harness-upstream.yml
        paper-harness-project.yml
        harnessops-core.yml
    adapters/
      __init__.py
      base.py
      generic_code.py
      python_package.py
      runops_upstream.py
      runops_project.py
      paper_harness_upstream.py
      paper_harness_project.py
      harnessops_core.py
    schemas/
      __init__.py
      loader.py
      json/
        harness-manifest.schema.json
        harnessops-project.schema.json
        profile.schema.json
        failure-record.schema.json
        feedback-record.schema.json
        eval-case.schema.json
        hypothesis.schema.json
        experiment.schema.json
        decision.schema.json
    migrations/
      __init__.py
      registry.py
      v0_1_to_v0_2.py

  specs/
    harness-common-spec.md
    harnessops-overlay-spec.md
    profile-spec.md
    feedback-routing-spec.md
    record-schemas.md
    cli-spec.md

  catalog/
    failure-taxonomy.yml
    capability-taxonomy.yml
    anti-patterns.yml
    scoring-rubrics.yml

  templates/
    feedback-source-overlay/
      harness-feedback/
        README.md
        records/
          failures/.gitkeep
          local-workarounds/.gitkeep
          upstream-feedback/.gitkeep
          meta-feedback/.gitkeep
        views/.gitkeep
    upstream-lab-overlay/
      harness-lab/
        README.md
        records/
          feedback/.gitkeep
          eval-cases/.gitkeep
          hypotheses/.gitkeep
          experiments/.gitkeep
          decisions/.gitkeep
        views/.gitkeep

  plugins/
    codex/
      harnessops/
        .codex-plugin/
          plugin.json
        skills/
          hops-diagnose/
            SKILL.md
          hops-add-failure/
            SKILL.md
          hops-route-feedback/
            SKILL.md
          hops-export-feedback/
            SKILL.md
          hops-import-feedback/
            SKILL.md
          hops-run-lab/
            SKILL.md
    claude/
      harnessops/
        .claude-plugin/
          plugin.json
        skills/
          hops-diagnose/
            SKILL.md
          hops-add-failure/
            SKILL.md
          hops-route-feedback/
            SKILL.md
          hops-export-feedback/
            SKILL.md
          hops-import-feedback/
            SKILL.md
          hops-run-lab/
            SKILL.md

  tests/
    test_cli/
    test_core/
    test_profiles/
    test_migrations/
    test_e2e/

  harness-lab/
    records/
      feedback/
      eval-cases/
      hypotheses/
      experiments/
      decisions/
    views/
```

### 3.2 target-repository layout

例: `runops`。

```text
runops/
  pyproject.toml
  src/runops/
  tests/
  docs/
  src/runops/templates/

  .harness/
    manifest.toml

  .harnessops/
    project.toml
    lock.json
    migrations/
    cache/

  harness-lab/
    README.md
    records/
      feedback/
      eval-cases/
      hypotheses/
      experiments/
      decisions/
    views/
      backlog.md
      score-trajectory.md
      imported-feedback.md

  src/runops/harnessops/
    profiles/
      runops-upstream.yml
      runops-project.yml
```

例: `paper-harness`。

```text
paper-harness/
  pyproject.toml or Makefile
  template/
  scripts/
  docs/
  tests/

  .harness/
    manifest.toml

  .harnessops/
    project.toml
    lock.json

  harness-lab/
    records/
      feedback/
      eval-cases/
      hypotheses/
      experiments/
      decisions/
    views/

  paper_harness/harnessops/profiles/
    paper-harness-upstream.yml
    paper-harness-project.yml
```

### 3.3 project-repository layout

例: runops generated project。

```text
my-simulation-project/
  campaign.toml
  cases/
  runs/
  notes/
  research/
    agenda.md
    hypotheses.md
    decisions/
    pivots/
  materials/
  refs/
  .runops/

  .harness/
    manifest.toml

  .harnessops/
    project.toml
    lock.json

  harness-feedback/
    README.md
    records/
      failures/
      local-workarounds/
      upstream-feedback/
      meta-feedback/
    views/
      upstream-feedback.md
      open-routing.md
      exported-feedback.md
```

例: paper-harness generated project。

```text
my-paper-project/
  manuscript/
  notes/
    claim-evidence-map.md
    reviewer-model.md
    research-strategy.md
    narrative-decisions/
  refs/
  submission/

  .harness/
    manifest.toml

  .harnessops/
    project.toml
    lock.json

  harness-feedback/
    records/
      failures/
      local-workarounds/
      upstream-feedback/
      meta-feedback/
    views/
```

---

## 4. Python package specification

### 4.1 `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "harnessops"
version = "0.1.0"
description = "Feedback and improvement experiment OS for AI-assisted harness projects"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.10"
dependencies = [
  "typer>=0.12",
  "rich>=13.0",
  "pydantic>=2.0",
  "tomli>=2.0; python_version < '3.11'",
  "tomli-w>=1.0",
  "ruamel.yaml>=0.18",
  "jinja2>=3.1",
]

[project.scripts]
harnessops = "harnessops.cli.main:app"
hops = "harnessops.cli.main:app"

[project.entry-points."harnessops.profiles"]
# Downstream harness packages may register profiles here.

[dependency-groups]
dev = [
  "pytest>=8.0",
  "ruff>=0.6",
  "mypy>=1.8",
  "jsonschema>=4.0",
]
```

### 4.2 CLI design principles

1. `hops` is the default short alias. `harnessops` is the explicit long command.
2. CLI is authoritative for state mutation.
3. Agent skills must call CLI commands rather than editing managed files directly.
4. Every write command supports `--dry-run` where meaningful.
5. No command creates GitHub issues, PRs, or remote changes without explicit user confirmation.
6. Commands must preserve local edits and avoid overwriting human-authored records.
7. Generated views are marked as generated and may be overwritten.
8. Record files are append-only by default. Mutation requires explicit commands.

---

## 5. Common manifest specification

### 5.1 `.harness/manifest.toml`

`.harness/manifest.toml` is a provider-neutral marker file. It is not HarnessOps-specific, but HarnessOps uses it for detection.

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

Paper project example:

```toml
schema_version = "0.1"

[harness]
provider = "paper-harness"
kind = "paper-project"
version = "0.1.0"

[commands]
doctor = "paper-harness doctor"
update = "paper-harness update-harness"
migrate = "paper-harness migrate"
feedback = "paper-harness feedback"
version = "paper-harness version"

[harnessops]
recommended_profile = "paper-harness-project"
```

HarnessOps itself:

```toml
schema_version = "0.1"

[harness]
provider = "harnessops"
kind = "core"
version = "0.1.0"

[commands]
doctor = "hops doctor"
migrate = "hops migrate"
version = "hops version"

[harnessops]
recommended_profile = "harnessops-core"
```

### 5.2 Semantics

| Field | Required | Meaning |
|---|---:|---|
| `schema_version` | yes | Common manifest schema version |
| `harness.provider` | yes | Upstream harness/tool name |
| `harness.kind` | yes | `upstream`, `generated-project`, `paper-project`, `core`, etc. |
| `harness.version` | recommended | Provider version |
| `commands.*` | optional | Provider command contract |
| `harnessops.recommended_profile` | optional | HarnessOps profile hint |

---

## 6. HarnessOps link specification

### 6.1 `.harnessops/project.toml`

```toml
schema_version = "0.1"
layout_version = "0.1"

[project]
name = "my-simulation-project"
root = "."
kind = "project-repository"

[profile]
id = "runops-project"
version = "0.1.0"
source = "builtin"
adapter = "runops_project"

[target_harness]
provider = "runops"
manifest = ".harness/manifest.toml"

[overlay]
mode = "feedback-source"
path = "harness-feedback"
managed_by = "harnessops"

[privacy]
default_visibility = "private-until-sanitized"

[agents]
codex = true
claude = true
```

Target repository example:

```toml
schema_version = "0.1"
layout_version = "0.1"

[project]
name = "runops"
root = "."
kind = "target-repository"

[profile]
id = "runops-upstream"
version = "0.1.0"
source = "runops"
adapter = "runops_upstream"

[overlay]
mode = "upstream-lab"
path = "harness-lab"
managed_by = "harnessops"

[feedback]
accepts_from = ["project-repository", "target-repository"]
exports_to = ["harnessops"]
```

### 6.2 Overlay modes

| Mode | Intended repository | Generated directory | Purpose |
|---|---|---|---|
| `feedback-source` | project-repository | `harness-feedback/` | Observation, local workaround, upstream/meta feedback |
| `local-and-feedback` | project-repository | `harness-feedback/` | Same as feedback-source, plus local process experiments |
| `upstream-lab` | target-repository | `harness-lab/` | Feedback import, eval case, hypothesis, experiment, decision |
| `meta-lab` | HarnessOps repository | `harness-lab/` | Improve HarnessOps itself |

Default mapping:

```text
profile id ending in -project     -> feedback-source
profile id ending in -upstream    -> upstream-lab
profile id harnessops-core        -> meta-lab
```

---

## 7. Profile specification

### 7.1 Profile ownership

Profiles exist in three layers.

```text
1. Built-in profiles
   Shipped by HarnessOps. Used for generic bootstrap and fallback.

2. Harness-owned profiles
   Shipped by target-repository packages such as runops or paper-harness.
   Registered via Python entry points.

3. Project-local overrides
   Stored in .harnessops/profile.local.yml or .harnessops/project.toml.
```

Resolution order:

```text
local override > harness-owned profile > HarnessOps built-in profile
```

### 7.2 Profile schema

```yaml
id: runops-project
version: 0.1.0
extends:
  - research-operations
adapter: runops_project
mode: feedback-source

root_markers:
  - .harness/manifest.toml
  - .runops/harness.lock
  - campaign.toml

feedback:
  path: harness-feedback

project_evolution:
  root: research
  agenda_file: research/agenda.md
  decision_dirs:
    - research/decisions
    - research/pivots

state_roots:
  - campaign.toml
  - cases/
  - runs/
  - notes/
  - research/
  - materials/
  - refs/
  - .runops/

quality_commands:
  doctor:
    - runo doctor
  lint:
    - runo lint --strict
  context:
    - runo context --json

capabilities:
  - campaign_case_run_separation
  - manifest_integrity
  - slurm_safety_gate
  - analysis_artifact_traceability
  - notes_to_knowledge_promotion
  - harness_update_without_overwrite

failure_classes:
  - project_specific_logic_leaks_into_template
  - update_harness_overwrites_local_edits
  - shallow_project_health_check
  - slurm_action_without_human_gate
  - manifest_provenance_gap
  - local_patch_not_classified

protected_paths:
  - runs/**/work/**
  - runs/**/manifest.toml
  - .runops/environment.toml

private_paths:
  - materials/private/**
  - refs/private/**
  - runs/**/work/**

upstream_targets:
  runops:
    type: target-harness
    repo: Nkzono99/runops
  harnessops:
    type: meta-harness
```

Paper project profile:

```yaml
id: paper-harness-project
version: 0.1.0
adapter: paper_harness_project
mode: feedback-source

root_markers:
  - manuscript/
  - notes/claim-evidence-map.md

feedback:
  path: harness-feedback

project_evolution:
  root: notes
  agenda_file: notes/research-strategy.md
  decision_dirs:
    - notes/narrative-decisions
    - notes/scope-decisions

state_roots:
  - manuscript/
  - notes/
  - refs/
  - submission/

quality_commands:
  ci:
    - make ci
  pre_submit:
    - make pre-submit

capabilities:
  - claim_calibration
  - public_terminology
  - citation_grounding
  - figure_story
  - mirror_consistency
  - venue_fit
  - ai_disclosure

failure_classes:
  - defensive_writing
  - local_vocabulary_leakage
  - citation_key_exists_but_does_not_support_claim
  - public_review_reads_private_context
  - governance_theater
  - skill_proliferation

upstream_targets:
  paper-harness:
    type: target-harness
  harnessops:
    type: meta-harness
```

---

## 8. Record formats

### 8.1 General record rules

All records are Markdown files with YAML frontmatter.

Rules:

1. Every record has an immutable `id`.
2. Every record has `record_type`.
3. Every record has `created_at` in ISO-8601 format.
4. Every record has `visibility`.
5. Every record has `disposition`.
6. Records must be human-readable.
7. Records may be edited by humans, but CLI must validate schema.
8. Generated views must not be treated as records.

ID conventions:

```text
F0001-*    failure record
LW0001-*   local workaround record
UF0001-*   upstream feedback record
MF0001-*   meta feedback record
FB0001-*   imported feedback in harness-lab
E0001-*    eval case
H0001-*    hypothesis
X0001-*    experiment
D0001-*    decision
```

### 8.2 Failure record in `harness-feedback/`

Path:

```text
harness-feedback/records/failures/F0001-local-term-leakage.md
```

Template:

```markdown
---
id: F0001
record_type: failure
created_at: 2026-05-11T00:00:00+09:00
status: open
visibility: private-until-sanitized
origin:
  repository_kind: project-repository
  profile: paper-harness-project
disposition:
  type: target-upstream-candidate
  target: paper-harness
  status: draft
privacy:
  contains_private_paths: false
  contains_unpublished_research: true
links:
  upstream_feedback: null
  meta_feedback: null
---

# F0001: Local terminology leaked into public manuscript

## Context

...

## What happened

...

## Why this matters

...

## Desired behavior

...

## Local workaround

...

## Routing rationale

...
```

### 8.3 Local workaround record

Path:

```text
harness-feedback/records/local-workarounds/LW0001-runops-local-patch.md
```

Template:

```markdown
---
id: LW0001
record_type: local_workaround
created_at: 2026-05-11T00:00:00+09:00
status: active
related_failure: F0001
disposition:
  type: upstream-candidate
  target: runops
expires_when: "runops >= 0.10.0"
---

# LW0001: Local patch for runops harness update

## Patch summary

...

## Current project check

...

## Upstreamable parts

...

## Project-specific parts to exclude

...
```

### 8.4 Upstream feedback record

Path:

```text
harness-feedback/records/upstream-feedback/UF0001-paper-harness-public-terms.md
```

Template:

```markdown
---
id: UF0001
record_type: upstream_feedback
created_at: 2026-05-11T00:00:00+09:00
status: draft
target: paper-harness
source_failure: F0001
sanitized: false
visibility: private-until-sanitized
issue:
  provider: github
  url: null
---

# Feedback to paper-harness: public terminology leakage not caught

## Summary

...

## Minimal reproduction

...

## Expected upstream improvement

...

## Private info excluded

...
```

### 8.5 Meta feedback record

Path:

```text
harness-feedback/records/meta-feedback/MF0001-routing-gap.md
```

Template:

```markdown
---
id: MF0001
record_type: meta_feedback
created_at: 2026-05-11T00:00:00+09:00
status: draft
target: harnessops
source_failure: F0001
sanitized: false
---

# Feedback to HarnessOps: routing between project decision and upstream feedback is unclear

## Problem

...

## Expected HarnessOps improvement

...
```

### 8.6 Imported feedback in `harness-lab/`

Path:

```text
harness-lab/records/feedback/FB0001-public-terms.md
```

Template:

```markdown
---
id: FB0001
record_type: imported_feedback
created_at: 2026-05-11T00:00:00+09:00
status: triaged
source:
  type: harness-feedback-export
  original_id: UF0001
  source_project: redacted
classification:
  failure_class: local_vocabulary_leakage
  capability: public_terminology
links:
  eval_case: E0001
  issue_url: null
---

# FB0001: Public terminology leakage not caught

## Summary

...

## Reproduction

...

## Expected upstream change

...
```

### 8.7 Eval case

```markdown
---
id: E0001
record_type: eval_case
created_at: 2026-05-11T00:00:00+09:00
status: active
capability: public_terminology
failure_class: local_vocabulary_leakage
source_feedback: FB0001
---

# E0001: Detect internal-only public terminology in manuscript text

## Fixture

...

## Task

...

## Expected behavior

...

## Pass criteria

- The internal term is detected.
- The public replacement is suggested.
- Public terms are not incorrectly flagged as internal.

## Fail criteria

- False negatives on internal terms.
- False positives on allowed public terms.
```

### 8.8 Hypothesis

```markdown
---
id: H0001
record_type: hypothesis
created_at: 2026-05-11T00:00:00+09:00
status: proposed
target_capability: public_terminology
source_eval_case: E0001
---

# H0001: Field-aware terminology schema reduces leakage and false positives

## Hypothesis

...

## Mechanism

...

## Minimal implementation

...

## Expected upside

...

## Expected downside

...

## Evaluation plan

...

## Kill criteria

...
```

### 8.9 Experiment

Directory:

```text
harness-lab/records/experiments/X0001-field-aware-terms/
  experiment.md
  before/
  after/
  scores.yml
```

`experiment.md`:

```markdown
---
id: X0001
record_type: experiment
created_at: 2026-05-11T00:00:00+09:00
status: running
hypothesis: H0001
eval_cases:
  - E0001
---

# X0001: Field-aware public terminology check

## Patch summary

...

## Commands

...

## Results

...
```

### 8.10 Decision

```markdown
---
id: D0001
record_type: decision
created_at: 2026-05-11T00:00:00+09:00
status: adopted
experiment: X0001
---

# D0001: Adopt field-aware public terminology check

## Decision

Adopt.

## Reason

...

## Evidence

...

## Regression risk

...

## Follow-up

...
```

---

## 9. CLI command specification

### 9.1 Command list

```text
hops version
hops profiles list
hops profiles show <id>
hops detect
hops init --profile <id>
hops link --profile <id>
hops doctor
hops migrate --check
hops migrate --apply
hops add-failure
hops add-feedback
hops route
hops feedback export
hops feedback import
hops lab import-feedback
hops lab new-eval-case
hops propose
hops eval
hops decide
hops report
hops agent install
hops agent bridge
```

### 9.2 `hops init`

Purpose: create HarnessOps metadata and overlay for a repository.

Examples:

```bash
uvx harnessops init --profile runops-project
uvx harnessops init --profile paper-harness-project
uvx harnessops init --profile runops-upstream
uvx harnessops init --profile harnessops-core
```

Behavior:

1. Detect repository root.
2. Load profile.
3. Determine overlay mode.
4. Create `.harnessops/project.toml`.
5. Create `.harnessops/lock.json`.
6. Create `harness-feedback/` or `harness-lab/`.
7. Create generated views.
8. Preserve existing files unless `--force`.
9. Run `doctor --check-overlay` after init.

Options:

```text
--profile <id>            required unless detect finds recommended profile
--mode <mode>             override profile mode
--path <path>             override overlay path
--with-agent-bridge       generate repo-local bridge skill
--dry-run                 print planned changes
--force                   overwrite generated files only if lock permits
```

Exit codes:

```text
0 success
1 validation error
2 unsafe overwrite prevented
3 profile not found
```

### 9.3 `hops detect`

Purpose: infer project type and recommended profile.

Detection priority:

```text
1. .harnessops/project.toml
2. .harness/manifest.toml
3. provider-specific markers
4. generic repository markers
```

Marker examples:

```text
runops upstream:
  pyproject.toml project.name == runops
  src/runops/
  src/runops/templates/

runops project:
  .runops/harness.lock
  campaign.toml
  cases/
  runs/

paper-harness upstream:
  template/
  scripts/publish-scaffold.sh
  template/manuscript/

paper-harness project:
  manuscript/
  notes/claim-evidence-map.md
  refs/
  submission/

HarnessOps core:
  pyproject.toml project.name == harnessops
  src/harnessops/
  profiles/
  schemas/
```

Output default: human-readable. `--json` returns structured result.

### 9.4 `hops doctor`

Purpose: validate HarnessOps link, overlay, profile, and optional provider commands.

Checks:

```text
- .harnessops/project.toml exists and validates.
- .harnessops/lock.json is consistent.
- profile exists and matches adapter.
- overlay directory exists.
- record directories exist.
- generated views are up to date or marked stale.
- protected/private paths are configured.
- provider manifest exists if configured.
- provider doctor command works if --provider is passed.
- schema migration is not pending, unless --allow-pending.
```

Examples:

```bash
hops doctor
hops doctor --json
hops doctor --provider
hops doctor --check-overlay --check-records
```

### 9.5 `hops add-failure`

Purpose: create a project-side failure record.

Use in `feedback-source` mode.

Examples:

```bash
hops add-failure --title "Local term leaked into manuscript" --target paper-harness
hops add-failure --interactive
hops add-failure --from-file note.md
```

Behavior:

1. Ensure current repo is `feedback-source` or `local-and-feedback`.
2. Ask for / accept context, what happened, why bad, desired behavior.
3. Classify disposition.
4. Create record under `harness-feedback/records/failures/`.
5. Update views.
6. Suggest feedback creation if target upstream/meta candidate.

### 9.6 `hops route`

Purpose: classify a record’s disposition.

Disposition values:

```text
project-evolution
project-local-process
target-upstream-candidate
meta-harness-candidate
protocol-candidate
external-candidate
do-not-upstream
```

Rules:

```text
If the issue changes only research content -> project-evolution.
If the issue reveals a missing domain workflow -> target-upstream-candidate.
If the issue reveals a missing routing/schema/process abstraction -> meta-harness-candidate.
If the issue concerns .harness/manifest or CLI common spec -> protocol-candidate.
```

### 9.7 `hops feedback export`

Purpose: generate sanitized upstream/meta feedback bundles from project-side records.

Examples:

```bash
hops feedback export --target runops --sanitize
hops feedback export --target paper-harness --sanitize --format issue
hops feedback export --target harnessops --sanitize --format markdown
```

Behavior:

1. Select records with matching disposition and target.
2. Apply sanitizer.
3. Remove private paths and unpublished project identifiers unless allowed.
4. Write export under `harness-feedback/views/exported-feedback/`.
5. Optionally draft GitHub issue body.
6. Never submit remotely without confirmation.

### 9.8 `hops feedback import`

Purpose: import a feedback bundle or issue into target-side `harness-lab/`.

Examples:

```bash
hops feedback import path/to/UF0001.md
hops feedback import --issue 42 --repo Nkzono99/paper-harness
```

Behavior:

1. Ensure current repo is `upstream-lab` or `meta-lab`.
2. Validate imported record.
3. Create `harness-lab/records/feedback/FBxxxx.md`.
4. Suggest eval case creation.
5. Link issue URL if present.

### 9.9 `hops lab new-eval-case`

Purpose: convert feedback into an eval case.

```bash
hops lab new-eval-case --from FB0001
```

Behavior:

1. Read imported feedback.
2. Map to capability and failure class.
3. Create eval case template.
4. Optionally create fixture directory.

### 9.10 `hops propose`

Purpose: generate or scaffold improvement hypotheses from eval cases.

This command may run in two modes:

```text
--manual-template
  create hypothesis template only.

--agent-assisted
  print a structured prompt for an agent or use configured LLM integration if available.
```

HarnessOps MVP should implement `--manual-template` first.

### 9.11 `hops eval`

Purpose: run eval cases and quality commands.

Examples:

```bash
hops eval --case E0001
hops eval --all
hops eval --experiment X0001
```

Behavior:

1. Load eval case.
2. Run profile-defined quality commands if requested.
3. Store results under experiment or views.
4. Preserve before/after artifacts where configured.

MVP may support manual scoring only:

```bash
hops eval --case E0001 --manual
```

### 9.12 `hops decide`

Purpose: create decision record for an experiment.

```bash
hops decide --experiment X0001 --status adopted
hops decide --experiment X0002 --status rejected
```

Required statuses:

```text
adopted
rejected
parked
needs-more-evidence
```

### 9.13 `hops agent install`

Purpose: install Codex / Claude plugin or repo-local bridge.

Examples:

```bash
hops agent install --codex --scope repo
hops agent install --codex --scope user
hops agent install --claude --scope repo
hops agent bridge --codex
hops agent bridge --claude
```

Rules:

- `bridge` writes only a thin repo-local skill that tells the agent to call `hops`.
- Full plugin is distributed from HarnessOps.
- Repo-local bridge is optional when plugin is installed globally.

---

## 10. Agent plugin specification

### 10.1 Design principle

Agent plugins provide workflow UX. They do not own state.

```text
Agent skill -> calls hops CLI -> CLI writes/validates/migrates files
```

No plugin skill should directly restructure `.harnessops/`, `harness-feedback/`, or `harness-lab/`.

### 10.2 Codex plugin layout

Codex package:

```text
plugins/codex/harnessops/
  .codex-plugin/
    plugin.json
  skills/
    hops-diagnose/
      SKILL.md
    hops-add-failure/
      SKILL.md
    hops-route-feedback/
      SKILL.md
    hops-export-feedback/
      SKILL.md
    hops-import-feedback/
      SKILL.md
    hops-run-lab/
      SKILL.md
```

`plugin.json`:

```json
{
  "name": "harnessops",
  "version": "0.1.0",
  "description": "Feedback routing and improvement experiment workflows for harness projects",
  "skills": "./skills/"
}
```

Codex notes:

- Codex skills are directories with `SKILL.md` and optional scripts/references/assets.
- Codex plugins use `.codex-plugin/plugin.json` and may include `skills/`.
- Repo-scoped marketplaces may use `.agents/plugins/marketplace.json`.

### 10.3 Claude plugin layout

Claude package:

```text
plugins/claude/harnessops/
  .claude-plugin/
    plugin.json
  skills/
    hops-diagnose/
      SKILL.md
    hops-add-failure/
      SKILL.md
    hops-route-feedback/
      SKILL.md
    hops-export-feedback/
      SKILL.md
    hops-import-feedback/
      SKILL.md
    hops-run-lab/
      SKILL.md
```

### 10.4 Skill contract

All skills must start by checking repository link:

```bash
hops doctor --check-overlay
```

If not linked:

```bash
hops detect
hops init --profile <detected-profile>
```

Skill example: `hops-add-failure/SKILL.md`.

```markdown
---
name: hops-add-failure
description: Use when a project failure, harness friction, local workaround, or upstream feedback candidate should be recorded through HarnessOps.
---

Use HarnessOps. Do not manually edit harness-feedback/ or harness-lab/ structure.

1. Run `hops doctor --check-overlay`.
2. If the repository is not linked, run `hops detect` and propose `hops init --profile <id>`.
3. Collect context: what happened, why bad, desired behavior, privacy risk.
4. Run `hops add-failure --interactive` or create a draft command.
5. Run `hops route --record <id>` if disposition is unclear.
6. If upstream/meta candidate, propose `hops feedback export --target <target> --sanitize`.
```

---

## 11. Sanitization specification

### 11.1 Default privacy posture

Default visibility for project-side feedback is:

```text
private-until-sanitized
```

Remote issue creation is never automatic.

### 11.2 Sanitizer inputs

Sanitizer reads:

```text
- profile.private_paths
- profile.protected_paths
- .harnessops/project.toml privacy settings
- optional .harnessops/sanitize.yml
```

Example `.harnessops/sanitize.yml`:

```yaml
redact_patterns:
  - pattern: "/home/[^\s]+"
    replacement: "<LOCAL_PATH>"
  - pattern: "cluster-[A-Za-z0-9_-]+"
    replacement: "<CLUSTER>"

private_terms:
  - unpublished-method-name
  - internal-dataset-code
```

### 11.3 Sanitizer outputs

Sanitized output must include:

```text
- private info excluded
- reproduction sufficient for upstream
- source project anonymized unless explicitly allowed
- local paths redacted
- unpublished research details removed or abstracted
```

---

## 12. Adapter specification

Adapters customize detection, diagnosis, routing hints, and eval defaults.

### 12.1 Base adapter interface

```python
class Adapter:
    id: str

    def detect(self, root: Path) -> DetectionResult: ...
    def default_profile_id(self, root: Path) -> str | None: ...
    def doctor_checks(self, project: Project) -> list[CheckResult]: ...
    def routing_hints(self, record: Record) -> list[RoutingHint]: ...
    def eval_case_templates(self) -> list[EvalCaseTemplate]: ...
```

### 12.2 runops project adapter

Responsibilities:

```text
- Detect .runops/harness.lock, campaign.toml, cases/, runs/.
- Recognize project evolution roots under research/.
- Route Slurm safety, manifest, adapter, update-harness issues to runops.
- Route feedback schema/routing issues to HarnessOps.
- Avoid classifying research direction changes as upstream issues unless tooling gap exists.
```

### 12.3 paper-harness project adapter

Responsibilities:

```text
- Detect manuscript/, notes/claim-evidence-map.md, refs/.
- Recognize project evolution roots under notes/.
- Route claim/evidence tool gaps, terminology gates, venue workflow gaps to paper-harness.
- Route overlay/schema/routing gaps to HarnessOps.
- Keep paper-specific claim decisions in notes/, not harness-feedback/.
```

### 12.4 upstream adapters

`runops-upstream` and `paper-harness-upstream` adapters should:

```text
- Use harness-lab/.
- Import downstream feedback.
- Convert feedback to eval cases.
- Run target quality commands.
- Track decisions.
```

---

## 13. Standardized bootstrap

### 13.1 HarnessOps project bootstrap

```bash
uvx harnessops init --profile harnessops-core
```

Creates:

```text
.harness/manifest.toml
.harnessops/project.toml
.harnessops/lock.json
harness-lab/
```

### 13.2 runops generated project with HarnessOps

Preferred:

```bash
uvx runops init --with-harnessops
```

Equivalent internal call:

```bash
uvx harnessops init --profile runops-project
```

If `runops` does not implement `--with-harnessops` yet, users run:

```bash
uvx runops init
uvx harnessops init --profile runops-project
```

### 13.3 paper-harness project with HarnessOps

Preferred:

```bash
uvx paper-harness init --with-harnessops
```

Equivalent:

```bash
uvx harnessops init --profile paper-harness-project
```

### 13.4 target repository bootstrap

For runops:

```bash
cd runops
uvx harnessops init --profile runops-upstream
```

For paper-harness:

```bash
cd paper-harness
uvx harnessops init --profile paper-harness-upstream
```

---

## 14. Development roadmap

### MVP: 0.1

Implement:

```text
- Python package and CLI entry points: harnessops, hops
- Built-in profiles
- .harnessops/project.toml
- .harnessops/lock.json
- harness-feedback/ generation
- harness-lab/ generation
- detect / init / doctor / migrate --check
- add-failure
- route
- feedback export --sanitize
- feedback import
- basic views generation
- repo-local agent bridge skill
```

MVP intentionally does not require:

```text
- automatic LLM judging
- automatic GitHub issue creation
- full experiment runner
- plugin marketplace publishing
- external protocol repository
```

### 0.2

```text
- Codex plugin package
- Claude plugin package
- eval case templates
- lab new-eval-case
- hypothesis templates
- decision records
- adapter-specific doctor checks
- harness-owned profiles via entry points
```

### 0.3

```text
- experiment runner
- score trajectory
- holdout case support
- GitHub issue import/export helper with explicit confirmation
- profile migration
- generated view dashboards
```

### 0.4+

```text
- protocol compliance tests
- optional MCP integration
- cross-project private knowledge overlay
- public pattern promotion pipeline
- potential split of Harness Common Spec into separate harness-protocol repository
```

---

## 15. Testing strategy

### 15.1 Unit tests

```text
- profile loading and resolution
- project detection
- project.toml validation
- lockfile generation
- overlay generation
- record ID allocation
- routing classification
- sanitizer redaction
- migration idempotency
```

### 15.2 CLI tests

```text
- hops init --profile runops-project creates harness-feedback/
- hops init --profile runops-upstream creates harness-lab/
- hops doctor passes after init
- hops add-failure creates valid failure record
- hops feedback export redacts private paths
- hops feedback import creates target feedback record
```

### 15.3 E2E fixtures

```text
tests/fixtures/runops-project-minimal/
tests/fixtures/paper-project-minimal/
tests/fixtures/runops-upstream-minimal/
tests/fixtures/paper-harness-upstream-minimal/
```

### 15.4 Golden snapshots

Use snapshot tests for generated files:

```text
.harnessops/project.toml
.harnessops/lock.json
harness-feedback/README.md
harness-lab/README.md
views/upstream-feedback.md
```

### 15.5 Safety tests

```text
- init does not overwrite user files
- migrate refuses dirty generated files not matching lock
- export refuses unsanitized issue draft unless --allow-private
- plugin bridge contains no long mutable logic
```

---

## 16. Lockfile specification

Path:

```text
.harnessops/lock.json
```

Example:

```json
{
  "schema_version": "0.1",
  "layout_version": "0.1",
  "harnessops_version": "0.1.0",
  "profile": {
    "id": "runops-project",
    "version": "0.1.0",
    "source": "builtin",
    "fingerprint": "sha256:..."
  },
  "overlay": {
    "mode": "feedback-source",
    "path": "harness-feedback"
  },
  "managed_files": {
    "harness-feedback/README.md": "sha256:...",
    "harness-feedback/views/upstream-feedback.md": "sha256:..."
  },
  "migrations": []
}
```

Rules:

```text
- Only generated files are tracked in managed_files.
- Human-authored records are not overwritten.
- Views may be regenerated.
- If a managed file hash differs, migrate/update must preserve it or create conflict copy.
```

---

## 17. Migration specification

Command:

```bash
hops migrate --check
hops migrate --apply
```

Migration rules:

1. Never delete human-authored records.
2. Generated views can be regenerated.
3. Managed files are updated only if lock hash matches.
4. If conflict, write `.new` file and report.
5. Migration writes an entry to `.harnessops/migrations/`.
6. Migration can update `layout_version`.

Example migration entry:

```text
.harnessops/migrations/2026-05-11-v0_1-to-v0_2.md
```

---

## 18. Feedback routing model

### 18.1 Dispositions

```text
project-evolution
  Project content changed. Store under research/ or notes/, not harness-feedback/.

project-local-process
  Project-specific process issue. Store as local workaround or local note.

target-upstream-candidate
  Should be considered by runops, paper-harness, or another target harness.

meta-harness-candidate
  Concerns HarnessOps routing/schema/CLI/plugin/process.

protocol-candidate
  Concerns common .harness/manifest or shared CLI convention.

external-candidate
  Concerns external systems such as cluster, journal, simulator, or tool.

do-not-upstream
  Explicitly local or private.
```

### 18.2 Event splitting

A single project event may create multiple records.

Example:

```text
Observed event:
  During a runops project, the research direction pivoted after failed runs.

Records:
  1. research/decisions/D001-pivot.md
     Object-level project evolution.

  2. harness-feedback/records/upstream-feedback/UF0001-runops-pivot-workflow-gap.md
     runops should provide better pivot workflow support.

  3. harness-feedback/records/meta-feedback/MF0001-routing-gap.md
     Only if HarnessOps cannot classify this event cleanly.
```

---

## 19. GitHub issue integration

HarnessOps may help create issue drafts. It must not create issues automatically.

Commands:

```bash
hops feedback export --target runops --format github-issue --sanitize
hops feedback create-issue --target runops --from UF0001
```

`create-issue` must:

1. Show title and body.
2. Confirm with user.
3. Check for `gh` availability.
4. Optionally search duplicate issues.
5. Run only after confirmation.

This feature is not MVP-critical.

---

## 20. Relationship with target-provided skills

Target repositories should continue to provide domain skills.

Examples for runops:

```text
/research-pivot-review
/deepen-or-broaden
/run-failure-to-next-plan
/promote-observation
/campaign-replan
```

Examples for paper-harness:

```text
/claim-pivot-review
/deepen-evidence-or-narrow-scope
/storyline-reframe
/reviewer-comment-strategy
/stopped-claim-review
```

HarnessOps provides meta skills:

```text
/hops-diagnose
/hops-add-failure
/hops-route-feedback
/hops-export-feedback
/hops-import-feedback
/hops-run-lab
```

Domain skills may call HarnessOps CLI when they discover harness feedback, but should not move project decisions into `harness-feedback/` unless it is a harness issue.

---

## 21. Implementation order

Recommended implementation sequence:

```text
1. Create package skeleton and CLI aliases.
2. Implement profile registry and built-in profiles.
3. Implement detect.
4. Implement init and overlay generation.
5. Implement doctor.
6. Implement record models and add-failure.
7. Implement routing and feedback export.
8. Implement feedback import for harness-lab.
9. Implement migration --check and lockfile logic.
10. Implement bridge skill generation.
11. Add Codex plugin package.
12. Add Claude plugin package.
13. Add eval-case and lab workflow.
```

---

## 22. Minimum viable file examples

### 22.1 `harness-feedback/README.md`

```markdown
# harness-feedback

This directory stores feedback from this project to upstream harnesses and HarnessOps.

Use this directory for:

- observed harness failures
- local workarounds
- upstream feedback drafts
- meta-harness feedback drafts

Do not use this directory for:

- research agenda changes
- paper claim changes
- experiment direction pivots
- raw private data

Use `hops add-failure`, `hops route`, and `hops feedback export` to manage records.
```

### 22.2 `harness-lab/README.md`

```markdown
# harness-lab

This directory stores upstream improvement experiments for this harness repository.

Use this directory for:

- imported feedback
- eval cases
- improvement hypotheses
- experiments
- adoption/rejection decisions

GitHub Issues remain the task tracker. `harness-lab/` is the evaluation and decision memory.
```

### 22.3 Repo-local bridge skill

Path for Codex:

```text
.agents/skills/harnessops-bridge/SKILL.md
```

Content:

```markdown
---
name: harnessops-bridge
description: Use when recording project failures, routing upstream feedback, or running HarnessOps improvement workflows.
---

This repository is linked to HarnessOps.

Do not directly restructure `.harnessops/`, `harness-feedback/`, or `harness-lab/`.
Use the CLI:

- `hops doctor`
- `hops add-failure`
- `hops route`
- `hops feedback export`
- `hops feedback import`
- `hops migrate --check`

Read `.harnessops/project.toml` before proposing harness feedback or lab changes.
```

---

## 23. Standardization policy

### 23.1 Where to manage CLI/common specs

Initially, manage common specs inside HarnessOps:

```text
HarnessOps/specs/
HarnessOps/schemas/
```

Rationale:

```text
- HarnessOps is the primary consumer.
- The spec will evolve with CLI, migration, and overlays.
- A separate protocol repository would add governance overhead too early.
```

### 23.2 When to split `harness-protocol`

Create a separate repository only when at least two independent tools need the common protocol without HarnessOps.

Split criteria:

```text
- runops, paper-harness, and another third-party harness all consume .harness/manifest independently.
- Common CLI compliance tests are needed outside HarnessOps.
- Spec release cycle must differ from HarnessOps release cycle.
- External contributors need stable protocol documents without adopting HarnessOps.
```

Potential future repository:

```text
harness-protocol/
  specs/
  schemas/
  examples/
  compliance-tests/
```

Until then, keep the protocol inside HarnessOps.

---

## 24. External compatibility notes

HarnessOps plugin packaging should follow current host-specific conventions:

- Codex skills use `SKILL.md` directories and plugins can package reusable skills. Codex plugins use `.codex-plugin/plugin.json` and may include `skills/`.
- Claude Code plugins are self-contained directories that can include skills, agents, hooks, MCP servers and other components. Claude skills are directories containing `SKILL.md`, and plugin skills are namespaced by plugin.

These host-specific formats should remain thin wrappers over the `hops` CLI. If host plugin formats change, HarnessOps should update plugin packaging without changing overlay semantics.

---

## 25. Acceptance criteria for version 0.1

HarnessOps 0.1 is acceptable when all of the following pass:

```text
- `uvx harnessops --help` works.
- `uvx harnessops init --profile runops-project` creates `.harnessops/` and `harness-feedback/`.
- `uvx harnessops init --profile runops-upstream` creates `.harnessops/` and `harness-lab/`.
- `hops detect` identifies runops project, runops upstream, paper-harness project, paper-harness upstream, and HarnessOps core fixtures.
- `hops doctor` passes immediately after init.
- `hops add-failure` creates a valid failure record.
- `hops route` classifies a record into a disposition.
- `hops feedback export --sanitize` writes a sanitized feedback bundle.
- `hops feedback import` imports a feedback bundle into harness-lab.
- `hops migrate --check` reports no pending migration after fresh init.
- Generated files are not overwritten when modified by users unless lock permits.
- Repo-local bridge skill can be generated for Codex.
- Test suite includes minimal fixtures for runops project and paper-harness project.
```

---

## 26. Key design decisions

1. Use `HarnessOps` as repository/product name.
2. Use `hops` as primary short CLI alias and `harnessops` as long alias.
3. Use `.harnessops/` for hidden metadata.
4. Use `.harness/manifest.toml` for provider-neutral common harness metadata.
5. Use `harness-feedback/` in project-repositories.
6. Use `harness-lab/` in target-repositories and HarnessOps itself.
7. Keep project evolution in `research/` or `notes/`, specified by profile.
8. Manage common CLI/specs inside HarnessOps initially.
9. Split protocol repository only after real external adoption.
10. Make plugin UX first-class, but keep CLI as authoritative state engine.

---

## 27. References

- OpenAI Codex Agent Skills documentation: https://developers.openai.com/codex/skills
- OpenAI Codex plugin build documentation: https://developers.openai.com/codex/plugins/build
- Claude Code plugin reference: https://code.claude.com/docs/en/plugins-reference
- Claude Code plugin creation documentation: https://code.claude.com/docs/ja/plugins
