"""
karmic-ledger: National Geopolitical Intelligence Briefing Module
Translates high-dimensional Medini astrodynamic telemetry (GSI, EDI, DPI, MSI, Dashas, Gochar)
into declassified executive intelligence dossiers using Gemini API with an offline fallback synthesizer.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any

from core.medini import compute_national_chart, evaluate_geopolitical_incident_index


def synthesize_offline_intelligence_brief(
    nation_name: str, target_date_str: str, telemetry: dict[str, Any]
) -> str:
    """
    High-fidelity deterministic intelligence synthesizer when Gemini API credentials
    are offline or unconfigured. Produces an unclassified national security dossier.
    """
    gsi = telemetry["geopolitical_stress_index"]
    edi = telemetry["ecological_disaster_index"]
    dpi = telemetry["diplomatic_prestige_index"]
    msi = telemetry["macroeconomic_stability_index"]
    dasha = telemetry["active_dasha"]
    status = telemetry["overall_status"]
    vectors = [v["vector"] for v in telemetry.get("active_vectors", [])]
    vectors_str = (
        ", ".join(vectors) if vectors else "NONE_DETECTED (Equilibrium Baseline)"
    )

    return f"""================================================================================
NATIONAL GEOPOLITICAL INTELLIGENCE MEMORANDUM // DECLASSIFIED
SUBJECT: {nation_name.upper()}
TEMPORAL RETICLE: {target_date_str} | ACTIVE CHRONO-THREAD: {dasha}
SYSTEMIC CLASSIFICATION: {status}
================================================================================

1. EXECUTIVE THREAT ASSESSMENT & DEFENSE MATRIX
   - Geopolitical Stress Index (GSI): {gsi}/100 [{"CRITICAL VULNERABILITY" if gsi >= 70 else "CONTROLLED FRICTION" if gsi >= 50 else "STABLE CONSOLIDATION"}]
   - Active Threat Vectors: {vectors_str}
   - Strategic Appraisal: Under the {dasha} dasha horizon, the sovereign perimeter operates
     under {"acute kinetic pressure, requiring elevated border surveillance and hardened forward logistics" if gsi >= 60 else "conventional equilibrium with routine diplomatic management"}.

2. ECOLOGICAL & HYDROLOGICAL POSTURE
   - Ecological Disaster Index (EDI): {edi}/100
   - Environmental Telemetry: Water-sign planetary sectors indicate {"elevated vulnerability for monsoonal inundation, coastal volatility, or flash flooding" if edi >= 60 else "normal seasonal variance with baseline disaster response capacity"}.

3. DIPLOMATIC & SOVEREIGN PRESTIGE HORIZON
   - Diplomatic Prestige Index (DPI): {dpi}/100
   - Multilateral Consensus: Benefic alignments on sovereign leadership sectors project {"high global summit prestige, leadership in bilateral accords, and elevated multilateral consensus" if dpi >= 65 else "standard multilateral bilateral friction with fragmented regional consensus"}.

4. MACROECONOMIC & CURRENCY LIQUIDITY POSTURE
   - Macroeconomic Stability Index (MSI): {msi}/100
   - Sovereign Reserves & Capital: Treasury sector indicators reflect {"robust liquidity and foreign reserve expansion" if msi >= 65 else "monetary tightening and potential structural liquidity friction" if msi <= 40 else "stable fiscal discipline and balanced reserve management"}.

================================================================================
STRATEGIC DIRECTIVE: PRIORITIZE DOMESTIC INFRASTRUCTURE RESILIENCE WHILE MAINTAINING
DEFENSIVE MOBILITY ALONG CRITICAL BORDER VECTORS.
================================================================================
"""


def generate_national_briefing(
    nation_key: str = "india", target_date_str: str | None = None
) -> dict[str, Any]:
    """
    Coordinates planetary telemetry and dispatches to Gemini API for natural language
    executive intelligence briefings, with seamless offline fallback.
    """
    if target_date_str is None:
        target_date_str = datetime.utcnow().strftime("%Y-%m-%d")

    target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    chart = compute_national_chart(nation_key)
    telemetry = evaluate_geopolitical_incident_index(chart, target_dt)
    nation_name = chart["metadata"]["name"]

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        briefing_text = synthesize_offline_intelligence_brief(
            nation_name, target_date_str, telemetry
        )
        return {
            "nation_id": nation_key,
            "target_date": target_date_str,
            "telemetry": telemetry,
            "briefing": briefing_text,
            "engine_source": "offline_tactical_synthesizer",
            "api_key_status": "UNCONFIGURED_FALLBACK",
        }

    # Online Gemini REST invocation
    prompt = f"""
You are a senior national security intelligence analyst and mundane Vedic chronometry specialist.
Analyze the following computational planetary telemetry for {nation_name} on {target_date_str}:

- Active Vimshottari Dasha: {telemetry["active_dasha"]}
- Geopolitical Stress Index (GSI): {telemetry["geopolitical_stress_index"]}/100
- Ecological Disaster Index (EDI): {telemetry["ecological_disaster_index"]}/100
- Diplomatic Prestige Index (DPI): {telemetry["diplomatic_prestige_index"]}/100
- Macroeconomic Stability Index (MSI): {telemetry["macroeconomic_stability_index"]}/100
- Overall Status: {telemetry["overall_status"]}
- Active Kinetic Vectors: {json.dumps(telemetry.get("active_vectors", []))}

Generate an executive intelligence briefing (HUD/Jarvis systems engineer style).
Include:
1. Executive Strategic Assessment (Sovereign posture and security climate).
2. Border & Defense Horizon (Territorial stability vs kinetic risk).
3. Diplomatic & Multilateral Summit Posture (Foreign treaties, prestige, and influence).
4. Macroeconomic & Ecological Risks (Currency liquidity, monsoons, and resource resilience).
Keep it extremely concise, high-signal, systems-focused, and objective. Zero fatalism.
"""

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024},
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidate = res_data.get("candidates", [{}])[0]
            parts = candidate.get("content", {}).get("parts", [{}])
            text = (
                parts[0].get("text", "")
                if parts
                else "Unable to extract response content."
            )
            return {
                "nation_id": nation_key,
                "target_date": target_date_str,
                "telemetry": telemetry,
                "briefing": text,
                "engine_source": "gemini-2.5-flash",
                "api_key_status": "ONLINE_LIVE",
            }
    except Exception as e:
        # Graceful fallback to offline tactical synthesizer on network/quota exception
        fallback_text = synthesize_offline_intelligence_brief(
            nation_name, target_date_str, telemetry
        )
        return {
            "nation_id": nation_key,
            "target_date": target_date_str,
            "telemetry": telemetry,
            "briefing": fallback_text,
            "engine_source": "offline_tactical_synthesizer_fallback",
            "api_key_status": f"NETWORK_EXCEPTION_FALLBACK: {e!s}",
        }
