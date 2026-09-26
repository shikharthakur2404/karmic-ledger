"""
karmic-ledger: Intelligent Geocoding & Location Resolution Engine
Resolves birth cities, towns, and rural villages into precise celestial coordinates
(Latitude, Longitude, City, Country) with zero user-side API keys required.
Powered by OpenStreetMap Nominatim with local in-memory fallback cache.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any

logger = logging.getLogger("karmic-ledger.geocoding")

# Local High-Velocity In-Memory Gazetteer for instant 0ms response on common cities
COMMON_CITIES: list[dict[str, Any]] = [
    {
        "name": "New Delhi, Delhi, India",
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "latitude": 28.6139,
        "longitude": 77.2090,
    },
    {
        "name": "Mumbai, Maharashtra, India",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0760,
        "longitude": 72.8777,
    },
    {
        "name": "Bengaluru, Karnataka, India",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "latitude": 12.9716,
        "longitude": 77.5946,
    },
    {
        "name": "Pune, Maharashtra, India",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 18.5204,
        "longitude": 73.8567,
    },
    {
        "name": "Satara, Maharashtra, India",
        "city": "Satara",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 17.6805,
        "longitude": 74.0183,
    },
    {
        "name": "Khatav, Satara, Maharashtra, India",
        "city": "Khatav",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 17.6370,
        "longitude": 74.4018,
    },
    {
        "name": "Kanpur, Uttar Pradesh, India",
        "city": "Kanpur",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 26.4499,
        "longitude": 80.3319,
    },
    {
        "name": "Lucknow, Uttar Pradesh, India",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 26.8467,
        "longitude": 80.9462,
    },
    {
        "name": "Kolkata, West Bengal, India",
        "city": "Kolkata",
        "state": "West Bengal",
        "country": "India",
        "latitude": 22.5726,
        "longitude": 88.3639,
    },
    {
        "name": "Chennai, Tamil Nadu, India",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    {
        "name": "Hyderabad, Telangana, India",
        "city": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "latitude": 17.3850,
        "longitude": 78.4867,
    },
    {
        "name": "Ahmedabad, Gujarat, India",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.0225,
        "longitude": 72.5714,
    },
    {
        "name": "Jaipur, Rajasthan, India",
        "city": "Jaipur",
        "state": "Rajasthan",
        "country": "India",
        "latitude": 26.9124,
        "longitude": 75.7873,
    },
    {
        "name": "Patna, Bihar, India",
        "city": "Patna",
        "state": "Bihar",
        "country": "India",
        "latitude": 25.5941,
        "longitude": 85.1376,
    },
    {
        "name": "Berlin, Germany",
        "city": "Berlin",
        "state": "Berlin",
        "country": "Germany",
        "latitude": 52.5200,
        "longitude": 13.4050,
    },
    {
        "name": "Munich, Bavaria, Germany",
        "city": "Munich",
        "state": "Bavaria",
        "country": "Germany",
        "latitude": 48.1351,
        "longitude": 11.5820,
    },
    {
        "name": "Frankfurt, Hesse, Germany",
        "city": "Frankfurt",
        "state": "Hesse",
        "country": "Germany",
        "latitude": 50.1109,
        "longitude": 8.6821,
    },
    {
        "name": "London, United Kingdom",
        "city": "London",
        "state": "England",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    },
    {
        "name": "New York, USA",
        "city": "New York",
        "state": "New York",
        "country": "United States",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    {
        "name": "San Francisco, California, USA",
        "city": "San Francisco",
        "state": "California",
        "country": "United States",
        "latitude": 37.7749,
        "longitude": -122.4194,
    },
    {
        "name": "Tokyo, Japan",
        "city": "Tokyo",
        "state": "Tokyo",
        "country": "Japan",
        "latitude": 35.6762,
        "longitude": 139.6503,
    },
    {
        "name": "Sydney, NSW, Australia",
        "city": "Sydney",
        "state": "NSW",
        "country": "Australia",
        "latitude": -33.8688,
        "longitude": 151.2093,
    },
]

# Simple in-memory session cache to avoid repeating external queries
_GEO_CACHE: dict[str, list[dict[str, Any]]] = {}


def geocode_location(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Resolves a search query (city, town, village, or district) into geographic coordinates.
    Checks memory cache first, then matches local gazetteer, then queries OpenStreetMap Nominatim.
    """
    clean_q = query.strip()
    if not clean_q:
        return []

    cache_key = clean_q.lower()
    if cache_key in _GEO_CACHE:
        return _GEO_CACHE[cache_key]

    results: list[dict[str, Any]] = []

    # 1. Exact or Prefix Match in Local Gazetteer
    for item in COMMON_CITIES:
        if (
            cache_key in item["name"].lower()
            or cache_key in item["city"].lower()
            or item["city"].lower().startswith(cache_key)
        ):
            results.append(item)
            if len(results) >= limit:
                _GEO_CACHE[cache_key] = results
                return results

    # 2. Query OpenStreetMap Nominatim for villages, talukas, and worldwide locations
    try:
        encoded_q = urllib.parse.quote(clean_q)
        url = (
            f"https://nominatim.openstreetmap.org/search?"
            f"q={encoded_q}&format=json&limit={limit}&addressdetails=1"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "KarmicLedger/1.0 (fun-kundli-observatory; contact@karmicledger.org)",
                "Accept-Language": "en",
            },
        )
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))

            for entry in data:
                addr = entry.get("address", {})
                city_name = (
                    addr.get("city")
                    or addr.get("town")
                    or addr.get("village")
                    or addr.get("hamlet")
                    or addr.get("suburb")
                    or addr.get("county")
                    or entry.get("name", "")
                )
                state_name = addr.get("state", "")
                country_name = addr.get("country", "")

                # Construct clean human-readable title
                parts = [p for p in [city_name, state_name, country_name] if p]
                display_title = (
                    ", ".join(parts) if parts else entry.get("display_name", "")
                )

                res_item = {
                    "name": display_title,
                    "city": city_name,
                    "state": state_name,
                    "country": country_name,
                    "latitude": round(float(entry["lat"]), 4),
                    "longitude": round(float(entry["lon"]), 4),
                }

                # Avoid duplicates
                if not any(
                    abs(r["latitude"] - res_item["latitude"]) < 0.01
                    and abs(r["longitude"] - res_item["longitude"]) < 0.01
                    for r in results
                ):
                    results.append(res_item)

                if len(results) >= limit:
                    break

    except Exception as exc:
        logger.warning("External geocoding error for '%s': %s", clean_q, exc)

    # 3. Fallback: If still empty, fuzzy match against local gazetteer
    if not results:
        for item in COMMON_CITIES:
            # Match first 3 chars
            if len(clean_q) >= 3 and clean_q[:3].lower() in item["name"].lower():
                results.append(item)
                if len(results) >= limit:
                    break

    _GEO_CACHE[cache_key] = results
    return results
