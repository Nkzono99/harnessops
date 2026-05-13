# AI Agent経由で使い始める

HarnessOps は、人間がCLIを直接覚えて操作するより、AI Agent に「失敗を記録して」「上流へ回せる形にして」「評価ケースにして」と依頼する使い方を想定しています。

## 最初に人間が決めること

1. どのリポジトリで使うか。
2. そのリポジトリが、プロジェクト側か、上流ハーネス側か、HarnessOps自身か。
3. 外部共有してはいけない語、パス、研究内容があるか。
4. AI Agent にどこまで実行させ、どこから人間確認にするか。

## Agentへの最初の依頼

リポジトリで次のように依頼してください。

```text
このリポジトリを HarnessOps で使えるか確認して。必要なら検出結果に基づいて初期化し、doctor まで実行して。
```

Agent は通常、次を実行します。

```bash
uvx --from harnessops hops detect
uvx --from harnessops hops init --profile <detected-profile>
uvx --from harnessops hops doctor --check-overlay
```

すでに初期化済みなら、doctor だけで状態を確認します。

## Agent向けスキルの入れ方

通常は、対象リポジトリに repo-local skill を展開します。runops などの target CLI が project repository を生成する場合も、この方式を本筋にします。

```bash
uvx --from harnessops hops init --profile <profile-id> --with-agent-bridge
```

すでに初期化済みなら、repo-local skill だけを展開します。

```bash
uvx --from harnessops hops agent bridge --codex
```

これにより `.agents/skills/harnessops-bridge/` に加えて、リポジトリの role に合う HarnessOps skill が `.agents/skills/` に入ります。project-side の `feedback-source` repo では `hops-add-failure`、`hops-route-feedback`、`hops-export-feedback`、`hops-update-harness` などに絞り、`hops-run-lab` や propose/eval/decide の導線は target/meta lab repo 側に置きます。Codex の新しいセッションでは repo-local skill として表示されます。

HarnessOps は repo-local skill を標準導線にします。ユーザー領域の plugin は配布・同期・権限の面が重く、標準運用からは外しています。複数リポジトリで使う場合も、各リポジトリで `hops agent bridge` または `update-harness --agent-bridge` を実行してください。

Claude 用の repo-local skill も同じ考え方です。

```bash
uvx --from harnessops hops agent bridge --claude
```

どの場合も、スキルやブリッジは薄い案内に限定します。状態変更の正本は常に `hops` CLI です。

## 失敗を記録したいとき

人間はCLI引数を組み立てる必要はありません。次の情報をAgentに渡します。

```text
この失敗を HarnessOps に記録して。

- 題名: ハーネス更新でローカル編集が消えそうになった
- 起きたこと: update 後に手元で編集した設定が上書き候補になった
- なぜ重要か: 研究プロジェクト固有の調整が失われる可能性がある
- 望ましい挙動: 上書き前に検出し、競合コピーまたは安全なマージにする
- 上流候補: runops
- 非公開情報: ローカルパスと未公開データセット名は出さない
```

Agent は失敗レコードを作り、必要ならルーティングとサニタイズ済みエクスポートまで進めます。

## 上流へ改善候補を渡したいとき

Agentに次のように依頼します。

```text
F0001 を上流へ共有できる形にして。非公開情報をサニタイズし、共有前に残存リスクを確認して。
```

人間は、生成された `views/exported-feedback/` 配下のバンドルを共有前に確認します。未サニタイズの内容は共有しません。

## 受け取ったフィードバックを評価したいとき

ターゲット側リポジトリでAgentに依頼します。

```text
このサニタイズ済みフィードバックバンドルを harness-lab に取り込み、評価ケースと仮説を作って。採用判断は証拠がそろうまで保留にして。
```

Agent は通常、次の流れで進めます。

```bash
hops feedback import <bundle>
hops lab new-eval-case --from FB0001
hops propose --from E0001
hops eval --case E0001 --manual
hops decide --from H0001 --status parked
```

## 採用判断をしたいとき

採用には、証拠、回帰リスク、ガードパスが必要です。Agentには次のように依頼します。

```text
H0001 を採用判断にできるか確認して。証拠、回帰リスク、回帰ガードが不足していれば採用せず、不足点を教えて。
```

採用可能な場合だけ、Agent は `adopted` の判断レコードを作ります。

## 非公開情報の扱い

非公開語やパスがある場合は、早めにAgentへ伝えてください。

```text
次の語とパスは外部共有しないで。HarnessOps のサニタイズ設定にも反映して。

- private term: internal-method-name
- private path: materials/private/**
- protected path: runs/**/work/**
```

HarnessOps は既定で未サニタイズエクスポートを拒否しますが、人間のレビューは省略しないでください。

## よく使う依頼文

```text
HarnessOps の状態を確認して。壊れている管理対象ファイルや未適用マイグレーションがあれば教えて。
```

```text
この失敗がプロジェクト固有の話か、上流へ回すべき話か、HarnessOps自体の不足かを分類して。
```

```text
この上流フィードバックから評価ケースを作り、改善仮説を最小実装と中止基準付きで作って。
```

```text
採用してよいか、証拠、回帰リスク、ガードパスの観点で確認して。足りないなら保留にして。
```

## トラブル時に見るもの

- `hops doctor --check-overlay --check-records` の結果
- `.harnessops/project.toml`
- `.harnessops/lock.json`
- `harness-feedback/records/`
- `harness-lab/records/`
- `harness-lab/views/eval-results/`

現行仕様を確認したい場合は `SPEC.md`、なぜこの運用になっているかを確認したい場合は `docs/design-principles.md` を読んでください。
