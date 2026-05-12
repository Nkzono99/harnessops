---
id: H0005
record_type: hypothesis
created_at: '2026-05-12T14:25:47+09:00'
status: proposed
target_capability: unclassified
source_eval_case: E0005
---

# H0005: E0005-fb0005-github-issue-4 の仮説

## 仮説

GitHub issue bridge helpersを hops 側に寄せると、target skill は record/routing/sanitize/export/import の正本を HarnessOps に委譲し、GitHub 固有 glue だけに薄くできる。

## メカニズム

feedback import --issue が issue title/body/labels/author/timestamps を取得し、export 側には sanitized issue draft/create helper を追加して、remote create は explicit confirmation flag でのみ実行する。

## 最小実装

第一段階として feedback import --issue の GitHub context capture を実装し、gh unavailable 時は既存 placeholder fallback を維持する。

## 代替案: 削除または統合

GitHub bridge は CLI に入れず repo-local skill のみで提供し、hops は bundle import/export だけを維持する。

## 期待される利点

runops などの target-specific wrappers から手書き glue を減らし、sanitize と duplicate 確認の責務を標準化できる。

## 想定される欠点

hops CLI が GitHub tooling に近づきすぎるため、依存境界と fallback 挙動を明確にする必要がある。

## 評価計画

gh がある場合は title/body/labels/comment metadata を record に反映し、gh がない場合は placeholder fallback で doctor が通ることをテストする。

## 中止基準

GitHub issue 操作が provider-specific すぎて HarnessOps core の責務を濁す場合は plugin/skill 側へ戻す。
