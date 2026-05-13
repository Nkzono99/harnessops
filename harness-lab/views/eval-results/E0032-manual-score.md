<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0032

送信元: `harness-lab/records/eval-cases/E0032-fb0035-expose-lab-health-in-steward-preflight.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

Implemented a narrow deterministic preflight extension. Validation: uv run pytest -q passed 94 tests; uv run ruff check changed files passed; hops doctor --check-overlay --check-records ok; hops migrate --check reported no pending migrations. Live preflight JSON now exposes lab_health.status=needs-abstraction and routes librarian with stale-memory trigger reasons.

## 評価ケース

- capability: daily_steward_orchestration
- failure_class: count_based_preflight_misses_stale_lab_health
- source_feedback: FB0035
