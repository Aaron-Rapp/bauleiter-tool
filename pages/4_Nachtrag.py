import streamlit as st
from utils.supabase_client import get_client
from utils.gemini_helper import beschreibe_foto_fuer_nachtrag
from datetime import date

st.set_page_config(page_title="Nachtrag-Generator", page_icon="📸", layout="wide")
st.title("📸 Nachtrag-Generator")
st.markdown("Foto der Situation hochladen → KI erstellt automatisch eine Mehrkostenanzeige")

try:
    db = get_client()
except Exception as e:
    st.error(str(e))
    st.stop()

try:
    baustellen = db.table("baustellen").select("id, name").execute().data
except Exception as e:
    st.error(f"Fehler: {e}")
    st.stop()

if not baustellen:
    st.warning("Erst eine Baustelle anlegen.")
    st.stop()

auswahl = st.selectbox("Baustelle", options=baustellen, format_func=lambda x: x["name"])
baustelle_id = auswahl["id"]

st.markdown("---")
col_links, col_rechts = st.columns([1, 1])

with col_links:
    st.subheader("Situation dokumentieren")
    foto = st.file_uploader(
        "Foto der Situation (JPG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="Mache ein Foto der unvorhergesehenen Leistung"
    )
    beschreibung = st.text_area(
        "Beschreibung der Situation *",
        placeholder="z.B. 'Bestehende Gasleitung lag nicht wie geplant, muss 3 m umverlegt werden'",
        height=120
    )
    nachtrag_datum = st.date_input("Datum des Vorkommnisses", value=date.today())

    if foto:
        st.image(foto, caption="Hochgeladenes Foto", use_column_width=True)

    generieren = st.button(
        "🤖 Mehrkostenanzeige erstellen",
        use_container_width=True,
        type="primary",
        disabled=not (foto and beschreibung)
    )

with col_rechts:
    st.subheader("Generierte Mehrkostenanzeige")

    if generieren:
        with st.spinner("KI analysiert das Foto und erstellt die Mehrkostenanzeige..."):
            try:
                ergebnis = beschreibe_foto_fuer_nachtrag(foto.read(), beschreibung)
                nachtrag_text = ergebnis["nachtrag_text"]

                db.table("nachtraege").insert({
                    "baustelle_id": baustelle_id,
                    "datum": str(nachtrag_datum),
                    "beschreibung": beschreibung,
                    "ki_text": nachtrag_text
                }).execute()

                st.session_state["letzter_nachtrag"] = nachtrag_text
                st.success("✅ Mehrkostenanzeige erstellt und gespeichert!")
            except Exception as e:
                st.error(f"Fehler: {e}")

    if "letzter_nachtrag" in st.session_state:
        st.markdown(st.session_state["letzter_nachtrag"])
        st.markdown("---")
        st.caption("💡 Diesen Text kopieren und per E-Mail an den Auftraggeber senden.")

    st.markdown("---")
    st.subheader("📋 Gespeicherte Nachträge")

    try:
        nachtraege = db.table("nachtraege").select("*").eq(
            "baustelle_id", baustelle_id
        ).order("datum", desc=True).execute().data
    except Exception:
        nachtraege = []

    if not nachtraege:
        st.info("Noch keine Nachträge für diese Baustelle.")
    else:
        st.caption(f"**{len(nachtraege)} Nachtrag/Nachträge gespeichert**")
        for n in nachtraege:
            kurz = (n.get("beschreibung") or "")[:60]
            with st.expander(f"📋 {n.get('datum', '–')} — {kurz}..."):
                st.markdown(n.get("ki_text", "Kein Text vorhanden"))
                if st.button("🗑️ Löschen", key=f"del_n_{n['id']}"):
                    db.table("nachtraege").delete().eq("id", n["id"]).execute()
                    st.rerun()
