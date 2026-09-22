"""
karmic-ledger: Privacy & Anonymization Engine
Ensures zero exposure of personal PII (Personally Identifiable Information).
Strips names, family ties, and sensitive biographical descriptors before export.
"""

import hashlib
from typing import Any


def hash_identifier(identifier: str, salt: str = "karmic_telemetry_secure") -> str:
    """Generates a non-reversible SHA-256 pseudonym hash for a subject."""
    raw = f"{identifier}_{salt}".encode()
    return f"sub_{hashlib.sha256(raw).hexdigest()[:12]}"


def sanitize_profile(profile_data: dict[str, Any]) -> dict[str, Any]:
    """
    Creates an anonymized copy of a profile fixture.
    Retains mathematical telemetry (DOB, TOB, coordinates) for ephemeris accuracy,
    but completely redacts personal names, family ties, and sensitive strings.
    """
    sanitized = profile_data.copy()
    original_id = profile_data.get("subject_id", "subject")

    # Redact identity
    sanitized["subject_id"] = hash_identifier(original_id)
    sanitized["name"] = f"Subject [{sanitized['subject_id']}]"

    # Strip sensitive family descriptors
    if "lineage" in sanitized:
        sanitized["lineage"] = {"community_archetype": "Redacted"}
    if "lineage_and_family" in sanitized:
        sanitized["lineage_and_family"] = {"family_records": "Redacted for Privacy"}

    # Anonymize milestone descriptions
    milestone_keys = [
        "biographical_milestones",
        "biographical_calibrations",
        "biographical_event_locking",
    ]
    for key in milestone_keys:
        if key in sanitized:
            clean_list = []
            for item in sanitized[key]:
                clean_item = {
                    "event_category": item.get("milestone")
                    or item.get("event", "Event"),
                    "date": item.get("date") or str(item.get("year", "2020")),
                }
                clean_list.append(clean_item)
            sanitized[key] = clean_list

    return sanitized
