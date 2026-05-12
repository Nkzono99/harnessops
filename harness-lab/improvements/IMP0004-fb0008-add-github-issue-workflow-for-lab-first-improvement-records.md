---
id: IMP0004
record_type: improvement_dossier
created_at: '2026-05-13T00:21:29+09:00'
updated_at: '2026-05-13T00:32:37+09:00'
status: adopted
source_feedback: FB0008
eval_cases:
- E0008
hypotheses:
- H0008
decisions:
- D0009
classification:
  capability: unclassified
  failure_class: unclassified
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/8
---

# IMP0004: FB0008: Add GitHub issue workflow for lab-first improvement records

## Status

- status: adopted
- source_feedback: `FB0008`
- linked_records: `FB0008`, `E0008`, `H0008`, `D0009`

## Source Observation

Source: `harness-lab/records/feedback/FB0008-add-github-issue-workflow-for-lab-first-improvement-records.md`

# FB0008: Add GitHub issue workflow for lab-first improvement records

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/8
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:54:12Z
updated_at: 2026-05-12T14:54:12Z

## Issue本文
## Context

HarnessOps now has `hops feedback issue create` for sanitized exported feedback bundles. That is useful for project-side feedback records.

However, in the current runops workflow we captured a HarnessOps improvement directly via:

```bash
hops lab capture ...
hops lab new-eval-case --from FB0001
hops propose --from E0001
```

When asked to create a GitHub issue from that lab-first record, `hops feedback export --target harnessops --sanitize --format github-issue` did not find a matching project-side feedback bundle. We had to create the GitHub issue manually with `gh issue create`.

This is a gap for the lab-first improvement workflow proposed in #5.

## Proposal

Add a first-class path from `harness-lab` records to GitHub Issue drafts/creation.

Possible command shapes:

```bash
hops lab issue draft --from FB0001
hops lab issue create --from FB0001 --repo owner/repo --confirm-create
```

or:

```bash
hops feedback issue create --from-lab FB0001 --repo owner/repo --confirm-create
```

Expected behavior:

- Build an issue title/body from a lab record or improvement dossier.
- Require sanitized/public-safe content for remote issue creation.
- Print the title/body and duplicate candidates before creating anything.
- Require `--confirm-create` for remote creation.
- Write the resulting Issue URL back to the source lab record.
- Support records created by `hops lab capture`, not only exported project feedback bundles.

## Why this matters

If HarnessOps wants agents to capture non-issue-driven improvements in `harness-lab`, those records also need a smooth promotion path to the external task tracker. Otherwise the lab becomes a side notebook that must be manually retyped into GitHub Issues.

## Related

- #4 added GitHub issue helpers for exported feedback workflows.
- #5 proposes a generic improve-harness workflow in HarnessOps.
- #7 discusses simplifying `harness-lab` around per-improvement dossiers.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Evaluation

### E0008: E0008: FB0008-add-github-issue-workflow-for-lab-first-improvement-records を評価


Source: `harness-lab/records/eval-cases/E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md`


# E0008: FB0008-add-github-issue-workflow-for-lab-first-improvement-records を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0008`。

## タスク

この失敗を防ぐべき挙動を記述してください。

## 期待される挙動

ターゲットハーネスが、非公開プロジェクト文脈を漏らさずに失敗クラスを扱います。

## 合格基準

- 失敗条件が検出または防止される。
- 提案される挙動が上流メンテナにとって実行可能である。
- 非公開プロジェクト詳細を必要としない。

## 不合格基準

- 失敗を見逃す。
- 再現に非公開文脈が必要になる。


## Hypotheses

### H0008: H0008: E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records の仮説


Source: `harness-lab/records/hypotheses/H0008-e0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md`


# H0008: E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records の仮説

## 仮説

lab-first records から sanitized GitHub issue draft/create へ進む first-class command を追加すると、harness-lab の改善記録を外部 task tracker に手入力せず昇格できる。

## メカニズム

lab record または improvement dossier から public-safe title/body を生成し、duplicate candidates を表示し、remote create は --confirm-create の時だけ実行し、作成 URL を source record に書き戻す。

## 最小実装

hops lab issue draft と create、または feedback issue create --from-lab を追加し、FB/E/H または dossier 由来の本文生成と sanitize gate を実装する。

## 代替案: 削除または統合

feedback export の project-side bundle flow だけを維持し、lab-first record は手動で GitHub issue 化する。

## 期待される利点

issue 起点ではない改善を lab に残した後、GitHub Issues へ自然に接続でき、lab が side notebook 化しにくくなる。

## 想定される欠点

GitHub provider 依存が core CLI に増えるため、provider 境界と gh unavailable fallback を明確にする必要がある。

## 評価計画

FB0001 のような lab capture 由来 record から issue draft を生成し、sanitize gate、duplicate 表示、confirm-create、URL writeback をテストする。

## 中止基準

未サニタイズ情報を remote issue body に混ぜるリスクが下げられない場合、または provider-specific glue が core を過度に複雑化する場合は採用しない。


## Evidence

`harness-lab/views/eval-results/E0008-manual-score.md`

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/8

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0009: D0009: adopted H0008


Source: `harness-lab/records/decisions/D0009-adopted-h0008.md`


# D0009: adopted H0008

## 判断

adopted

## 理由

H0008 の最小実装を採用。lab-first record から sanitized draft/create へ進む first-class command を追加し、remote create は重複確認と --confirm-create の下だけにした。

## 証拠

Tests: uv run pytest tests/test_cli/test_safety.py -k 'lab_issue or feedback_issue_create_writes_back'; uv run pytest tests/test_cli/test_mvp_flow.py tests/test_cli/test_safety.py tests/test_agent_harness_contract.py; uv run pytest; uv run ruff check src/harnessops/cli/lab.py tests/test_cli/test_safety.py; hops lab issue --help; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0008-manual-score.yml

## 回帰リスク

Moderate. The command reuses existing GitHub issue helpers and sanitizer, but imports private helper functions from feedback CLI; future cleanup can move them to a shared GitHub issue bridge module.

## フォローアップ

Consider provider abstraction or shared helper extraction if more lab issue workflows are added.

## 回帰ガード

tests/test_cli/test_safety.py

