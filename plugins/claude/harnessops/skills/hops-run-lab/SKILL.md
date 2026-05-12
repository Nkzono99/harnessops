---
name: hops-run-lab
description: harness-lab で評価ケース、仮説、判断を扱うときに使う。
---

`hops doctor --check-overlay` を実行する。`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えない。

非自明なローカル改善、issue化前の観測、HarnessOps 自身の改善は、実装前または遅くともrelease前に `hops lab capture` で `FB` レコードにする。

```bash
hops lab capture --title "<title>" --summary "<summary>" --expected-change "<expected>"
hops lab dossier --from FB0001
hops lab investigate --from IMP0001 --kind codebase --summary "<調査結果>"
hops lab classify --from IMP0001 --source-type friction --scope harnessops-core --maturity investigated
```

その後、`hops lab new-eval-case`、`hops propose --manual-template`、`hops eval --manual`、`hops decide` を使う。採用後は `hops lab classify --guard-status implemented --guard-path <path>` でガードをdossierに反映する。

メタ仮説スキャン:

- ユーザー割り込み、繰り返し摩擦、局所判断の一般化、既存判断への反例、移行/互換判断、評価の空白、外部比較の発見、認知負荷の兆候が出たら30秒だけスキャンする。
- 問い: 「この作業中に、今のタスクを越えて再利用できる考え方、反例、設計原則、評価方法、移行方針、agent行動ルールは見えたか」。
- 既存テーマに関係するなら `hops lab investigate` または `hops lab classify` に留める。新しい失敗クラスや二階観測なら `hops lab capture` する。
- スキャンは作業を止めるためではなく、忘れやすい高信号の気づきを短く保存するために行う。

ガードレール:

- 評価証拠なしに採用を勧めない。
- 観測を実装へ直行させず、コード調査、再現確認、外部比較、既存判断との関係を `hops lab investigate` に残す。
- `source-type`、`scope`、`maturity`、`relation`、`promotion-level` を分類し、既存テーマへの反例や拡張は孤立レコードにしない。
- 仮説にはメカニズム、評価計画、中止基準を含める。
- 新しいワークフロー面を追加する前に、削除または統合を優先する。
- 採用済み判断には、証拠、回帰リスク、ガードパスを含める。
- ホールドアウトケースや非公開プロジェクト文脈を露出しない。
