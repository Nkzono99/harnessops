# HarnessOps: 自己改善ループを成功させるためのコア思想

## 0. 一文要約

自己改善ループの本体は、AIに「もっと良くして」と頼むことではない。  
本体は、**失敗を観測し、改善仮説に変換し、評価で選別し、採用判断を記録し、再発防止パターンとして蓄積するシステム**である。

```text
AI generates candidates.
HarnessOps selects, evaluates, records, and promotes what actually works.
```

HarnessOps の役割は、AIを賢く見せることではなく、AIの改善提案を **検証可能な改善実験** に変換することである。

---

## 1. 根本原則: 自己改善は「生成」ではなく「選別」である

AIは改善案を大量に出せる。  
しかし、それだけでは自己改善にはならない。

多くの自己改善ループが失敗する理由は、改善案の生成能力が不足しているからではなく、**どの改善が本当に効いたかを選別する仕組みがないから**である。

したがって、HarnessOps の中心設計は次である。

```text
Candidate generation is cheap.
Selection is the core capability.
Evidence is the currency.
History is the memory.
```

言い換えると、自己改善ループに必要なのは「賢い反省」ではなく、**改善案を落とす力**である。

採用する改善よりも、却下する改善の質がシステム全体の品質を決める。

---

## 2. バグ修正ループと根本改善ループの違い

バグ修正ループが比較的成功しやすいのは、外部オラクルがあるからである。

```text
failing test -> patch -> passing test
```

一方、根本改善は次のようになりやすい。

```text
vague dissatisfaction -> AI review -> plausible additions -> temporary satisfaction
```

この後者は改善ではない。多くの場合、次のような **改善劇場** になる。

```text
- README が長くなる
- skill が増える
- ルールが増える
- チェック項目が増える
- しかし実際の失敗クラスは減っていない
```

HarnessOps は、この差を埋めるために存在する。

根本改善を成立させるには、バグ修正におけるテストに相当するものを人工的に作る必要がある。

```text
failure corpus
capability map
eval cases
holdout cases
scorecards
kill criteria
decision log
regression checks
```

---

## 3. 自己改善ループを構成する5つの役割

自己改善を1つのAIエージェントに閉じ込めてはいけない。  
成功するループには、少なくとも5つの役割がある。

| 役割 | 責務 |
|---|---|
| Generator | 改善案、仮説、実装候補を出す |
| Judge | 失敗クラス、評価基準、採用可否を判定する |
| Environment | 実行結果、テスト、現場運用、ユーザー反応を返す |
| Memory | 失敗、評価、判断、却下理由、再発防止を蓄積する |
| Owner | 価値判断、優先順位、複雑性の許容量を決める |

AIは Generator と Judge の一部を担える。  
しかし、Owner まで完全に委任してはいけない。

Owner が決めるべきものは次である。

```text
- 何を価値とみなすか
- どの失敗を重く見るか
- どの複雑性を許容するか
- どの改善を採用し、どの改善を捨てるか
- 何を project-local に留め、何を upstream 化するか
```

HarnessOps は、Owner の判断を置き換えるのではなく、Owner が判断しやすい構造を作る。

---

## 4. 改善ループの標準形

HarnessOps が前提とする自己改善ループは次である。

```text
1. Observe
   現場で失敗・違和感・運用負荷・品質低下を観測する

2. Record
   失敗を構造化して記録する

3. Route
   project-local / target-upstream / meta-harness / external に分類する

4. Hypothesize
   改善仮説を作る

5. Evaluate
   eval case / holdout / scorecard で比較する

6. Decide
   採用・却下・保留を記録する

7. Apply
   最小差分で実装または運用変更する

8. Guard
   回帰テスト・再発防止・migration を整える

9. Promote
   繰り返す失敗を一般化し、profile / adapter / protocol に昇格する
```

重要なのは、`Improve` という曖昧な工程を置かないことである。  
改善は、観測・仮説・評価・判断・昇格に分解する。

---

## 5. 3種類の改善を混ぜない

自己改善が破綻する最大の原因の一つは、異なる種類の改善をすべて `improvement` と呼ぶことである。

HarnessOps では、少なくとも次の3種類を分ける。

## 5.1 Project evolution

project-repository の中身の進化である。

例:

```text
- 実験の方向性を変える
- 深掘り対象を変える
- 論文の中心 claim を変える
- 研究仮説を更新する
- 追加解析を行う
```

これは `research/` や `notes/` に置く。  
`harness-feedback/` には置かない。

## 5.2 Harness feedback

project-repository で観測された、target-repository や meta-harness に戻すべき問題である。

例:

```text
- runops に pivot decision workflow がない
- paper-harness に claim pivot skill がない
- meta-harness が project-local decision と upstream feedback を分類できない
```

これは project-repository の `harness-feedback/` に置く。

## 5.3 Harness lab improvement

target-repository や HarnessOps 自身で、upstream として改善を評価・実装する活動である。

例:

```text
- runops の update-harness を改善する
- paper-harness の public terminology check を改善する
- HarnessOps の feedback routing schema を改善する
```

これは target-repository または HarnessOps repository の `harness-lab/` に置く。

---

## 6. 置き場所の原則

HarnessOps の情報配置は次の原則に従う。

```text
project-repository:
  project の中身と、現場で観測された harness feedback を持つ

target-repository:
  upstream としての改善実験、評価、採用判断を持つ

HarnessOps repository:
  改善方法、schema、migration、plugin、CLI、profile、adapter を持つ
```

具体的には次の通り。

| Repository | 置き場所 | 意味 |
|---|---|---|
| project-repository | `research/`, `notes/` | project の中身の進化 |
| project-repository | `harness-feedback/` | harness / upstream / meta への feedback |
| target-repository | `harness-lab/` | upstream 改善の実験・評価・採用判断 |
| HarnessOps repository | `harness-lab/` | HarnessOps 自体の改善 |
| all repositories | `.harnessops/` | link, lock, migration, managed metadata |

この分離により、研究判断・運用改善・メタ改善が混ざらない。

---

## 7. Feedback と Lab は別物である

HarnessOps では、project 側と upstream 側の責務を明確に分ける。

```text
harness-feedback/
  観測と送信の場所

harness-lab/
  評価と採用判断の場所
```

project-repository は原則として upstream 本体を改善しない。  
project-repository は、失敗を記録し、local workaround を整理し、sanitized feedback を target-repository または HarnessOps に送る。

一方で target-repository は、受け取った feedback を eval case に変換し、改善仮説を作り、実装し、採用・却下を記録する。

この分離により、次の両方を満たせる。

```text
- 開発上は issue / PR flow を保つ
- AI改善ループ上は失敗・評価・判断の履歴を保つ
```

---

## 8. 改善仮説には必ず kill criteria を持たせる

自己改善ループで最も重要な設計要素の一つは、**改善案を捨てる条件を先に決めること**である。

改善仮説は必ず次を持つ。

```text
- Hypothesis
- Mechanism
- Target capability
- Expected benefit
- Expected side effect
- Minimal implementation
- Evaluation plan
- Kill criteria
```

`Kill criteria` がない改善案は採用候補にしない。

理由は単純である。  
失敗した改善案を捨てられないループは、複雑性を蓄積し続ける。

```text
No kill criteria -> no real experiment.
No real experiment -> no self-improvement.
```

---

## 9. すべての変更は failure class に紐づける

HarnessOps では、変更は「良さそうだから」では採用しない。  
原則として、すべての変更は既知の失敗クラスまたは新規観測 failure に紐づける。

```text
Bad:
  Add a new skill because it might be useful.

Good:
  Add or modify a skill because F012 shows that users repeatedly fail to route project-local pivots into research/decisions, causing upstream feedback pollution.
```

このルールにより、以下を防ぐ。

```text
- skill proliferation
- rule proliferation
- documentation theater
- speculative architecture
- governance overhead
```

新機能追加よりも、既存機能の削除・統合・評価強化を優先する。

---

## 10. 評価は単一スコアにしない

自己改善は単一の点数では測れない。  
単一スコアは最適化されやすく、Goodhart 化しやすい。

HarnessOps の scorecard は多軸であるべきである。

```text
impact
mechanism clarity
evaluability
minimality
regression risk
operator burden
anti-theater score
maintainability
privacy / sanitization risk
```

特に重要なのは `anti-theater score` である。

これは次を問う。

```text
この変更は、実際の失敗クラスを減らしているか。
それとも、改善っぽい構造を増やしているだけか。
```

---

## 11. AI Judge を信用しすぎない

AI に改善案を出させ、同じAIに採点させると、自己承認ループになりやすい。

HarnessOps では、可能な限り次を分ける。

```text
generator
judge
adversary
human owner
static checks
runtime checks
holdout cases
```

同じモデル・同じコンテキスト・同じプロンプトで生成と評価を閉じない。

AI judge は有用だが、最終オラクルではない。  
AI judge は評価支援者であり、評価基準・実行結果・人間判断を置き換えるものではない。

---

## 12. Holdout を持たない自己改善は過適合する

eval case は改善案作成に使ってよい。  
holdout case は改善案作成に使ってはいけない。

```text
eval-cases:
  改善案の設計・調整に使う

holdout-cases:
  採用前の最終確認に使う
```

holdout がないと、AIは評価ケースに合わせて改善案を作り、実運用で悪化する。

HarnessOps は、最初から大規模な holdout を要求しない。  
しかし、重要な capability には少なくとも少数の holdout を持つべきである。

---

## 13. 改善方法の改善は低頻度で行う

毎回メタ改善をしてはいけない。

```text
Bad:
  project を改善するたびに、評価方法・schema・profile・分類法も変える

Good:
  project 改善は短周期で回す
  改善方法の改善は、複数回の実験結果を見てから行う
```

評価方法を毎回変えると、比較不能になる。  
自己改善のための自己改善は、別レーンで管理する。

```text
Fast lane:
  project / target の通常改善

Slow lane:
  HarnessOps の方法論、schema、profile、protocol の改善
```

この分離がないと、改善システム自体が不安定になる。

---

## 14. 昇格パイプラインを持つ

project 固有の出来事を、いきなり汎用ルールにしてはいけない。

HarnessOps では、知識を次の段階で昇格させる。

```text
Level 0: Raw observation
  project の notes / research / harness-feedback に残る

Level 1: Project-local record
  failure, workaround, feedback として構造化される

Level 2: Target feedback
  runops / paper-harness などに sanitized feedback として送られる

Level 3: Target lab case
  eval case / hypothesis / decision として upstream で評価される

Level 4: Cross-project pattern
  複数projectで再発した failure pattern として認識される

Level 5: HarnessOps profile / adapter / protocol
  汎用的な仕組みとして実装される
```

この昇格パイプラインにより、project-specific な事情が upstream template や meta-level protocol を汚染することを防ぐ。

---

## 15. Local patch は禁止ではなく、disposition を必須にする

project-repository では、upstream 修正を待てないことがある。  
そのため local patch は完全禁止にしない。

ただし、必ず disposition を持たせる。

```yaml
local_patch:
  type: workaround | upstream-candidate | project-specific | discard-after-update | do-not-upstream
  reason: "..."
  expires_when: "..."
  target: "runops | paper-harness | harnessops | none"
```

local patch は、記録されていないと負債になる。  
記録され、期限と行き先が明確なら、改善ループの入力になる。

---

## 16. Plugin-first, CLI-authoritative

HarnessOps の利用体験は plugin-first でよい。  
しかし、状態管理は CLI が authoritative でなければならない。

```text
Codex / Claude plugin:
  人間とAI Agentの操作入口
  workflow guidance
  skill routing

hops CLI:
  state mutation
  schema validation
  migration
  lock management
  feedback export/import
  lab workflow
```

plugin や skill は `harness-feedback/` や `harness-lab/` の内部構造を直接編集しない。  
必ず `hops` CLI を呼ぶ。

これにより、overlay layout が変わっても下流 project は追従しやすくなる。

---

## 17. HarnessOps が守るべき不変条件

HarnessOps の設計では、次を不変条件とする。

```text
1. Every change should be linked to a failure, feedback, eval case, or explicit strategic decision.

2. Every failure should be routed.

3. Every hypothesis should include mechanism, evaluation plan, and kill criteria.

4. Every adopted change should create or update a regression guard.

5. Every local patch should have disposition.

6. Every project-specific observation must be sanitized before target/meta promotion.

7. Every generated overlay change must be schema-versioned and migratable.

8. Every plugin workflow must delegate state mutation to the CLI.

9. Every lab decision should record adoption, rejection, or deferral rationale.

10. Every meta-level change should be justified by multiple observations or a severe single failure.
```

---

## 18. Anti-patterns

HarnessOps が明示的に避けるべきアンチパターンは次である。

## 18.1 Reflection theater

AIが反省文を書くだけで、評価ケースや再発防止が増えない。

## 18.2 Governance theater

ルール・文書・skill が増えるが、失敗クラスが減らない。

## 18.3 Skill proliferation

問題ごとに新skillを作り、統合・削除・責務整理をしない。

## 18.4 Self-approving judge

生成したAIが、そのまま自分の改善案を高評価する。

## 18.5 Metric hacking

単一スコアを上げるために、実運用品質を犠牲にする。

## 18.6 Upstream pollution

project-specific な事情を、そのまま target template や meta protocol に混ぜる。

## 18.7 Context leakage

非公開研究情報、ローカルパス、HPC site 固有情報、投稿先固有事情を public feedback に混ぜる。

## 18.8 Endless meta-improvement

改善方法そのものを毎回変更し、比較不能にする。

---

## 19. 最小実用ループ

HarnessOps の最小実用ループは次で足りる。

```bash
hops init --profile <profile>
hops add-failure
hops route
hops feedback export --sanitize
hops lab import
hops lab decide
```

0.1 の段階では、完全な自動評価よりも以下を重視する。

```text
- 失敗を構造化できること
- 行き先を分類できること
- sanitized feedback を作れること
- target 側で lab record に取り込めること
- 採用・却下・保留の判断を残せること
```

これだけでも、AIの改善提案はかなり扱いやすくなる。

---

## 20. 成熟度モデル

HarnessOps の導入成熟度は次のように見る。

| Level | 状態 | 説明 |
|---|---|---|
| 0 | Ad hoc reflection | AIにレビューさせるだけ |
| 1 | Feedback capture | 失敗・違和感を記録できる |
| 2 | Routing | project / target / meta を分類できる |
| 3 | Eval-backed improvement | eval case に基づき改善できる |
| 4 | Lab discipline | 仮説、実験、scorecard、decision が揃う |
| 5 | Cross-project learning | 複数projectから pattern promotion できる |
| 6 | Protocol evolution | profile / adapter / protocol が evidence-based に進化する |

目指すべき最初の到達点は Level 3 である。  
Level 6 を最初から目指すと、仕組みが重くなりすぎる。

---

## 21. HarnessOps の最終的な思想

HarnessOps は「AIに自己改善させるツール」ではない。  
HarnessOps は、AIが出す改善案を、失敗・評価・判断・履歴に接続するための運用基盤である。

```text
Do not ask AI to improve itself.
Build a system where improvement candidates must survive evidence, evaluation, and decision history.
```

この思想の中心は次である。

```text
- 失敗は資産である
- 改善案は仮説である
- 評価は選別機構である
- 採用判断は記録すべき意思決定である
- 却下理由は将来の改善品質を上げる
- project-specific な知見は、すぐに汎用化しない
- 汎用化は、観測・sanitize・評価・昇格を経て行う
- AIは候補生成者であり、HarnessOps は改善実験OSである
```

一文でまとめると、HarnessOps のコア思想は次である。

> **自己改善を、反省ではなく、証拠に基づく改善実験として扱う。**

