from __future__ import annotations

ID_PREFIXES = {
    "failure": "F",
    "local_workaround": "LW",
    "upstream_feedback": "UF",
    "meta_feedback": "MF",
    "imported_feedback": "FB",
    "eval_case": "E",
    "hypothesis": "H",
    "experiment": "X",
    "decision": "D",
    "improvement_dossier": "IMP",
    "research_scan": "RS",
}


RECORD_DIRS = {
    "failure": "records/failures",
    "local_workaround": "records/local-workarounds",
    "upstream_feedback": "records/upstream-feedback",
    "meta_feedback": "records/meta-feedback",
    "imported_feedback": "records/feedback",
    "eval_case": "records/eval-cases",
    "hypothesis": "records/hypotheses",
    "experiment": "records/experiments",
    "decision": "records/decisions",
    "improvement_dossier": "improvements",
    "research_scan": "records/research-scans",
}
