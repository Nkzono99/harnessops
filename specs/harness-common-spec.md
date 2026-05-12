# Harness共通仕様

`.harness/manifest.toml` はプロバイダ中立のマーカーファイルです。HarnessOps は検出とプロファイルヒントに使いますが、このファイル自体は HarnessOps 固有ではありません。

## 必須形状

```toml
schema_version = "0.1"

[harness]
provider = "runops"
kind = "generated-project"
version = "0.9.0"

[commands]
doctor = "runo doctor"
update = "runo update-harness"
migrate = "runo migrate"
feedback = "runo feedback"
version = "runo version"

[harnessops]
recommended_profile = "runops-project"
```

## セマンティクス

| フィールド | 必須 | 意味 |
|---|---:|---|
| `schema_version` | はい | 共通マニフェストのスキーマバージョン。 |
| `harness.provider` | はい | 上流ハーネスまたはツール名。 |
| `harness.kind` | はい | `generated-project`、`paper-project`、`upstream`、`core` など。 |
| `harness.version` | 推奨 | プロバイダバージョン。 |
| `commands.*` | 任意 | プロバイダコマンド契約。 |
| `harnessops.recommended_profile` | 任意 | HarnessOps 検出ヒント。 |

## 検出優先順位

`hops detect` は次の順序でリポジトリの同一性を解決します。

1. `.harnessops/project.toml`
2. `.harness/manifest.toml`
3. プロバイダ固有マーカー
4. 汎用リポジトリマーカー
