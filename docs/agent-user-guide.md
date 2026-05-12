# AI Agent向け利用ガイド

このガイドは、AI Agent が HarnessOps を操作するときの標準手順です。状態変更は必ず `hops` 経由で行い、管理対象ディレクトリの構造を手作業で組み替えないでください。

## 基本原則

- 先に `hops doctor --check-overlay` を実行し、リポジトリが HarnessOps にリンクされているか確認する。
- リンクされていなければ `hops detect` を実行し、検出されたプロファイルで `hops init --profile <id>` を提案または実行する。
- プロジェクト固有の内容は `research/` または `notes/` に残し、`harness-feedback/` へ混ぜない。
- 上流またはメタ改善へ回す内容は、ルーティング後に `hops feedback export --sanitize` でサニタイズする。
- 採用判断を作る前に、評価ケース、スコアカード、証拠、回帰ガードをそろえる。
- 改善案は仮説として扱う。メカニズム、評価計画、中止基準がない提案を採用候補にしない。
- 変更を増やす前に、削除または統合で失敗クラスを減らせないか確認する。

## プロジェクト側で失敗を記録する

使う場面:

- ハーネス更新でローカル編集が失われた。
- doctor や検証が浅く、重要な状態を見逃した。
- ローカル回避策が繰り返されている。
- 上流テンプレートやツールに直すべき不足が見つかった。

手順:

```bash
hops doctor --check-overlay
hops add-failure --title "<短い題名>" --target <target> \
  --context "<文脈>" \
  --what-happened "<起きたこと>" \
  --why-matters "<重要性>" \
  --desired-behavior "<望ましい挙動>" \
  --local-workaround "<回避策>"
hops route --record F0001
```

上流またはメタ候補なら、下書きとエクスポートを作ります。

```bash
hops add-feedback --from F0001 --target <target> --summary "<要約>"
hops feedback export --target <target> --sanitize
hops feedback export --target <target> --sanitize --format github-issue
```

`--format github-issue` はローカルのMarkdown下書きだけを作り、リモートIssueは作成しません。未サニタイズ出力は共有しないでください。`--allow-private` は、人間が明示的に非公開出力を求めた場合だけ使います。GitHub Issue下書きでは `--allow-private` を使えません。

## ターゲット側で改善を評価する

使う場面:

- サニタイズ済みフィードバックバンドルを受け取った。
- 上流ハーネスや HarnessOps 自身の改善候補を評価する。
- issue や外部バンドルになる前のローカル改善観測を、評価可能な形で残したい。

手順:

```bash
hops doctor --check-overlay
hops feedback import path/to/UF0001-target-feedback.md
hops lab new-eval-case --from FB0001
hops propose --from E0001
hops eval --case E0001 --manual --score impact=4 --score anti-theater=5
```

外部バンドルや issue がないローカル改善は、まず capture します。

```bash
hops lab capture --title "<題名>" --summary "<観測>" --expected-change "<期待する変更>"
hops lab new-eval-case --from FB0001
```

判断は、証拠の成熟度に合わせて作ります。

```bash
hops decide --from H0001 --status parked
```

採用する場合は、証拠、回帰リスク、ガードパスを必ず指定します。

```bash
hops decide --from H0001 --status adopted \
  --reason "<採用理由>" \
  --evidence "<評価結果や証拠への参照>" \
  --regression-risk "<回帰リスク>" \
  --guard-path "<テストまたは検出ガードのパス>"
```

## ルーティング判断

1つの出来事に複数の意味がある場合は、1レコードへ押し込まず分割します。

- `project-evolution`: 研究方針、論文主張、実験内容の変化。`research/` または `notes/` に置く。
- `project-local-process`: プロジェクト固有の回避策や運用問題。
- `target-upstream-candidate`: ターゲットハーネス側で直すべき不足。
- `meta-harness-candidate`: HarnessOps のCLI、スキーマ、ルーティング、プラグインの不足。
- `protocol-candidate`: `.harness/manifest` や共通CLI規約の不足。
- `external-candidate`: クラスタ、シミュレータ、ジャーナルなど外部システムの問題。
- `do-not-upstream`: 明示的にローカルまたは非公開。

## Feedbackとtriageの分担

feedback の記録、routing、sanitize、export/import は HarnessOps の責務です。target 固有の skill は、runops や paper-harness の domain 判断だけを担当し、`harness-feedback/` や `harness-lab/` の records を直接作りません。

使い分け:

- meta routing triage: `hops route --record <id>` で project-local / target-upstream / meta-harness / external / private を分類する。
- domain diagnosis triage: target 側 skill が Slurm、campaign、claim、citation、venue などの固有判断を補助する。
- lab triage: `hops feedback import` 後に、評価ケース化、backlog、reject、issue draft のどれに進めるかを判断する。

既存の `feedback-runops` や `feedback-paper-harness` のような target 側 skill は、移行期には `hops add-failure`、`hops route`、`hops add-feedback`、`hops feedback export --sanitize` を呼ぶ thin wrapper として扱います。

## プライバシー確認

外部共有前に次を確認します。

- ローカル絶対パスが残っていない。
- `private_terms` に該当する語が残っていない。
- `protected_paths` や `private_paths` の内容を含んでいない。
- 送信元プロジェクトを不要に特定できない。
- 評価や再現に非公開文脈を要求していない。

必要に応じて `.harnessops/sanitize.yml` を人間に提案します。

```yaml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - internal-method-name
```

## Agentがしてはいけないこと

- `records/` 配下の履歴をビュー更新の都合で書き換えない。
- `.harnessops/lock.json` を手作業で都合よく修正しない。
- 未サニタイズのフィードバックを外部IssueやPR本文に貼らない。
- 評価ケースなしに採用を勧めない。
- 証拠、回帰リスク、ガードパスなしに `adopted` 判断を作らない。
- プロジェクト固有の研究判断を上流テンプレートへ混ぜない。

## 作業後の検証

HarnessOps 自身のリポジトリで変更した場合は、少なくとも次を実行します。

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uv run --with-editable . hops doctor --check-overlay --check-records
uv run --with-editable . hops migrate --check
```

詳細な仕様はリポジトリ直下の `SPEC.md`、設計思想は `docs/design-principles.md` を参照してください。
