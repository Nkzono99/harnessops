---
id: H0041
record_type: hypothesis
created_at: '2026-05-19T03:29:32+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0041
---

# H0041: E0041-fb0045-harness-lab-needs-forgetting-policy の仮説

## 仮説

A source-preserving lab retire command can remove stale research candidates from active priority and memory inputs while preserving the canonical record.

## メカニズム

Update record frontmatter with archived or superseded status plus retirement metadata, then make queue and abstraction-source collectors treat retired records as closed unless explicitly requested.

## 最小実装

Add a narrow hops lab retire command for existing lab records, skip retired records in review queue and abstraction input by default, and guard it with a CLI fixture test.

## 代替案: 削除または統合

Only document a forgetting policy or manually edit records, but that leaves no repeatable guard and keeps stale next commands in the queue.

## 期待される利点

Priority lanes can retire stale local-only or superseded items without deleting audit records, reducing repeated queue pressure.

## 想定される欠点

A too-broad retire primitive could hide useful counterexamples, so the command must preserve reason and evidence metadata and avoid deleting files.

## 評価計画

Create a research scan with a next command, retire it, verify the file remains, queue omits it, and abstraction input sources omit it while doctor and migrate still pass.

## 中止基準

Reject or park if retirement deletes records, hides adopted guards, bypasses source feedback links, or requires direct manual edits to harness-lab.
