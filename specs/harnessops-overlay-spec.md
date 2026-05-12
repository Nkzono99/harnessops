# HarnessOpsオーバーレイ仕様

HarnessOps は2つの可視オーバーレイと1つの隠しメタデータディレクトリを使います。

## プロジェクトオーバーレイ: `harness-feedback/`

プロジェクトリポジトリは、プロジェクト側の観測と外部向けフィードバック下書きに `harness-feedback/` を使います。

```text
harness-feedback/
  README.md
  records/
    failures/
    local-workarounds/
    upstream-feedback/
    meta-feedback/
  views/
    open-routing.md
    upstream-feedback.md
    exported-feedback/
```

研究アジェンダ変更、論文主張の変更、実験方針転換、生の非公開データ、ターゲット実装パッチは、ルーティング済みハーネスフィードバックとして表現されていない限り、ここに置かないでください。

## ラボオーバーレイ: `harness-lab/`

ターゲットリポジトリと HarnessOps リポジトリは、上流改善の評価に `harness-lab/` を使います。

```text
harness-lab/
  README.md
  records/
    feedback/
    eval-cases/
      fixtures/
    hypotheses/
    experiments/
    decisions/
    research-scans/
  improvements/
  knowledge/
    lab-memory.yml
    lab-memory.md
  views/
    imported-feedback.md
    backlog.md
    improvements.md
    research-scans.md
    score-trajectory.md
    eval-results/
```

`harness-lab/` はフィードバック、評価、仮説、実験、判断の記憶です。GitHub Issues は引き続きタスクトラッカーです。`records/` は正規化された正本で、`improvements/IMP*.md` は日常レビュー用に1改善分の履歴を集約した dossier です。

`knowledge/` は `hops lab compact` が更新する mutable working memory です。一定のサイズ閾値を超えた lab、または `--force` で明示された lab から、capability、failure class、scores、guards、外部比較、open questions を source ID 付きで圧縮します。これは正本ではなく、採用判断や反例処理では必ず `records/` または `improvements/` に戻ります。

`records/research-scans/` は、意図的なメタ改善調査の結果を構造化して保存します。`RS` レコードは scope、evidence、candidate、relation、recommendation、next command を持ち、調査結果を `investigate`、`capture`、`propose`、`park`、`reject` のどれへ進めるかを後から追えるようにします。

## 隠しメタデータ: `.harnessops/`

```text
.harnessops/
  project.toml
  lock.json
  migrations/
  cache/
```

`lock.json` は生成ファイルだけを追跡します。人が作成したレコードは `managed_files` に列挙しません。

## 生成ファイル

生成ファイルにはオーバーレイのREADMEとビューが含まれます。これらには生成マーカーが入り、更新される場合があります。管理対象ファイルのハッシュがロックと異なる場合、`init` またはマイグレーションは、`--force` が使われ安全な競合動作が可能な場合を除き、上書きを拒否します。
