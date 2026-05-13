# Daily Steward 自動化プロンプト

この文書は、常時起動している PC の Codex App automation で `hops-daily-steward` を定期実行するための推奨プロンプトです。HarnessOps core だけでなく、HarnessOps を導入した target repository / project repository にも配布して使えます。

目的は、夜間に clean な既定 branch を pull してから、issue / feedback / lab / doctor の状態を読み、repo role に応じて既存 skill に委譲しながら lane ごとの上限内で改善候補を local advance することです。通常運用では systemic candidate は conservative に 1 件へ抑え、metadata / guard backfill や read-only park/reject は別枠で処理できます。remote write は automation branch と、その branch から許可された merge target への merge に限定し、既定 branch への direct push は使いません。

以下の prompt は GitHub Flow を基本にし、`base-branch: main` から automation feature branch を切って PR を作り、branch protection / required checks 通過後に `main` へ merge します。対象リポジトリの既定 branch が `master` なら置き換えてください。Git Flow 風に運用する repo だけ `merge-target-branch: develop` に変更できます。validation も対象リポジトリの実際の test / lint / build / domain check に置き換えます。

## 推奨プロンプト

```text
このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。

Runtime config:
- mode: advance-local
- timezone: Asia/Tokyo
- base-branch: main
- merge-target-branch: main
- subagents: explicitly allowed
- max-systemic-candidates: 1
- lane-budgets:
  - systemic-candidates: 1
  - metadata-guard-backfills: 3
  - read-only-park-reject: 5
- remote-write: automation-branch-merge
- base-branch-push: false
- protected-branch-direct-push: false
- create-pr: true
- merge-automation-branch: true
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
3. `can_continue` が false の場合は、HOPS state change に進む前に停止し、blocker を報告してください。`lab_health.status` が `needs-abstraction` の場合は、librarian lane の入力として扱い、preflight 内では memory 更新を書き込まないでください。
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
- metadata / guard backfill は最大 3 件まで処理してよいですが、各 item に evidence、risk、guard path、validation result を持たせてください。
- read-only の park / reject / no-op / routing 判断は最大 5 件まで処理してよいです。
- item 数を増やしても validation や採用判断の証拠基準は下げないでください。
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
  3. `git fetch --prune origin` を実行してください。
  4. `merge-target-branch` が behind / diverged でないことを確認してください。remote が進んでいれば fast-forward pull し、できなければ停止してください。
  5. automation branch から `merge-target-branch` への PR を作成または更新してください。
  6. required checks がある場合は通過を確認し、通っていない場合は merge せずに PR / branch を残して報告してください。
  7. checks と branch protection が許す場合は PR を merge してください。squash / merge commit / fast-forward は repo の通常ポリシーに従ってください。
  8. `base-branch` または `merge-target-branch` に戻り、clean であることを確認してください。
  9. コメント、Issue、release、既定 branch direct push は作成しないでください。
- validation が失敗した場合は patch を残し、失敗内容を報告してください。

最終報告:
- sync / doctor result
- subagents used または inline fallback
- selected candidate または no-op rationale
- actions performed
- validation result
- branch と commit hash が作成された場合はその値
- push した automation branch があればその branch
- PR または merge を行った場合はその番号 / merge target
- blocked / parked / rejected items
- human decisions needed
```

## 運用メモ

- `base-branch-push: false` と `protected-branch-direct-push: false` により、夜間ループは `main` へ direct push しません。
- `end-policy: commit-local` により、前回 run の dirty worktree が次回の scheduled run を止め続ける事態を避けます。
- automation branch は、validation 後に PR/merge できる場合は自動で merge します。branch protection、required checks、conflict で止まる場合だけ、人間が review、merge、削除します。
- 標準は GitHub Flow です。automation branch を feature branch として扱い、PR を通して `main` へ merge します。
- Git Flow 風に運用する repository だけ、`merge-target-branch: develop` にして automation を `develop` へ集約し、`main` は release/promotion 用に保護します。
- より慎重に運用したい場合は `end-policy` を `patch-only` に変更してください。その場合、次回 run は patch が review されるまで停止します。

## 完全自動化プロンプト: automation branch merge と remote action

この章は、nightly run が validation 済みの変更を automation branch から merge target へ merge し、必要に応じて Issue、PR、release などの remote action も実行してよい完全自動化運用向けです。`main` への direct push は使わず、branch protection と required checks を merge gate として扱います。停止条件は、開始時の同期不備、validation failure、git の明確な競合、merge gate failure に絞ります。

```text
このリポジトリで repo-local skill `.agents/skills/hops-daily-steward/SKILL.md` を実行してください。

Runtime config:
- mode: advance-local
- timezone: Asia/Tokyo
- base-branch: main
- merge-target-branch: main
- subagents: explicitly allowed
- max-systemic-candidates: 1
- lane-budgets:
  - systemic-candidates: 1
  - metadata-guard-backfills: 3
  - read-only-park-reject: 5
- remote-write: automation-branch-merge
- base-branch-push: false
- protected-branch-direct-push: false
- create-pr: true
- merge-automation-branch: true
- issue-comment-close-create: true
- release: true
- end-policy: commit-local
- automation-branch-prefix: codex/steward
- stop-on-dirty-start: true
- stop-on-diverged-branch: true
- stop-on-validation-failure: true

開始:
1. worktree が `base-branch` 上にあることを確認してください。別 branch 上で clean なら `base-branch` に切り替えてください。dirty なら停止して報告してください。
2. `hops steward preflight --pull --json` を実行してください。
3. `can_continue` が false の場合は、HOPS state change に進む前に停止し、blocker を報告してください。`lab_health.status` が `needs-abstraction` の場合は、librarian lane の入力として扱い、preflight 内では memory 更新を書き込まないでください。
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
- systemic candidate は最大 1 件だけ選んでください。明示的な backlog cleanup run では 3 件まで、maintenance sweep では 5 件まで増やしてよいですが、各 candidate は個別に evidence、validation、guard、kill criteria を持つ必要があります。
- metadata / guard backfill は最大 3 件まで、read-only の park / reject / no-op / routing 判断は最大 5 件まで処理してよいです。
- evidence / routing / park / reject には `hops-research-improvements` を使ってください。
- eval case、hypothesis、manual eval、decision、guard には `hops-run-lab` を使ってください。
- doctor / update / bridge / managed-file の signal がある場合だけ `hops-update-harness` を使ってください。
- local advance に人間レビューは不要ですが、evidence、validation、guard、kill criteria は必須です。
- Issue の作成/コメント/クローズ、PR の作成/更新/merge、release は、選択した候補の自然な次の一手であれば実行してよいです。既定 branch direct push はしないでください。

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
  2. `merge-target-branch` が behind または diverged ではないことを確認してください。remote が進んでいる場合は、可能なら fast-forward pull してください。できない場合は停止して報告してください。
  3. `hops steward finalize --policy commit-local --validation-passed --branch "codex/steward/<YYYYMMDD>-daily" --message "Daily steward automation"` を実行してください。
  4. automation branch だけを push してください: `git push -u origin HEAD`
  5. automation branch から `merge-target-branch` への PR を作成または更新してください。
  6. required checks と branch protection が通るまで確認してください。通らない、または衝突する場合は merge せずに停止して報告してください。
  7. PR を repo policy に従って merge してください。merge 後、必要なら automation branch を削除してください。
  8. GitHub Issue の作成、更新、コメント、クローズが必要なら実行してください。
  9. release が適切で、version/tag 条件を満たしているなら、repo-local の `release` skill または対象リポジトリの documented release command を使って release を作成してください。

最終報告:
- sync / doctor result
- subagents used または inline fallback
- selected candidate または no-op rationale
- actions performed
- validation result
- automation branch、commit hash、PR、merge target
- remote actions performed
- blocked / parked / rejected items
- human decisions needed
```

この完全自動化プロンプトは、validation 成功と branch protection / required checks を merge の十分な gate とみなせるリポジトリだけで使ってください。
