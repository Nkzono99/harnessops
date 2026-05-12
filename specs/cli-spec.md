# CLI仕様

`hops` は主要なコマンドエイリアスで、`harnessops` は明示的な長いエイリアスです。どちらのエントリポイントも `harnessops.cli.main:app` を呼び出します。

CLI は状態管理の正本です。プラグイン、スキル、エージェントはワークフローを案内できますが、管理対象状態の変更はCLIコマンドを通して行います。

## コマンド群

| コマンド | 状態変更 | 目的 |
|---|---:|---|
| `hops version` | いいえ | パッケージバージョンを表示します。 |
| `hops profiles list/show` | いいえ | 組み込みプロファイルとプロファイル指紋を確認します。 |
| `hops detect` | いいえ | リポジトリ種別と推奨プロファイルを推定します。 |
| `hops init --profile <id>` | はい | `.harness/`、`.harnessops/`、プロファイルオーバーレイを作成します。 |
| `hops link --profile <id>` | はい | 既存リポジトリを HarnessOps に関連付けるエイリアスです。 |
| `hops doctor` | いいえ | プロジェクトリンク、オーバーレイ、ロック、レコードを検証します。 |
| `hops migrate --check/--apply` | `--apply` のみ | スキーマ/レイアウトマイグレーションを確認または適用します。 |
| `hops update-harness` | はい | managed file、migration確認、repo-local skill展開を現在の `hops` 実装に合わせます。編集済みmanaged fileは `<path>.new` に書きます。 |
| `hops add-failure` | はい | プロジェクト側の失敗レコードを作成します。 |
| `hops add-feedback --from <Fid>` | はい | 非公開の上流/メタフィードバック下書きを作成します。 |
| `hops route --record <id>` | はい | レコードのdispositionを分類して保存します。 |
| `hops feedback export --sanitize` | はい | 生成ビュー配下にサニタイズ済み外部向けバンドルを書き出します。`--format github-issue` は公開Issue用Markdown下書きだけを書き、リモートIssueは作りません。 |
| `hops feedback issue create <bundle> --repo <owner/repo>` | `--confirm-create` のみ | サニタイズ済み `--format github-issue` バンドルを表示し、重複候補を検索します。`--confirm-create` 付きでのみ GitHub Issue を作成し、成功時に元レコードへIssue URLを書き戻します。 |
| `hops feedback import <bundle>` | はい | サニタイズ済みバンドルを `harness-lab` にインポートします。 |
| `hops lab capture` | はい | 外部bundleやissue化前のローカル改善観測を `harness-lab` の `FB` レコードにします。 |
| `hops lab new-eval-case --from <FBid>` | はい | インポート済みフィードバックを評価ケースに変換します。 |
| `hops lab dossier --from <FB/E/H/D id>` | はい | 正規化済み `FB/E/H/D` レコードから、1つの改善履歴を読むための `harness-lab/improvements/IMPxxxx-*.md` を作成または更新します。 |
| `hops lab classify --from <FB/E/H/D/IMP id>` | はい | 改善dossierの source_type、scope、maturity、relation、promotion_level、guard を更新します。 |
| `hops lab investigate --from <FB/E/H/D/IMP id>` | はい | 改善dossierにコード調査、外部比較、反例、追加観測などの調査メモを追記します。 |
| `hops lab issue draft/create --from <FB/E/H/D/IMP id>` | draftははい、createは`--confirm-create`のみ | lab-first record からサニタイズ済みGitHub Issue下書きを作り、重複確認後に明示確認付きでIssueを作成します。成功時はlab recordへIssue URLを書き戻します。 |
| `hops lab refresh-views` | はい | `harness-lab` の生成ビューを再生成し、managed file hash を更新します。 |
| `hops propose --from <Eid>` | はい | メカニズムと中止基準を含む仮説を作成します。 |
| `hops eval --case <Eid> --manual` | はい | 多軸の手動スコアカードを保存します。 |
| `hops decide --from <id> --status <status>` | はい | 採用、却下、保留の判断を記録します。 |
| `hops agent bridge/install/verify` | bridge/installのみ | repo-local skill展開と任意plugin成果物を管理します。 |

将来の互換 alias として `hops feedback add --target <target>` を予約できます。ただし現行の正本コマンドは、観測記録の `hops add-failure` と、上流/メタ下書きの `hops add-feedback --from <Fid>` です。

## 安全ルール

1. GitHub Issue、プルリクエスト、リモート変更は暗黙に作成しません。`hops feedback issue create` は title/body と重複候補を表示し、`--confirm-create` が明示された場合だけ GitHub Issue を作成します。
2. `feedback export` は、`--allow-private` が明示されない限り未サニタイズ出力を拒否します。`--format github-issue` は公開共有前提のため、`--sanitize` を必須とし、`--allow-private` との併用を拒否します。
3. `init` と `update-harness` が書くのは生成ファイルだけです。生成ファイルが編集され、ロックのハッシュと一致しない場合、`update-harness` は元ファイルを保持して `<path>.new` に新しい生成物を書きます。
4. `records/` 配下のレコードは人が作成した履歴であり、ビュー更新では再生成されません。
5. `improvements/IMP*.md` は正規化レコードから再生成できる dossier です。日常レビューでは dossier を読み、採用判断や評価証拠を確定する時は元の `FB/E/H/D` レコードを更新します。
6. 後方互換性は絶対条件ではありません。`hops migrate` または `hops update-harness` で移行できるなら、古い構造を温存せず整理できます。
7. 採用済み判断には、証拠、回帰リスク、ガードパスが必要です。

## 終了コード

| コード | 意味 |
|---:|---|
| 0 | 成功。 |
| 1 | 検証エラーまたは使い方のエラー。 |
| 2 | 安全でない上書き、またはインストール競合を防止。 |
| 3 | プロファイルが見つからない。 |

## 受け入れ確認コマンド

```bash
hops --help
hops profiles list
hops detect --json
hops init --profile runops-project
hops doctor --check-overlay --check-records
hops migrate --check
hops add-failure --title "ハーネス摩擦" --target runops
hops route --record F0001 --json
hops feedback export --sanitize
hops feedback export --sanitize --format github-issue
hops feedback issue create harness-feedback/views/exported-feedback/UF0001-runops-feedback.md --repo owner/repo
```
