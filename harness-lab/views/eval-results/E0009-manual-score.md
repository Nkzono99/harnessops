<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0009

送信元: `harness-lab/records/eval-cases/E0009-fb0009-github-issue-import-fails-on-windows-console-decoding.md`

## スコア

- impact: 3
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 5
- privacy_sanitization_risk: 1

## メモ

Implemented explicit UTF-8 decoding for gh issue view during feedback import, with replacement on invalid bytes and TypeError fallback handling. Regression test now imports Unicode Japanese issue body/comment and asserts encoding=utf-8 is used. Verified with focused ruff/test, full pytest, doctor, and migrate.

## 評価ケーススナップショット

# E0009: FB0009-github-issue-import-fails-on-windows-console-decoding を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0009`。

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
