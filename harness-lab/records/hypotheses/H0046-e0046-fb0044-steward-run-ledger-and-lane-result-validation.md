---
id: H0046
record_type: hypothesis
created_at: '2026-05-22T03:39:31+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0046
---

# H0046: E0046-fb0044-steward-run-ledger-and-lane-result-validation の仮説

## 仮説

Steward lane results should optionally carry typed remote_actions so finalize lanes can discover requested GitHub issue, PR, label, merge, or release actions without scraping prose.

## メカニズム

Expose remote_actions as an optional lane-result field in the supervisor plan, mention it in every lane handoff, and validate each action as a small object with action, target, intent, and optional condition/privacy text.

## 最小実装

Keep the required lane result contract unchanged; add optional remote_actions validation and steward tests for valid and malformed remote-action payloads.

## 代替案: 削除または統合

Continue putting issue closure, PR body, and release intent only in recommended_next prose.

## 期待される利点

Finalize agents can build PR bodies and authorized remote issue actions from durable ledger data while old lanes remain valid when they omit the field.

## 想定される欠点

Lane authors have one more optional field to understand; overly strict action schemas could reject useful future remote intents.

## 評価計画

Run tests/test_cli/test_steward.py and verify validate-lane-result accepts well-formed remote_actions and rejects malformed remote_actions while legacy lane results still pass.

## 中止基準

Reject if the field must become required for all lanes or if validation cannot catch malformed remote action payloads.
