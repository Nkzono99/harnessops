from harnessops.core.detect import detect_repository


def test_detect_fixture_matrix(copy_fixture):
    cases = {
        "runops-project-minimal": "runops-project",
        "paper-project-minimal": "paper-harness-project",
        "runops-upstream-minimal": "runops-upstream",
        "paper-harness-upstream-minimal": "paper-harness-upstream",
        "harnessops-core-minimal": "harnessops-core",
    }
    for fixture, profile in cases.items():
        root = copy_fixture(fixture)
        assert detect_repository(root)["profile"] == profile

