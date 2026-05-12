---
id: D0010
record_type: decision
created_at: '2026-05-13T00:35:01+09:00'
status: adopted
source: H0009
evidence:
  summary: 'Tests: uv run pytest tests/test_cli/test_mvp_flow.py -k feedback_import_issue_captures_github_context;
    uv run pytest; uv run ruff check src/harnessops/cli/feedback.py tests/test_cli/test_mvp_flow.py;
    hops doctor --check-overlay --check-records; hops migrate --check. Manual eval:
    harness-lab/views/eval-results/E0009-manual-score.yml'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0010: adopted H0009

## 判断

adopted

## 理由

H0009 の最小修正を採用。gh issue view の JSON を UTF-8 として明示的に読み、Windows cp932 既定環境でも Unicode issue import が壊れないようにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py -k feedback_import_issue_captures_github_context; uv run pytest; uv run ruff check src/harnessops/cli/feedback.py tests/test_cli/test_mvp_flow.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0009-manual-score.yml

## 回帰リスク

Low. The change is limited to the gh issue view subprocess call used by feedback import; invalid UTF-8 bytes are replaced and existing fallback behavior is retained for malformed output.

## フォローアップ

Consider moving all gh subprocess calls to a shared UTF-8 wrapper.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
