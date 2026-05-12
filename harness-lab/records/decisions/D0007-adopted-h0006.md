---
id: D0007
record_type: decision
created_at: '2026-05-13T00:14:30+09:00'
status: adopted
source: H0006
evidence:
  summary: 'Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py;
    uv run pytest; uv run ruff check src/harnessops/core/agent_bridge.py src/harnessops/cli/update_harness.py
    src/harnessops/core/overlay.py src/harnessops/cli/agent.py tests/test_cli/test_mvp_flow.py;
    hops doctor --check-overlay --check-records; hops migrate --check. Manual eval:
    harness-lab/views/eval-results/E0006-manual-score.yml'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0007: adopted H0006

## 判断

adopted

## 理由

H0006 の最小実装を採用。agent bridge 管理ファイルは lock metadata で前回管理版を追跡し、update-harness が unmodified stale、local edit conflict、force overwrite を区別できるようになった。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/core/agent_bridge.py src/harnessops/cli/update_harness.py src/harnessops/core/overlay.py src/harnessops/cli/agent.py tests/test_cli/test_mvp_flow.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0006-manual-score.yml

## 回帰リスク

Moderate-low. The change adds lock metadata under agent_bridge and keeps write_bridge compatibility; legacy files without metadata are treated as conflicts rather than silently overwritten.

## フォローアップ

Consider documenting the new agent_bridge lock section in SPEC/CLI docs when preparing the next release notes.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
