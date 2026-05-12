---
id: E0015
record_type: eval_case
created_at: '2026-05-13T02:32:03+09:00'
status: active
capability: lab_evaluation_review
failure_class: eval_template_noise_in_dossier
source_feedback: FB0016
---

# E0015: FB0016-remove-unused-eval-case-template-noise-from-dossiers を評価

## フィクスチャ

フィクスチャディレクトリ: `harness-lab/records/eval-cases/fixtures/E0015`。

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
