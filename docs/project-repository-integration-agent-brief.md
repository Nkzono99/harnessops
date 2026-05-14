# Project Repository向け HarnessOps 組み込みブリーフ

この文書は、project repository単体へ HarnessOps を組み込むAI Agentにそのまま渡すための指示書です。コード開発リポジトリ、研究プロジェクト、論文プロジェクト、target CLIで生成済みのプロジェクトなどが対象です。

target repository 本体へ組み込む場合は `docs/target-integration-agent-brief.md` を使ってください。

## Agentへの依頼文

対象リポジトリで、次の依頼とこの文書を渡してください。

```text
この project repository に HarnessOps を組み込んでください。
添付の project-repository-integration-agent-brief.md に従い、適切な profile を選び、harness-feedback を作成し、doctor/migrate まで検証してください。
既存ファイルを安全でなく上書きせず、未サニタイズ情報を外部へ出さず、最後に作成ファイル・検証結果・残課題を報告してください。
```

## 前提: project repository の役割

project repository は、研究、論文、解析、アプリケーション開発などの実作業が行われるリポジトリです。target repository の `init` などで生成される場合もあれば、単体のコード開発リポジトリとして存在する場合もあります。

HarnessOps を project repository に入れる目的は、現場で観測したハーネス失敗、ローカル回避策、上流へ戻すべき不足を `harness-feedback/` に記録し、必要なものだけをサニタイズしてtarget repositoryまたはHarnessOpsへ渡すことです。

project repository に `harness-lab/` を作らないでください。上流改善を評価し採用判断する場所は target repository 側の `harness-lab/` です。

## 絶対ルール

- 状態変更は `hops` または `harnessops` CLIを通す。
- `.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を手作業で再設計しない。
- 既存ファイルを安全でなく上書きしない。
- 未サニタイズのフィードバックを外部Issue、PR、公開文書に貼らない。
- 研究方針、論文主張、実験転換など project evolution は `research/` または `notes/` に残す。
- project-specific な事情を上流テンプレートへ混ぜない。
- GitHub Issue、Pull Request、pushなどのリモート操作はユーザー確認なしに行わない。

## 事前確認

```bash
pwd
git status --short --branch
uvx --from harnessops hops detect
uvx --from harnessops hops detect --json
```

未コミット変更があっても勝手に戻しません。HarnessOps組み込みに関係ない変更は触りません。

## HarnessOps CLIの実行方法

対象リポジトリでは、PATH 上の `hops` に依存せず、PyPI の `harnessops` パッケージから `uvx` で実行します。対象リポジトリから次の形式で実行します。

```bash
uvx --from harnessops hops --help
uvx --from harnessops hops detect
```

## Profile選択

| 対象 | profile | overlay |
|---|---|---|
| runops生成プロジェクト | `runops-project` | `harness-feedback/` |
| paper-harness生成プロジェクト | `paper-harness-project` | `harness-feedback/` |
| Python packageプロジェクト | `python-package` | `harness-feedback/` |
| その他のコードリポジトリ | `generic-code` | `harness-feedback/` |

`hops detect` が推奨profileを返した場合は、それを優先します。target repository と判定された場合は、この文書ではなく `docs/target-integration-agent-brief.md` を使うべきか確認してください。

## 初期化

profileが決まったら初期化します。

```bash
uvx --from harnessops hops init --profile <profile-id>
```

repo-local skillも入れる場合:

```bash
uvx --from harnessops hops init --profile <profile-id> --with-agent-bridge
```

project repository の repo-local bridge は role-scoped です。`feedback-source` / `local-and-feedback` では `hops-add-failure`、routing、feedback export、update/doctor/migrate を中心に展開し、`hops-run-lab`、`hops-issue-triage`、`hops-github-flow`、propose/eval/decide など upstream/meta lab 側の skill は展開しません。

すでに初期化済みの場合は、むやみに `--force` を使いません。まず検証します。

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
uvx --from harnessops hops migrate --check
```

## target CLIから生成される場合

project repository が target CLI の `init` や `update-harness` で作られる場合も、HarnessOps の状態は target CLI が直接書かず、生成先で `hops` を呼びます。

初回生成後:

```bash
uvx --from harnessops hops init --profile <target-project-profile>
uvx --from harnessops hops doctor --check-overlay --check-records
```

更新時:

```bash
uvx --refresh-package harnessops --from harnessops hops update-harness
```

`hops update-harness` は `hops doctor --check-overlay --check-records` と `hops migrate --check` 相当の確認を含みます。PATH 上の `hops` が古い可能性があるため、project repo の更新導線は uvx で最新版を確認してから実行します。lock の `harnessops_version` が古い場合、通常の `update-harness` は PyPI 上の checkpoint 版を `uvx --from harnessops==<version> hops update-harness` で順に適用してから現在版の更新を続けます。編集済みmanaged fileは runops と同様に `<path>.new` へ書き、元ファイルを保持します。

段階更新を事前確認する場合:

```bash
uvx --refresh-package harnessops --from harnessops hops update-harness --plan-upgrade
```

未適用migrationを適用する場合は、人間確認または明示フラグ付きで `uvx --from harnessops hops update-harness --apply-migrations` または `uvx --from harnessops hops migrate --apply` を呼びます。repo-local skill 展開は明示オプションで `uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge --codex` または `uvx --from harnessops hops agent bridge --codex` を使います。project repo では GitHub Flow skill は通常配布されません。ユーザー領域の plugin install は標準運用から外しているため、複数repoで使う場合も各repoで repo-local skill を展開します。

## target固有triageとの分担

project repository で観測した feedback は HarnessOps に記録します。runops や paper-harness の domain skill は、原因分類や再現観点の補助に使いますが、`harness-feedback/` の records、routing、sanitize、export は `hops` が行います。

```bash
hops add-failure --target <target> ...
hops route --record F0001
hops add-feedback --from F0001 --target <target>
hops feedback export --target <target> --sanitize
```

## 作成されるべき構造

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

## 最初の失敗レコード例

HarnessOps導入後、観測済みのハーネス問題がある場合だけ作成します。

```bash
hops add-failure --title "<短い題名>" --target <target> \
  --context "<文脈>" \
  --what-happened "<起きたこと>" \
  --why-matters "<重要性>" \
  --desired-behavior "<望ましい挙動>" \
  --local-workaround "<回避策>"
hops route --record F0001
```

上流へ渡す候補なら、必ずサニタイズしてからエクスポートします。

```bash
hops add-feedback --from F0001 --target <target> --summary "<要約>"
hops feedback export --target <target> --sanitize
```

## プライバシー設定

非公開語、保護パス、ローカルパスが分かっている場合は、`.harnessops/sanitize.yml` を提案または作成します。

```yaml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - internal-method-name
```

コード開発リポジトリでは、社内パス、顧客名、未公開機能名、private branch名、内部API名が漏れやすいので注意してください。

## 組み込み後の検証

最低限、次を実行します。

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
uvx --from harnessops hops migrate --check
```

通常テストがある場合は実行します。

```bash
python -m pytest -q
```

## 受け入れ条件

- 適切なprofileで `.harnessops/project.toml` が作成されている。
- `.harness/manifest.toml` が作成されている。
- project repository に `harness-feedback/` が作成されている。
- project repository に target repository用の `harness-lab/` を作っていない。
- `.harnessops/lock.json` が生成ファイルだけを管理している。
- `uvx --from harnessops hops doctor --check-overlay --check-records` が通る。
- `uvx --from harnessops hops migrate --check` が未適用マイグレーションなしを報告する。
- 既存の人間作成ファイルを安全でなく上書きしていない。
- 未サニタイズ情報を外部へ出していない。

## 最終報告フォーマット

```text
HarnessOps project repository 組み込み結果:
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
- target repository なのか project repository なのか判断できない。
- 既存の `.harnessops/project.toml` と新しい判定が矛盾する。
- 生成ファイルの上書きを `hops` が拒否した。
- private terms や protected paths が不明なまま外部共有が必要。
