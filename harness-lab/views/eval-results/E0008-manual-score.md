<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0008

送信元: `harness-lab/records/eval-cases/E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 2

## メモ

Implemented lab-first GitHub issue promotion: hops lab issue draft/create --from <FB/E/H/D/IMP> builds a sanitized issue body from the generated dossier, writes local markdown drafts, searches duplicates, requires --confirm-create for remote creation, and writes the created URL back to the dossier plus source feedback. Verified sanitizer, draft, duplicate-safe create, URL writeback, help, full pytest, doctor, and migrate.

## 評価ケーススナップショット

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
