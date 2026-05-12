# harness-feedback

This directory stores feedback from this project to upstream harnesses and HarnessOps.

Use this directory for:

- observed harness failures
- local workarounds with disposition and expiry
- upstream feedback drafts
- meta-harness feedback drafts

Do not use this directory for:

- research agenda changes
- paper claim changes
- experiment direction pivots
- raw private data
- implementation patches to the target harness

Use `hops add-failure`, `hops route`, and `hops feedback export --sanitize` to
manage records. Exported feedback is written under `views/exported-feedback/`
and is generated from records.
