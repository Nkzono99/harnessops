# フィードバックルーティング仕様

ルーティングは、プロジェクト発展、ローカルプロセスの問題、ターゲットハーネスの不足、HarnessOps のメタ不足、プロトコル不足、外部システムの問題、非公開レコードを分離し、上流汚染を防ぎます。

## 分類値一覧

| 分類値 | 意味 | 既定の行き先 |
|---|---|---|
| `project-evolution` | 研究、論文、プロジェクト内容が変化した。 | `research/` または `notes/` |
| `project-local-process` | プロジェクト固有のプロセスまたは回避策。 | ローカルメモまたは回避策レコード |
| `target-upstream-candidate` | ターゲットハーネスが変更を検討すべき内容。 | runops、paper-harness など |
| `meta-harness-candidate` | HarnessOps のスキーマ、CLI、ルーティング、マイグレーション、プラグインの不足。 | HarnessOps |
| `protocol-candidate` | 共通 `.harness/manifest` または共有CLI規約の不足。 | HarnessOps プロトコル/仕様 |
| `external-candidate` | クラスタ、シミュレータ、ジャーナルなどの外部システム。 | 外部トラッカーまたはメモ |
| `do-not-upstream` | 明示的にローカル/非公開。 | 上流エクスポートなし |

## イベント分割

1つの観測イベントから複数のレコードが生まれる場合があります。研究方針の転換は `research/decisions/` に置きます。一方、runops に方針転換ワークフローが不足しているなら `harness-feedback/records/upstream-feedback/` になり、ルーティングの曖昧さは `meta-feedback` になります。

## 責務境界

HarnessOps は feedback の状態管理と運搬を担当します。target harness は domain 固有の診断材料を提供します。

HarnessOps の責務:

- failure / feedback / imported feedback の record schema。
- disposition、routing evidence、sanitize、export/import。
- `harness-feedback/` と `harness-lab/` の管理。
- imported feedback から eval case、hypothesis、decision へ進む共通フロー。

target repository の責務:

- profile、failure class、capability、protected/private path。
- domain-specific triage skill。
- target CLI から `hops` を呼ぶ lifecycle hook。
- 既存 feedback skill を残す場合は、HarnessOps CLI への thin wrapper にする。

triage は分割します。

| triage | 管理者 | 例 |
|---|---|---|
| meta routing triage | HarnessOps | project-local か、target-upstream か、meta-harness かを分類する。 |
| domain diagnosis triage | target repository | runops の Slurm/campaign/manifest 問題、paper-harness の claim/citation/venue 問題を判定する。 |
| lab triage | HarnessOps + target profile | imported feedback を eval case、backlog、reject、issue draft に分ける。 |

target 側の `feedback/triage` は独自に `records/` を作らず、`hops add-failure`、`hops route`、`hops add-feedback`、`hops feedback export --sanitize`、`hops feedback import` を呼びます。

## ルーティング証拠

`hops route --record <id>` はdispositionを保存します。人間のレビュアーは次を確認します。

- これは対象プロジェクト自体の発展か。
- プロジェクト詳細から独立した上流ツールの不足があるか。
- サニタイズ後に問題を再現できるか。
- HarnessOps のスキーマ、ルーティング、プロセスの不足を示しているか。
- 上流化すると非公開またはプロジェクト固有の文脈が漏れるか。

## 現在の実装

MVP は決定的ヒューリスティックと明示的な `--target` / `--disposition` 上書きを使います。アダプタ固有のルーティングは、同じレコードスキーマを迂回せず、この規則から拡張します。

`hops feedback add --target <target>` は将来の alias 候補です。現行実装では、観測は `hops add-failure`、上流/メタ下書きは `hops add-feedback --from <Fid>` を正本にします。
