# レコードスキーマ

HarnessOps レコードは YAML frontmatter 付きのMarkdownファイルです。frontmatter は機械検証され、本文には人間が読む証拠と根拠を書きます。

## 共通ルール

- すべてのレコードに `id`、`record_type`、`created_at` が必要です。
- IDプレフィックスはレコード種別と一致する必要があります: `F`、`LW`、`UF`、`MF`、`FB`、`E`、`H`、`X`、`D`。
- レコードは既定で追記専用です。変更には明示的なCLIコマンドが必要です。
- 生成ビューはレコードではなく、上書きされる場合があります。
- 証拠を持つ成果物を作るコマンドの後、レコード本文に未解決の `TODO` プレースホルダーを残してはいけません。

## 必須セクション

| 種別 | 必須本文セクション |
|---|---|
| `failure` | 文脈、起きたこと、重要性、望ましい挙動、ローカル回避策、ルーティング根拠 |
| `upstream_feedback` | 概要、最小再現、期待する上流改善、除外した非公開情報 |
| `meta_feedback` | 概要、最小再現、期待する上流改善、除外した非公開情報 |
| `imported_feedback` | 概要、再現、期待する上流変更 |
| `eval_case` | フィクスチャ、タスク、期待される挙動、合格基準、不合格基準 |
| `hypothesis` | 仮説、メカニズム、最小実装、代替案: 削除または統合、期待される利点、想定される欠点、評価計画、中止基準 |
| `decision` | 判断、理由、証拠、回帰リスク、フォローアップ、回帰ガード |

`eval_case` の本文は正本として保持しますが、日常レビュー用の dossier では全文を展開しません。dossier では manual eval yml/md、score、notes を優先して表示し、テンプレート本文が評価証拠の読解を邪魔しないようにします。

## Knowledge Layer

`harness-lab/knowledge/lab-memory.yml` と `lab-memory.md` はレコードではありません。`hops lab compact` が更新する mutable working memory で、`records/`、`improvements/`、manual eval yml から capability/failure class、lesson、score、guard、外部比較、open question を圧縮します。

この層は source ID と source digest を持ちますが、採用判断や検証の正本にはなりません。`lab-memory.md` の `Curator Notes` は手編集可能で、次回 compaction でも保持されます。

## 証拠規律

メカニズム、評価計画、中止基準がない仮説は、本当の実験ではありません。証拠のない判断は採用可能ではありません。採用済み判断では、再発を検出するテストパス、評価結果、生成チェックなどの回帰ガードを明示する必要があります。

## 検証

`hops doctor --check-records` は frontmatter、IDプレフィックス、必須本文セクション、disposition、採用証拠を検証します。`src/harnessops/schemas/json/` 配下のJSON Schemaファイルが機械可読な契約を文書化します。
