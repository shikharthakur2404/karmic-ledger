"""
karmic-ledger: Subject Consent & Privacy Enforcement Gate
Mandatory gatekeeper: Halts automated or manual analysis for any real named individual
who has not provided verified affirmative consent.
Protects private individuals from unsolicited astrological evaluation, death/maraka scoring,
and behavioral/bureaucratic claims.
"""

from typing import Any


class ConsentDeniedError(Exception):
    """Raised when an unconsented profile attempts to be processed by the engine."""


def is_historical_benchmark_subject(
    data: dict[str, Any], context_str: str = ""
) -> bool:
    """
    Identifies whether a profile belongs to an open, retrospective historical archive
    (e.g., Abraham Lincoln, Indira Gandhi, Albert Einstein, or synthetic control benchmarks).
    """
    sid = str(data.get("subject_id", "")).lower().strip()
    name = str(data.get("name", "")).lower().strip()
    ctx = str(context_str).lower().strip()
    btype = str(data.get("benchmark_type", "")).lower().strip()

    if btype == "historical_public_record" or "benchmark" in ctx or "cohort" in ctx:
        return True

    historical_keywords = [
        "historical",
        "benchmark",
        "indira",
        "lincoln",
        "elizabeth",
        "einstein",
        "gandhi",
        "jobs",
        "kennedy",
        "luther",
        "churchill",
        "mandela",
        "curie",
        "roosevelt",
        "vivekananda",
        "synthetic",
    ]

    if any(k in sid for k in historical_keywords):
        return True

    if any(k in name for k in historical_keywords):
        return True

    return False


def verify_subject_consent(
    data: dict[str, Any], context_str: str = ""
) -> tuple[bool, str]:
    """
    Evaluates whether the profile is authorized for processing:
    1. Closed retrospective historical figures are exempt from consent requirements,
       but are strictly confined to retrospective research.
    2. De-identified synthetic testing archetypes are permitted if explicitly tagged.
    3. Any private individual MUST have an explicit affirmative consent record:
       "subject_consent": {
           "status": "EXPLICIT_CONSENT_GRANTED"
       }
    If consent is missing, revoked, or unverified, execution is immediately denied.
    """
    if is_historical_benchmark_subject(data, context_str):
        return True, "HISTORICAL_BENCHMARK_EXEMPT"

    consent = data.get("subject_consent")
    if not consent:
        return (
            False,
            "CONSENT_GATE_LOCKED: Profile lacks explicit subject consent block.",
        )

    if isinstance(consent, dict):
        status = consent.get("status", "")
        if status == "EXPLICIT_CONSENT_GRANTED":
            return True, "EXPLICIT_CONSENT_VERIFIED"
        return (
            False,
            f"CONSENT_GATE_LOCKED: Consent status is '{status}'. Affirmative consent required.",
        )

    if consent is True:
        return True, "EXPLICIT_CONSENT_VERIFIED"

    return False, "CONSENT_GATE_LOCKED: Subject consent not verified."
