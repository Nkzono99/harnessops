# HarnessOps 設計思想

HarnessOps の中心は、AIに「もっと良くして」と頼むことではありません。失敗を観測し、改善仮説に変換し、評価で選別し、採用判断を記録し、再発防止パターンとして蓄積することです。

```text
AIは候補を生成する。
HarnessOpsは本当に機能したものを選別し、評価し、記録し、昇格する。
```

## 自己改善は生成ではなく選別

AIは改善案を大量に出せます。しかし、どの改善が本当に効いたかを選別できなければ、自己改善にはなりません。

HarnessOps では次を前提にします。

- 候補生成のコストは低い。
- 選別が中核能力である。
- 証拠が通貨である。
- 履歴が記憶である。

採用する改善よりも、却下する改善の質がシステム全体の品質を決めます。

## バグ修正と根本改善の違い

バグ修正は、失敗テストという外部オラクルを持てます。

```text
failing test -> patch -> passing test
```

根本改善は、何もしないと次のような改善劇場になりがちです。

- README が長くなる。
- skill が増える。
- ルールが増える。
- チェック項目が増える。
- しかし実際の失敗クラスは減らない。

そのため HarnessOps は、失敗コーパス、能力マップ、評価ケース、スコアカード、中止基準、判断ログ、回帰ガードを持ちます。

## 5つの役割

自己改善を1つのAI Agentだけに閉じ込めません。

| 役割 | 責務 |
|---|---|
| 生成者 | 改善案、仮説、実装候補を出す。 |
| 判定者 | 失敗クラス、評価基準、採用可否を判定する。 |
| 環境 | 実行結果、テスト、現場運用、ユーザー反応を返す。 |
| 記憶 | 失敗、評価、判断、却下理由、再発防止を蓄積する。 |
| オーナー | 価値判断、優先順位、複雑性の許容量を決める。 |

AIは生成者と判定者の一部を担えます。ただしオーナーを完全に委任してはいけません。

## 標準改善ループ

```text
1. 観測
2. 記録
3. ルーティング
4. 仮説化
5. 評価
6. 判断
7. 適用
8. ガード
9. 昇格
```

`Improve` という曖昧な工程は置きません。改善は、観測、仮説、評価、判断、昇格へ分解します。

## 3種類の改善を混ぜない

| 種別 | 置き場所 | 意味 |
|---|---|---|
| プロジェクト発展 | `research/`, `notes/` | 研究方針、論文主張、実験内容などプロジェクト自体の進化。 |
| ハーネスフィードバック | `harness-feedback/` | target-repository や HarnessOps へ戻すべき問題。 |
| ハーネスラボ改善 | `harness-lab/` | 上流改善を評価し、仮説・実験・判断にする活動。 |

この分離により、project-specific な判断が上流テンプレートやメタプロトコルを汚染することを防ぎます。

## 仮説には中止基準を持たせる

改善仮説には必ず次を含めます。

- 仮説
- メカニズム
- 対象能力
- 最小実装
- 削除または統合の代替案
- 期待される利点
- 想定される欠点
- 評価計画
- 中止基準

中止基準がない改善案は、本当の実験ではありません。失敗した改善案を捨てられないループは、複雑性を蓄積し続けます。

## 変更は失敗クラスへ紐づける

「良さそうだから」では採用しません。原則として、すべての変更は既知の失敗クラスまたは新規観測 failure に紐づけます。

避けるもの:

- skill増殖
- rule増殖
- documentation theater
- 投機的アーキテクチャ
- governance overhead

新機能追加よりも、既存機能の削除、統合、評価強化を優先します。

## 評価は単一スコアにしない

単一スコアはGoodhart化しやすいため、HarnessOps は多軸scorecardを使います。

- impact
- mechanism_clarity
- evaluability
- minimality
- regression_risk
- operator_burden
- anti_theater
- maintainability
- privacy_sanitization_risk

特に `anti_theater` は、改善に見える構造を増やしているだけではないかを確認する軸です。

## AI Judgeを信用しすぎない

同じAI、同じコンテキスト、同じプロンプトで生成と評価を閉じると、自己承認ループになります。

可能な限り次を分けます。

- 生成者
- 判定者
- adversary
- 人間オーナー
- 静的チェック
- 実行時チェック
- holdout cases

AI judge は評価支援者であり、最終オラクルではありません。

## Holdoutと過適合

eval case は改善案の設計に使えます。holdout case は、採用前の最終確認や回帰ガードに使うものです。

holdout がない自己改善は、評価ケースに過適合しやすくなります。重要な capability には、少数でもholdoutを持つべきです。

## メタ改善は低頻度で行う

projectやtargetの改善は短周期で回して構いません。一方で、評価方法、schema、profile、protocolの改善は、複数回の実験結果を見てから別レーンで扱います。

```text
Fast lane:
  project / target の通常改善

Slow lane:
  HarnessOps の方法論、schema、profile、protocol の改善
```

## 昇格パイプライン

project固有の出来事を、いきなり汎用ルールにしません。

```text
Level 0: Raw observation
Level 1: Project-local record
Level 2: Target feedback
Level 3: Target lab case
Level 4: Cross-project pattern
Level 5: HarnessOps profile / adapter / protocol
```

この段階化により、個別事情をサニタイズし、証拠があるものだけを汎用化できます。

## 主要アンチパターン

- Reflection theater: 反省文だけで評価ケースや再発防止が増えない。
- Governance theater: ルールや文書は増えるが失敗クラスが減らない。
- Skill proliferation: 問題ごとにskillを増やし、責務整理しない。
- Self-approving judge: 生成したAIがそのまま自分の改善案を高評価する。
- Metric hacking: 単一スコアのために実運用品質を犠牲にする。
- Upstream pollution: project-specific な事情を上流テンプレートへ混ぜる。
- Context leakage: 非公開研究情報、ローカルパス、HPC site固有情報を公開feedbackへ混ぜる。
- Endless meta-improvement: 改善方法自体を毎回変え、比較不能にする。
