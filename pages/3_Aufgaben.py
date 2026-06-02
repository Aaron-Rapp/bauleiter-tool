import streamlit as st
from utils.supabase_client import get_client

st.set_page_config(page_title="Aufgaben", page_icon="✅", layout="wide")
st.title("✅ Aufgaben-Checkliste")

try:
    db = get_client()
except Exception as e:
    st.error(str(e))
    st.stop()

STANDARD_AUFGABEN = {
    "Arbeitsvorbereitung": [
        "Leitungsauskunft einholen (DLKG / Netzbetreiber)",
        "Beweissicherung durchführen (Fotos aller angrenzenden Flächen/Gebäude)",
        "Verkehrszeichenplan genehmigen lassen",
        "Baustelleneinrichtungsplan erstellen",
        "Subunternehmer beauftragen",
        "Materialbestellung auslösen",
        "Erste Baubesprechung mit AG durchführen",
        "Baugenehmigung und Sondergenehmigungen prüfen",
        "Arbeitssicherheit: Gefährdungsbeurteilung erstellen",
    ],
    "Bauausführung": [
        "Bautagebuch täglich führen",
        "Aufmaße regelmäßig dokumentieren und unterschreiben lassen",
        "Mängelprotokoll pflegen",
        "Regelmäßige Baubesprechungen (Protokoll erstellen)",
        "Nachtragsleistungen schriftlich ankündigen (§2 VOB/B)",
        "Lieferscheine sammeln und ablegen",
        "Fotos zu jeder Leistungsphase machen",
        "Abweichungen vom Plan dokumentieren",
    ],
    "Fertiggestellt": [
        "Bauwerksabnahme mit AG terminieren und durchführen",
        "Abnahmeprotokoll erstellen und unterschreiben lassen",
        "Mängelliste aus Abnahme abarbeiten",
        "Schlussrechnung stellen",
        "Vollständig abgerechnet",
        "Bürgschaften zurückfordern",
        "Baustelleneinrichtung abbauen und Fläche beräumen",
        "Gewährleistungsfristen notieren",
    ],
}

# Baustelle auswählen
try:
    baustellen = db.table("baustellen").select("id, name, status").execute().data
except Exception as e:
    st.error(f"Daten konnten nicht geladen werden: {e}")
    st.stop()

if not baustellen:
    st.warning("Erst eine Baustelle unter 'Baustellen' anlegen.")
    st.stop()

# Session State für persistente Auswahl
if "aktive_baustelle_id" not in st.session_state:
    st.session_state.aktive_baustelle_id = baustellen[0]["id"]

baustelle_namen = {b["id"]: b["name"] for b in baustellen}
auswahl_index = next(
    (i for i, b in enumerate(baustellen) if b["id"] == st.session_state.aktive_baustelle_id),
    0
)

auswahl = st.selectbox(
    "Baustelle",
    options=baustellen,
    format_func=lambda x: x["name"],
    index=auswahl_index
)
baustelle_id = auswahl["id"]
aktuelle_phase = auswahl["status"]
st.session_state.aktive_baustelle_id = baustelle_id

st.markdown("---")

# Standard-Aufgaben initialisieren falls noch nicht vorhanden
try:
    vorhandene = db.table("aufgaben").select("titel").eq("baustelle_id", baustelle_id).execute().data
    vorhandene_titel = {a["titel"] for a in vorhandene}

    neue_aufgaben = []
    for phase, aufgaben in STANDARD_AUFGABEN.items():
        for titel in aufgaben:
            if titel not in vorhandene_titel:
                neue_aufgaben.append({
                    "baustelle_id": baustelle_id,
                    "phase": phase,
                    "titel": titel,
                    "erledigt": False
                })
    if neue_aufgaben:
        db.table("aufgaben").insert(neue_aufgaben).execute()
except Exception as e:
    st.error(f"Fehler beim Initialisieren: {e}")

# Alle Aufgaben laden
try:
    alle_aufgaben = db.table("aufgaben").select("*").eq(
        "baustelle_id", baustelle_id
    ).order("created_at").execute().data
except Exception as e:
    st.error(f"Aufgaben konnten nicht geladen werden: {e}")
    st.stop()

# Gesamtfortschritt
gesamt_alle = len(alle_aufgaben)
erledigt_alle = sum(1 for a in alle_aufgaben if a["erledigt"])
if gesamt_alle > 0:
    st.progress(erledigt_alle / gesamt_alle, text=f"Gesamtfortschritt: {erledigt_alle}/{gesamt_alle} Aufgaben erledigt")
    st.markdown("")

# Phasen anzeigen
phasen_config = {
    "Arbeitsvorbereitung": {"icon": "🟡", "farbe": "orange"},
    "Bauausführung": {"icon": "🟠", "farbe": "red"},
    "Fertiggestellt": {"icon": "🟢", "farbe": "green"},
}

for phase in ["Arbeitsvorbereitung", "Bauausführung", "Fertiggestellt"]:
    phase_aufgaben = [a for a in alle_aufgaben if a["phase"] == phase]
    erledigt = sum(1 for a in phase_aufgaben if a["erledigt"])
    gesamt = len(phase_aufgaben)
    cfg = phasen_config[phase]
    aktiv_label = " ← **aktuelle Phase**" if phase == aktuelle_phase else ""

    st.subheader(f"{cfg['icon']} {phase} — {erledigt}/{gesamt}{aktiv_label}")
    if gesamt > 0:
        st.progress(erledigt / gesamt)

    for aufgabe in phase_aufgaben:
        col_check, col_del = st.columns([20, 1])
        with col_check:
            neu = st.checkbox(
                aufgabe["titel"],
                value=aufgabe["erledigt"],
                key=f"aufgabe_{aufgabe['id']}"
            )
        with col_del:
            if st.button("✕", key=f"del_aufg_{aufgabe['id']}", help="Aufgabe löschen"):
                db.table("aufgaben").delete().eq("id", aufgabe["id"]).execute()
                st.rerun()
        if neu != aufgabe["erledigt"]:
            db.table("aufgaben").update({"erledigt": neu}).eq("id", aufgabe["id"]).execute()
            st.rerun()

    # Eigene Aufgabe hinzufügen
    with st.expander(f"➕ Eigene Aufgabe zu '{phase}' hinzufügen"):
        with st.form(f"form_neu_{phase}"):
            neue_aufgabe = st.text_input("Aufgabe beschreiben", key=f"input_{phase}")
            if st.form_submit_button("Hinzufügen"):
                if neue_aufgabe.strip():
                    db.table("aufgaben").insert({
                        "baustelle_id": baustelle_id,
                        "phase": phase,
                        "titel": neue_aufgabe.strip(),
                        "erledigt": False
                    }).execute()
                    st.rerun()

    st.markdown("---")
