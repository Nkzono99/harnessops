---
id: H0006
record_type: hypothesis
created_at: '2026-05-13T00:01:05+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0006
---

# H0006: E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files の仮説

## 仮説

agent bridge の管理対象ファイルに packaged digest または lock metadata を持たせ、未変更なら自動更新し、local edits なら .new へ分岐すれば、stale skill を成功扱いにしない。

## メカニズム

update-harness が bridge metadata と現在ファイルの digest を比較し、clean stale は packaged version で更新、local edits は保持して .new を書き、updated/unchanged/conflicted/written_new を出力する。

## 最小実装

Codex/Claude agent bridge の install/update path に managed file inventory と hash comparison を追加し、--force-agent-bridge は明示上書きモードとして残す。

## 代替案: 削除または統合

既存の skip-if-exists を維持し、doctor warning だけ追加する。

## 期待される利点

target repo に古い HOPS skill が残っても ok と報告される状態を防ぎ、bridge 更新の信頼性を上げる。

## 想定される欠点

bridge metadata の互換性と、既存 target repo に metadata がない場合の初回判定を慎重に扱う必要がある。

## 評価計画

未変更 refresh、local edit conflict、force overwrite の3ケースを fixture repo で実行し、text/json 出力とファイル結果を確認する。

## 中止基準

unmodified と locally edited を安全に区別できない場合、または metadata 移行が既存 bridge を壊す場合は採用しない。
