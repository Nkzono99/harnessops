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
- `domain_triage`: target固有の診断skillと責務。HarnessOps のroutingを置き換えず、判断材料を提供する。

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

`domain_triage` は target-specific な診断に限定します。record schema、routing、sanitize、export/import を target profile や target skill が再実装してはいけません。
