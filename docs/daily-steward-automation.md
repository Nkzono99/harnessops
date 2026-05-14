# Daily Steward 自動化プロンプト

この文書は、常時起動している PC の Codex App automation で `hops-daily-steward` を強い自動化として定期実行するための prompt です。HarnessOps core だけでなく、HarnessOps を導入した target repository / project repository にも配布して使えます。

方針は、権限を弱めず、探索圧を上げることです。clean repo で global gate が通るなら、status-only no-op を通常結果にせず、reactive work、既存 queue、proactive discovery、record/metadata work、safe work packet のいずれかへ進めます。remote write は automation branch から PR/merge へ通し、protected base branch への direct push は使いません。

## Prompt

```text
このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。

Runtime:
- mode: autonomous-improvement
- intensity: aggressive
- timezone: Asia/Tokyo
- base-branch: main
- merge-target-branch: main
- subagents: explicitly allowed
- remote-write: automation-branch-merge
- github-flow: use `hops github-flow ...` in target/meta repos when available
- protected-branch-direct-push: false
- direct-push-protected-branch: false
- end-policy: commit-local
- automation-branch-prefix: codex/steward
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true
- stop-on-privacy-risk: true

Budgets:
- discovery-cards: 8
- recordable-candidates: 5
- low-risk-work-packets: 5
- medium-risk-work-packets: 3
- high-risk-work-packets: 1
- remote-issue-actions: 10
- auto-merge-prs: repo-policy-limited

Authority:
- create/update/merge automation PRs: true
- create/comment/close GitHub issues: true
- release: true, only when repo-native release criteria are met
- push only automation branches
- never direct-push protected base branch
- never stash/reset/rebase/force-push

Progress policy:
- no status-only no-op when global gates pass
- if reactive work exists, process it first
- if no reactive work exists but a candidate queue exists, advance queue work within risk budget
- if no candidate queue exists, run `hops-open-meta-scan` and create discovery cards
- use `hops-research-improvements` to promote selected cards to research-scan / feedback / issue / work packet
- record/research/metadata work may proceed with concrete evidence or observation; validation/guard is required only from implementation onward

Update lane:
- do not update HarnessOps to latest as a mandatory start step
- if preflight / doctor / update notice / lock drift / managed-file drift shows stale HarnessOps state, treat `hops-update-harness` as a T2/T3 work packet
- in target/project repos, use `uvx --refresh-package harnessops --from harnessops hops update-harness` when the latest published HarnessOps runtime is needed
- in the HarnessOps core repo, treat update work as repo-local implementation/release work rather than PyPI self-update
- after update-harness, rerun doctor, migrate check, and relevant repo-native validation

Start:
1. Ensure the worktree is clean.
2. Switch to `base-branch` if clean and needed.
3. Run `hops steward preflight --pull --json`.
4. Stop if `can_continue=false`; report the blocker before any HOPS state change.
5. Read `.harnessops/project.toml`.
6. Route core / target / meta lab repos through `harness-lab/`; route project repos through `harness-feedback/`; project repo に `harness-lab/` を作らないでください。

Gate levels:
- Global gate: dirty start, diverged branch, failed preflight, unknown repo role, fatal doctor result, privacy risk, or unauthorized remote action stops all writes.
- Record gate: research-scan / investigate / classify / feedback / issue draft requires concrete observation, evidence ref, or explicit hypothesis; validation and guard are not yet required.
- Implementation gate: code / docs / skill / workflow edits require validation command or validation gap statement, plus guard plan when behavior changes.
- Merge gate: PR merge / issue close / release requires validation passed, no conflict, and repo policy / required checks satisfied.

Validation:
- run repo-native test/lint/build/domain checks when discoverable
- run `hops doctor --check-overlay --check-records`
- run `hops migrate --check`
- if validation is unavailable, report the validation gap and only perform record/queue-level work

Finalize:
- if no changes, report discovery/selection attempts and the blocker, exhausted budget, or discovery failure
- if validation fails, leave patch and do not push
- if validation passes:
  - fetch/prune and confirm `merge-target-branch` is not behind or diverged
  - in target/meta repos with GitHub Flow enabled, publish with `hops github-flow publish --branch "codex/steward/<YYYYMMDD>-daily" --message "Daily steward automation" --validation-passed`
  - create PR with `hops github-flow pr --base <merge-target-branch> --title "Daily steward automation" --body "<summary>"`
  - merge with `hops github-flow merge --require-checks` when checks and branch protection pass
  - in repos without GitHub Flow enabled, use the repo-native finalize path documented by that repo
  - perform authorized issue actions tied to the selected work packet
  - release only if documented release criteria are satisfied

Release may run only when:
- PR was merged into `merge-target-branch`
- repo has documented release command or repo-local release skill
- version/changelog/tag condition is explicit
- tests and required checks passed
- generated tag does not already exist
- release notes contain only sanitized public information

Final report:
- sync / doctor result
- discovery generated
- selected work packets
- actions performed
- validation result
- branch / commit / PR / merge / release
- remote issue actions
- blocked / parked / rejected
- remaining queue
- human decisions needed
```

## Operating Notes

- The old single systemic-candidate cap is intentionally absent. Candidate count is controlled by risk tier and work-packet budgets.
- `hops-open-meta-scan` is the proactive discovery lane when reactive work and queue work are thin.
- `no-op` is not the happy path. It is valid only for a concrete blocker, failed validation, exhausted budget, or explicit discovery failure.
- Record-level work can create useful queue depth before implementation guards exist. Implementation, merge, issue close, and release still require the stronger gates.
- GitHub Flow is the default remote path for target/meta repos: automation branch, PR, required checks / branch protection, then merge. Project repos usually do not receive `hops-github-flow`. Git Flow-style repositories can set `merge-target-branch: develop`.
