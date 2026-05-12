---
name: hops-export-feedback
description: Use when exporting sanitized project-side feedback to a target harness or HarnessOps.
---

Run `hops doctor --check-overlay`, then use
`hops feedback export --target <target> --sanitize`. Do not create remote issues
or pull requests.

