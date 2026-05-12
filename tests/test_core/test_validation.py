from harnessops.core.validation import validate_record


def test_validate_record_rejects_todo_hypothesis(tmp_path):
    record = tmp_path / "H0001-bad.md"
    record.write_text(
        """---
id: H0001
record_type: hypothesis
created_at: 2026-05-12T00:00:00+09:00
status: proposed
target_capability: routing
source_eval_case: E0001
---

# H0001: Bad

## Hypothesis

TODO

## Mechanism

TODO

## Minimal implementation

TODO

## Alternative: deletion or consolidation

TODO

## Expected upside

TODO

## Expected downside

TODO

## Evaluation plan

TODO

## Kill criteria

TODO
""",
        encoding="utf-8",
    )

    assert any("unresolved TODO" in error for error in validate_record(record))

