from harnessops.core.routing import classify_text


def test_routing_dispositions_cover_required_values():
    cases = {
        "paper claim changed after new evidence": "project-evolution",
        "local process workaround only": "project-local-process",
        "target harness missed validation": "target-upstream-candidate",
        "HarnessOps schema cannot express this": "meta-harness-candidate",
        ".harness/manifest common manifest gap": "protocol-candidate",
        "external cluster failure": "external-candidate",
        "private only do not upstream": "do-not-upstream",
    }
    for text, expected in cases.items():
        assert classify_text(text)["type"] == expected

