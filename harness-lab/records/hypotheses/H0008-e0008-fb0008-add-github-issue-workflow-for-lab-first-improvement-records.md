---
id: H0008
record_type: hypothesis
created_at: '2026-05-13T00:01:40+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0008
---

# H0008: E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records の仮説

## 仮説

lab-first records から sanitized GitHub issue draft/create へ進む first-class command を追加すると、harness-lab の改善記録を外部 task tracker に手入力せず昇格できる。

## メカニズム

lab record または improvement dossier から public-safe title/body を生成し、duplicate candidates を表示し、remote create は --confirm-create の時だけ実行し、作成 URL を source record に書き戻す。

## 最小実装

hops lab issue draft と create、または feedback issue create --from-lab を追加し、FB/E/H または dossier 由来の本文生成と sanitize gate を実装する。

## 代替案: 削除または統合

feedback export の project-side bundle flow だけを維持し、lab-first record は手動で GitHub issue 化する。

## 期待される利点

issue 起点ではない改善を lab に残した後、GitHub Issues へ自然に接続でき、lab が side notebook 化しにくくなる。

## 想定される欠点

GitHub provider 依存が core CLI に増えるため、provider 境界と gh unavailable fallback を明確にする必要がある。

## 評価計画

FB0001 のような lab capture 由来 record から issue draft を生成し、sanitize gate、duplicate 表示、confirm-create、URL writeback をテストする。

## 中止基準

未サニタイズ情報を remote issue body に混ぜるリスクが下げられない場合、または provider-specific glue が core を過度に複雑化する場合は採用しない。
