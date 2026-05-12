---
name: release
description: HarnessOps repository を GitHub release するときに使う repo-local skill。version/tag確認、検証、push、gh release create、release後のworkflow確認を行う。
---

この skill は HarnessOps repository 専用です。共通 plugin ではなく repo-local skill として扱います。

`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えず、HarnessOps 状態変更は `hops` に委譲します。

手順:

1. `git status --short --branch`、`git log --oneline --decorate -5`、`git tag --list` を確認する。
2. `pyproject.toml` の version から tag `v<version>` を決める。既存 tag/release がある場合は上書きしない。
3. release 前に次を実行する。

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uv run --with-editable . hops doctor --check-overlay --check-records
uv run --with-editable . hops migrate --check
```

4. `main` がリリース対象なら必要な commit を作り、`git push origin main` で remote に反映する。
5. この repository は published GitHub release で PyPI publish workflow が走る。PyPI Trusted Publisher の environment は `pypi` なので、workflow の publish job は `environment: pypi` を持つ必要がある。
6. `gh release create v<version> --target main --title "harnessops v<version>" --notes <notes>` で release を作る。
7. 作成後に `gh release view v<version>`、`gh run list --limit 5`、`git status --short --branch` を確認する。

追加の GitHub Actions workflow dispatch は、ユーザーが明示した場合だけ行う。
