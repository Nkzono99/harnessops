# HarnessOps ロードマップ

この文書は将来設計の整理です。現行仕様の正本は `SPEC.md` です。

## 0.1: 現行実装

中心テーマ: bootstrap / feedback routing / 最小ラボワークフロー

現行で扱うもの:

- PythonパッケージとCLI entry points: `harnessops`, `hops`
- 組み込みprofile
- `.harness/manifest.toml`
- `.harnessops/project.toml`
- `.harnessops/lock.json`
- `harness-feedback/` 生成
- `harness-lab/` 生成
- `detect`, `init`, `doctor`, `migrate`
- `add-failure`, `route`
- `feedback export --sanitize`, `feedback import`
- `lab new-eval-case`
- `propose`
- `eval --manual`
- `decide`
- repo-local HarnessOps skills
- Codex / Claude plugin package as optional global UX

意図的にまだ扱わないもの:

- 自動LLM判定
- 自動GitHub Issue / PR作成
- 本格的experiment runner
- holdout gate
- multi-repo orchestration
- external protocol repository

## 0.2: repo-local skill-first UX と harness-lab 実用化

目的: Agent と人間が自然に `harness-feedback/` と `harness-lab/` を使えるようにする。

導入済みの足場:

- `hops lab capture` から始まるローカル改善記録

候補機能:

- `hops profiles discover`
- `hops profiles validate <profile-id-or-path>`
- `hops feedback add --target <target>` as alias for the add-failure/add-feedback flow
- `hops lab inbox`
- `hops lab triage <feedback-id>`
- `hops lab new-hypothesis --from <eval-case-id>`
- `hops lab decide --from <hypothesis-or-experiment-id>`
- `hops views refresh`
- `hops views status`
- adapter-specific doctor checks
- harness-owned profiles via entry points
- profile `domain_triage` hooks for target-specific diagnostic skills

0.2の設計では、repo-local skill展開をfirst-classにします。pluginは複数repoで共有する任意UXとし、どちらも状態を持たず、必ず `hops` CLIへ委譲します。

## 0.3: experiment runner とスコア推移

目的: 改善仮説を「よさそう」ではなく before/after とscoreで比較できるようにする。

候補機能:

- `hops experiment start --from <hypothesis-id>`
- `hops experiment run <experiment-id>`
- `hops experiment score <experiment-id>`
- `hops experiment compare <experiment-a> <experiment-b>`
- `hops experiment close <experiment-id> --decision adopted|rejected|parked`
- `hops scorecard history`
- `hops holdout init/add/run`
- `hops report lab`

runner mode:

- `manual`
- `command`
- `agent-assisted`
- `git-worktree`

スコア推移は `harness-lab/views/score-trajectory.md` に生成し、capabilityごとの改善傾向、悪化したdimension、governance theaterを検出します。

holdout は通常の仮説生成には使わず、採用前の最終確認と回帰ガードに使います。

## 0.4: cross-project knowledge とパターン昇格

目的: 複数project / targetで得られた失敗、成功、却下判断を汎用パターンへ昇格する。

候補機能:

- private knowledge overlay
- `hops knowledge init/link/import/list`
- `hops pattern promote`
- `hops pattern sanitize`
- `hops pattern publish-candidate --to catalog`
- `hops report recurring-failures`
- `hops protocol test`

promotion pipeline:

```text
project event
  -> harness-feedback failure
  -> target/meta feedback
  -> harness-lab eval/experiment/decision
  -> private cross-project pattern
  -> sanitized public catalog pattern
  -> built-in taxonomy/profile/check
```

0.4時点でも、protocolは HarnessOps repository 内の `specs/` と `schemas/` に置く想定です。

## 0.5: operational integration とmulti-repo orchestration

目的: 単一リポジトリのツールから、複数project / target / private knowledgeをまたぐ運用ツールへ拡張する。

候補機能:

- repository registry
- multi-project feedback inbox
- GitHub issue draft/create helper
- CI snippet generation
- repo-local skill package verification
- optional plugin package verification
- optional MCP integration

remote action の原則:

- `--confirm` なしでは作成しない。
- bodyを必ず表示する。
- sanitizer passを必須にする。
- duplicate searchは任意。
- `gh` がない場合はmarkdown draftのみ。

## 1.0: stable HarnessOps

1.0で安定化するもの:

- CLIの主要コマンド名と意味
- `.harnessops/project.toml` schema compatibility
- `harness-feedback/` と `harness-lab/` のrecord compatibility
- migration path
- repo-local skill and plugin contract
- profile resolution order
- sanitizer default behavior

stable directory:

- `.harnessops/`
- `harness-feedback/`
- `harness-lab/`
- `.harness/manifest.toml`

## `harness-protocol` 分離判断

1.0前後で、次の条件を満たすなら `harness-protocol` repository の分離を検討します。

- 複数のtarget harnessが `.harness/manifest.toml` をHarnessOpsなしで独立利用している。
- common manifest schema を外部で使いたい需要がある。
- protocol compliance tests を複数repoがCIで利用している。
- spec release cycle を HarnessOps release cycle と分ける必要がある。

条件を満たすまでは、common protocol は HarnessOps 内で管理します。

## 将来機能のガードレール

- eval case なしのhypothesisは採用不可。
- decision record に evidence、regression risk、guard pathを必須化する。
- scorecard に anti_theater dimensionを残す。
- deletion/consolidation alternativeをhypothesisに残す。
- repo-local skillとplugin skillはCLI commandだけを呼ぶ。
- public promotionはsanitized candidateを経由する。
- single aggregate scoreだけで採用しない。
- project-specific workaroundをtarget templateへ混ぜない。
