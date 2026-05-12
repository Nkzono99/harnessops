<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0003

送信元: `harness-lab/records/eval-cases/E0003-fb0003-github-issue-2.md`

## スコア

- impact: 3
- mechanism_clarity: 4
- evaluability: 4
- minimality: 4
- regression_risk: 2
- operator_burden: 3
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented the minimal sanitized GitHub issue draft path: feedback export --sanitize --format github-issue writes a local markdown draft, refuses unsanitized issue drafts, and refuses --allow-private for public issue draft format. Remote issue creation, duplicate search, and URL write-back remain follow-up.

## 評価ケーススナップショット

# E0003: FB0003-github-issue-2 を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0003`。

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
