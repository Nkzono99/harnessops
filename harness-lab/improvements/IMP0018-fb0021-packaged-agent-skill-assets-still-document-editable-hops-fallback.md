---
id: IMP0018
record_type: improvement_dossier
created_at: '2026-05-13T17:15:18+09:00'
updated_at: '2026-05-13T17:19:45+09:00'
status: adopted
source_type: external-issue
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0021
eval_cases:
- E0021
hypotheses:
- H0021
decisions:
- D0022
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract
investigation:
- created_at: '2026-05-13T17:15:29+09:00'
  kind: issue-overlap
  summary: 'Issue #10 narrows issue #9 to packaged Codex/Claude SKILL and README assets: downstream repositories should be instructed to use the PyPI/uvx HarnessOps invocation instead of uv run --with-editable . hops, which only works from the HarnessOps checkout.'
  evidence_ref: https://github.com/Nkzono99/harnessops/issues/10
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/10
---

# IMP0018: FB0021: Packaged agent SKILL assets still document editable hops fallback

## Status

- status: adopted
- maturity: adopted
- source_type: external-issue
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0021`
- linked_records: `FB0021`, `E0021`, `H0021`, `D0022`

## Source Observation

Source: `harness-lab/records/feedback/FB0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`

# FB0021: Packaged agent SKILL assets still document editable hops fallback

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/10
author: Nkzono99
labels: なし
created_at: 2026-05-13T08:01:45Z
updated_at: 2026-05-13T08:01:45Z

## Issue本文
## Summary

The packaged HarnessOps agent assets still tell agents to use an editable local checkout fallback:

```text
uv run --with-editable . hops <command>
```

Current HarnessOps docs for target/project integration already assume the PyPI package path, so linked downstream repositories should be guided toward the PyPI-installed CLI instead, for example:

```text
uvx --from harnessops hops <command>
```

## Observed from downstream update

While updating a linked downstream repository with PyPI `harnessops==0.1.3`, the repo-local agent SKILL copies had to be adjusted from editable fallback to PyPI/`uvx` fallback.

## Affected upstream assets

`rg "uv run --with-editable|with-editable"` shows at least:

- `src/harnessops/core/agent_bridge.py`
- `src/harnessops/agent_assets/plugins/codex/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/codex/harnessops/README.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/README.md`

## Desired behavior

- Packaged Codex/Claude SKILL assets should match the PyPI distribution model documented in `docs/`.
- When `hops` is not on `PATH`, agent instructions should prefer PyPI execution, e.g. `uvx --from harnessops hops <command>`.
- `hops update-harness` should propagate that guidance into linked downstream repositories without requiring local manual edits.

## Notes

This came up because downstream `paperops` was updated to use the PyPI install path rather than a local editable HarnessOps checkout.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

- 2026-05-13T17:15:29+09:00 [issue-overlap] Issue #10 narrows issue #9 to packaged Codex/Claude SKILL and README assets: downstream repositories should be instructed to use the PyPI/uvx HarnessOps invocation instead of uv run --with-editable . hops, which only works from the HarnessOps checkout. (evidence: https://github.com/Nkzono99/harnessops/issues/10)

## Research Scans

research scan はまだありません。


## Evaluation

### E0021: E0021: FB0021-packaged-agent-skill-assets-still-document-editable-hops-fallback を評価


- source: `harness-lab/records/eval-cases/E0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0021-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0021-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=4, maintainability=4, privacy_sanitization_risk=1
- notes: Packaged/generated agent assets now use uvx --from harnessops hops for missing PATH fallback; editable checkout commands remain only in HarnessOps development docs. Contract tests, targeted update-harness tests, full pytest, ruff, doctor, and migrate all passed.


## Hypotheses

### H0021: H0021: E0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback の仮説


Source: `harness-lab/records/hypotheses/H0021-e0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`


# H0021: E0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback の仮説

## 仮説

Packaged agent assets should guide downstream agents to a PyPI-backed hops invocation when hops is not on PATH.

## メカニズム

Replace editable checkout fallback text in generated bridge, packaged Codex/Claude skill assets, and packaged plugin READMEs with uvx --from harnessops hops; keep editable commands only in HarnessOps repository development docs.

## 最小実装

Update BRIDGE_TEXT, packaged plugin skill/readme assets, source package asset copies, and contract tests that reject editable fallback in packaged assets.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0021` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run agent harness contract tests and grep packaged/generated assets to confirm uvx fallback is present and editable fallback is absent from target-facing assets.

## 中止基準

Reject if HarnessOps repository development workflows lose their editable checkout commands or generated target skills still mention uv run --with-editable . hops <command>.


## Evidence

`harness-lab/views/eval-results/E0021-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/10

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0022: D0022: adopted H0021


Source: `harness-lab/records/decisions/D0022-adopted-h0021.md`


# D0022: adopted H0021

## 判断

adopted

## 理由

Adopted because packaged agent assets now match the PyPI/uvx downstream invocation model while preserving editable commands for HarnessOps development workflows.

## 証拠

pytest -q; ruff check .; hops doctor --check-overlay --check-records; hops migrate --check; rg confirms target-facing editable fallback is absent.

## 回帰リスク

Low; changes are text guidance and contract assertions, with update-harness propagation verified through targeted CLI tests.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_agent_harness_contract.py::test_generated_bridge_explains_hops_contract
