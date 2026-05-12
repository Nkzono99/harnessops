---
id: D0008
record_type: decision
created_at: '2026-05-13T00:24:49+09:00'
status: adopted
source: H0007
evidence:
  summary: 'Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py;
    uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py
    src/harnessops/core/render.py src/harnessops/core/overlay.py tests/test_cli/test_mvp_flow.py;
    hops doctor --check-overlay --check-records; hops migrate --check. Generated dossiers:
    IMP0001-IMP0004. Manual eval: harness-lab/views/eval-results/E0007-manual-score.yml'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0008: adopted H0007

## 判断

adopted

## 理由

H0007 の最小実装を採用。正規化レコードは正本として残し、日常レビュー用に IMP dossier を生成/更新する互換レイヤーを追加した。

## 証拠

Tests: uv run pytest tests/test_cli/test_mvp_flow.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/overlay.py tests/test_cli/test_mvp_flow.py; hops doctor --check-overlay --check-records; hops migrate --check. Generated dossiers: IMP0001-IMP0004. Manual eval: harness-lab/views/eval-results/E0007-manual-score.yml

## 回帰リスク

Moderate-low. Dossiers are generated from existing records and do not replace the normalized source of truth; new managed view introduction required refresh_views to register generated view hashes.

## フォローアップ

Consider adding richer dossier update options after the lab-first issue workflow is implemented.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
