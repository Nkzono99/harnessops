# HarnessOps 現行仕様

バージョン: 0.1  
対象: `harnessops` Pythonパッケージ / `hops` CLI / HarnessOpsオーバーレイ  
状態: 現行実装の正本仕様

## 目的

HarnessOps は、AI Agent が出す改善候補を、失敗、フィードバック、評価ケース、仮説、スコアカード、判断履歴へ接続するための運用基盤です。

改善案の生成そのものはAIが担えます。HarnessOps の責務は、生成された候補を証拠で選別し、採用・却下・保留を後から追跡できる形で残すことです。

標準ループ:

```text
failure / feedback observation
  -> routing / disposition
  -> upstream or meta feedback
  -> eval case
  -> improvement hypothesis
  -> manual scorecard
  -> decision
```

## 非目標

HarnessOps は次をしません。

- プロジェクトの研究内容、論文主張、実験方向性そのものを決める。
- target-repository のドメイン固有設計を肩代わりする。
- GitHub Issues や Pull Requests をユーザー確認なしに作成する。
- すべての project evolution を `harness-feedback/` に集約する。
- AI の自己評価だけで改善を採用する。

## 中核原則

- 自己改善の中心は生成ではなく選別である。
- 失敗は資産であり、改善案は仮説である。
- 仮説にはメカニズム、評価計画、中止基準が必要である。
- 採用判断には証拠、回帰リスク、ガードパスが必要である。
- project-specific な事情は、サニタイズと評価を経るまで上流テンプレートやメタプロトコルへ混ぜない。
- AgentやpluginはUX層であり、状態変更の正本は常に `hops` CLIである。

## リポジトリ役割

| 役割 | 例 | 標準オーバーレイ | 責務 |
|---|---|---|---|
| project-repository | runops生成プロジェクト、論文プロジェクト | `harness-feedback/` | 現場で観測した失敗、ローカル回避策、上流/メタフィードバック候補を記録する。 |
| target-repository | `runops`, `paper-harness` | `harness-lab/` | 受け取ったフィードバックを評価ケース、仮説、判断に変換する。 |
| HarnessOps repository | `HarnessOps` | `harness-lab/` | HarnessOps 自身のCLI、スキーマ、profile、adapter、plugin workflowを改善する。 |

`project-repository` の研究方針、論文主張、実験転換は `research/` または `notes/` に残します。`harness-feedback/` は、ハーネスや上流へ戻すべき観測だけを扱います。

## ディレクトリ契約

### `harness-feedback/`

project-repository に置くプロジェクト側オーバーレイです。

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

### `harness-lab/`

target-repository と HarnessOps repository に置く評価側オーバーレイです。

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

### `.harnessops/`

HarnessOps の隠しメタデータです。

```text
.harnessops/
  project.toml
  lock.json
  migrations/
  cache/
  sanitize.yml   # 任意
```

### `.harness/manifest.toml`

プロバイダ中立の共通マニフェストです。HarnessOps 固有ではありませんが、検出とprofile hintに使います。

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

## `.harnessops/project.toml`

HarnessOps linkの正本です。

```toml
schema_version = "0.1"
layout_version = "0.1"

[project]
name = "my-project"
root = "."
kind = "project-repository"

[profile]
id = "runops-project"
version = "0.1.0"
source = "builtin"
adapter = "runops_project"

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

## オーバーレイモード

| mode | 対象 | 生成ディレクトリ | 目的 |
|---|---|---|---|
| `feedback-source` | project-repository | `harness-feedback/` | 観測、回避策、上流/メタフィードバックを扱う。 |
| `local-and-feedback` | project-repository | `harness-feedback/` | `feedback-source` に加えてローカル運用実験を扱う。 |
| `upstream-lab` | target-repository | `harness-lab/` | フィードバックを評価し、仮説と判断を残す。 |
| `meta-lab` | HarnessOps repository | `harness-lab/` | HarnessOps 自身の改善を評価する。 |

既定の対応:

```text
profile id ending in -project   -> feedback-source
profile id ending in -upstream  -> upstream-lab
profile id harnessops-core      -> meta-lab
```

## Profile

profile は検出、初期化、検証、ルーティング、サニタイズの設定を持ちます。

解決順:

```text
local override > harness-owned entry point > built-in profile
```

現行の組み込みprofile:

- `generic-code`
- `python-package`
- `target-harness`
- `runops-project`
- `runops-upstream`
- `paper-harness-project`
- `paper-harness-upstream`
- `harnessops-core`

profile は少なくとも次を表現します。

- `id`, `version`, `adapter`, `mode`
- `root_markers`
- `feedback.path`
- `project_evolution`
- `state_roots`
- `quality_commands`
- `capabilities`
- `failure_classes`
- `protected_paths`
- `private_paths`
- `upstream_targets`

## レコード

レコードは YAML frontmatter 付きMarkdownです。frontmatter は機械検証対象、本文は人間向けの証拠と根拠です。

ID規約:

| prefix | record_type | 場所 |
|---|---|---|
| `F` | `failure` | `harness-feedback/records/failures/` |
| `LW` | `local_workaround` | `harness-feedback/records/local-workarounds/` |
| `UF` | `upstream_feedback` | `harness-feedback/records/upstream-feedback/` |
| `MF` | `meta_feedback` | `harness-feedback/records/meta-feedback/` |
| `FB` | `imported_feedback` | `harness-lab/records/feedback/` |
| `E` | `eval_case` | `harness-lab/records/eval-cases/` |
| `H` | `hypothesis` | `harness-lab/records/hypotheses/` |
| `X` | `experiment` | `harness-lab/records/experiments/` |
| `D` | `decision` | `harness-lab/records/decisions/` |

共通ルール:

- `id`, `record_type`, `created_at` は必須。
- ID prefix は `record_type` と一致する。
- `records/` 配下の履歴は人間が読む正本であり、ビュー更新で再生成しない。
- 生成ビューは正本ではなく、更新される場合がある。
- 証拠を持つ成果物に未解決の `TODO` を残さない。

必須本文セクション:

| record_type | 必須セクション |
|---|---|
| `failure` | 文脈、起きたこと、重要性、望ましい挙動、ローカル回避策、ルーティング根拠 |
| `upstream_feedback` / `meta_feedback` | 概要、最小再現、期待する上流改善、除外した非公開情報 |
| `imported_feedback` | 概要、再現、期待する上流変更 |
| `eval_case` | フィクスチャ、タスク、期待される挙動、合格基準、不合格基準 |
| `hypothesis` | 仮説、メカニズム、最小実装、代替案: 削除または統合、期待される利点、想定される欠点、評価計画、中止基準 |
| `decision` | 判断、理由、証拠、回帰リスク、フォローアップ、回帰ガード |

## ルーティング

分類値:

| 分類値 | 意味 |
|---|---|
| `project-evolution` | 研究方針、論文主張、実験内容などプロジェクト自体の変化。 |
| `project-local-process` | プロジェクト固有のプロセスまたは回避策。 |
| `target-upstream-candidate` | target harness が変更を検討すべき内容。 |
| `meta-harness-candidate` | HarnessOps のスキーマ、CLI、ルーティング、マイグレーション、pluginの不足。 |
| `protocol-candidate` | `.harness/manifest` または共通CLI規約の不足。 |
| `external-candidate` | クラスタ、シミュレータ、ジャーナルなど外部システムの問題。 |
| `do-not-upstream` | 明示的にローカルまたは非公開。 |

1つのイベントが複数の意味を持つ場合は、1つの分類値へ押し込まず、プロジェクトレコードと上流/メタフィードバックに分割します。

## Feedbackとtriageの責務境界

feedback の記録、分類、サニタイズ、エクスポート/インポートは HarnessOps の共通責務です。target harness はこの流れを再実装せず、domain 固有の判断材料と thin wrapper だけを提供します。

HarnessOps が管理するもの:

- `harness-feedback/` と `harness-lab/` のレコードスキーマ。
- failure、upstream/meta feedback、imported feedback の作成・検証。
- disposition の保存、routing evidence、local/upstream/meta/external/private の分離。
- sanitizer、feedback bundle、export/import。
- imported feedback から eval case、hypothesis、decision へ進む共通ラボフロー。
- repo-local skill と Codex / Claude plugin のCLI委譲契約。

target repository が提供するもの:

- `runops-project`、`paper-harness-project` などの profile。
- domain-specific failure class、capability、protected/private path。
- runops や paper-harness 固有の triage skill。
- target CLI の `init` / `setup` / `update-harness` から `hops` を呼ぶ lifecycle hook。
- 必要なら既存 `feedback-*` skill を HarnessOps CLI へ委譲する thin wrapper。

triage は次の3層に分けます。

| 層 | 正本 | 目的 |
|---|---|---|
| meta routing triage | HarnessOps | project-local、target-upstream、meta-harness、protocol、external、private の分類。 |
| domain diagnosis triage | target repository | runops の campaign/Slurm/manifest/adapter 判断や paper-harness の claim/citation/venue/terminology 判断。 |
| lab triage | HarnessOps + target profile | imported feedback を eval case、backlog、reject、issue draft へ振り分ける。 |

target 側の `feedback` / `triage` skill は、独自に `records/` を作ったり sanitizer を持ったりしません。移行期は `hops add-failure`、`hops route`、`hops add-feedback`、`hops feedback export --sanitize` を呼ぶ wrapper として残します。

`hops feedback add --target <target>` は将来の ergonomic alias として予約できますが、現行の正本コマンドは `hops add-failure` と `hops add-feedback --from <Fid>` です。

## CLI

`hops` が主要エイリアス、`harnessops` が長いエイリアスです。状態変更はCLIが正本です。

現行コマンド:

| コマンド | 状態変更 | 目的 |
|---|---:|---|
| `hops version` | いいえ | バージョン表示。 |
| `hops profiles list/show` | いいえ | 組み込みprofile確認。 |
| `hops detect` | いいえ | repository kind と推奨profileの推定。 |
| `hops init --profile <id>` | はい | `.harness/`, `.harnessops/`, overlay の作成。 |
| `hops link --profile <id>` | はい | 既存リポジトリを HarnessOps にリンク。 |
| `hops doctor` | いいえ | link、overlay、lock、recordの検証。 |
| `hops migrate --check/--apply` | `--apply` のみ | layout migrationの確認または適用。 |
| `hops update-harness` | はい | managed file、migration確認、repo-local skill展開を現在の `hops` 実装に合わせる。編集済みmanaged fileは `<path>.new` に退避。 |
| `hops add-failure` | はい | project側失敗レコード作成。 |
| `hops add-feedback --from <Fid>` | はい | 上流/メタフィードバック下書き作成。 |
| `hops route --record <id>` | はい | record dispositionの分類保存。 |
| `hops feedback export --sanitize` | はい | サニタイズ済みフィードバックバンドル生成。 |
| `hops feedback import <bundle>` | はい | `harness-lab` へフィードバックをインポート。 |
| `hops lab new-eval-case --from <FBid>` | はい | imported feedback を評価ケース化。 |
| `hops propose --from <Eid>` | はい | 仮説テンプレート作成。 |
| `hops eval --case <Eid> --manual` | はい | 手動多軸スコアカード保存。 |
| `hops decide --from <id> --status <status>` | はい | 採用、却下、保留などの判断を記録。 |
| `hops agent bridge/install/verify` | bridge/installのみ | repo-local skill展開と任意plugin成果物の管理。 |
| `hops report` | いいえ | 簡潔なrepository report表示。 |

## Target harness lifecycle連携

target harness の `init`、`setup`、`update-harness` などのライフサイクルコマンドは、HarnessOps を直接内包せず、`hops` を呼び出す委譲境界として実装します。

原則:

- target harness は `.harnessops/`、`harness-feedback/`、`harness-lab/` を直接生成・再編しない。
- project repository を生成する `init` は、生成先で `hops init --profile <target-project-profile>` と `hops doctor --check-overlay --check-records` を呼ぶ。
- target repository 自身の `setup` は、target repo で `hops init --profile <target-upstream-profile>` と `hops doctor --check-overlay --check-records` を呼ぶ。
- `update-harness` は `hops update-harness` を基本にする。これは `hops doctor --check-overlay --check-records` と `hops migrate --check` 相当の確認を含み、編集済みmanaged fileは runops と同様に `<path>.new` へ退避する。
- migration適用は明示オプションまたは人間確認後に `hops update-harness --apply-migrations` または `hops migrate --apply` で行う。
- target harness は通常 `hops init --force` を自動実行しない。生成ファイル競合や危険な上書き拒否は上位コマンドで報告して停止する。
- repo-local skill展開は対象repoの状態なので、`--with-agent-bridge` や target CLI 側の明示オプションで入れてよい。
- user領域のAgent plugin installはグローバル副作用なので、target/project lifecycleの暗黙処理に含めない。複数repoで同じglobal pluginを使う場合だけ、任意手順として案内する。

例:

```bash
# target CLI が project repository を生成した後、生成先で実行する
hops init --profile runops-project
hops doctor --check-overlay --check-records

# target repository 自身のsetupで実行する
hops init --profile runops-upstream
hops doctor --check-overlay --check-records

# update-harnessで実行する
hops update-harness
```

終了コード:

| code | 意味 |
|---:|---|
| 0 | 成功 |
| 1 | 検証または使用方法エラー |
| 2 | 危険な上書きまたはinstall競合の防止 |
| 3 | profile未検出または未指定 |

## プライバシーとサニタイズ

project側フィードバックの既定可視性は `private-until-sanitized` です。`hops feedback export` は、`--allow-private` が明示されない限り未サニタイズ出力を拒否します。

サニタイザは次を扱います。

- ローカル絶対パス
- `/LARGE...` などの環境固有パス
- クラスタ名
- `.harnessops/sanitize.yml` の `redact_patterns`
- `.harnessops/sanitize.yml` の `private_terms`
- profile の `private_paths`
- profile の `protected_paths`

任意設定:

```yaml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - internal-method-name
```

## Agent SkillとPluginの契約

標準ルートは、`hops init --with-agent-bridge` または `hops agent bridge --codex` による repo-local skill 展開です。Codex / Claude plugin は、複数repoで同じグローバル入口を使いたい場合の任意UX層です。どちらも状態変更は `hops` に委譲します。

必須契約:

- 最初に `hops doctor --check-overlay` を実行する。
- 未リンクなら `hops detect` と `hops init --profile <id>` を使う。
- `.harnessops/`, `harness-feedback/`, `harness-lab/` の構造を直接再編しない。
- レコード作成・更新はCLIに委譲する。
- リモートIssue/PRは自動作成しない。
- holdoutや非公開文脈を通常ワークフローへ露出しない。

## ロックとマイグレーション

`.harnessops/lock.json` は生成ファイルだけを追跡します。人間が作成したレコードは `managed_files` に含めません。

ルール:

- 生成ビューは再生成可能。
- 管理対象ファイルのhashがlockと異なる場合、`init` やmigrationは上書きを拒否する。
- `--force` でも、既存hashと合わない場合は競合コピーを書いて停止する。
- migration は人間が作成したレコードを削除しない。

## テストと受け入れ条件

現行実装は次を満たす必要があります。

- `hops --help` が動作する。
- `hops init --profile runops-project` が `.harnessops/` と `harness-feedback/` を作成する。
- `hops init --profile runops-upstream` が `.harnessops/` と `harness-lab/` を作成する。
- `hops detect` が最小fixtureのprofileを識別する。
- `hops doctor --check-overlay --check-records` が初期化直後に通る。
- `hops add-failure` が有効なfailureレコードを作る。
- `hops route` が分類値を保存する。
- `hops feedback export --sanitize` がサニタイズ済みバンドルを書く。
- `hops feedback import` が `harness-lab` にfeedbackレコードを作る。
- `hops lab new-eval-case` が評価ケースとfixture directoryを作る。
- `hops propose` が中止基準を含むhypothesisレコードを作る。
- `hops eval --manual` がscorecardを保存する。
- `hops decide --status adopted` は証拠、回帰リスク、ガードパスなしでは失敗する。
- 生成ファイルのユーザー編集を安全でなく上書きしない。
- repo-local skill と Codex/Claude plugin はCLI委譲の薄い契約を守る。

標準確認:

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uv run --with-editable . hops doctor --check-overlay --check-records
uv run --with-editable . hops migrate --check
```

## 補助仕様

このファイルが現行仕様の正本です。より細かい補助仕様は `specs/` にあります。

- `specs/cli-spec.md`
- `specs/feedback-routing-spec.md`
- `specs/harness-common-spec.md`
- `specs/harnessops-overlay-spec.md`
- `specs/profile-spec.md`
- `specs/record-schemas.md`

設計思想は `docs/design-principles.md`、将来ロードマップは `docs/roadmap.md` に分離します。
target repository へ HarnessOps を組み込むAgentへ渡す文書は `docs/target-integration-agent-brief.md` です。
