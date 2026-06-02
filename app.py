import streamlit as st

st.set_page_config(
    page_title="Bauleiter-Tool",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verbindung prüfen
try:
    from utils.supabase_client import get_client
    db = get_client()
    verbunden = True
except ValueError as e:
    verbunden = False
    fehler = str(e)
except Exception as e:
    verbunden = False
    fehler = f"Verbindungsfehler: {e}"

st.title("🏗️ Bauleiter-Tool")

if not verbunden:
    st.error(f"⚠️ {fehler}")
    st.info("Trage SUPABASE_URL und SUPABASE_KEY in die .env-Datei ein und starte die App neu.")
    st.stop()

st.markdown("---")

# Statistiken laden
try:
    baustellen = db.table("baustellen").select("id, status").execute().data
    aktive = len([b for b in baustellen if b["status"] != "Fertiggestellt"])
    aufgaben = db.table("aufgaben").select("erledigt").eq("erledigt", False).execute().data
    offene_aufgaben = len(aufgaben)
except Exception:
    aktive = "–"
    offene_aufgaben = "–"

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📋 Baustellen\nBaustellen anlegen und verwalten")
    if st.button("Zu den Baustellen", use_container_width=True):
        st.switch_page("pages/1_Baustellen.py")

with col2:
    st.info("### 📁 Dokumente & KI-Chat\nVerträge hochladen und Fragen stellen")
    if st.button("Zu den Dokumenten", use_container_width=True):
        st.switch_page("pages/2_Dokumente.py")

with col3:
    st.info("### ✅ Aufgaben\nCheckliste für alle Bauphasen")
    if st.button("Zu den Aufgaben", use_container_width=True):
        st.switch_page("pages/3_Aufgaben.py")

st.markdown("---")
col4, col5 = st.columns(2)

with col4:
    st.warning("### 📸 Nachtrag\nFoto hochladen → Mehrkostenanzeige automatisch erstellen")
    if st.button("Zum Nachtrag-Generator", use_container_width=True):
        st.switch_page("pages/4_Nachtrag.py")

with col5:
    st.success("### 📊 Übersicht")
    col_a, col_b = st.columns(2)
    col_a.metric("Aktive Baustellen", aktive)
    col_b.metric("Offene Aufgaben", offene_aufgaben)
