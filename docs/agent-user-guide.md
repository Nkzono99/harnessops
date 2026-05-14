# AI Agent向け利用ガイド

このガイドは、AI Agent が HarnessOps を操作するときの標準手順です。状態変更は必ず `hops` 経由で行い、管理対象ディレクトリの構造を手作業で組み替えないでください。

## 基本原則

- 下流の target/project repo では PATH 上の `hops` に依存せず、原則 `uvx --from harnessops hops <command>` で実行する。以下の例で `hops` と書かれている場合も、この形式で読み替えてよい。
- 先に `uvx --from harnessops hops doctor --check-overlay` を実行し、リポジトリが HarnessOps にリンクされているか確認する。
- リンクされていなければ `uvx --from harnessops hops detect` を実行し、検出されたプロファイルで `uvx --from harnessops hops init --profile <id>` を提案または実行する。
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
hops feedback issue create harness-feedback/views/exported-feedback/UF0001-<target>-feedback.md --repo owner/repo
```

`--format github-issue` は公開Issue用のMarkdown下書きを作ります。`hops feedback issue create` は title/body と重複候補を表示しますが、`--confirm-create` なしではリモートIssueを作成しません。作成に成功した場合は、元の feedback record へ Issue URL を書き戻します。未サニタイズ出力は共有しないでください。`--allow-private` は、人間が明示的に非公開出力を求めた場合だけ使います。GitHub Issue下書きでは `--allow-private` を使えません。

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

日常の改善レビューでは、正規化された `FB/E/H/D` を1枚に集約した dossier を作れます。

```bash
hops lab dossier --from FB0001
hops lab investigate --from IMP0001 --kind external-benchmark --summary "<外部比較や調査結果>"
hops lab research-scan --title "<調査名>" --scope "<対象>" --candidate "<候補>|<relation>|<recommendation>|<next command>" --recommendation "<推奨>"
hops lab classify --from IMP0001 --source-type friction --scope harnessops-core --maturity investigated
```

単純な改善や作業中の状況把握では `harness-lab/improvements/IMP*.md` を開きます。dossier の `Evaluation` は評価ケース本文を丸ごと展開せず、source record、capability、failure class、manual eval yml/md、score、notes を要約します。評価ケース、仮説、採用判断を確定する時は、引き続き元の `records/feedback`、`records/eval-cases`、`records/hypotheses`、`records/decisions` を正本として更新し、その後 dossier を再生成します。

`harness-lab/` が大きくなり、dossier を全部読むのが重くなったら、まず memory lint で発火基準を確認します。lint は書き込みを行わず、lab のサイズ、source digest、deterministic snapshot、抽象知識 manifest の状態だけを見ます。

```bash
hops lab memory lint --warn-only
```

`hops lab compact` は残しますが、役割は deterministic knowledge snapshot です。source ID、score、guard、open question へ戻るための索引であり、抽象化や原則化そのものではありません。索引を更新する時だけ使います。

```bash
hops lab compact --force
```

抽象化が必要な場合は、CLI が入力 bundle だけを作り、実際の意味づけは `hops-compact-lab-memory` skill が行います。

```bash
hops lab memory prepare --force
```

`harness-lab/knowledge/lab-memory.yml` と `.md` は source-linked な索引です。`harness-lab/knowledge/lab-memory-input.yml` と `.md` は skill の入力です。skill は `principles.md`、`patterns.yml`、`anti-patterns.md`、`evaluation-playbook.md`、`lab-memory-abstraction.yml` を更新し、すべての抽象知に source ID と source digest を持たせます。records と dossier は引き続き正本です。`lab-memory.md` の `Curator Notes` は手編集してよく、次回 snapshot でも保持されます。

発散的な改善案を出したい時は `hops-open-meta-scan` skill を使います。これは lab record や issue を作る前の invention lane で、Raw Ideas、Counterframes、Routing Hints を出し、まだ `hops lab capture` や `research-scan` を実行しません。

メタ改善案を意図的に調査・選別する時は `hops-research-improvements` skill を使います。これは HarnessOps core だけでなく、HarnessOps を導入した target/project repository でも使う selection/routing lane です。作業中の短いメタ仮説スキャンや `hops-open-meta-scan` とは別に、コードベース、既存 dossier/feedback、過去判断、tests、skills、docs を見たうえで、必要なら web/外部実務/公式 docs を比較します。target/meta lab repo では、まず `hops lab research-scan` で scope、evidence、candidate、relation、recommendation、next command を構造化できます。その後、新規レコード乱立を避けながら `hops lab investigate`、`hops lab classify`、必要な場合だけ `hops lab capture` や `hops propose` に落とします。project repo では `harness-lab/` を作らず、観測を `hops add-failure`、`hops route`、`hops add-feedback`、`hops feedback export --sanitize` に流します。

定期的に issue、feedback、lab、doctor/update 状態、発想的改善、既存評価の前進をまとめて見る時は `hops-daily-steward` skill を使います。これは単一の万能 agent ではなく、既存 skill へ委譲する薄い conductor です。常時起動PCの Codex App automation で夜間に走らせる場合は、[daily steward automation prompt](daily-steward-automation.md) を使い、最初に `hops steward preflight --pull --json` を実行します。この command は `git fetch --prune`、clean worktree 上の `git pull --ff-only`、doctor、migrate check、overlay counts、lab health、lane trigger scaffold、run ledger を機械的に返します。dirty、diverged、conflict の場合は HOPS state change へ進みません。HarnessOps 最新化は毎回の開始 step ではなく、preflight、doctor、update notice、lock drift、managed-file drift が示した時の update lane / work packet として扱います。Human review は local advance の前提ではありませんが、implementation 以降は validation と guard plan が必須です。record / research / metadata work は concrete observation や evidence ref があれば queue を厚くするために進められます。作業量は `max 1` ではなく risk tier と work-packet budget で制御します。clean repo で global gate が通るなら status-only no-op を通常結果にせず、reactive work、candidate queue、`hops-open-meta-scan`、safe cleanup のいずれかへ進みます。remote merge / issue / PR / release は automation prompt で明示した場合だけ実行し、標準は GitHub Flow として automation branch から protected `main` への PR/merge を使います。Git Flow 風の repo だけ `develop` を merge target にできます。

lab 起点の改善を GitHub Issue に昇格する時は、まず下書きで title/body を確認します。

```bash
hops lab issue draft --from IMP0001
hops lab issue create --from IMP0001 --repo owner/repo
```

リモート Issue は作成されません。作成する場合だけ、重複候補を確認した上で `--confirm-create` を付けます。

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
