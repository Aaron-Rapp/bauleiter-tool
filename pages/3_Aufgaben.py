import streamlit as st
from utils.supabase_client import get_client

st.set_page_config(page_title="Aufgaben", page_icon="✅", layout="wide")
st.title("✅ Aufgaben-Checkliste")

db = get_client()

STANDARD_AUFGABEN = {
    "Arbeitsvorbereitung": [
        "Leitungsauskunft einholen (DLKG / Netzbetreiber)",
        "Beweissicherung durchführen (Fotos aller angrenzenden Flächen)",
        "Verkehrszeichenplan genehmigen lassen",
        "Baustelleneinrichtung planen",
        "Subunternehmer beauftragen",
        "Materialbestellung auslösen",
        "Erste Baubesprechung durchführen",
        "Baugenehmigung / Genehmigungen prüfen",
    ],
    "Bauausführung": [
        "Bautagebuch täglich führen",
        "Aufmaße regelmäßig dokumentieren",
        "Mängelprotokoll pflegen",
        "Regelmäßige Baubesprechungen (Protokoll)",
        "Nachtragsleistungen schriftlich ankündigen",
        "Lieferscheine sammeln und ablegen",
        "Fotos zu jeder Leistungsphase machen",
    ],
    "Fertiggestellt": [
        "Bauwerksabnahme mit AG durchführen",
        "Abnahmeprotokoll erstellen und unterschreiben lassen",
        "Mängelliste abarbeiten",
        "Schlussrechnung stellen",
        "Vollständig abgerechnet",
        "Bürgschaften zurückfordern",
        "Baustelleneinrichtung abbauen",
    ],
}

# Baustelle auswählen
baustellen = db.table("baustellen").select("id, name, status").execute().data
if not baustellen:
    st.warning("Erst eine Baustelle anlegen.")
    st.stop()

auswahl = st.selectbox("Baustelle", options=baustellen, format_func=lambda x: x["name"])
baustelle_id = auswahl["id"]
aktuelle_phase = auswahl["status"]

st.markdown("---")

# Aufgaben beim ersten Aufruf initialisieren
vorhandene = db.table("aufgaben").select("titel").eq("baustelle_id", baustelle_id).execute().data
vorhandene_titel = {a["titel"] for a in vorhandene}

for phase, aufgaben in STANDARD_AUFGABEN.items():
    for titel in aufgaben:
        if titel not in vorhandene_titel:
            db.table("aufgaben").insert({
                "baustelle_id": baustelle_id,
                "phase": phase,
                "titel": titel,
                "erledigt": False
            }).execute()

# Phasen anzeigen
phasen_farben = {
    "Arbeitsvorbereitung": "🟡",
    "Bauausführung": "🟠",
    "Fertiggestellt": "🟢"
}

alle_aufgaben = db.table("aufgaben").select("*").eq("baustelle_id", baustelle_id).execute().data

for phase in ["Arbeitsvorbereitung", "Bauausführung", "Fertiggestellt"]:
    phase_aufgaben = [a for a in alle_aufgaben if a["phase"] == phase]
    erledigt = sum(1 for a in phase_aufgaben if a["erledigt"])
    gesamt = len(phase_aufgaben)

    farbe = phasen_farben[phase]
    aktiv = "← aktuelle Phase" if phase == aktuelle_phase else ""

    st.subheader(f"{farbe} {phase} — {erledigt}/{gesamt} erledigt {aktiv}")
    st.progress(erledigt / gesamt if gesamt > 0 else 0)

    for aufgabe in phase_aufgaben:
        neu = st.checkbox(
            aufgabe["titel"],
            value=aufgabe["erledigt"],
            key=f"aufgabe_{aufgabe['id']}"
        )
        if neu != aufgabe["erledigt"]:
            db.table("aufgaben").update({"erledigt": neu}).eq("id", aufgabe["id"]).execute()
            st.rerun()

    # Eigene Aufgabe hinzufügen
    with st.expander(f"➕ Eigene Aufgabe zu '{phase}' hinzufügen"):
        neue_aufgabe = st.text_input("Aufgabe", key=f"neu_{phase}")
        if st.button("Hinzufügen", key=f"btn_{phase}"):
            if neue_aufgabe:
                db.table("aufgaben").insert({
                    "baustelle_id": baustelle_id,
                    "phase": phase,
                    "titel": neue_aufgabe,
                    "erledigt": False
                }).execute()
                st.rerun()

    st.markdown("---")
