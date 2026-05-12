---
id: H0002
record_type: hypothesis
created_at: '2026-05-12T14:25:18+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0002
---

# H0002: E0002-fb0002-github-issue-1 の仮説

## 仮説

paper-harness-upstream profile の command references を現行 paperops/pops CLI に追従させると、target repo 初期化後の manifest が陳腐化しない。

## メカニズム

built-in profile metadata の doctor/update/migrate/feedback/version command を pops ベースへ更新し、必要なら互換 alias を保持する。

## 最小実装

paper-harness-upstream profile の command entries を更新し、generated manifest のテストで pops command を確認する。

## 代替案: 削除または統合

paper-harness-upstream を残し、新規 paperops-upstream profile を追加して detect 側で新 profile を選ばせる。

## 期待される利点

paperops target repo で init 直後から正しい CLI 導線を提示できる。

## 想定される欠点

既存 paper-harness CLI 名を期待している利用者がいる場合は移行案内が必要になる。

## 評価計画

profile fixture または init 実行結果の manifest.toml を検証し、hops doctor と migrate --check を通す。

## 中止基準

paperops 側が paper-harness command を正式互換として維持している、または pops へ切り替えると既存 target repo を壊す場合は保留する。
