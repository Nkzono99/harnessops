from harnessops.core.sanitize import sanitize_text


def test_sanitize_redacts_local_paths(tmp_path):
    text = f"Failure in {tmp_path}/runs/work/file and /home/user/private.txt"
    sanitized = sanitize_text(text, root=tmp_path, profile={"private_paths": ["runs/**/work/**"]})
    assert str(tmp_path) not in sanitized
    assert "/home/user" not in sanitized
    assert "private info excluded" in sanitized

