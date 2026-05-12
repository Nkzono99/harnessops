---
id: IMP0002
record_type: improvement_dossier
created_at: '2026-05-13T00:21:08+09:00'
updated_at: '2026-05-13T02:42:00+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0006
eval_cases:
- E0006
hypotheses:
- H0006
decisions:
- D0007
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: not-defined
  path:
investigation: []
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/6
---

# IMP0002: FB0006: Make update-harness conflict-aware for agent bridge files

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0006`
- linked_records: `FB0006`, `E0006`, `H0006`, `D0007`

## Source Observation

Source: `harness-lab/records/feedback/FB0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`

# FB0006: Make update-harness conflict-aware for agent bridge files

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/6
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:53:22Z
updated_at: 2026-05-12T14:53:22Z

## Issue本文
## Context

While updating runops' HarnessOps bridge, `.agents/skills/hops-export-feedback/SKILL.md` was stale. Running:

```bash
hops update-harness --agent-bridge --codex
```

reported `ok` and `agent bridge: checked 9 paths`, but the stale skill file was not updated because existing skill directories are skipped unless `--force-agent-bridge` is used.

Using `--force-agent-bridge` did update the file, but that is a blunt overwrite mode. It does not distinguish between an unmodified managed file that should be refreshed and a locally edited file that should be preserved.

## Proposal

Make `hops update-harness` conflict-aware for agent bridge files, similar to the behavior expected from `runo update-harness`:

- If a managed file has not been changed locally, overwrite it with the current packaged version.
- If a managed file has local edits, preserve it and write `<path>.new` for the updated packaged version.
- `--force-agent-bridge` should remain available for explicit overwrite.
- JSON and text output should report exact counts and paths for `updated`, `unchanged`, `conflicted`, and `written_new`.
- Agent bridge files should either be tracked in the existing lock metadata or in an equivalent bridge metadata file so stale-but-unmodified files can be detected safely.

## Why this matters

The current behavior can leave target repositories with old HOPS skills while reporting a successful bridge check. In this case, runops kept a stale `hops-export-feedback` skill that said remote issues were not supported, even though HarnessOps had already added `hops feedback issue create`.

## Acceptance criteria

- `hops update-harness --agent-bridge --codex` refreshes an unmodified stale skill without requiring force.
- A locally edited managed skill is not overwritten; a `.new` file is produced instead.
- The command output makes it clear whether files were updated, skipped, or conflicted.
- Tests cover unmodified refresh, local-edit conflict, and forced overwrite.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

調査メモはまだありません。

## Evaluation

### E0006: E0006: FB0006-make-update-harness-conflict-aware-for-agent-bridge-files を評価


- source: `harness-lab/records/eval-cases/E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0006-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0006-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=3, operator_burden=4, anti_theater=5, maintainability=4, privacy_sanitization_risk=1
- notes: Implemented conflict-aware agent bridge refresh: managed bridge hashes are stored in lock metadata; unmodified stale files update automatically, local edits produce .new files, --force-agent-bridge overwrites explicitly, and JSON/text output reports checked, updated, unchanged, conflicted, and written_new paths. Verified with focused tests, full pytest, ruff, doctor, and migrate.


## Hypotheses

### H0006: H0006: E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files の仮説


Source: `harness-lab/records/hypotheses/H0006-e0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`


# H0006: E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files の仮説

## 仮説

agent bridge の管理対象ファイルに packaged digest または lock metadata を持たせ、未変更なら自動更新し、local edits なら .new へ分岐すれば、stale skill を成功扱いにしない。

## メカニズム

update-harness が bridge metadata と現在ファイルの digest を比較し、clean stale は packaged version で更新、local edits は保持して .new を書き、updated/unchanged/conflicted/written_new を出力する。

## 最小実装

Codex/Claude agent bridge の install/update path に managed file inventory と hash comparison を追加し、--force-agent-bridge は明示上書きモードとして残す。

## 代替案: 削除または統合

既存の skip-if-exists を維持し、doctor warning だけ追加する。

## 期待される利点

target repo に古い HOPS skill が残っても ok と報告される状態を防ぎ、bridge 更新の信頼性を上げる。

## 想定される欠点

bridge metadata の互換性と、既存 target repo に metadata がない場合の初回判定を慎重に扱う必要がある。

## 評価計画

未変更 refresh、local edit conflict、force overwrite の3ケースを fixture repo で実行し、text/json 出力とファイル結果を確認する。

## 中止基準

unmodified と locally edited を安全に区別できない場合、または metadata 移行が既存 bridge を壊す場合は採用しない。


## Evidence

`harness-lab/views/eval-results/E0006-manual-score.md`

## Guard

- status: not-defined
- path: None

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/6

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0007: D0007: adopted H0006


Source: `harness-lab/records/decisions/D0007-adopted-h0006.md`


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
