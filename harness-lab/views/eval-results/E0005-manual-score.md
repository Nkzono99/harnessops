<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0005

送信元: `harness-lab/records/eval-cases/E0005-fb0005-github-issue-4.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 2

## メモ

Implemented the GitHub issue bridge helper: sanitized github-issue bundles can be previewed with title/body, duplicate searched via gh, created only with --confirm-create, blocked on duplicates unless --allow-duplicate, and successful creates write the Issue URL back to source records. gh-unavailable fallback writes a markdown draft.

## 評価ケーススナップショット

# E0005: FB0005-github-issue-4 を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0005`。

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
