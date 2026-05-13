# Daily Steward Automation Prompt

この文書は、常時起動PCの Codex App automation で `hops-daily-steward` を定期実行するための推奨プロンプトです。

目的は、夜間に clean な `main` を pull してから、issue / feedback / lab / doctor 状態を読み、既存 skill に委譲しながら最大1件の改善候補を local advance することです。remote write は automation branch の push までに留め、main push、PR、Issue操作、release は人間確認に残します。

## Recommended Prompt

```text
Run the repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` for this repository.

Runtime config:
- mode: advance-local
- timezone: Asia/Tokyo
- subagents: explicitly allowed
- max-systemic-candidates: 1
- remote-write: automation-branch-only
- main-push: false
- create-pr: false
- issue-comment-close-create: false
- release: false
- end-policy: commit-local
- automation-branch-prefix: codex/steward
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true
- stop-on-privacy-risk: true

Start:
1. Ensure the worktree is on `main`. If it is on another branch and clean, switch to `main`. If it is dirty, stop and report.
2. Run `uv run --with-editable . hops steward preflight --pull --json`.
3. If `can_continue` is false, stop before HOPS state changes and report the blocker.

Subagents:
- You are explicitly authorized to use subagents.
- Spawn separate subagents for triggered independent lanes when available:
  - issue-triager
  - open-inventor
  - librarian
  - critic
  - maintainer
  - evaluator only when advancing E/H/D or guard work
- Keep the main agent as conductor/editor-in-chief.
- Pass minimal context to each subagent.
- If subagents are unavailable, run lanes sequentially and report `inline-fallback`.

Open invention:
- Run `hops-open-meta-scan` only on weekly runs, release prep, repeated friction, issue clusters, loop stagnation, or explicit high-signal trigger.
- Raw Ideas are ephemeral. Do not capture them directly.

Selection and advance:
- Prefer existing issues, dossiers, or records over new records.
- Select at most one systemic candidate.
- Use `hops-research-improvements` for evidence/routing/park/reject.
- Use `hops-run-lab` for eval case, hypothesis, manual eval, decision, and guard.
- Use `hops-update-harness` only for doctor/update/bridge/managed-file signals.
- Human review is not required for local advance, but evidence, validation, guard, and kill criteria are mandatory.

Validation:
Run, at minimum:
- `uv run pytest -q`
- `uv run ruff check src tests`
- `uv run --with-editable . hops doctor --check-overlay --check-records`
- `uv run --with-editable . hops migrate --check`

End:
- If no changes were made, report no-op.
- If changes were made and validation passed:
  1. Run `uv run --with-editable . hops steward finalize --policy commit-local --validation-passed --branch "codex/steward/<YYYYMMDD>-daily" --message "Daily steward automation"`
  2. Push only that automation branch: `git push -u origin HEAD`
  3. Switch back to `main`
  4. Do not create PRs, comments, issues, releases, or push main.
- If validation failed, leave the patch in place and report the failure.

Final report:
- sync / doctor result
- subagents used or inline fallback
- selected candidate or no-op rationale
- actions performed
- validation result
- branch and commit hash if created
- pushed automation branch if any
- blocked / parked / rejected items
- human decisions needed
```

## Operator Notes

- `main-push: false` keeps the nightly loop from changing the release branch without review.
- `end-policy: commit-local` keeps the next scheduled run from being blocked by the previous run's dirty worktree.
- The automation branch can be reviewed, merged, or deleted later by a human.
- For a more conservative setup, change `end-policy` to `patch-only`; the next run will stop until the patch is reviewed.
