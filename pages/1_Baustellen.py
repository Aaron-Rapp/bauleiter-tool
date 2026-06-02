import streamlit as st
from utils.supabase_client import get_client

st.set_page_config(page_title="Baustellen", page_icon="🏗️", layout="wide")
st.title("🏗️ Baustellen")

try:
    db = get_client()
except Exception as e:
    st.error(str(e))
    st.stop()

# --- Neue Baustelle anlegen ---
with st.expander("➕ Neue Baustelle anlegen", expanded=False):
    with st.form("neue_baustelle"):
        name = st.text_input("Baustellen-Name *")
        auftraggeber = st.text_input("Auftraggeber *")
        ort = st.text_input("Ort")
        auftragssumme = st.number_input("Auftragssumme (€)", min_value=0.0, step=1000.0)
        baubeginn = st.date_input("Baubeginn")
        submitted = st.form_submit_button("Baustelle anlegen", use_container_width=True)

        if submitted:
            if not name or not auftraggeber:
                st.error("Name und Auftraggeber sind Pflichtfelder.")
            else:
                try:
                    db.table("baustellen").insert({
                        "name": name,
                        "auftraggeber": auftraggeber,
                        "ort": ort,
                        "auftragssumme": auftragssumme,
                        "baubeginn": str(baubeginn),
                        "status": "Arbeitsvorbereitung"
                    }).execute()
                    st.success(f"Baustelle '{name}' angelegt!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler: {e}")

st.markdown("---")

# --- Bestehende Baustellen ---
try:
    result = db.table("baustellen").select("*").order("created_at", desc=True).execute()
    baustellen = result.data
except Exception as e:
    st.error(f"Daten konnten nicht geladen werden: {e}")
    st.stop()

if not baustellen:
    st.info("Noch keine Baustellen angelegt. Klappe oben 'Neue Baustelle anlegen' auf.")
else:
    for b in baustellen:
        status_farbe = {
            "Arbeitsvorbereitung": "🟡",
            "Bauausführung": "🟠",
            "Fertiggestellt": "🟢"
        }.get(b["status"], "⚪")

        with st.expander(f"{status_farbe} **{b['name']}** — {b['auftraggeber']}"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**Ort:** {b.get('ort') or '–'}")
                st.write(f"**Auftragssumme:** {b.get('auftragssumme', 0):,.0f} €")
                st.write(f"**Baubeginn:** {b.get('baubeginn') or '–'}")
            with col2:
                neuer_status = st.selectbox(
                    "Phase / Status",
                    ["Arbeitsvorbereitung", "Bauausführung", "Fertiggestellt"],
                    index=["Arbeitsvorbereitung", "Bauausführung", "Fertiggestellt"].index(b["status"]),
                    key=f"status_{b['id']}"
                )
                if neuer_status != b["status"]:
                    db.table("baustellen").update({"status": neuer_status}).eq("id", b["id"]).execute()
                    st.rerun()
            with col3:
                if st.button("🗑️ Löschen", key=f"del_{b['id']}"):
                    db.table("baustellen").delete().eq("id", b["id"]).execute()
                    st.rerun()
