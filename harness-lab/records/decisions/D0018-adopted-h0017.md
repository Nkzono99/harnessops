---
id: D0018
record_type: decision
created_at: '2026-05-13T03:37:48+09:00'
status: adopted
source: H0017
evidence:
  summary: tests/test_cli/test_mvp_flow.py records a research scan and asserts structured frontmatter, candidate next_command, generated view, and doctor compatibility; tests/test_agent_harness_contract.py keeps packaged research skill guidance aligned.
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0018: adopted H0017

## 判断

adopted

## 理由

The RS record path makes meta-improvement research reviewable and routable before converting candidates into lab actions.

## 証拠

tests/test_cli/test_mvp_flow.py records a research scan and asserts structured frontmatter, candidate next_command, generated view, and doctor compatibility; tests/test_agent_harness_contract.py keeps packaged research skill guidance aligned.

## 回帰リスク

Moderate: a new record type could add meta-noise, mitigated by deliberate skill trigger criteria, candidate recommendations, and not replacing existing investigate/capture/propose commands.

## フォローアップ

Use research-scan for deliberate multi-candidate meta improvement research; avoid it for one-off notes that fit existing dossier investigate/classify.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
