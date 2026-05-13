# Daily Steward 自動化プロンプト

この文書は、常時起動している PC の Codex App automation で `hops-daily-steward` を定期実行するための推奨プロンプトです。HarnessOps core だけでなく、HarnessOps を導入した target repository / project repository にも配布して使えます。

目的は、夜間に clean な既定 branch を pull してから、issue / feedback / lab / doctor の状態を読み、repo role に応じて既存 skill に委譲しながら最大 1 件の改善候補を local advance することです。通常運用では remote write は automation branch の push までに留め、既定 branch push、PR、Issue 操作、release は人間確認に残します。

以下の prompt では `base-branch: main` としています。対象リポジトリの既定 branch が `master` や `develop` なら置き換えてください。validation も対象リポジトリの実際の test / lint / build / domain check に置き換えます。

## 推奨プロンプト

```text
このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。

Runtime config:
- mode: advance-local
- timezone: Asia/Tokyo
- base-branch: main
- subagents: explicitly allowed
- max-systemic-candidates: 1
- remote-write: automation-branch-only
- base-branch-push: false
- create-pr: false
- issue-comment-close-create: false
- release: false
- end-policy: commit-local
- automation-branch-prefix: codex/steward
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true
- stop-on-privacy-risk: true

開始:
1. worktree が `base-branch` 上にあることを確認してください。別 branch 上で clean なら `base-branch` に切り替えてください。dirty なら停止して報告してください。
2. `hops steward preflight --pull --json` を実行してください。
3. `can_continue` が false の場合は、HOPS state change に進む前に停止し、blocker を報告してください。
4. `.harnessops/project.toml` の repo role を読み、target/meta lab repo では `harness-lab/`、project repo では `harness-feedback/` を使うように routing してください。project repo に `harness-lab/` を作らないでください。

サブエージェント:
- サブエージェントの利用を明示的に許可します。
- 独立して発火した lane があり、利用可能な場合は、lane ごとに別サブエージェントを起動してください。
  - issue-triager
  - open-inventor
  - librarian
  - critic
  - maintainer
  - evaluator は E/H/D または guard work を advance する時だけ使う
- main agent は conductor / editor-in-chief として振る舞ってください。
- 各サブエージェントへ渡す context は最小限にしてください。
- サブエージェントを利用できない場合は、lane を順番に実行し、`inline-fallback` として報告してください。

発散的な発想:
- `hops-open-meta-scan` は、weekly run、release prep、繰り返し発生する摩擦、issue cluster、loop stagnation、または明確な high-signal trigger がある場合だけ実行してください。
- Raw Ideas は一時的な材料です。直接 capture しないでください。

選別と advance:
- 新しい record を作る前に、既存 issue、dossier、record に接続できないかを優先してください。
- systemic candidate は最大 1 件だけ選んでください。
- evidence / routing / park / reject には `hops-research-improvements` を使ってください。
- eval case、hypothesis、manual eval、decision、guard には `hops-run-lab` を使ってください。
- doctor / update / bridge / managed-file の signal がある場合だけ `hops-update-harness` を使ってください。
- local advance に人間レビューは不要ですが、evidence、validation、guard、kill criteria は必須です。

Validation:
対象リポジトリの README、CI、package metadata、Makefile、task runner から test / lint / build / domain check を選んで実行してください。
- `<repo-native test command>`
- `<repo-native lint/build/domain check command>`
- `hops doctor --check-overlay --check-records`
- `hops migrate --check`

妥当な validation command が見つからない場合は、HOPS の doctor / migrate check と、実行できなかった validation gap を報告してください。

終了:
- 変更がない場合は no-op として報告してください。
- 変更があり、validation が成功した場合:
  1. `hops steward finalize --policy commit-local --validation-passed --branch "codex/steward/<YYYYMMDD>-daily" --message "Daily steward automation"` を実行してください。
  2. automation branch だけを push してください: `git push -u origin HEAD`
  3. `base-branch` に戻ってください。
  4. PR、コメント、Issue、release、既定 branch push は作成しないでください。
- validation が失敗した場合は patch を残し、失敗内容を報告してください。

最終報告:
- sync / doctor result
- subagents used または inline fallback
- selected candidate または no-op rationale
- actions performed
- validation result
- branch と commit hash が作成された場合はその値
- push した automation branch があればその branch
- blocked / parked / rejected items
- human decisions needed
```

## 運用メモ

- `base-branch-push: false` により、夜間ループが review なしで既定 branch を変更しないようにします。
- `end-policy: commit-local` により、前回 run の dirty worktree が次回の scheduled run を止め続ける事態を避けます。
- automation branch は、あとで人間が review、merge、削除できます。
- より慎重に運用したい場合は `end-policy` を `patch-only` に変更してください。その場合、次回 run は patch が review されるまで停止します。

## 完全自動化プロンプト: 既定 branch push と remote action

この章は、nightly run が validation 済みの変更を `main` へ直接 push し、必要に応じて Issue、PR、release などの remote action も実行してよい完全自動化運用向けです。停止条件は、開始時の同期不備、validation failure、git の明確な競合に絞ります。

```text
このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。

Runtime config:
- mode: advance-local
- timezone: Asia/Tokyo
- base-branch: main
- subagents: explicitly allowed
- max-systemic-candidates: 1
- remote-write: full
- base-branch-push: true
- create-pr: true
- issue-comment-close-create: true
- release: true
- end-policy: commit-local
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true

開始:
1. worktree が `base-branch` 上にあることを確認してください。別 branch 上で clean なら `base-branch` に切り替えてください。dirty なら停止して報告してください。
2. `hops steward preflight --pull --json` を実行してください。
3. `can_continue` が false の場合は、HOPS state change に進む前に停止し、blocker を報告してください。
4. `.harnessops/project.toml` の repo role を読み、target/meta lab repo では `harness-lab/`、project repo では `harness-feedback/` を使うように routing してください。project repo に `harness-lab/` を作らないでください。

サブエージェント:
- サブエージェントの利用を明示的に許可します。
- 独立して発火した lane があり、利用可能な場合は、lane ごとに別サブエージェントを起動してください。
  - issue-triager
  - open-inventor
  - librarian
  - critic
  - maintainer
  - evaluator は E/H/D または guard work を advance する時だけ使う
- main agent は conductor / editor-in-chief として振る舞ってください。
- 各サブエージェントへ渡す context は最小限にしてください。
- サブエージェントを利用できない場合は、lane を順番に実行し、`inline-fallback` として報告してください。

発散的な発想:
- `hops-open-meta-scan` は、weekly run、release prep、繰り返し発生する摩擦、issue cluster、loop stagnation、または明確な high-signal trigger がある場合だけ実行してください。
- Raw Ideas は一時的な材料です。直接 capture しないでください。

選別と advance:
- 新しい record を作る前に、既存 issue、dossier、record に接続できないかを優先してください。
- systemic candidate は最大 1 件だけ選んでください。
- evidence / routing / park / reject には `hops-research-improvements` を使ってください。
- eval case、hypothesis、manual eval、decision、guard には `hops-run-lab` を使ってください。
- doctor / update / bridge / managed-file の signal がある場合だけ `hops-update-harness` を使ってください。
- local advance に人間レビューは不要ですが、evidence、validation、guard、kill criteria は必須です。
- Issue の作成/コメント/クローズ、PR の作成/更新/merge、既定 branch push、release は、選択した候補の自然な次の一手であれば実行してよいです。

Validation:
対象リポジトリの README、CI、package metadata、Makefile、task runner から test / lint / build / domain check を選んで実行してください。
- `<repo-native test command>`
- `<repo-native lint/build/domain check command>`
- `hops doctor --check-overlay --check-records`
- `hops migrate --check`

妥当な validation command が見つからない場合は、HOPS の doctor / migrate check と、実行できなかった validation gap を報告してください。

終了:
- 変更がない場合は no-op として報告してください。
- validation が失敗した場合は patch を残し、失敗内容を報告してください。push はしないでください。
- 変更があり、validation が成功した場合:
  1. `git fetch --prune origin` を実行してください。
  2. `git rev-list --left-right --count HEAD...origin/<base-branch>` で、現在の branch が behind または diverged ではないことを確認してください。remote が進んでいる場合は、可能なら fast-forward pull してください。できない場合は停止して報告してください。
  3. `hops steward finalize --policy commit-local --validation-passed --branch <base-branch> --message "Daily steward automation"` を実行してください。
  4. `git status --short --branch` が clean で、`base-branch` が `origin/<base-branch>` より ahead であることを確認してください。
  5. 既定 branch を push してください: `git push origin <base-branch>`
  6. GitHub Issue の作成、更新、コメント、クローズが必要なら実行してください。
  7. branch-based change に PR が適している場合は、PR を作成、更新、または merge してください。
  8. release が適切で、version/tag 条件を満たしているなら、repo-local の `release` skill または対象リポジトリの documented release command を使って release を作成してください。

最終報告:
- sync / doctor result
- subagents used または inline fallback
- selected candidate または no-op rationale
- actions performed
- validation result
- main commit hash が作成された場合はその値
- remote actions performed
- blocked / parked / rejected items
- human decisions needed
```

この完全自動化プロンプトは、validation 成功を `main` 更新や remote action の十分な gate とみなせるリポジトリだけで使ってください。
