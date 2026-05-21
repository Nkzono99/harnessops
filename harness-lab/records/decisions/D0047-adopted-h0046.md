---
id: D0047
record_type: decision
created_at: '2026-05-22T03:43:08+09:00'
status: adopted
source: H0046
evidence:
  summary: tests/test_cli/test_steward.py validates supervisor-plan exposure, well-formed remote_actions acceptance, malformed remote_actions rejection, and legacy lane-result compatibility.
  guard_path: tests/test_cli/test_steward.py
---

# D0047: adopted H0046

## 判断

adopted

## 理由

Optional typed remote_actions extends the existing steward ledger without changing required lane fields, making finalize-facing issue/PR/release intent durable instead of prose-only.

## 証拠

tests/test_cli/test_steward.py validates supervisor-plan exposure, well-formed remote_actions acceptance, malformed remote_actions rejection, and legacy lane-result compatibility.

## 回帰リスク

Future remote action payloads may need richer fields, but unknown extra fields remain allowed and malformed core fields fail validation.

## フォローアップ

Finalize lane should prefer recorded remote_actions when present and can still fall back to prior lane prose for this run's #40 closure.

## 回帰ガード

tests/test_cli/test_steward.py
