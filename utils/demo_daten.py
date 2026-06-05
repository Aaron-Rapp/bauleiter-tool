"""
Demo-Daten für die Präsentation.
Erstellt ein realistisches Musterprojekt mit Todos, Kalender-Einträgen.
"""
import uuid
import datetime


def lade_demo_projekt(db) -> str:
    """
    Legt ein Demo-Projekt an (falls noch keins mit diesem Namen existiert).
    Gibt die Projekt-ID zurück.
    """
    demo_name = "Neubau Bürogebäude Konstanz"

    # Prüfe ob Demo-Projekt schon existiert
    existing = db.table("projekte").select("id").execute().data
    for p in existing:
        row = db.table("projekte").select("*").eq("id", p["id"]).execute().data
        if row and row[0].get("name") == demo_name:
            return row[0]["id"]

    pid = str(uuid.uuid4())

    # Projekt anlegen
    db.table("projekte").insert({
        "id": pid,
        "name": demo_name,
        "kostenstelle": "KST-2026-042",
        "anschrift": "Scheffelstraße 12, 78462 Konstanz",
        "bauzeit_von": "2026-04-01",
        "bauzeit_bis": "2026-11-30",
        "foto_url": "",
    }).execute()

    # ── Kalender-Einträge ────────────────────────────────────────
    heute = datetime.date.today()
    termine = [
        # Vergangene / laufende
        {"titel": "Rohbau Erdgeschoss",       "datum": str(heute - datetime.timedelta(days=14)), "kategorie": "gruen", "beschreibung": "EG Betonage abgeschlossen"},
        {"titel": "Jour Fixe mit AG",          "datum": str(heute - datetime.timedelta(days=7)),  "kategorie": "blau",  "uhrzeit_von": "10:00", "uhrzeit_bis": "11:30"},
        # Diese Woche
        {"titel": "Betonlieferung OG 1",       "datum": str(heute + datetime.timedelta(days=2)),  "kategorie": "orange","uhrzeit_von": "07:00", "uhrzeit_bis": "12:00", "beschreibung": "Lieferant: Heidelberg Materials"},
        {"titel": "Kranlieferung",             "datum": str(heute + datetime.timedelta(days=3)),  "kategorie": "blau",  "uhrzeit_von": "06:30", "uhrzeit_bis": "08:00"},
        # Nächste Woche
        {"titel": "Rohbau OG 1",               "datum": str(heute + datetime.timedelta(days=7)),  "kategorie": "gruen"},
        {"titel": "Sicherheitsbegehung",       "datum": str(heute + datetime.timedelta(days=8)),  "kategorie": "blau",  "uhrzeit_von": "09:00", "uhrzeit_bis": "10:00", "beschreibung": "Mit Bauleiter und SiGe-Koordinator"},
        {"titel": "Polier-Einweisung Fenstermontage", "datum": str(heute + datetime.timedelta(days=10)), "kategorie": "orange", "uhrzeit_von": "07:30"},
        # Übernächste Woche
        {"titel": "Fenster- & Fassadenarbeiten","datum": str(heute + datetime.timedelta(days=14)), "kategorie": "gruen"},
        {"titel": "Abnahme Rohbau mit Statiker","datum": str(heute + datetime.timedelta(days=16)), "kategorie": "blau",  "uhrzeit_von": "14:00", "uhrzeit_bis": "16:00"},
        {"titel": "Elektrounternehmer Einzug", "datum": str(heute + datetime.timedelta(days=21)), "kategorie": "orange","beschreibung": "Leerrohre EG"},
        # Weiter in der Zukunft
        {"titel": "Zwischenbegehung Auftraggeber","datum": str(heute + datetime.timedelta(days=28)),"kategorie": "blau","uhrzeit_von": "11:00", "uhrzeit_bis": "13:00"},
        {"titel": "Innenausbau Start",         "datum": str(heute + datetime.timedelta(days=35)), "kategorie": "gruen"},
    ]

    for t in termine:
        db.table("kalender").insert({
            "projekt_id": pid,
            "titel": t["titel"],
            "datum": t["datum"],
            "kategorie": t["kategorie"],
            "uhrzeit_von": t.get("uhrzeit_von", ""),
            "uhrzeit_bis": t.get("uhrzeit_bis", ""),
            "beschreibung": t.get("beschreibung", ""),
        }).execute()

    # ── Todos ────────────────────────────────────────────────────
    todos = [
        # Arbeitsvorbereitung — meistens erledigt
        ("Baustelleneinrichtungsplan erstellen",   "Arbeitsvorbereitung", True),
        ("Subunternehmer beauftragen",             "Arbeitsvorbereitung", True),
        ("Pläne freigeben lassen",                 "Arbeitsvorbereitung", True),
        ("Materialbestellung vorbereiten",         "Arbeitsvorbereitung", True),
        ("Einweisungen und Sicherheitsunterweisung planen", "Arbeitsvorbereitung", False),
        # Bauausführung — gemischt
        ("Tagesbericht führen",                    "Bauausführung", True),
        ("Qualitätskontrolle durchführen",         "Bauausführung", True),
        ("Mängel dokumentieren",                   "Bauausführung", False),
        ("Abrechnung der Subunternehmer prüfen",   "Bauausführung", False),
        ("Besprechungsprotokolle führen",          "Bauausführung", True),
        # Abnahme — alles offen
        ("Begehung mit Auftraggeber planen",       "Abnahme & Übergabe", False),
        ("Restmängelliste erstellen",              "Abnahme & Übergabe", False),
        ("Dokumentation zusammenstellen",          "Abnahme & Übergabe", False),
        ("Schlussrechnung stellen",                "Abnahme & Übergabe", False),
        ("Bürgschaften zurückfordern",             "Abnahme & Übergabe", False),
    ]

    for titel, phase, erledigt in todos:
        db.table("todos").insert({
            "projekt_id": pid,
            "titel": titel,
            "phase": phase,
            "erledigt": 1 if erledigt else 0,
        }).execute()

    return pid
