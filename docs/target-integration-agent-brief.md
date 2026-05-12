# Target Repository向け HarnessOps 組み込みブリーフ

この文書は、target repository や既存プロジェクトへ HarnessOps を組み込むAI Agentにそのまま渡すための指示書です。対象リポジトリ側のAgentは、この文書だけを読んで、必要な確認、初期化、検証、差分報告まで進めてください。

## Agentへの依頼文

対象リポジトリで、次の依頼とこの文書を渡してください。

```text
このリポジトリに HarnessOps を組み込んでください。
添付の target-integration-agent-brief.md に従い、リポジトリ種別を判定し、適切な profile で初期化し、doctor/migrate まで検証してください。
既存ファイルを安全でなく上書きせず、未サニタイズ情報を外部へ出さず、最後に作成ファイル・検証結果・残課題を報告してください。
```

## 目的

HarnessOps を対象リポジトリに追加し、AI Agentが失敗、フィードバック、評価、改善判断を `hops` CLI経由で扱える状態にします。

組み込み後の状態:

- project-repository なら `harness-feedback/` がある。
- target-repository または HarnessOps repository なら `harness-lab/` がある。
- `.harness/manifest.toml` がある。
- `.harnessops/project.toml` と `.harnessops/lock.json` がある。
- `hops doctor --check-overlay --check-records` が通る。
- 必要に応じて repo-local Agent bridge がある。

## 絶対ルール

- 状態変更は `hops` または `harnessops` CLIを通す。
- `.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を手作業で再設計しない。
- 既存ファイルを安全でなく上書きしない。
- 未サニタイズのフィードバックを外部Issue、PR、公開文書に貼らない。
- GitHub Issue、Pull Request、pushなどのリモート操作はユーザー確認なしに行わない。
- project-specific な研究判断や論文主張を `harness-feedback/` に移さない。

## 事前確認

対象リポジトリで次を確認します。

```bash
pwd
git status --short --branch
```

未コミット変更があっても勝手に戻しません。HarnessOps組み込みに関係ない変更は触りません。

## HarnessOps CLIの実行方法

対象環境に `hops` が入っているなら、そのまま使います。

```bash
hops --help
```

HarnessOps のソースディレクトリを渡されている場合は、対象リポジトリから次の形式で実行します。

```bash
uvx --isolated --from /path/to/HarnessOps harnessops --help
uvx --isolated --from /path/to/HarnessOps harnessops detect
```

以降の例で `hops` と書かれている箇所は、必要に応じて次に読み替えます。

```bash
uvx --isolated --from /path/to/HarnessOps harnessops <command>
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
| runops生成プロジェクト | `runops-project` | `harness-feedback/` |
| paper-harness生成プロジェクト | `paper-harness-project` | `harness-feedback/` |
| Python packageプロジェクト | `python-package` | `harness-feedback/` |
| その他のコードリポジトリ | `generic-code` | `harness-feedback/` |

target repository に組み込む依頼なら、通常は `*-upstream` または `target-harness` を選びます。

## 初期化

profileが決まったら初期化します。

```bash
hops init --profile <profile-id>
```

repo-local bridgeも入れる場合:

```bash
hops init --profile <profile-id> --with-agent-bridge
```

すでに初期化済みの場合は、むやみに `--force` を使いません。まず検証します。

```bash
hops doctor --check-overlay --check-records
hops migrate --check
```

生成ファイルが編集済みで `init` が拒否した場合は、拒否を尊重して停止し、どのファイルが競合したか報告します。

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
harness-lab/views/
```

`harness-lab/` は上流改善の評価と判断の記憶です。通常のタスク管理はGitHub Issuesなど既存の仕組みに残します。

## project repositoryで確認すること

project repository の場合、次があることを確認します。

```text
.harness/manifest.toml
.harnessops/project.toml
.harnessops/lock.json
harness-feedback/README.md
harness-feedback/records/failures/
harness-feedback/records/local-workarounds/
harness-feedback/records/upstream-feedback/
harness-feedback/records/meta-feedback/
harness-feedback/views/
```

`harness-feedback/` は観測と送信用です。研究方針、論文主張、実験転換は `research/` または `notes/` に残します。

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

HarnessOpsのローカルソースから実行している場合:

```bash
uvx --isolated --from /path/to/HarnessOps harnessops doctor --check-overlay --check-records
uvx --isolated --from /path/to/HarnessOps harnessops migrate --check
```

## 受け入れ条件

組み込み完了と判断できる条件:

- 適切なprofileで `.harnessops/project.toml` が作成されている。
- `.harness/manifest.toml` が作成されている。
- 対象種別に応じて `harness-feedback/` または `harness-lab/` が作成されている。
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
- target repository なのか project repository なのか判断できない。
