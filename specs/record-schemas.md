# レコードスキーマ

HarnessOps レコードは YAML frontmatter 付きのMarkdownファイルです。frontmatter は機械検証され、本文には人間が読む証拠と根拠を書きます。

実装上は、レコード種別と保存先の正本を `harnessops.core.record_types` に置き、frontmatter IO を `record_io`、ID/path lookup を `record_index`、作成系を `lab_records`、dossier 集約と更新を `improvement_dossier` に分けます。`harnessops.core.records` は既存 import 互換の facade として残します。

## 共通ルール

- すべてのレコードに `id`、`record_type`、`created_at` が必要です。
- IDプレフィックスはレコード種別と一致する必要があります: `F`、`LW`、`UF`、`MF`、`FB`、`E`、`H`、`X`、`D`、`RS`。
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
| `research_scan` | Scope、Evidence、Candidates、Recommendation、Next Commands |

`eval_case` の本文は正本として保持しますが、日常レビュー用の dossier では全文を展開しません。dossier では manual eval yml/md、score、notes を優先して表示し、テンプレート本文が評価証拠の読解を邪魔しないようにします。

`research_scan` は、メタ改善調査の結果を構造化するための軽量レコードです。frontmatter は `scope`、`classification`、`evidence`、`candidates`、`recommendation` を持ちます。candidate は title、relation、recommendation、next_command を持ち、既存 dossier への `investigate`、新規 `capture`、評価ケース化、保留、却下などの次アクションへ接続します。

## Knowledge Layer

`harness-lab/knowledge/lab-memory.yml` と `lab-memory.md` はレコードではありません。`hops lab memory compact` が更新する deterministic snapshot で、`records/`、`improvements/`、manual eval yml から capability/failure class、lesson、score、guard、外部比較、open question を source-linked な索引として圧縮します。

`hops lab memory lint` は抽象化の発火基準だけを判定し、`hops lab memory prepare` は `hops-compact-lab-memory` skill 用の入力 bundle を作ります。skill が更新する `principles.md`、`patterns.yml`、`anti-patterns.md`、`evaluation-playbook.md`、`lab-memory-abstraction.yml` も採用判断や検証の正本にはなりません。source ID と source digest から必ず正本へ戻れる必要があります。`lab-memory.md` の `Curator Notes` は手編集可能で、次回 snapshot でも保持されます。

## 証拠規律

メカニズム、評価計画、中止基準がない仮説は、本当の実験ではありません。証拠のない判断は採用可能ではありません。採用済み判断では、再発を検出するテストパス、評価結果、生成チェックなどの回帰ガードを明示する必要があります。

## 検証

`hops doctor --check-records` は frontmatter、IDプレフィックス、必須本文セクション、disposition、採用証拠を検証します。`src/harnessops/schemas/json/` 配下のJSON Schemaファイルが機械可読な契約を文書化します。
