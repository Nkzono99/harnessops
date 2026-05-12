---
id: H0004
record_type: hypothesis
created_at: '2026-05-12T14:25:38+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0004
---

# H0004: E0004-fb0004-github-issue-3 の仮説

## 仮説

feedback import と update-harness が generated view 更新と managed lock hash 更新を同じ経路で扱えば、直後の doctor warning を防げる。

## メカニズム

refresh_views が生成した view の実ファイル bytes と同じ sha256 を lock managed_files に反映し、update-harness でも同じ helper を使う。

## 最小実装

feedback import 後の doctor --check-overlay --check-records が warning を出さない回帰テストを追加し、update-harness の managed hash 更新経路も同じ関数に寄せる。

## 代替案: 削除または統合

動的 generated view を managed_files の drift 判定から外す。

## 期待される利点

import/update 直後の false positive warning が減り、target repo 側の更新導線が安定する。

## 想定される欠点

lock 更新タイミングを誤ると、ユーザー編集済み view を見落とすリスクがある。

## 評価計画

issue の再現手順を fixture 化し、feedback import と update-harness 後に doctor が ok であることを確認する。

## 中止基準

warning が実際には stale view を検出しており、lock 更新でユーザー編集を隠すことが分かった場合は設計を見直す。
