from harnessops.profiles.registry import load_profile, profile_ids


def test_builtin_profiles_are_available():
    expected = {
        "generic-code",
        "python-package",
        "target-harness",
        "runops-project",
        "runops-upstream",
        "paper-harness-project",
        "paper-harness-upstream",
        "harnessops-core",
    }
    assert expected.issubset(set(profile_ids()))
    assert load_profile("runops-project")["adapter"] == "runops_project"

