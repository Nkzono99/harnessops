# Daily Steward 自動化プロンプト

この文書は、常時起動している PC の Codex App automation で `hops-daily-steward` を単一 automation として走らせるための prompt です。HarnessOps を導入した target repository / project repository にも配布して使えます。強い自動化の入口は1つに保ち、実作業は supervisor が順番に lane skill へ委譲します。

方針は、prompt を太らせず、lane を飛ばさないことです。supervisor は pull/preflight、停止判断、subagent 同期、最終要約だけを担当し、maintenance、issue、open-meta-scan、invention、priority improvement、finalize の中身は各 skill に任せます。

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
- update-policy: apply
- protected-branch-direct-push: false
- direct-push-protected-branch: false
- automation-branch-prefix: codex/steward
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true
- stop-on-privacy-risk: true

Authority:
- create/update/merge automation PRs: true
- create/comment/close GitHub issues: true
- release: true, only when repo-native release criteria are met
- push only automation branches
- never direct-push protected base branch
- never stash/reset/rebase/force-push

Supervisor rules:
- first read `.harnessops/project.toml`
- run `hops steward run start --pull --json --update-policy apply`
- stop before writes if `can_continue=false`
- use `run_id` and `supervisor_plan` from run start as the source of truth for lane order, handoff text, and lane result contract
- do not perform lane work directly
- for each lane, spawn one subagent, wait for its final result, then decide whether to continue
- after each lane, record its result with `hops steward run record-lane-result --run-id <run_id> --lane <lane>`
- end the ledger with `hops steward run end --run-id <run_id> --status <status>`
- if subagents are unavailable, run the lane skill inline one at a time and report `inline_fallback=true`
- do not skip a later lane merely because an earlier lane made a valid change
- project repo に `harness-lab/` を作らないでください

Finalize:
- if validation fails, leave patch local and do not push
- require repo-native validation plus HOPS doctor/migrate checks before push or merge
- if validation passes in target/meta repos with GitHub Flow enabled:
  - `hops github-flow publish --branch "codex/steward/<YYYYMMDD>-daily" --message "Daily steward automation" --validation-passed`
  - `hops github-flow pr --base <merge-target-branch> --title "Daily steward automation" --body "<summary>"`
  - `hops github-flow merge --require-checks`
- in repos without GitHub Flow, use the repo-native finalize path documented by that repo
- release only when PR is merged, a release skill or documented command exists, version/changelog/tag criteria are explicit, checks passed, tag is new, and notes are sanitized
- before release, if `harness-lab/records/` or `harness-lab/improvements/` deletions occurred since the previous release tag, create and verify a `hops lab archive pack` asset and attach it to the release

Final report:
- sync / doctor result
- lane result summary
- validation result
- branch / commit / PR / merge / release
- remote issue actions
- blocked / parked / rejected
- remaining queue
- human decisions needed
```

## Operating Notes

- The supervisor skill should stay small. Add procedural detail to lane skills, not to the automation prompt.
- The run ledger lives under `.harnessops/cache/steward-runs/` and is local operational state, not a PR artifact.
- `open-meta-scan` returns its broad scan as optional structured `artifacts.meta_scan`; the open scan skill itself stays a non-recording idea generator.
- A maintenance PR does not end the run by itself; open-meta-scan, invention, and priority lanes still run unless a fatal gate blocks them.
- `update-policy: apply` lets target/project repos apply current published HarnessOps assets during the maintenance lane. HarnessOps core treats update work as repo-local implementation/release work.
- GitHub Flow is the default remote path for target/meta repos: automation branch, PR, required checks / branch protection, then merge. Project repos usually do not receive `hops-github-flow`.
- Lab physical forgetting belongs to release, not daily cleanup. Finalize/release should use `hops lab archive plan --since-ref <previous-tag>` and only create a pack when deleted source records or dossier exist.
