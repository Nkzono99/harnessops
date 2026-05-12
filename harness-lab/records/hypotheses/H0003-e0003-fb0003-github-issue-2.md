---
id: H0003
record_type: hypothesis
created_at: '2026-05-12T14:25:30+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0003
---

# H0003: E0003-fb0003-github-issue-2 の仮説

## 仮説

sanitized feedback を GitHub Issue 化する標準 CLI または skill 導線を追加すると、外部共有時の sanitize 確認と record link の戻し忘れを減らせる。

## メカニズム

exported sanitized bundle を入力に、issue draft 表示、duplicate search、明示確認、Issue URL の feedback record 反映を一つの workflow にまとめる。

## 最小実装

まず remote create は行わず、hops feedback export --sanitize --format github-issue の出力を検証して markdown draft を生成する skill/CLI を追加する。

## 代替案: 削除または統合

既存 hops feedback export の github-issue format を強化し、repo-local skill はその thin wrapper に留める。

## 期待される利点

target skill が GitHub 固有処理を抱えず、未サニタイズ情報を公開 issue へ戻す事故を減らせる。

## 想定される欠点

GitHub tooling 有無や認証状態により挙動分岐が増える。

## 評価計画

未サニタイズ bundle は拒否し、sanitized bundle は issue draft を出し、remote create は explicit flag なしで行わないことをテストする。

## 中止基準

既存 export format の薄い改善だけで十分で、独立 workflow が重複導線になる場合は統合案へ切り替える。
