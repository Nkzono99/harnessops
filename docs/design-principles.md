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
2. 調査
3. 記録
4. 分類・ルーティング
5. 仮説化
6. 評価設計
7. 判断
8. 適用
9. ガード
10. 昇格
```

`Improve` という曖昧な工程は置きません。改善は、観測、調査、分類、仮説、評価、判断、ガード、昇格へ分解します。

| 工程 | 具体的な意味 |
|---|---|
| 観測 | 改善の入口。GitHub Issue、ユーザーの不便、作業中の摩擦、失敗、ローカル回避策、外部プロジェクトとの差分、既存判断への反例、もう一歩進んだ改善案を含む。 |
| 調査 | 観測をそのまま実装しない。コードベース調査、再現確認、既存レコード確認、類似プロジェクトや外部実務との比較、既存決定との矛盾確認を行う。 |
| 記録 | 観測と調査を、あとで評価できる改善テーマとして残す。生ログではなく、source、scope、failure class、evidence、open questions を持つ dossier にする。 |
| 分類・ルーティング | 棚卸しではなく、責務と置き場所を決める工程。project-local、target feedback、HarnessOps lab、schema/profile/protocol 改善、既存テーマへの追加のどれかに振り分ける。 |
| 仮説化 | 何を変えると、どの失敗クラスが、なぜ減るのかを案にする。最小実装、削除または統合の代替案、期待される利点、欠点、中止基準を含む。 |
| 評価設計 | 評価ケース、比較ベースライン、外部知見との比較軸、holdout、成功条件、失敗条件を決める。 |
| 判断 | 評価結果を見て、adopt、trial、park、reject、merge、supersede などを決める。評価は測定、判断は責任ある意思決定。 |
| 適用 | 実装、docs、skill、profile、adapter、protocol、migration など実際の変更を行う。 |
| ガード | 採用した改善が残り、同じ失敗や過適合が戻らないようにする仕掛け。テスト、doctor check、eval case、holdout、lint、運用チェック、警告、kill criteria を含む。 |
| 昇格 | 局所的な学びをより広い層へ上げること。project-local から target、target lab、cross-project pattern、profile/adapter/protocol へ移す。 |

棚卸しは `分類・ルーティング` そのものではありません。棚卸しは、古い記録、未判断の dossier、反例、追加観測を定期的に見直し、必要なら再ルーティングする保守作業です。

## 改善テーマとdossier

日常の改善単位は `improvement dossier` です。dossier は1つの改善テーマに対して、観測、調査、分類、仮説、評価、判断、適用、ガード、後続観測を1枚で読めるようにします。

```text
Improvement Theme
  source observations
  investigation notes
  classification
  candidate hypotheses
  chosen hypothesis
  eval cases
  decisions
  applied changes
  guards
  later observations
  benchmark / score trajectory
```

dossier は `records/feedback`、`records/eval-cases`、`records/hypotheses`、`records/decisions` を置き換える正本ではありません。日常レビュー用の集約ビューです。正規化レコードが重すぎる場合は、`hops migrate` や `hops update-harness` で移行できるようにしたうえで整理して構いません。古い構造を永久に温存することより、移行可能で評価可能な形に保つことを優先します。

## 改善分類

改善テーマには少なくとも次の分類を持たせます。

| 軸 | 例 | 意味 |
|---|---|---|
| source_type | issue, friction, failure, workaround, external-benchmark, contradiction, extension, drift | 観測がどこから来たか。 |
| scope | project-local, target-harness, harnessops-core, profile, adapter, protocol-schema | 誰が直すべきか。 |
| capability | issue-triage, lab-memory, agent-bridge, sanitization | どの能力に関する改善か。 |
| failure_class | record-sprawl, stale-bridge, unicode-decode-failure | どの失敗クラスを減らすのか。 |
| maturity | raw, investigated, hypothesis, trial, adopted, guarded, superseded, rejected | テーマの成熟度。 |
| relation | new, duplicate, extends, contradicts, supersedes, regression | 既存テーマや判断との関係。 |
| promotion_level | raw-observation, project-record, target-feedback, target-lab-case, cross-project-pattern, harnessops-protocol | 昇格パイプライン上の位置。 |
| guard_status | not-defined, planned, implemented, holdout, monitoring, retired | 再発防止や反例検出の状態。 |

後から採用済み判断に反する観測が来た場合は、新しい孤立テーマにせず、まず既存 dossier へ `contradicts` または `regression` として紐づけます。採用済み改善をさらに進める観測なら `extends` として紐づけます。これにより、改善は単発の成功談ではなく、ベンチマークと経験の蓄積になります。

## メタ仮説スキャン

HarnessOps の狙いは、ユーザーが明示した改善だけでなく、作業中に見えた二階の改善仮説を捕捉できるようにすることです。agent は常に長い内省をする必要はありませんが、重要な局面では短い `meta-hypothesis scan` を行います。

スキャンの問い:

```text
この作業中に、今のタスクを越えて再利用できる考え方、反例、設計原則、評価方法、移行方針、agent行動ルールは見えたか。
```

### 発火シグナル

次のシグナルが出たら、30秒程度のスキャンを行います。

| シグナル | 例 |
|---|---|
| ユーザー割り込み | 「AGENTS.md にも書いて」「これは長期的には」「互換性は切ってよい」 |
| 繰り返し摩擦 | 同じ手作業、同じ確認、同じ失敗、同じ説明が複数回出る |
| 局所判断の一般化 | 「この考え方は他の target でも効く」「これは protocol の原則では」 |
| 既存判断への反例 | 採用済み改善が邪魔になった、前提が崩れた、過去の決定と矛盾した |
| 移行・互換判断 | 古い構造を温存するか、migrate/update-harness で移行して整理するか |
| 評価の空白 | 実装はできたが、何で成功と見るべきか、どの holdout が必要かが曖昧 |
| 外部比較の発見 | 他プロジェクト、標準実務、論文、運用パターンとの有用な差分が見えた |
| 認知負荷の兆候 | agent や user が工程名、責務、置き場所、Go/No-Go を迷った |

### チェックポイント

イベントがなくても、次のタイミングでは短いスキャンを挟みます。

- 非自明な実装に入る直前
- 予想外の失敗、テスト失敗、仕様の曖昧さに遭遇した時
- ユーザーから方針修正や割り込みが入った直後
- 採用判断、release、commit、PR 作成の直前
- 作業完了時の最終報告前

### 出力レベル

スキャン結果は必ず新規レコードにするわけではありません。ノイズを抑えるため、次の順に軽く扱います。

| レベル | 出力 | 使う場面 |
|---|---|---|
| none | 何もしない | 既存テーマと関係が薄い思いつき。 |
| note | `hops lab investigate --from <IMP>` | 既存テーマへの調査、反例、外部比較、追加観測。 |
| classify | `hops lab classify --from <IMP>` | maturity、relation、promotion、guard を更新すべき時。 |
| capture | `hops lab capture` | 既存テーマに入らない新しい失敗クラスや二階観測。 |
| propose | `hops lab new-eval-case` + `hops propose` | 実装または評価可能な改善仮説にする価値がある時。 |

新規 capture の目安は、次のいずれかです。

- 将来の agent 行動、評価方法、移行方針、公開/非公開境界に影響する。
- 複数の target/project に効きそうな cross-project pattern である。
- 採用済み判断への反例、拡張、回帰として残す必要がある。
- 今回の作業で忘れると、次回も同じ摩擦を繰り返す可能性が高い。

### ガードレール

メタ仮説スキャン自体が meta-noise になってはいけません。

- 作業を止めて長い設計会議にしない。通常は30秒、重い場合でも短い note に留める。
- 「良さそう」だけで capture しない。失敗クラス、対象 capability、または既存テーマとの relation を最低1つ持たせる。
- 新しい構造を増やす前に、既存 dossier への `investigate` または `classify` で済まないか確認する。
- 採用判断なしに protocol や AGENTS.md へ強いルールを増やさない。
- 後方互換を守るためだけに古い構造を温存しない。`hops migrate` または `hops update-harness` で移行できるなら整理を優先する。

## 手動メタ改善調査

作業中の `メタ仮説スキャン` は短い捕捉です。それとは別に、意図的に時間を取って改善候補を探す `hops-research-improvements` skill を持ちます。

使う場面:

- ユーザーが「meta改善を調査したい」「外部知見も含めて比較したい」と明示した。
- release 前に、最近の lab/dossier/issue/skill 変更を棚卸ししたい。
- 同じ摩擦や説明が複数回出ており、局所修正ではなく workflow、profile、protocol の問題かもしれない。
- 採用済み改善に反する観測、またはもう一歩進んだ改善案が出た。

この調査は、コードベース、既存 dossier、過去判断、tests、skills、docs を見たうえで、必要な場合だけ web や外部プロジェクト、公式 docs、論文、実務パターンを比較します。外部知見はそのまま輸入せず、HarnessOps の failure class、capability、評価ケース、guard、promotion level へ写像してから採否を考えます。

調査結果は次のいずれかに落とします。

| 出力 | 意味 |
|---|---|
| `hops lab investigate` | 既存 dossier へコード調査、外部比較、反例、追加観測を足す。 |
| `hops lab classify` | maturity、relation、promotion、guard を更新する。 |
| `hops lab capture` | 既存 dossier に入らない新しい failure class や cross-project pattern を記録する。 |
| `hops lab new-eval-case` + `hops propose` | 評価可能な改善仮説へ進める。 |
| `park` / `reject` | 証拠不足、過剰一般化、評価不能、既存構造で足りるものを増殖させない。 |

手動調査は非定期に行います。定期実行だけにすると棚卸し儀式になりやすいため、強い発火条件、release前、または人間の依頼で起動します。将来的に自動化する場合も、即実装や即Issue化ではなく、まず候補一覧と lab への追記案を出すだけに留めます。

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
Level 0: raw-observation
Level 1: project-record
Level 2: target-feedback
Level 3: target-lab-case
Level 4: cross-project-pattern
Level 5: harnessops-profile / adapter / protocol
```

この段階化により、個別事情をサニタイズし、証拠があるものだけを汎用化できます。

昇格は、作業を大きくすることではありません。次の条件を満たした時だけ、より広い level に上げます。

- 元の観測がサニタイズされている。
- 失敗クラスと対象 capability が説明できる。
- 少なくとも1つの評価ケースか、実運用上の証拠がある。
- 既存の project-specific 文脈を上流へ混ぜていない。
- ガードまたは反例検出の方法がある。

逆に、反例が出た改善は `superseded` または `rejected` に下げても構いません。昇格パイプラインは一方通行ではなく、証拠に応じて成熟度を更新するためのレーダーです。

## 主要アンチパターン

- Reflection theater: 反省文だけで評価ケースや再発防止が増えない。
- Governance theater: ルールや文書は増えるが失敗クラスが減らない。
- Skill proliferation: 問題ごとにskillを増やし、責務整理しない。
- Self-approving judge: 生成したAIがそのまま自分の改善案を高評価する。
- Metric hacking: 単一スコアのために実運用品質を犠牲にする。
- Upstream pollution: project-specific な事情を上流テンプレートへ混ぜる。
- Context leakage: 非公開研究情報、ローカルパス、HPC site固有情報を公開feedbackへ混ぜる。
- Endless meta-improvement: 改善方法自体を毎回変え、比較不能にする。
