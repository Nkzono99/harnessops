# Target Repository向け HarnessOps 組み込みブリーフ

この文書は、target repository へ HarnessOps を組み込むAI Agentにそのまま渡すための指示書です。target repository 側のAgentは、この文書だけを読んで、必要な確認、初期化、検証、差分報告まで進めてください。

コード開発プロジェクト、研究プロジェクト、生成済みプロジェクトなど、project repository単体へ HarnessOps を入れる場合は `docs/project-repository-integration-agent-brief.md` を使ってください。

## Agentへの依頼文

対象リポジトリで、次の依頼とこの文書を渡してください。

```text
このリポジトリに HarnessOps を組み込んでください。
添付の target-integration-agent-brief.md に従い、リポジトリ種別を判定し、適切な profile で初期化し、doctor/migrate まで検証してください。
既存ファイルを安全でなく上書きせず、未サニタイズ情報を外部へ出さず、最後に作成ファイル・検証結果・残課題を報告してください。
```

## 前提: target repository と project repository

HarnessOps では、target repository と project repository を分けます。

| 種別 | 例 | 役割 | HarnessOps overlay |
|---|---|---|---|
| target repository | `runops`, `paper-harness`, 社内のプロジェクト生成CLI | プロジェクトを作成・更新する上流ハーネス本体。テンプレート、CLI、検証ロジック、生成器を持つ。 | `harness-lab/` |
| project repository | target CLIが `init` などで作成した実利用プロジェクト | 研究、論文、解析、コード開発などの現場。失敗や回避策を観測する。 | `harness-feedback/` |

この文書では、target repository がCLIの `init` などで project repository を作成する構成を前提にします。

例:

```text
runops repository
  `runo init` で runops project repository を作成する

paper-harness repository
  `paper-harness init` で paper project repository を作成する
```

target repository に HarnessOps を入れる目的は、project repository から送られてくるサニタイズ済みフィードバックを `harness-lab/` に取り込み、評価ケース、仮説、判断へ変換することです。

target repository に `harness-feedback/` を作らないでください。project repository側の観測・送信用overlayは、project repositoryで別途作成します。

## 目的

HarnessOps をtarget repositoryに追加し、AI Agentが受け取ったフィードバック、評価ケース、改善仮説、採用判断を `hops` CLI経由で扱える状態にします。

組み込み後の状態:

- target repository に `harness-lab/` がある。
- `.harness/manifest.toml` がある。
- `.harnessops/project.toml` と `.harnessops/lock.json` がある。
- `hops doctor --check-overlay --check-records` が通る。
- 必要に応じて repo-local HarnessOps skill が `.agents/skills/` にある。

## 絶対ルール

- 状態変更は `hops` または `harnessops` CLIを通す。
- `.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を手作業で再設計しない。
- 既存ファイルを安全でなく上書きしない。
- 未サニタイズのフィードバックを外部Issue、PR、公開文書に貼らない。
- GitHub Issue、Pull Request、pushなどのリモート操作はユーザー確認なしに行わない。
- project-specific な研究判断や論文主張を `harness-feedback/` に移さない。
- target repository に project repository用の `harness-feedback/` を作らない。

## 事前確認

対象リポジトリで次を確認します。

```bash
pwd
git status --short --branch
```

未コミット変更があっても勝手に戻しません。HarnessOps組み込みに関係ない変更は触りません。

## HarnessOps CLIの実行方法

対象環境に `hops` が入っているなら、そのまま使います。未導入またはクリーンな一回実行が必要なら、PyPI の `harnessops` パッケージから `uvx` で実行します。

```bash
hops --help
```

対象リポジトリから次の形式で実行します。

```bash
uvx --isolated --from harnessops hops --help
uvx --isolated --from harnessops hops detect
```

以降の例で `hops` と書かれている箇所は、必要に応じて次に読み替えます。

```bash
uvx --isolated --from harnessops hops <command>
```

## Profile選択

まず検出を実行します。

```bash
hops detect
hops detect --json
```

検出結果が明確なら、そのprofileを使います。判断に迷う場合は次の表を使います。

| 対象 | profile | overlay |
|---|---|---|
| runops の上流実装リポジトリ | `runops-upstream` | `harness-lab/` |
| paper-harness の上流実装リポジトリ | `paper-harness-upstream` | `harness-lab/` |
| 汎用target harnessリポジトリ | `target-harness` | `harness-lab/` |
| HarnessOps 自身 | `harnessops-core` | `harness-lab/` |

target repository に組み込む依頼なら、通常は `*-upstream` または `target-harness` を選びます。

## 初期化

profileが決まったら初期化します。

```bash
hops init --profile <profile-id>
```

repo-local skillも入れる場合:

```bash
hops init --profile <profile-id> --with-agent-bridge
```

すでに初期化済みの場合は、むやみに `--force` を使いません。まず検証します。

```bash
hops doctor --check-overlay --check-records
hops migrate --check
```

生成ファイルが編集済みで `init` が拒否した場合は、拒否を尊重して停止し、どのファイルが競合したか報告します。

## target CLIのlifecycleへ組み込む場合

target repository の `init`、`setup`、`update-harness` などに HarnessOps 連携を入れる場合は、target CLI が `.harnessops/`、`harness-feedback/`、`harness-lab/` を直接書かず、`hops` を呼び出す境界にします。

project repository を生成する `init` の後処理:

```bash
hops init --profile <target-project-profile>
hops doctor --check-overlay --check-records
```

target repository 自身の `setup`:

```bash
hops init --profile <target-upstream-profile>
hops doctor --check-overlay --check-records
```

`update-harness`:

```bash
hops update-harness
```

`hops update-harness` は `hops doctor --check-overlay --check-records` と `hops migrate --check` 相当の確認を含みます。編集済みmanaged fileは runops と同様に `<path>.new` へ書き、元ファイルを保持します。

未適用migrationを適用する場合は、target CLI 側の明示フラグまたは人間確認を通してから `hops update-harness --apply-migrations` または `hops migrate --apply` を呼びます。`hops init --force` や migration 適用を暗黙に実行しないでください。

repo-local skill 展開は対象repoの状態なので、明示オプションで入れてかまいません。

```bash
hops agent bridge --codex
```

これにより `.agents/skills/hops-issue-triage/` などが対象repoに入ります。Codex は既存セッションへskillを後から注入しないため、新しい Codex セッションを開いて確認してください。

Agent plugin のユーザー領域インストールはグローバル副作用なので、target/project lifecycle から暗黙に実行しません。複数repoで同じglobal pluginを共有したい場合だけ任意手順として案内します。

## feedback/triageを移行する場合

target repository に既存の `feedback` や `triage` skill がある場合、共通処理は HarnessOps へ寄せます。

- record schema、routing、sanitize、export/import は `hops` に委譲する。
- target skill は domain diagnosis に限定する。
- 既存 skill は移行期だけ thin wrapper として残す。
- domain-specific failure class、protected path、triage skill 名は profile の `domain_triage` に置く。

悪い例:

```text
feedback-runops が独自に records/ を作る。
feedback-paper-harness が独自 sanitizer を持つ。
```

良い例:

```bash
hops add-failure --target runops ...
hops route --record F0001
hops add-feedback --from F0001 --target runops
hops feedback export --target runops --sanitize
```

## target repositoryで確認すること

target repository の場合、次があることを確認します。

```text
.harness/manifest.toml
.harnessops/project.toml
.harnessops/lock.json
harness-lab/README.md
harness-lab/records/feedback/
harness-lab/records/eval-cases/
harness-lab/records/hypotheses/
harness-lab/records/experiments/
harness-lab/records/decisions/
harness-lab/knowledge/
harness-lab/views/
```

`harness-lab/` は上流改善の評価と判断の記憶です。通常のタスク管理はGitHub Issuesなど既存の仕組みに残します。メタ改善調査で複数候補が出た場合は `hops lab research-scan` で evidence、candidate、recommendation、next command を構造化します。lab が大きくなったら `hops lab compact` または `hops lab compact --force` で、records/dossier を残したまま `harness-lab/knowledge/` の作業記憶を更新します。
外部バンドルや issue がまだないローカル改善観測は、`hops lab capture --title <title> --summary <summary> --expected-change <expected>` で `FB` レコードにしてから、評価ケース、仮説、判断へ進めます。

## プライバシー設定

非公開語、保護パス、ローカルパスが分かっている場合は、`.harnessops/sanitize.yml` を提案または作成します。

```yaml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - internal-method-name
```

対象profileに `private_paths` や `protected_paths` がある場合は、それを尊重します。

## 組み込み後の検証

最低限、次を実行します。

```bash
hops doctor --check-overlay --check-records
hops migrate --check
```

Python packageやテスト環境がある場合は、そのリポジトリの通常テストも実行します。例:

```bash
python -m pytest -q
```

PyPI の `harnessops` パッケージから実行する場合:

```bash
uvx --isolated --from harnessops hops doctor --check-overlay --check-records
uvx --isolated --from harnessops hops migrate --check
```

## 受け入れ条件

組み込み完了と判断できる条件:

- 適切なprofileで `.harnessops/project.toml` が作成されている。
- `.harness/manifest.toml` が作成されている。
- target repository に `harness-lab/` が作成されている。
- target repository に project repository用の `harness-feedback/` を作っていない。
- `.harnessops/lock.json` が生成ファイルだけを管理している。
- `hops doctor --check-overlay --check-records` が通る。
- `hops migrate --check` が未適用マイグレーションなしを報告する。
- 既存の人間作成ファイルを安全でなく上書きしていない。
- リモートIssue/PR/pushを作成していない。

## 最終報告フォーマット

作業後、Agentは次の形式で報告します。

```text
HarnessOps 組み込み結果:
- 対象リポジトリ:
- 判定した種別:
- 使用profile:
- 作成/更新した主なファイル:
- 実行した検証:
- 検証結果:
- 触らなかった既存変更:
- 残課題:
```

## 失敗時の扱い

次の場合は無理に進めず、人間へ確認します。

- profile選択が曖昧。
- 既存の `.harnessops/project.toml` と新しい判定が矛盾する。
- 生成ファイルの上書きを `hops` が拒否した。
- private terms や protected paths が不明なまま外部共有が必要。
- target repository なのか project repository なのか判断できない。この場合は、この文書ではなく `docs/project-repository-integration-agent-brief.md` が適切か確認する。
