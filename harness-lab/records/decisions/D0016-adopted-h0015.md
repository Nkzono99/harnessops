---
id: D0016
record_type: decision
created_at: '2026-05-13T02:37:35+09:00'
status: adopted
source: H0015
evidence:
  summary: 'tests/test_cli/test_mvp_flow.py asserts dossiers omit ## フィクスチャ and manual eval markdown omits the full snapshot; E0015 manual score records this change.'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0016: adopted H0015

## 判断

adopted

## 理由

The functioning evaluation artifact is the manual eval yml/score path, while full eval case bodies were adding template noise to dossiers. Summarizing evaluation evidence keeps dossiers readable and preserves canonical eval records for linking.

## 証拠

tests/test_cli/test_mvp_flow.py asserts dossiers omit ## フィクスチャ and manual eval markdown omits the full snapshot; E0015 manual score records this change.

## 回帰リスク

Low: eval_case records remain canonical, and dossier still links source, scores, and notes.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
