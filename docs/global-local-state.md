# Global Local State

この導線は、普通のリポジトリを HarnessOps 非依存のまま保ち、開発者のローカル環境だけで HarnessOps の記録、分類、評価、共有準備を使うためのものです。

対象リポジトリには次を作りません。

- `.harnessops/`
- `harness-feedback/`
- `harness-lab/`
- `.agents/skills/`

状態はユーザー領域に置きます。

```text
~/.harnessops/
  registry.toml
  projects/
    <project-id>/
      .harnessops/
        project.toml
        lock.json
      harness-feedback/ または harness-lab/
      cache/
```

## 使い分け

| 導線 | 使う場面 | repoへの書き込み |
|---|---|---:|
| global local state | 普通のrepoを汚さず、開発時だけメタ的に使う | なし |
| repo-local state | HarnessOps 状態をPRやチームで共有する target/project repo | あり |

global local state は個人用の作業記憶です。共有が必要になった時だけ `hops local pack/import/merge` を使います。

## 初回リンク

`hops` は PATH に置かず、基本は `uvx` 経由で使います。

```bash
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops doctor --check-overlay --check-records
```

汎用コードリポジトリなら、まずは次で十分です。

```bash
uvx --from harnessops hops project link --storage local --profile generic-code
```

`HOPS_HOME` を指定すると、既定の `~/.harnessops` ではなく別の場所に registry と state を置けます。

```bash
HOPS_HOME=/path/to/hops-state uvx --from harnessops hops project resolve --json
```

## 日常操作

プロジェクト側の失敗を記録する例です。レコードは対象repoではなく local state 側に作られます。

```bash
uvx --from harnessops hops feedback add-failure \
  --title "<短い題名>" \
  --context "<文脈>" \
  --what-happened "<起きたこと>" \
  --desired-behavior "<望ましい挙動>"

uvx --from harnessops hops feedback route --record F0001
uvx --from harnessops hops feedback export --sanitize
```

target/meta lab として使うプロファイルでリンクした場合は、通常の lab 操作も同じように local state 側へ書かれます。

```bash
uvx --from harnessops hops feedback import path/to/UF0001-feedback.md
uvx --from harnessops hops lab capture --title "<題名>" --summary "<観測>" --expected-change "<期待する変更>"
uvx --from harnessops hops lab review queue
```

## Codex Global Plugin

Codex から使う場合は、同梱の global plugin をユーザー領域へ入れます。

```bash
uvx --from harnessops hops install-codex-plugin
```

基本操作は plugin 内の `harnessops-global` skill 経由で実行します。共有、issue化、failure記録のような定型作業は専用 skill に分かれており、人間が毎回CLIを組み立てる必要はありません。

```text
このrepoを HarnessOps local state で使えるようにして。repoにはファイルを作らないで。
```

```text
この失敗を HarnessOps local state に記録して。必要なら分類までして。
```

```text
このフィードバックをサニタイズ済みの GitHub Issue 下書きにして。作成はまだしないで。
```

```text
この local state を共有用zipにまとめて。
```

plugin は repo-local skill を作りません。Codex の skill は次の順で解決してから、依頼内容に応じた `hops` コマンドを実行します。

```bash
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
```

既に対象repoに `.harnessops/project.toml` がある場合は、repo-local state が優先されます。この状態では `project link --storage local` は新しい global link を作らず、repo-local 利用を続けるよう案内します。

`hops install-codex-plugin` はインストール後に、Codex で `/plugin` を開いて `HarnessOps Global` / `harnessops-global` を有効化する手順を表示します。`codex` CLI が PATH にない場合は、Codex CLI のインストール案内も表示します。

同梱される主な skill:

- `harnessops-global`: global/local-state の入口と intent routing。
- `hops-global-add-failure`: repo を汚さず failure/feedback 候補を記録。
- `hops-global-route-feedback`: 記録済み feedback の disposition を分類。
- `hops-global-feedback-issue`: sanitize 済み GitHub Issue 下書きと、明示確認付き issue 作成。
- `hops-global-share-state`: local-state bundle の pack/import/merge。

## 共有と Merge

local state を zip にまとめます。

```bash
uvx --from harnessops hops local pack
```

`--output` を省略すると、対象repoではなく `~/.harnessops/exports/` に bundle を作ります。repo内や任意の共有先に zip を置きたい場合だけ `--output <path>.zip` を明示します。

別環境へ取り込む場合です。

```bash
uvx --from harnessops hops local import harnessops-local-state.zip
```

現在の project の local state へ別の pack または state directory を merge します。

```bash
uvx --from harnessops hops local merge harnessops-local-state.zip
```

merge は既存ファイルを上書きしません。同一内容は skip し、異なる内容の衝突は `conflicts/` に退避します。外部共有前には必ず sanitize/export を通してください。

## 状態確認と解除

現在の repo がどの HarnessOps project に解決されるかを確認します。

```bash
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops project list
```

registry から外すだけなら:

```bash
uvx --from harnessops hops project unlink
```

local state も削除するなら:

```bash
uvx --from harnessops hops project unlink --delete-state
```

## Repo-Local にしたい場合

HarnessOps 状態をrepoに含めてチームで共有したい場合は、global local state ではなく repo-local 導線を使います。

```bash
uvx --from harnessops hops init --profile <profile-id>
uvx --from harnessops hops doctor --check-overlay --check-records
```

Agent 向け repo-local skill も入れる場合:

```bash
uvx --from harnessops hops agent bridge --codex
```
