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

## 仮説

TODO

## メカニズム

TODO

## 最小実装

TODO

## 代替案: 削除または統合

TODO

## 期待される利点

TODO

## 想定される欠点

TODO

## 評価計画

TODO

## 中止基準

TODO
""",
        encoding="utf-8",
    )

    assert any("未解決の TODO" in error for error in validate_record(record))
