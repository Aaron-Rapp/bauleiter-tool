import streamlit as st
import PyPDF2
import io
from utils.supabase_client import get_client
from utils.gemini_helper import frage_an_dokumente

st.set_page_config(page_title="Dokumente & KI-Chat", page_icon="📁", layout="wide")
st.title("📁 Dokumente & KI-Chat")

try:
    db = get_client()
except Exception as e:
    st.error(str(e))
    st.stop()

# Baustelle auswählen
try:
    baustellen = db.table("baustellen").select("id, name").execute().data
except Exception as e:
    st.error(f"Daten konnten nicht geladen werden: {e}")
    st.stop()

if not baustellen:
    st.warning("Erst eine Baustelle unter 'Baustellen' anlegen.")
    st.stop()

auswahl = st.selectbox("Baustelle auswählen", options=baustellen, format_func=lambda x: x["name"])
baustelle_id = auswahl["id"]

st.markdown("---")
col_links, col_rechts = st.columns([1, 2])

# --- Linke Spalte: Dokumente ---
with col_links:
    st.subheader("Dokumente hochladen")
    uploads = st.file_uploader(
        "PDF oder Word (.docx)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Lade Verträge, Leistungsverzeichnisse oder Pläne hoch"
    )

    if uploads:
        for datei in uploads:
            if st.button(f"💾 '{datei.name}' speichern", key=f"save_{datei.name}"):
                inhalt = datei.read()
                text = ""
                try:
                    if datei.name.lower().endswith(".pdf"):
                        reader = PyPDF2.PdfReader(io.BytesIO(inhalt))
                        for seite in reader.pages:
                            text += seite.extract_text() or ""
                    elif datei.name.lower().endswith(".docx"):
                        import docx
                        doc = docx.Document(io.BytesIO(inhalt))
                        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                except Exception as e:
                    st.error(f"Fehler beim Lesen von '{datei.name}': {e}")
                    continue

                if not text.strip():
                    st.warning(f"'{datei.name}' enthält keinen lesbaren Text (evtl. gescanntes Bild).")
                    continue

                try:
                    db.table("dokumente").insert({
                        "baustelle_id": baustelle_id,
                        "dateiname": datei.name,
                        "text": text[:100000]  # Max 100k Zeichen
                    }).execute()
                    st.success(f"✅ '{datei.name}' gespeichert ({len(text):,} Zeichen)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Speicherfehler: {e}")

    st.markdown("---")
    st.subheader("Gespeicherte Dokumente")
    try:
        docs = db.table("dokumente").select("id, dateiname, text").eq("baustelle_id", baustelle_id).execute().data
    except Exception:
        docs = []

    if not docs:
        st.info("Noch keine Dokumente für diese Baustelle.")
    else:
        for doc in docs:
            zeichen = len(doc.get("text") or "")
            col_a, col_b = st.columns([4, 1])
            col_a.write(f"📄 {doc['dateiname']} *({zeichen:,} Zeichen)*")
            if col_b.button("🗑️", key=f"del_{doc['id']}", help="Löschen"):
                db.table("dokumente").delete().eq("id", doc["id"]).execute()
                st.rerun()

# --- Rechte Spalte: KI-Chat ---
with col_rechts:
    st.subheader("KI-Chat — Frage an deine Dokumente")

    if "chat_verlauf" not in st.session_state:
        st.session_state.chat_verlauf = []

    try:
        docs_mit_text = db.table("dokumente").select("dateiname, text").eq("baustelle_id", baustelle_id).execute().data
    except Exception:
        docs_mit_text = []

    if not docs_mit_text:
        st.info("📤 Lade erst Dokumente hoch, um Fragen stellen zu können.")
    else:
        st.caption(f"**{len(docs_mit_text)} Dokument(e) geladen.** Stelle deine Frage:")

        for msg in st.session_state.chat_verlauf:
            with st.chat_message(msg["rolle"]):
                st.markdown(msg["text"])

        frage = st.chat_input(
            "z.B. 'Schulde ich das Baumfällen?' oder 'Wer ist verantwortlich für die Verkehrssicherung?'"
        )

        if frage:
            st.session_state.chat_verlauf.append({"rolle": "user", "text": frage})
            with st.chat_message("user"):
                st.markdown(frage)

            with st.chat_message("assistant"):
                with st.spinner("KI analysiert Dokumente..."):
                    try:
                        texte = [f"[{d['dateiname']}]\n{d['text']}" for d in docs_mit_text]
                        antwort = frage_an_dokumente(frage, texte)
                    except Exception as e:
                        antwort = f"Fehler bei der KI-Anfrage: {e}"

                st.markdown(antwort)

                if antwort.strip().upper().startswith("NEIN"):
                    st.warning("⚠️ Leistung wird nicht geschuldet → **Nachtrag empfohlen!**")
                    if st.button("➡️ Zum Nachtrag-Generator", key="goto_nachtrag"):
                        st.switch_page("pages/4_Nachtrag.py")

            st.session_state.chat_verlauf.append({"rolle": "assistant", "text": antwort})

        if st.session_state.chat_verlauf:
            if st.button("🗑️ Chat leeren"):
                st.session_state.chat_verlauf = []
                st.rerun()
