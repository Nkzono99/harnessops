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
| `hops add-failure` | はい | プロジェクト側の失敗レコードを作成します。 |
| `hops add-feedback --from <Fid>` | はい | 非公開の上流/メタフィードバック下書きを作成します。 |
| `hops route --record <id>` | はい | レコードのdispositionを分類して保存します。 |
| `hops feedback export --sanitize` | はい | 生成ビュー配下にサニタイズ済み外部向けバンドルを書き出します。 |
| `hops feedback import <bundle>` | はい | サニタイズ済みバンドルを `harness-lab` にインポートします。 |
| `hops lab new-eval-case --from <FBid>` | はい | インポート済みフィードバックを評価ケースに変換します。 |
| `hops propose --from <Eid>` | はい | メカニズムと中止基準を含む仮説を作成します。 |
| `hops eval --case <Eid> --manual` | はい | 多軸の手動スコアカードを保存します。 |
| `hops decide --from <id> --status <status>` | はい | 採用、却下、保留の判断を記録します。 |
| `hops agent bridge/install/verify` | bridge/installのみ | repo-local skill展開と任意plugin成果物を管理します。 |

将来の互換 alias として `hops feedback add --target <target>` を予約できます。ただし現行の正本コマンドは、観測記録の `hops add-failure` と、上流/メタ下書きの `hops add-feedback --from <Fid>` です。

## 安全ルール

1. どのコマンドも GitHub Issue、プルリクエスト、リモート変更を作成しません。
2. `feedback export` は、`--allow-private` が明示されない限り未サニタイズ出力を拒否します。
3. `init` が書くのは生成ファイルだけです。生成ファイルが編集され、ロックのハッシュと一致しない場合、コマンドは上書きを拒否するか、安全な競合コピーを書きます。
4. `records/` 配下のレコードは人が作成した履歴であり、ビュー更新では再生成されません。
5. 採用済み判断には、証拠、回帰リスク、ガードパスが必要です。

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
```
