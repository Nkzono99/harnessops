---
id: D0020
record_type: decision
created_at: '2026-05-13T11:48:26+09:00'
status: adopted
source: H0019
evidence:
  summary: Focused regression test passes; tests/test_cli/test_mvp_flow.py passes; running hops lab refresh-views on this repository clears generated-view warnings from doctor.
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0020: adopted H0019

## 判断

adopted

## 理由

H0019 の最小実装を採用。既存の lab refresh-views を広げるだけで、doctor が管理する lab generated artifact の stale warning を同じコマンドで修復できる。

## 証拠

Focused regression test passes; tests/test_cli/test_mvp_flow.py passes; running hops lab refresh-views on this repository clears generated-view warnings from doctor.

## 回帰リスク

Low to moderate: refresh_managed_files may touch generated static lab files, but existing conflict handling writes .new for locally edited managed files and dynamic views are regenerated as before.

## フォローアップ

Consider a future top-level hops views refresh/status alias if generated-view management grows beyond lab-specific usage.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
