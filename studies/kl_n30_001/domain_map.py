"""Fixed event-type → VCS domain mapping (prereg §3).

Primary scoring must NOT use core.confluence.classify_event_domain.
Pass the returned key as domain_override into evaluate_event_confluence.
"""

from __future__ import annotations

# Closed list from KL-N30-001_preregistration.md §3
EVENT_TYPES = (
    "MARRIAGE",
    "CHILDBIRTH",
    "CAREER_START",
    "CAREER_END",
    "RELOCATION_ABROAD",
    "PARENT_BEREAVEMENT",
)

# Keys must exist in evaluate_event_confluence domain_rules
DOMAIN_BY_EVENT: dict[str, str] = {
    "MARRIAGE": "MARRIAGE_OR_RELATIONSHIP",
    # No dedicated Santana domain in engine — family-axis houses 5/4/9
    "CHILDBIRTH": "FAMILY_AXIS_RESTRUCTURING",
    "CAREER_START": "CAREER_OR_POWER_ELEVATION",
    "CAREER_END": "CAREER_OR_STATUS_LOSS",
    "RELOCATION_ABROAD": "FOREIGN_RELOCATION",
    # Parent unspecified → family axis (mat/pat split needs extractor tag)
    "PARENT_BEREAVEMENT": "FAMILY_AXIS_RESTRUCTURING",
}


def map_event_domain(event_type: str) -> str:
    key = (event_type or "").strip().upper()
    if key not in DOMAIN_BY_EVENT:
        raise ValueError(
            f"Unknown event_type {event_type!r}; allowed: {EVENT_TYPES}"
        )
    return DOMAIN_BY_EVENT[key]
