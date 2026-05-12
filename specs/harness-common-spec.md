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

## HarnessOps lifecycle連携

target harness の `init`、`setup`、`update-harness` などは、HarnessOps の管理対象状態を直接書かず、`hops` を呼び出します。

- project repository 生成後: `hops init --profile <target-project-profile>` と `hops doctor --check-overlay --check-records`
- target repository setup時: `hops init --profile <target-upstream-profile>` と `hops doctor --check-overlay --check-records`
- update時: `hops doctor --check-overlay --check-records` と `hops migrate --check`
- migration適用時: 人間確認または明示フラグ付きで `hops migrate --apply`
- user領域のAgent plugin installは暗黙に実行せず、明示的に `hops agent install --codex --scope user` などを案内する
- repo-local bridgeは、明示オプションで `hops agent bridge --codex` または `hops init --with-agent-bridge` を呼んでよい

## 検出優先順位

`hops detect` は次の順序でリポジトリの同一性を解決します。

1. `.harnessops/project.toml`
2. `.harness/manifest.toml`
3. プロバイダ固有マーカー
4. 汎用リポジトリマーカー
