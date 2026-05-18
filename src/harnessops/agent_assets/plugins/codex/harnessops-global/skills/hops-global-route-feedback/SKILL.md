---
name: hops-global-route-feedback
description: global/local-state HarnessOps の failure や feedback を project-local、target-upstream、meta-harness、protocol、external、private に分類するときに使う。
---

Use `uvx --from harnessops hops <command>`; do not rely on `hops` being on PATH.

1. Resolve/link local state and validate.

```bash
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops doctor --check-overlay --check-records
```

2. Route an existing record.

```bash
uvx --from harnessops hops feedback route --record <id>
```

3. If the user gives only text, classify the text first and recommend whether to create a record.

```bash
uvx --from harnessops hops feedback route --text "<text>" --target <target> --json
```

Split one event into separate records when it contains both project-specific decisions and upstream/meta harness deficiencies.

Do not create repo-local HarnessOps files. Do not put project research direction into HarnessOps feedback; use project `research/` or `notes/`.
