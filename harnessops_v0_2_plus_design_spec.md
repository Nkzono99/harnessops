# HarnessOps 0.2 以降の設計仕様書

Version: 0.2+-draft  
作成日: 2026-05-11  
対象: `HarnessOps` repository / `harnessops` package / `hops` CLI  
前提仕様: `HarnessOps 実装仕様書 Version 0.1-draft`

---

## 0. この文書の目的

この文書は、HarnessOps 0.1 で定義した以下の基盤を前提に、0.2 以降で実装すべき機能・責務・CLI・データ構造・リリース順を定義する。

0.1 の中核は以下である。

```text
project-repository
  harness-feedback/
    現場で観測した harness / upstream / meta への feedback を記録する

 target-repository / HarnessOps repository
  harness-lab/
    feedback を評価ケース化し、仮説・実験・採用判断に変換する

.harnessops/
  link / lock / schema / migration metadata

hops CLI
  状態変更の authoritative engine

Codex / Claude plugin
  UX layer。状態変更は hops CLI に委任する
```

0.2 以降の目的は、単なる記録・ルーティングから、以下へ拡張することである。

```text
0.2: plugin-first UX と harness-lab の実用化
0.3: 実験 runner、score trajectory、holdout 評価
0.4: cross-project knowledge、pattern promotion、protocol compliance
0.5: multi-repo orchestration、CI/Issue/Plugin marketplace 実運用
1.0: 安定 API / 安定 overlay / protocol 分離判断
```

---

## 1. バージョン設計の基本方針

### 1.1 0.1 と 0.2 以降の役割差

| Version | 中心テーマ | できること | まだやらないこと |
|---|---|---|---|
| 0.1 | bootstrap / feedback routing | link, detect, add-failure, route, export/import | 本格的な実験評価、score履歴、holdout |
| 0.2 | plugin UX / lab workflow | feedback を eval/hypothesis/decision に変換 | 自動実験runner、holdout gate |
| 0.3 | experiment execution | before/after比較、score trajectory、holdout | 横断知識昇格の完全自動化 |
| 0.4 | knowledge/pattern promotion | project固有失敗を汎用patternへ昇格 | protocol独立repo化はまだ任意 |
| 0.5 | operational integration | multi-repo inbox、GitHub補助、CI統合 | 完全自律PR/Issue作成 |
| 1.0 | stability | API/CLI/schema互換性保証 | 仕様を無制限に変えること |

### 1.2 非目標を維持する

0.2 以降でも、以下はしない。

```text
- AI に project の研究判断そのものを委譲しない
- project-specific な出来事を自動で upstream に混ぜない
- GitHub Issue / PR をユーザー確認なしに作らない
- holdout case を通常の agent workflow に露出しない
- plugin に状態管理を持たせない
- generated views と human-authored records を混同しない
```

### 1.3 追加よりも評価を優先する

0.2 以降の最大の危険は、HarnessOps 自体が「改善っぽい governance layer」を増殖させることである。したがって、各バージョンの機能追加は、必ず以下のいずれかを満たす。

```text
- downstream project から上がる feedback をより良く分類できる
- feedback を eval case に変換できる
- 改善仮説の採用/却下を判断しやすくする
- 既存改善が悪化していないことを検出できる
- project固有知識とupstream汎用知識を分離できる
```

---

## 2. 0.2 の設計: plugin-first UX と harness-lab の実用化

### 2.1 0.2 のゴール

0.2 は、0.1 で作った `harness-feedback/` と `harness-lab/` を、Agent と人間が自然に使える実運用フローにする段階である。

0.2 完了時点で、次ができることを目標にする。

```text
project-repository:
  - plugin/skill 経由で失敗を記録する
  - 失敗を route して upstream/meta feedback に変換する
  - sanitized feedback bundle を作る

target-repository:
  - feedback bundle を harness-lab に import する
  - imported feedback を triage する
  - eval case を作る
  - hypothesis template を作る
  - decision record を残す

HarnessOps repository:
  - 自分自身にも harness-lab を持つ
  - plugin UX に対する feedback を受けられる
```

### 2.2 0.2 で追加する CLI

0.1 の CLI に加えて、0.2 では以下を実装する。

```text
hops profiles discover
hops profiles validate <profile-id-or-path>
hops agent install --codex|--claude --scope repo|user
hops agent verify
hops lab inbox
hops lab triage <feedback-id>
hops lab new-eval-case --from <feedback-id>
hops lab new-hypothesis --from <eval-case-id>
hops lab decide --from <hypothesis-or-experiment-id>
hops views refresh
hops views status
```

### 2.3 `hops profiles discover`

目的: target-repository が提供する harness-owned profile を発見する。

想定:

```text
runops package:
  runops-upstream.yml
  runops-project.yml

paper-harness package:
  paper-harness-upstream.yml
  paper-harness-project.yml
```

Python entry point:

```toml
[project.entry-points."harnessops.profiles"]
runops = "runops.harnessops_profiles:profiles"
paper_harness = "paper_harness.harnessops_profiles:profiles"
```

CLI:

```bash
hops profiles discover
hops profiles list --include-entrypoints
hops profiles show runops-project
hops profiles validate runops-project
```

Acceptance:

```text
- built-in profile と harness-owned profile の両方を表示できる
- local override > harness-owned > built-in の解決順を維持する
- profile fingerprint が lockfile に記録される
- profile schema validation ができる
```

### 2.4 `hops agent install` と plugin packaging

0.2 では、Codex / Claude plugin を first-class にする。ただし、状態変更は CLI に委任する。

```bash
hops agent install --codex --scope repo
hops agent install --codex --scope user
hops agent install --claude --scope repo
hops agent bridge --codex
hops agent bridge --claude
hops agent verify
```

#### 2.4.1 Codex plugin layout

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
    hops-lab-triage/
      SKILL.md
    hops-lab-new-eval-case/
      SKILL.md
    hops-lab-new-hypothesis/
      SKILL.md
    hops-lab-decide/
      SKILL.md
    hops-feedback-meta/
      SKILL.md
```

#### 2.4.2 Claude plugin layout

```text
plugins/claude/harnessops/
  .claude-plugin/
    plugin.json
  skills/
    hops-diagnose/
    hops-add-failure/
    hops-route-feedback/
    hops-export-feedback/
    hops-import-feedback/
    hops-lab-triage/
    hops-lab-new-eval-case/
    hops-lab-new-hypothesis/
    hops-lab-decide/
    hops-feedback-meta/
```

#### 2.4.3 Skill contract

全 skill は以下を守る。

```text
- まず `hops doctor --check-overlay` を実行する
- repository が未linkなら `hops detect` を使う
- `.harnessops/`, `harness-feedback/`, `harness-lab/` の構造を直接再編しない
- record 作成・更新は hops CLI に委任する
- remote issue/PR 作成はしない
- holdout case は触らない
```

### 2.5 `hops lab inbox`

目的: target-repository の `harness-lab/` に入った imported feedback の状態を一覧する。

```bash
hops lab inbox
hops lab inbox --status triaged
hops lab inbox --capability public_terminology
hops lab inbox --json
```

表示項目:

```text
- feedback id
- source
- target capability
- failure class
- status
- linked issue
- eval case linked? yes/no
- hypothesis linked? yes/no
- decision linked? yes/no
```

Generated view:

```text
harness-lab/views/imported-feedback.md
harness-lab/views/backlog.md
```

### 2.6 `hops lab triage`

目的: imported feedback を target-repository 側で分類する。

```bash
hops lab triage FB0001
hops lab triage FB0001 --capability public_terminology --failure-class local_vocabulary_leakage
```

Triage fields:

```yaml
triage:
  status: accepted | duplicate | project-specific | needs-more-info | rejected | external
  capability: public_terminology
  failure_class: local_vocabulary_leakage
  priority: P0 | P1 | P2 | P3
  upstream_scope: template | cli | skill | docs | adapter | profile | test | protocol
  issue_url: null
  eval_case_required: true
  rationale: "..."
```

Acceptance:

```text
- feedback を accepted/rejected/duplicate 等に分類できる
- accepted かつ eval_case_required の場合、eval case 未作成を backlog に出す
- project-specific と判断された feedback は upstream 実装対象にしない
```

### 2.7 `hops lab new-eval-case`

目的: feedback を評価ケースへ変換する。

```bash
hops lab new-eval-case --from FB0001
hops lab new-eval-case --from FB0001 --template public-terminology
hops lab new-eval-case --interactive
```

Output:

```text
harness-lab/records/eval-cases/E0001-public-terminology-leakage.md
harness-lab/records/eval-cases/fixtures/E0001/
```

Eval case frontmatter:

```yaml
id: E0001
record_type: eval_case
status: active
capability: public_terminology
failure_class: local_vocabulary_leakage
source_feedback: FB0001
fixture:
  path: harness-lab/records/eval-cases/fixtures/E0001
  visibility: sanitized
scoring:
  mode: manual
  rubric: public_terminology_basic
```

Eval case body:

```markdown
# E0001: Public terminology leakage should be detected

## Fixture

...

## Task

...

## Expected behavior

...

## Pass criteria

...

## Fail criteria

...

## Regression risk

...
```

### 2.8 `hops lab new-hypothesis`

目的: eval case に対する改善仮説を作る。

```bash
hops lab new-hypothesis --from E0001
hops lab new-hypothesis --from E0001 --n 3
```

0.2 では、LLM 自動生成は必須ではない。テンプレート生成を必須、agent-assisted prompt 出力を optional とする。

Hypothesis fields:

```yaml
id: H0001
record_type: hypothesis
status: proposed
source_eval_cases:
  - E0001
target_capability: public_terminology
change_type: script | skill | template | profile | docs | migration | deletion | consolidation
risk_level: low | medium | high
```

Body:

```markdown
# H0001: Field-aware terminology schema

## Hypothesis

...

## Mechanism

...

## Minimal implementation

...

## Alternative: deletion or consolidation

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

重要: 0.2 から `deletion or consolidation` を必須項目にする。これにより、AI が新機能追加に逃げることを抑制する。

### 2.9 `hops lab decide`

0.2 では experiment runner は未完成でもよい。仮説段階または手動評価段階で decision record を作れるようにする。

```bash
hops lab decide --from H0001 --status parked
hops lab decide --from H0001 --status rejected
hops lab decide --from E0001 --status needs-more-evidence
```

Decision statuses:

```text
adopted
rejected
parked
needs-more-evidence
merged-into-other
not-upstreamable
```

Decision template:

```markdown
---
id: D0001
record_type: decision
status: rejected
source: H0001
created_at: 2026-05-11T00:00:00+09:00
---

# D0001: Reject field-aware terminology schema for now

## Decision

...

## Reason

...

## Evidence considered

...

## Regression risk

...

## What would change this decision

...
```

### 2.10 Adapter-specific doctor checks

0.2 では、adapter が profile-specific な doctor check を返せるようにする。

Examples:

#### runops-project

```text
- .runops/harness.lock exists
- campaign.toml exists
- research/agenda.md exists or profile says optional
- runs/ exists
- harness-feedback/ does not contain raw run workdir files
- feedback records do not include protected paths
```

#### paper-harness-project

```text
- manuscript/ exists
- notes/claim-evidence-map.md exists if profile requires it
- harness-feedback/ does not contain manuscript-private drafts unless visibility marks private
- feedback export targets paper-harness or HarnessOps only unless configured
```

#### upstream-lab

```text
- harness-lab/records/feedback exists
- accepted feedback without eval case is listed in backlog
- eval cases without hypothesis are listed
- adopted decisions link to implementation PR or commit if available
```

### 2.11 0.2 acceptance criteria

0.2 は以下を満たしたら完了とする。

```text
- Codex plugin package が生成・検証できる
- Claude plugin package が生成・検証できる
- repo-local bridge skill と full plugin の差が明確
- harness-owned profiles を entry point から発見できる
- hops lab inbox が feedback backlog を表示できる
- hops lab triage が imported feedback を分類できる
- hops lab new-eval-case が eval case と fixture directory を作れる
- hops lab new-hypothesis が hypothesis record を作れる
- hops lab decide が decision record を作れる
- adapter-specific doctor checks が最低 runops/project, paper/project, upstream-lab に対して動く
- generated views を hops views refresh で再生成できる
- 0.1 overlay から 0.2 overlay へ migrate --apply できる
```

---

## 3. 0.3 の設計: experiment runner と score trajectory

### 3.1 0.3 のゴール

0.3 は、改善仮説を「試した」「よさそう」ではなく、before/after と score で比較できるようにする段階である。

0.3 完了時点の目標:

```text
- hypothesis から experiment を作れる
- experiment の before/after artifacts を保存できる
- eval case を manual / command / agent-assisted で評価できる
- score trajectory を記録できる
- holdout case を管理できる
- accepted improvement が別 case を悪化させていないか見る
```

### 3.2 新規 CLI

```text
hops experiment start --from <hypothesis-id>
hops experiment run <experiment-id>
hops experiment score <experiment-id>
hops experiment compare <experiment-a> <experiment-b>
hops experiment close <experiment-id> --decision adopted|rejected|parked
hops scorecard init
hops scorecard update --experiment <id>
hops scorecard history
hops holdout init
hops holdout add
hops holdout run --experiment <id>
hops report lab
```

### 3.3 Experiment directory structure

```text
harness-lab/records/experiments/X0001-field-aware-terms/
  experiment.md
  plan.md
  before/
    snapshot.json
    artifacts/
  after/
    snapshot.json
    artifacts/
  runs/
    2026-05-11T120000+0900/
      commands.log
      results.yml
      stdout.log
      stderr.log
  scores.yml
  decision.md    # optional symlink or generated link to Dxxxx
```

`experiment.md`:

```yaml
id: X0001
record_type: experiment
status: running
hypothesis: H0001
eval_cases:
  - E0001
runner:
  mode: manual | command | agent-assisted | git-worktree
risk_level: medium
```

### 3.4 Runner modes

#### manual

人間または Agent が結果を記入する。

```bash
hops experiment score X0001 --manual
```

Use when:

```text
- qualitative writing quality
- UX review
- design decision
- early MVP
```

#### command

profile-defined command または eval case command を実行する。

```yaml
evaluation:
  commands:
    - make ci
    - python scripts/check-public-terms.py --fixture harness-lab/records/eval-cases/fixtures/E0001
```

Use when:

```text
- lint / unit test / script check
- fixture-based regression
- generated file comparison
```

#### agent-assisted

Agent にレビューさせるが、scorecard format を固定する。

Rules:

```text
- generator と judge は分けるのが望ましい
- judge prompt は eval case から生成する
- judge は採用判断をしない。score と rationale のみ
- 最終 decision は D record で行う
```

#### git-worktree

将来用。experiment ごとに別 worktree を作る。

```bash
hops experiment start --from H0001 --runner git-worktree
```

0.3 では optional。0.4 以降で安定化する。

### 3.5 Scorecard schema

```yaml
schema_version: "0.3"
experiment: X0001
scores:
  impact:
    score: 4
    rationale: "Addresses repeated terminology leakage failures."
  evaluability:
    score: 5
    rationale: "Fixture has clear expected detection behavior."
  minimality:
    score: 3
    rationale: "Adds schema fields but no new skill."
  regression_risk:
    score: 2
    rationale: "May cause false positives on allowed public terms."
  anti_theater:
    score: 4
    rationale: "Changes executable check, not just docs."
  deletion_or_consolidation_considered:
    score: 1
    rationale: "Consolidated existing terminology fields."
summary:
  recommendation: adopt | reject | park | needs-more-evidence
  confidence: low | medium | high
```

Required score dimensions:

```text
impact
mechanism_clarity
evaluability
minimality
regression_risk
anti_theater
deletion_or_consolidation_considered
```

### 3.6 Score trajectory

Generated view:

```text
harness-lab/views/score-trajectory.md
```

Purpose:

```text
- capability ごとの改善傾向を見る
- 前回より悪化した dimension を検出する
- governance theater 的な改善増殖を検出する
```

Example:

```markdown
# Score trajectory

| Date | Experiment | Capability | Impact | Evaluability | Minimality | Regression risk | Decision |
|---|---|---|---:|---:|---:|---:|---|
| 2026-05-11 | X0001 | public_terminology | 4 | 5 | 3 | 2 | adopted |
```

### 3.7 Holdout case support

0.3 では holdout を導入するが、Agent から簡単に見えない設計にする。

```text
harness-lab/records/holdouts/
  HLD0001-private-case.md
```

または private overlay:

```text
.harnessops/private/holdouts/
```

Rules:

```text
- holdout は通常の propose / hypothesis 生成に使わない
- holdout は final evaluation / regression gate に使う
- holdout path は .gitignore 可能にする
- public target repo では sanitized holdout fixture のみ持つ
```

CLI:

```bash
hops holdout init
hops holdout add --private
hops holdout run --experiment X0001
```

### 3.8 0.3 acceptance criteria

```text
- hypothesis から experiment directory を作れる
- manual runner で scorecard を保存できる
- command runner で profile/eval command を実行できる
- score-trajectory view が生成される
- holdout cases を通常 eval と分離して管理できる
- experiment close から decision record を生成できる
- adopted experiment が linked eval case / hypothesis / decision を持つ
- regression risk が high の場合、decision で明示的な rationale を要求する
```

---

## 4. 0.4 の設計: cross-project knowledge と pattern promotion

### 4.1 0.4 のゴール

0.4 は、複数 project / target で得られた失敗・成功・却下判断を、汎用パターンへ昇格させる段階である。

0.4 完了時点の目標:

```text
- project-local failure を private cross-project knowledge に昇格できる
- private pattern を sanitized public catalog candidate に変換できる
- target-specific feedback と meta-level feedback を分離できる
- recurring failure class を検出できる
- protocol compliance tests を導入できる
```

### 4.2 Private knowledge overlay

HarnessOps 本体に全知識を集約しない。個人・組織の横断知識は private overlay に置く。

Default locations:

```text
~/.harnessops/knowledge/
```

または任意の repo:

```text
harnessops-knowledge/
  knowledge.toml
  records/
    cross-project-failures/
    adopted-principles/
    rejected-patterns/
    promotion-candidates/
  private-holdouts/
```

`.harnessops/project.toml` optional:

```toml
[knowledge]
private_overlay = "../harnessops-knowledge"
```

### 4.3 新規 CLI

```text
hops knowledge init
hops knowledge link <path>
hops knowledge import --from <project-record>
hops knowledge list
hops pattern promote --from <record-id>
hops pattern sanitize --from <promotion-id>
hops pattern publish-candidate --to catalog
hops pattern reject --reason <text>
hops taxonomy suggest
```

### 4.4 Promotion pipeline

```text
project event
  -> harness-feedback failure
  -> target/meta feedback
  -> harness-lab eval/experiment/decision
  -> private cross-project pattern
  -> sanitized public catalog pattern
  -> built-in taxonomy/profile/check
```

Promotion record:

```yaml
id: P0001
record_type: promotion_candidate
source_records:
  - F0001
  - FB0003
  - D0002
pattern_type: failure_class | capability | anti_pattern | scoring_rule | profile_rule
visibility: private
status: candidate
```

Body:

```markdown
# P0001: Project-specific logic leaks into upstream templates

## Observed across

...

## Generalized pattern

...

## Why this is not project-specific

...

## Sanitization requirements

...

## Candidate catalog entry

...
```

### 4.5 Recurring failure detection

CLI:

```bash
hops report recurring-failures
hops report recurring-failures --across ../project-a ../project-b ../runops
```

Detection heuristics:

```text
- same failure_class appears >= N times
- same target capability appears in multiple projects
- same local workaround repeats
- same rejected hypothesis repeats
- feedback exported to same target but no eval case exists
```

### 4.6 Protocol compliance tests

0.4 から `.harness/manifest.toml` と standard CLI conventions の compliance test を追加する。

CLI:

```bash
hops protocol test
hops protocol test --target runops
hops protocol test --target paper-harness
```

Checks:

```text
- .harness/manifest.toml validates schema
- commands.doctor exists and runs if declared
- commands.version returns parseable version if declared
- recommended_profile resolves
- provider/kind/version exist
- target repository can generate project manifest if it implements init
```

0.4 時点では、protocol はまだ HarnessOps repo 内の `specs/` と `schemas/` に置く。独立 repo 化は 1.0 前後で判断する。

### 4.7 0.4 acceptance criteria

```text
- private knowledge overlay を初期化・link できる
- project/target records を private knowledge に import できる
- promotion candidate を作れる
- sanitizer により public catalog candidate を作れる
- recurring failure report が出せる
- protocol test が .harness/manifest.toml を検証できる
- failure-taxonomy.yml に promotion candidate を反映する流れがある
```

---

## 5. 0.5 の設計: operational integration と multi-repo orchestration

### 5.1 0.5 のゴール

0.5 は、HarnessOps を単一 repo のツールから、複数の project / target / private knowledge をまたぐ運用ツールへ拡張する段階である。

0.5 完了時点の目標:

```text
- 複数 project からの feedback inbox を target 側で扱える
- GitHub Issue helper を explicit confirmation 付きで使える
- CI で doctor/eval/protocol test を走らせられる
- plugin marketplace 配布の準備ができる
- optional MCP integration の設計がある
```

### 5.2 Repository registry

```text
~/.harnessops/registry.toml
```

Example:

```toml
[repositories.runops]
path = "/path/to/runops"
kind = "target-repository"
profile = "runops-upstream"

[repositories.paper_harness]
path = "/path/to/paper-harness"
kind = "target-repository"
profile = "paper-harness-upstream"

[repositories.sim_project_a]
path = "/path/to/project-a"
kind = "project-repository"
profile = "runops-project"
```

CLI:

```bash
hops registry add .
hops registry list
hops registry doctor
hops registry report
```

### 5.3 Multi-project feedback inbox

```bash
hops inbox collect --target runops --from-registry
hops inbox collect --target paper-harness --from ../project-a ../project-b
hops inbox report --target runops
```

Output:

```text
harness-lab/views/multi-project-inbox.md
```

Rules:

```text
- collect は sanitized bundles のみ取り込む
- private project details は target repo へ渡さない
- duplicate feedback は candidate duplicate としてまとめる
```

### 5.4 GitHub issue helper

0.5 では Issue 作成補助を入れる。ただし remote action は必ず確認する。

```bash
hops github issue draft --from UF0001
hops github issue create --from UF0001 --confirm
hops github issue import --url <issue-url>
hops github issue link --record FB0001 --url <issue-url>
```

Rules:

```text
- --confirm なしでは作成しない
- body を必ず表示する
- sanitizer pass が必要
- duplicate search を optional で行う
- gh CLI がない場合は markdown draft のみ
```

### 5.5 CI integration

Generated CI snippets:

```bash
hops ci install --github-actions
```

Target repository CI checks:

```text
- hops doctor --check-overlay
- hops views status
- hops protocol test
- hops eval --smoke
```

Project repository CI checks:

```text
- hops doctor --check-overlay
- hops feedback lint --privacy
```

No CI should fail because there are open feedback records. It should fail only for schema/privacy/generated-view issues.

### 5.6 Plugin marketplace preparation

0.5 で plugin packaging を正式化する。

```text
plugins/codex/harnessops/
plugins/claude/harnessops/
```

Validation:

```bash
hops agent package --codex
hops agent package --claude
hops agent verify --all
```

### 5.7 Optional MCP integration

MCP は 0.5 では optional。必須化しない。

Potential MCP tools:

```text
- list_linked_repositories
- read_harnessops_project
- list_feedback_records
- create_failure_record
- export_feedback_bundle
- list_lab_backlog
```

Rules:

```text
- MCP server must call the same core library as CLI
- MCP must not bypass sanitizer
- MCP must not create remote issues without explicit confirmation
```

### 5.8 0.5 acceptance criteria

```text
- registry に複数 repo を登録できる
- registry doctor が各 repo の HarnessOps 状態を確認できる
- target repo が複数 project から feedback を collect できる
- GitHub issue draft/create helper が explicit confirmation 付きで動く
- CI snippet を生成できる
- plugin package verification ができる
- MCP は optional experimental として利用可能、または設計だけ完了
```

---

## 6. 1.0 の設計: stable HarnessOps

### 6.1 1.0 のゴール

1.0 は、HarnessOps を日常運用できる安定ツールとして扱える状態にする。

1.0 で保証するもの:

```text
- CLI の主要コマンド名と意味
- `.harnessops/project.toml` schema compatibility
- `harness-feedback/` と `harness-lab/` の record compatibility
- migration path
- plugin skill contract
- profile resolution order
- sanitizer default behavior
```

### 6.2 安定化対象

Stable:

```text
hops init
hops detect
hops doctor
hops migrate
hops add-failure
hops route
hops feedback export/import
hops lab inbox/triage/new-eval-case/new-hypothesis/decide
hops experiment start/run/score/close
hops views refresh/status
hops agent install/verify
```

Stable directories:

```text
.harnessops/
harness-feedback/
harness-lab/
.harness/manifest.toml
```

Stable record types:

```text
failure
local_workaround
upstream_feedback
meta_feedback
imported_feedback
eval_case
hypothesis
experiment
decision
promotion_candidate
```

### 6.3 `harness-protocol` 分離判断

1.0 時点で以下の条件を満たすなら、`harness-protocol` repo 分離を検討する。

```text
- runops / paper-harness / 第三の target harness が `.harness/manifest.toml` を独立利用している
- HarnessOps なしで common manifest schema を使いたい需要がある
- protocol compliance tests を複数 repo が CI で利用している
- spec release cycle を HarnessOps release cycle と分けたい
```

分離する場合:

```text
harness-protocol/
  specs/
  schemas/
  examples/
  compliance-tests/

HarnessOps/
  depends on harness-protocol
```

分離しない場合:

```text
HarnessOps/specs/
HarnessOps/schemas/
```

を継続する。

### 6.4 1.0 acceptance criteria

```text
- 0.1 -> latest の migration がテスト済み
- runops-project / paper-harness-project / runops-upstream / paper-harness-upstream / harnessops-core fixtures が全て通る
- plugin packages が verify される
- sanitizer の privacy tests が通る
- score trajectory と holdout gate が target repo で実運用できる
- public docs に quickstart / concepts / CLI reference / plugin guide / migration guide がある
```

---

## 7. 0.2 以降のデータモデル変更

### 7.1 `.harnessops/project.toml` 追加フィールド

0.2:

```toml
[agents]
codex_plugin = "harnessops"
claude_plugin = "harnessops"
bridge_installed = true

[views]
path = "harness-lab/views"
auto_refresh = false
```

0.3:

```toml
[evaluation]
default_runner = "manual"
holdout_path = ".harnessops/private/holdouts"
scorecard_schema_version = "0.3"
```

0.4:

```toml
[knowledge]
private_overlay = "~/.harnessops/knowledge"
promotion_policy = "manual"
```

0.5:

```toml
[remote.github]
repo = "Nkzono99/runops"
allow_issue_creation = false
```

### 7.2 `.harnessops/lock.json` 追加フィールド

```json
{
  "schema_version": "0.3",
  "layout_version": "0.3",
  "plugins": {
    "codex": {
      "installed": true,
      "version": "0.2.0",
      "fingerprint": "sha256:..."
    }
  },
  "views": {
    "last_refreshed_at": "2026-05-11T00:00:00+09:00"
  },
  "profiles": {
    "resolution_order": ["local", "entrypoint", "builtin"]
  }
}
```

### 7.3 Views は generated artifact として扱う

```text
harness-feedback/views/**
harness-lab/views/**
```

Rules:

```text
- CLI が再生成してよい
- 人間が編集した場合は stale / conflict として扱う
- records は views より canonical
- views を評価根拠に使う場合、source record link を必須にする
```

---

## 8. Testing strategy for 0.2+

### 8.1 0.2 tests

```text
- profile entry point discovery
- plugin package validation
- agent bridge generation
- lab inbox generation
- triage state transitions
- feedback -> eval case conversion
- eval case -> hypothesis conversion
- hypothesis -> decision conversion
- adapter-specific doctor checks
```

### 8.2 0.3 tests

```text
- experiment directory creation
- manual scorecard write/read
- command runner success/failure
- score trajectory generation
- holdout path isolation
- experiment close creates decision
- high regression risk requires rationale
```

### 8.3 0.4 tests

```text
- private knowledge overlay init/link
- record import into knowledge overlay
- promotion candidate creation
- sanitizer for promotion candidate
- recurring failure report
- protocol test for .harness/manifest.toml
```

### 8.4 0.5 tests

```text
- repository registry add/list/doctor
- multi-project inbox collect
- GitHub issue draft without remote creation
- explicit confirmation required for remote creation
- CI snippet generation
- plugin package verify
```

### 8.5 1.0 tests

```text
- full migration path from 0.1 fixtures
- backwards compatibility tests
- fixture matrix for all profiles
- docs examples executable
- privacy regression tests
```

---

## 9. Documentation roadmap

### 0.2 docs

```text
docs/plugin-first-workflow.md
docs/harness-lab-triage.md
docs/profile-ownership.md
docs/agent-skill-contract.md
```

### 0.3 docs

```text
docs/experiments.md
docs/scorecards.md
docs/holdouts.md
docs/regression-gates.md
```

### 0.4 docs

```text
docs/private-knowledge-overlay.md
docs/pattern-promotion.md
docs/protocol-compliance.md
```

### 0.5 docs

```text
docs/multi-repo-operations.md
docs/github-issue-integration.md
docs/ci-integration.md
docs/plugin-packaging.md
```

### 1.0 docs

```text
docs/stability-policy.md
docs/migration-guide.md
docs/cli-reference.md
docs/schema-reference.md
docs/profile-authoring.md
```

---

## 10. Guardrails and failure modes

### 10.1 Governance theater

Risk:

```text
HarnessOps 自体が docs / rules / skills を増やすだけで、実際の改善能力が上がらない。
```

Guardrails:

```text
- eval case なしの hypothesis は adoption 不可
- decision record に evidence と regression risk を必須化
- scorecard に anti_theater dimension を入れる
- deletion/consolidation alternative を hypothesis に必須化
```

### 10.2 Plugin drift

Risk:

```text
Codex plugin, Claude plugin, CLI の挙動がずれる。
```

Guardrails:

```text
- plugin skill は CLI command だけを呼ぶ
- skill 内に長いロジックを書かない
- hops agent verify で CLI command coverage を確認する
- plugin generated content に fingerprint を持たせる
```

### 10.3 Project/private information leakage

Risk:

```text
project-specific research details が upstream issue や public catalog に漏れる。
```

Guardrails:

```text
- project-side visibility default は private-until-sanitized
- feedback export は sanitizer 必須
- public promotion は sanitized candidate を経由する
- GitHub issue creation は explicit confirmation 必須
```

### 10.4 Metric hacking

Risk:

```text
AI が scorecard に過適合し、実質改善ではなく点数改善を行う。
```

Guardrails:

```text
- scorecard は複数軸にする
- holdout cases を分離する
- human decision record を必須にする
- single aggregate score だけで採用しない
```

### 10.5 Upstream contamination

Risk:

```text
project-specific workaround が target-repository の template に混ざる。
```

Guardrails:

```text
- feedback import 時に project-specific 判定を必須化
- target-side triage に upstream_scope を持たせる
- profile.private_paths / protected_paths を sanitizer が読む
- decision に “why upstreamable” を必須化する
```

---

## 11. 推奨実装順

### Phase A: 0.2 core

```text
1. profile entry point discovery
2. plugin package skeleton
3. agent install / verify
4. lab inbox
5. lab triage
6. new-eval-case
7. new-hypothesis
8. lab decide
9. adapter doctor checks
10. views refresh/status
```

### Phase B: 0.3 experiment

```text
1. experiment start
2. manual runner
3. command runner
4. scorecard schema
5. score trajectory view
6. holdout storage
7. holdout run
8. experiment close -> decision
```

### Phase C: 0.4 knowledge

```text
1. private knowledge overlay
2. knowledge import
3. promotion candidate
4. sanitize promotion
5. recurring failure report
6. protocol test
```

### Phase D: 0.5 operations

```text
1. repository registry
2. multi-project feedback inbox
3. GitHub issue draft helper
4. CI snippet generation
5. plugin package verification
6. optional MCP design/experimental implementation
```

### Phase E: 1.0 stabilization

```text
1. migration compatibility test matrix
2. stable CLI reference
3. stable schema reference
4. plugin compatibility policy
5. protocol split decision
6. release candidate
```

---

## 12. 0.2+ の最終設計判断

1. 0.2 は plugin-first UX と lab workflow を完成させる。
2. 0.3 は experiment runner と score trajectory を導入する。
3. 0.4 は cross-project knowledge と pattern promotion を導入する。
4. 0.5 は multi-repo operations と GitHub/CI/plugin packaging を実運用化する。
5. 1.0 は schema/CLI/plugin contract の安定化を行う。
6. `hops` CLI は常に authoritative state engine であり、plugin は thin orchestration layer とする。
7. `harness-feedback/` は project 側の観測・送信用、`harness-lab/` は target/meta 側の評価・実験用という境界を維持する。
8. project evolution は `research/` や `notes/` に残し、HarnessOps は harness feedback の分類・移送・評価を管理する。
9. common protocol は 1.0 までは HarnessOps 内で管理し、外部採用が進んだ場合のみ `harness-protocol` へ分離する。
