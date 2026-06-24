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


import re


def wetter_icon_svg(code: int, size: int = 30) -> str:
    """Dezentes Line-SVG (Feather-Stil) passend zur Wetterlage. Kein Emoji."""
    s = size
    sun = "#F0A030"; cloud = "#9AA5B1"; rain = "#5B8DEF"; snow = "#7FB5D9"; storm = "#E0A020"
    head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{s}' height='{s}' "
            f"viewBox='0 0 24 24' fill='none' stroke-width='1.7' "
            f"stroke-linecap='round' stroke-linejoin='round'>")
    if code in (0, 1):  # klar
        rays = "".join(f"<line x1='12' y1='{a}' x2='12' y2='{b}' transform='rotate({r} 12 12)'/>"
                       for a, b, r in [(1,3,0),(1,3,45),(1,3,90),(1,3,135),(1,3,180),(1,3,225),(1,3,270),(1,3,315)])
        return f"{head}<g stroke='{sun}'><circle cx='12' cy='12' r='4.2' fill='{sun}' fill-opacity='0.18'/>{rays}</g></svg>"
    if code == 2:  # teilweise bewölkt
        return (f"{head}<g stroke='{sun}'><circle cx='8' cy='8' r='3.2' fill='{sun}' fill-opacity='0.18'/>"
                f"<line x1='8' y1='2.5' x2='8' y2='3.8'/><line x1='2.5' y1='8' x2='3.8' y2='8'/>"
                f"<line x1='12.2' y1='3.8' x2='13' y2='3'/></g>"
                f"<path d='M7 18h10a3.2 3.2 0 0 0 0-6.4 4.4 4.4 0 0 0-8.3-1.2A3.4 3.4 0 0 0 7 18z' "
                f"stroke='{cloud}' fill='{cloud}' fill-opacity='0.10'/></svg>")
    if code == 3 or code in (45, 48):  # bedeckt / Nebel
        base = (f"{head}<path d='M7 16h10a3.2 3.2 0 0 0 0-6.4 4.4 4.4 0 0 0-8.3-1.2A3.4 3.4 0 0 0 7 16z' "
                f"stroke='{cloud}' fill='{cloud}' fill-opacity='0.12'/>")
        if code in (45, 48):
            base += f"<g stroke='{cloud}'><line x1='5' y1='19' x2='15' y2='19'/><line x1='8' y1='21.5' x2='18' y2='21.5'/></g>"
        return base + "</svg>"
    if code in (71, 73, 75):  # Schnee
        return (f"{head}<path d='M7 15h10a3.2 3.2 0 0 0 0-6.4 4.4 4.4 0 0 0-8.3-1.2A3.4 3.4 0 0 0 7 15z' "
                f"stroke='{cloud}' fill='{cloud}' fill-opacity='0.10'/>"
                f"<g stroke='{snow}'><line x1='8.5' y1='19' x2='8.5' y2='21.5'/><line x1='12' y1='19.5' x2='12' y2='22'/>"
                f"<line x1='15.5' y1='19' x2='15.5' y2='21.5'/></g></svg>")
    if code in (95, 99):  # Gewitter
        return (f"{head}<path d='M7 15h10a3.2 3.2 0 0 0 0-6.4 4.4 4.4 0 0 0-8.3-1.2A3.4 3.4 0 0 0 7 15z' "
                f"stroke='{cloud}' fill='{cloud}' fill-opacity='0.12'/>"
                f"<polygon points='12,16 9.5,20 11.5,20 10,23 14,18.5 11.8,18.5' stroke='{storm}' fill='{storm}' fill-opacity='0.5'/></svg>")
    # Regen / Nieselregen / Schauer (51-65, 80-82) + Fallback
    return (f"{head}<path d='M7 15h10a3.2 3.2 0 0 0 0-6.4 4.4 4.4 0 0 0-8.3-1.2A3.4 3.4 0 0 0 7 15z' "
            f"stroke='{cloud}' fill='{cloud}' fill-opacity='0.10'/>"
            f"<g stroke='{rain}'><line x1='8.5' y1='18.5' x2='7.5' y2='21.5'/><line x1='12' y1='18.5' x2='11' y2='21.5'/>"
            f"<line x1='15.5' y1='18.5' x2='14.5' y2='21.5'/></g></svg>")


def _nominatim(query: str):
    """Eine einzelne Nominatim-Abfrage. Gibt (lat, lon) oder None."""
    try:
        q = urllib.parse.quote(query)
        url = (
            f"https://nominatim.openstreetmap.org/search?q={q}"
            f"&format=json&limit=1&countrycodes=de,at,ch"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "bauleiter-tool/1.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read())
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None


def geocode(adresse: str):
    """
    Robuste Geocodierung einer Baustellen-Adresse → (lat, lon) oder None.
    Probiert mehrere Varianten, damit auch unvollständige oder ungewöhnlich
    sortierte Adressen (z.B. 'PLZ Ort, Straße') ein Ergebnis liefern.
    """
    adresse = (adresse or "").strip()
    if not adresse:
        return None

    kandidaten = [adresse]

    # PLZ + Ort extrahieren (deutsche 5-stellige PLZ) — egal an welcher Position
    m = re.search(r'(\d{5})\s+([A-Za-zÄÖÜäöüß.\-]+(?:\s+[A-Za-zÄÖÜäöüß.\-]+)?)', adresse)
    if m:
        kandidaten.append(f"{m.group(1)} {m.group(2).strip()}")
        kandidaten.append(m.group(1))  # nur PLZ

    # Ort-Teil nach dem letzten Komma (oft 'Straße, Ort')
    if "," in adresse:
        letzter = adresse.split(",")[-1].strip()
        if letzter and letzter not in kandidaten:
            kandidaten.append(letzter)

    gesehen = set()
    for kand in kandidaten:
        if not kand or kand in gesehen:
            continue
        gesehen.add(kand)
        treffer = _nominatim(kand)
        if treffer:
            return treffer
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
            "code": code,
            "ok": True,
        }
    except Exception:
        return {"ok": False}
