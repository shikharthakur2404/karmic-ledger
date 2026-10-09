"""
Symbolic partnership / shaadi timing windows from Vimshottari chapters.

Not a wedding-date prophecy — highlights dasha periods classically tied to
Venus, the 7th-lord, and Jupiter for reflection only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from core.ephemeris import ZODIAC_SIGNS

SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}


def seventh_lord(lagna_sign: str) -> str:
    idx = ZODIAC_SIGNS.index(lagna_sign)
    seventh = ZODIAC_SIGNS[(idx + 6) % 12]
    return SIGN_LORDS[seventh]


def _parse_date(s: str) -> datetime:
    return datetime.strptime(s[:10], "%Y-%m-%d")


def evaluate_shaadi_timing_windows(
    natal: dict[str, Any],
    timeline: list[dict[str, Any]],
    *,
    as_of: datetime | None = None,
    horizon_year: int = 2045,
) -> dict[str, Any]:
    """
    Return current chapter + upcoming Venus / 7th-lord / Jupiter antardasha windows.
    """
    as_of = as_of or datetime.utcnow()
    lagna_sign = natal["lagna"]["sign"]
    lord7 = seventh_lord(lagna_sign)
    focus = {"Venus", lord7, "Jupiter"}

    windows: list[dict[str, Any]] = []
    for maha in timeline:
        md = maha["mahadasha"]
        for antar in maha.get("antardashas") or []:
            ad = antar["antardasha"]
            if md not in focus and ad not in focus:
                continue
            start = _parse_date(antar["start_date"])
            end = _parse_date(antar["end_date"])
            if end < as_of or start.year > horizon_year:
                continue
            weight = 0
            reasons: list[str] = []
            if md == "Venus" or ad == "Venus":
                weight += 3
                reasons.append("Venus chapter (attraction / bonding significator)")
            if md == lord7 or ad == lord7:
                weight += 3
                reasons.append(f"7th-lord {lord7} chapter (partnership house ruler)")
            if md == "Jupiter" or ad == "Jupiter":
                weight += 2
                reasons.append("Jupiter chapter (growth / ceremony significator)")
            if md == "Venus" and ad in focus:
                weight += 1
            label = "Stronger symbolic window" if weight >= 5 else "Supportive window"
            if weight >= 6:
                label = "Peak symbolic window"
            windows.append(
                {
                    "mahadasha": md,
                    "antardasha": ad,
                    "label": f"{md} – {ad}",
                    "start": antar["start_date"][:10],
                    "end": antar["end_date"][:10],
                    "weight": weight,
                    "strength": label,
                    "reasons": reasons,
                }
            )

    windows.sort(key=lambda w: (w["start"], -w["weight"]))
    # Keep top upcoming by weight then chronological uniqueness
    seen: set[str] = set()
    ranked = sorted(windows, key=lambda w: (-w["weight"], w["start"]))
    top: list[dict[str, Any]] = []
    for w in ranked:
        key = w["label"] + w["start"]
        if key in seen:
            continue
        seen.add(key)
        top.append(w)
        if len(top) >= 8:
            break
    top.sort(key=lambda w: w["start"])

    current_md = None
    current_ad = None
    for maha in timeline:
        st = _parse_date(maha["start_date"])
        en = _parse_date(maha["end_date"])
        if st <= as_of <= en:
            current_md = maha["mahadasha"]
            for antar in maha.get("antardashas") or []:
                ast = _parse_date(antar["start_date"])
                aen = _parse_date(antar["end_date"])
                if ast <= as_of <= aen:
                    current_ad = antar["antardasha"]
                    break
            break

    return {
        "status": "OK",
        "title": "Partnership timing windows",
        "seventh_lord": lord7,
        "lagna_sign": lagna_sign,
        "current_chapter": f"{current_md} – {current_ad}"
        if current_md and current_ad
        else None,
        "windows": top,
        "epistemic_notice": (
            "Symbolic Vimshottari timing only — not a fixed wedding date, "
            "legal advice, or a promise. Life choices and consent come first."
        ),
    }
