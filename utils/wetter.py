"""Kostenlose Wetterdaten via Open-Meteo + Nominatim Geocoding."""
import urllib.request
import urllib.parse
import json

# Lesbare deutsche Bezeichnungen (ohne Emoji)
WMO_LABELS = {
    0: "Klar",
    1: "Überwiegend klar",
    2: "Teilweise bewölkt",
    3: "Bedeckt",
    45: "Nebel",
    48: "Nebel mit Reif",
    51: "Leichter Nieselregen",
    53: "Mäßiger Nieselregen",
    55: "Starker Nieselregen",
    61: "Leichter Regen",
    63: "Mäßiger Regen",
    65: "Starker Regen",
    71: "Leichter Schneefall",
    73: "Mäßiger Schneefall",
    75: "Starker Schneefall",
    80: "Leichte Schauer",
    81: "Mäßige Schauer",
    82: "Starke Schauer",
    95: "Gewitter",
    99: "Gewitter mit Hagel",
}


def geocode(adresse: str):
    """Gibt (lat, lon) oder None zurück."""
    try:
        q = urllib.parse.quote(adresse)
        url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "bauleiter-tool/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None


def get_wetter(lat: float, lon: float) -> dict:
    """Aktuelle Wetterdaten von Open-Meteo."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,weathercode,windspeed_10m,precipitation"
            f"&wind_speed_unit=kmh&timezone=auto"
        )
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        cur = data["current"]
        code = cur.get("weathercode", 0)
        beschr = WMO_LABELS.get(code, "Unbekannt")
        return {
            "temp": round(cur.get("temperature_2m", 0), 1),
            "beschreibung": beschr,
            "wind": round(cur.get("windspeed_10m", 0)),
            "niederschlag": round(cur.get("precipitation", 0), 1),
            "ok": True,
        }
    except Exception:
        return {"ok": False}
