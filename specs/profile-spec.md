# プロファイル仕様

プロファイルは、HarnessOps がリポジトリをどのように検出、初期化、検証、ルーティング、サニタイズするかを記述します。

## 必須フィールド

```yaml
id: runops-project
version: 0.1.0
adapter: runops_project
mode: feedback-source
root_markers:
  - campaign.toml
feedback:
  path: harness-feedback
capabilities:
  - manifest_integrity
failure_classes:
  - manifest_provenance_gap
```

推奨フィールド:

- `repository_kind`: project、target、HarnessOps のリポジトリカテゴリ。
- `provider`: 上流ハーネスプロバイダ。
- `project_evolution`: 対象プロジェクト自体の変更を置くルート。
- `state_roots`: doctor や将来のコンテキストツールが使うプロジェクト状態パス。
- `quality_commands`: 人またはCIが実行できるプロバイダコマンド。
- `protected_paths`: 公開フィードバックへコピーしてはいけないパス。
- `private_paths`: サニタイザが伏せるべきパス。
- `upstream_targets`: ターゲットハーネスとメタハーネスの行き先。

## 解決順序

```text
local override > harness-owned entry point > built-in profile
```

ロックファイルは、解決済みプロファイルID、ソース、バージョン、指紋を保存し、将来のマイグレーションがプロファイルのずれを検出できるようにします。

## 組み込みプロファイル

HarnessOps には次のプロファイルが含まれます。

- `generic-code`
- `python-package`
- `target-harness`
- `runops-project`
- `runops-upstream`
- `paper-harness-project`
- `paper-harness-upstream`
- `harnessops-core`

## ガードレール

プロファイルは、プロジェクト発展ルートとハーネスフィードバックルートを区別しなければなりません。論文主張の転換を `notes/` に置くべきなら、上流テンプレートを汚染しないよう、そのことをプロファイルで明確にします。
