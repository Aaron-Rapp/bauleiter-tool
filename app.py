import streamlit as st
from utils.db import get_db_client
from utils.config import get_rolle, set_rolle, reset_rolle, get_name, set_name
import datetime
import html as html_mod

st.set_page_config(
    page_title="Bauleiter-Tool",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap');

/* ── Base ───────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
[data-testid="collapsedControl"] { display: none; }
[data-testid="stSidebarNav"]     { display: none; }

.stApp { background: #F2F1EF !important; }

.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1200px;
}

/* ── Typography ─────────────────────────────────── */
h1 { font-weight: 800 !important; letter-spacing: -0.04em !important;
     color: #111111 !important; line-height: 1.1 !important; }
h2, h3 { font-weight: 700 !important; letter-spacing: -0.025em !important;
          color: #1A1A1A !important; }
p { color: #1A1A1A !important; }

/* ── Buttons — Primary (dark charcoal) ──────────── */
.stButton > button[kind="primary"] {
    background: #1A1A1A !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.87rem !important;
    padding: 0.55rem 1.3rem !important;
    letter-spacing: 0.015em !important;
    transition: background 0.15s, box-shadow 0.15s !important;
    box-shadow: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: #333333 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18) !important;
}

/* ── Buttons — Secondary ────────────────────────── */
.stButton > button[kind="secondary"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.87rem !important;
    border: 1px solid #DDDBD8 !important;
    background: white !important;
    color: #333333 !important;
    transition: border-color 0.15s, color 0.15s !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #F07030 !important;
    color: #F07030 !important;
    background: white !important;
}

/* ── Cards ──────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1px solid #E8E6E2 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.07) !important;
    background: #FFFFFF !important;
    overflow: visible !important;
    transition: box-shadow 0.22s ease, transform 0.22s ease, border-color 0.22s ease !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 12px 40px rgba(240,112,48,0.13), 0 4px 12px rgba(0,0,0,0.08) !important;
    transform: translateY(-3px) scale(1.01) !important;
    border-color: rgba(240,112,48,0.35) !important;
    z-index: 10 !important;
    position: relative !important;
}

/* ── Projekt-Bild-Button ────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"]:first-child { min-height:148px!important; height:148px!important; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"]:first-child > button { min-height:148px!important; height:148px!important; width:100%!important; background: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='44' viewBox='0 0 24 24' fill='none' stroke='%23C8C5BF' stroke-width='1.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='2' y='7' width='20' height='14' rx='2'/%3E%3Cpath d='M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2'/%3E%3Cline x1='12' y1='12' x2='12' y2='16'/%3E%3Cline x1='10' y1='14' x2='14' y2='14'/%3E%3C/svg%3E") center/44px no-repeat,#F5F4F1!important; border:none!important; border-radius:10px 10px 0 0!important; box-shadow:none!important; cursor:pointer!important; color:transparent!important; font-size:0!important; padding:0!important; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"]:first-child > button > div { min-height:148px!important; height:148px!important; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"]:first-child > button:hover { background-color:#EDECEA!important; }

/* ── Inputs ─────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    border-radius: 8px !important;
    border: 1px solid #DDDBD8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.89rem !important;
    background: #FAFAF9 !important;
    color: #1A1A1A !important;
    transition: border-color 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #F07030 !important;
    box-shadow: 0 0 0 2.5px rgba(240,112,48,0.14) !important;
    background: white !important;
    outline: none !important;
}
.stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1px solid #DDDBD8 !important;
    background: #FAFAF9 !important;
}
.stMultiSelect > div > div {
    border-radius: 8px !important;
    border: 1px solid #DDDBD8 !important;
}

/* ── Tabs ───────────────────────────────────────── */
div[data-testid="stTabs"] div[role="tablist"],
.stTabs [data-baseweb="tab-list"] {
    background: #E9E8E5 !important;
    border-radius: 10px !important;
    padding: 3px !important;
    gap: 1px !important;
    border: none !important;
}
div[data-testid="stTabs"] button[role="tab"],
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    padding: 7px 13px !important;
    color: #777672 !important;
    border: none !important;
    background: transparent !important;
    letter-spacing: 0.005em !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1A1A1A !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
div[data-testid="stTabs"] div[role="tablist"]::after,
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Expander ───────────────────────────────────── */
.streamlit-expanderHeader {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    background: white !important;
    border: 1px solid #E8E6E2 !important;
    color: #1A1A1A !important;
}
.streamlit-expanderContent {
    border: 1px solid #E8E6E2 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    background: white !important;
}

/* ── Alerts ─────────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; }
.stInfo { background: #F9F8F6 !important; border-left: 3px solid #DDDBD8 !important; }
.stWarning { border-left: 3px solid #F07030 !important; }

/* ── Divider / HR ───────────────────────────────── */
hr { border-color: #E8E6E2 !important; margin: 1.1rem 0 !important; }

/* ── Caption ────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #888683 !important;
    font-size: 0.81rem !important;
}

/* ── Form background ────────────────────────────── */
[data-testid="stForm"] {
    background: #F7F6F4 !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    border: 1px solid #E8E6E2 !important;
}

/* ── Image + Camera ─────────────────────────────── */
[data-testid="stImage"] img { border-radius: 10px !important; }
.stCameraInput { border-radius: 10px !important; }

/* ── Progress bar ───────────────────────────────── */
.stProgress > div > div { border-radius: 999px !important; }
</style>
""", unsafe_allow_html=True)

# ── DB ────────────────────────────────────────────────────────
if "db" not in st.session_state or "db_modus" not in st.session_state:
    db, modus = get_db_client()
    st.session_state.db = db
    st.session_state.db_modus = modus

db    = st.session_state.db
modus = st.session_state.db_modus

# ── Query-Param Navigation (von HTML-Bild-Button) ────────────
open_id = st.query_params.get("open_project")
if open_id:
    try:
        projekte_tmp = db.table("projekte").select("*").eq("id", open_id).execute().data
        if projekte_tmp:
            st.session_state.aktives_projekt = open_id
            st.session_state.aktives_projekt_name = projekte_tmp[0]["name"]
            st.session_state.db = db
            st.session_state.db_modus = modus
            st.query_params.clear()
            st.switch_page("pages/1_Projekt.py")
    except Exception:
        st.query_params.clear()

# ── Rolle ─────────────────────────────────────────────────────
rolle = get_rolle()

if not rolle:
    col_c, col_mid, col_c2 = st.columns([1, 4, 1])
    with col_mid:
        # Logo + Branding
        st.markdown("""
        <div style='text-align:center; padding:3rem 0 2rem 0;'>
          <div style='display:inline-flex; align-items:center; gap:14px; margin-bottom:1.5rem;'>
            <div style='
              width:56px; height:56px; background:#F07030; border-radius:14px;
              display:flex; align-items:center; justify-content:center;
              box-shadow:0 4px 16px rgba(240,112,48,0.28);
            '>
              <span style='color:white; font-family:Inter,sans-serif;
                           font-weight:900; font-size:28px; letter-spacing:-0.06em;'>R</span>
            </div>
            <div style='text-align:left; line-height:1.1;'>
              <div style='font-family:Inter,sans-serif; font-size:32px; font-weight:800;
                          letter-spacing:-0.04em; color:#1A1A1A;'>
                <span style='color:#F07030;'>·</span>APP
              </div>
              <div style='font-size:10px; font-weight:500; color:#BBBBBB;
                          letter-spacing:0.14em; text-transform:uppercase;'>Bauleitung Digital</div>
            </div>
          </div>
          <p style='color:#888683; font-size:0.95rem; margin:0;'>
            Wähle deine Rolle, um zu starten
          </p>
        </div>
        """, unsafe_allow_html=True)

        eingabe_name = st.text_input(
            "Dein Name",
            placeholder="z.B. Max Mustermann",
            help="Wird in Tagesberichten und VOB-Dokumenten verwendet"
        )

        ROLLEN = {
            "Bauleiter": (
                "Alle Termine · Konflikt-Erkennung zwischen Projekten · VOB-Schriftverkehr",
                "B"
            ),
            "Polier": (
                "Polier-Termine · Baustellen-Besetzung im Fokus · Tagesberichte",
                "P"
            ),
            "Außenstehend": (
                "Lesezugriff auf alle Projektinfos und Dokumente",
                "A"
            ),
        }
        for r, (desc, initial) in ROLLEN.items():
            with st.container(border=True):
                col_icon, col_t, col_b = st.columns([1, 6, 2])
                with col_icon:
                    st.markdown(
                        f"<div style='width:38px;height:38px;background:#F07030;border-radius:9px;"
                        f"display:flex;align-items:center;justify-content:center;margin-top:4px;'>"
                        f"<span style='color:white;font-weight:800;font-size:15px;"
                        f"font-family:Inter,sans-serif;'>{initial}</span></div>",
                        unsafe_allow_html=True
                    )
                with col_t:
                    st.markdown(
                        f"<p style='margin:0 0 2px 0;font-weight:700;font-size:0.97rem;"
                        f"color:#1A1A1A;'>{html_mod.escape(r)}</p>"
                        f"<p style='margin:0;font-size:0.8rem;color:#888683;'>{desc}</p>",
                        unsafe_allow_html=True
                    )
                with col_b:
                    if st.button("Auswählen", key=f"rolle_{r}", use_container_width=True,
                                 type="primary"):
                        set_rolle(r)
                        if eingabe_name.strip():
                            set_name(eingabe_name.strip())
                        st.rerun()
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    st.stop()

st.session_state.rolle = rolle
name = get_name()
st.session_state.bauleiter_name = name

if modus == "lokal":
    st.markdown("""
    <div style='font-size:0.78rem; color:#999693; padding:0.35rem 0.8rem;
                background:#EFEFED; border-radius:6px; display:inline-block;
                margin-bottom:0.5rem; border:1px solid #E8E6E2;'>
      Lokaler Modus — Daten werden lokal gespeichert
    </div>
    """, unsafe_allow_html=True)

# ── Konflikt-Check ────────────────────────────────────────────
if rolle == "Bauleiter":
    try:
        heute = str(datetime.date.today())
        termine = db.table("kalender").select("titel, datum, projekt_id").eq("kategorie", "blau").gte("datum", heute).execute().data
        datum_map = {}
        for t in termine:
            datum_map.setdefault(t["datum"], []).append(t)
        for datum, ts in datum_map.items():
            if len(ts) > 1:
                namen = ", ".join([f"'{x['titel']}'" for x in ts])
                st.warning(f"**Terminkonflikt am {datum}:** {namen}")
    except Exception:
        pass

# ── Header ────────────────────────────────────────────────────
st.markdown(f"""
<div style='
  display:flex; align-items:center; justify-content:space-between;
  padding:0.5rem 0 0.4rem 0; flex-wrap:wrap; gap:0.5rem;
'>
  <!-- Logo -->
  <div style='display:flex; align-items:center; gap:12px;'>
    <div style='
      width:42px; height:42px; background:#F07030; border-radius:10px;
      display:flex; align-items:center; justify-content:center; flex-shrink:0;
      box-shadow:0 2px 10px rgba(240,112,48,0.22);
    '>
      <span style='color:white; font-family:Inter,sans-serif;
                   font-weight:900; font-size:21px; letter-spacing:-0.06em;'>R</span>
    </div>
    <div style='line-height:1.15;'>
      <div style='font-family:Inter,sans-serif; font-size:25px; font-weight:800;
                  letter-spacing:-0.04em; color:#1A1A1A;'>
        <span style='color:#F07030;'>·</span>APP
      </div>
      <div style='font-size:8.5px; font-weight:500; color:#AAAAAA;
                  letter-spacing:0.14em; text-transform:uppercase;'>Bauleitung Digital</div>
    </div>
  </div>
  <!-- Rolle + Button -->
  <div style='display:flex; align-items:center; gap:8px;'>
    <span style='background:white; color:#555552; padding:5px 12px;
                 border-radius:999px; font-size:0.79rem; font-weight:500;
                 border:1px solid #E8E6E2; white-space:nowrap;
                 font-family:Inter,sans-serif;'>{html_mod.escape((name + " · " + rolle) if name else rolle)}</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:0.4rem 0 0.5rem 0; border-color:#E8E6E2;'>", unsafe_allow_html=True)

# Sektions-Titel + Rolle-Button in einer Zeile
c_titel, c_rolle = st.columns([7, 3])
with c_titel:
    st.markdown("""
    <h2 style='font-size:1.5rem; font-weight:700; color:#111111;
               letter-spacing:-0.03em; margin:0.2rem 0 1.2rem 0;'>Meine Baustellen</h2>
    """, unsafe_allow_html=True)
with c_rolle:
    st.markdown("<div style='padding-top:0.15rem; text-align:right;'>", unsafe_allow_html=True)
    if st.button("Rolle wechseln", help="Andere Rolle wählen"):
        reset_rolle()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Projekte laden ────────────────────────────────────────────
try:
    projekte = db.table("projekte").select("*").order("erstellt_am").execute().data
except Exception:
    projekte = []

# ── Neues Projekt ─────────────────────────────────────────────
with st.expander("Neues Projekt anlegen", expanded=(len(projekte) == 0)):
    with st.form("neues_projekt", clear_on_submit=True):
        col_cam, col_up = st.columns(2)
        with col_cam:
            foto_kamera = st.camera_input("Direkt fotografieren")
        with col_up:
            foto_upload = st.file_uploader("Oder Bild hochladen", type=["jpg","jpeg","png","webp"])

        name = st.text_input("Name der Baustelle *", placeholder="z.B. Neubau Bürogebäude Konstanz")
        col1, col2 = st.columns(2)
        with col1:
            auftraggeber = st.text_input("Auftraggeber *", placeholder="z.B. Stadtwerke Konstanz GmbH")
        with col2:
            vertragsnummer = st.text_input("Vertragsnummer", placeholder="z.B. V-2026-042")
        col1b, col2b = st.columns(2)
        with col1b:
            kostenstelle = st.text_input("Kostenstelle", placeholder="z.B. KST-2026-042")
        with col2b:
            anschrift = st.text_input("Anschrift", placeholder="z.B. Hauptstraße 1, 78462 Konstanz")
        col3, col4 = st.columns(2)
        with col3:
            bauzeit_von = st.date_input("Baubeginn", value=None, format="DD.MM.YYYY")
        with col4:
            bauzeit_bis = st.date_input("Bauende", value=None, format="DD.MM.YYYY")

        if st.form_submit_button("Projekt anlegen", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Bitte einen Projektnamen eingeben.")
            else:
                foto_url = ""
                bild_datei = foto_kamera or foto_upload
                if bild_datei:
                    if modus == "supabase":
                        try:
                            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            pfad = f"projekte/{ts}.jpg"
                            db.storage.from_("bauleiter-dateien").upload(
                                pfad, bild_datei.getvalue(),
                                {"content-type": "image/jpeg", "upsert": "true"}
                            )
                            foto_url = db.storage.from_("bauleiter-dateien").get_public_url(pfad)
                        except Exception:
                            foto_url = ""
                    else:
                        import base64
                        foto_url = "data:image/jpeg;base64," + base64.b64encode(bild_datei.getvalue()).decode()

                eintrag = {
                    "name": name.strip(),
                    "auftraggeber": auftraggeber.strip(),
                    "vertragsnummer": vertragsnummer.strip(),
                    "kostenstelle": kostenstelle.strip(),
                    "anschrift": anschrift.strip(),
                    "foto_url": foto_url,
                }
                if bauzeit_von:
                    eintrag["bauzeit_von"] = str(bauzeit_von)
                if bauzeit_bis:
                    eintrag["bauzeit_bis"] = str(bauzeit_bis)

                try:
                    try:
                        res = db.table("projekte").insert(eintrag).execute()
                    except Exception as _e:
                        if "auftraggeber" in str(_e) or "vertragsnummer" in str(_e):
                            eintrag.pop("auftraggeber", None)
                            eintrag.pop("vertragsnummer", None)
                            res = db.table("projekte").insert(eintrag).execute()
                        else:
                            raise
                    new_pid = res.data[0]["id"] if res.data else None
                    if new_pid:
                        _default_todos = [
                            ("Leitungspläne einholen",                          "Arbeitsvorbereitung"),
                            ("Bestandsaufnahme durchführen",                     "Arbeitsvorbereitung"),
                            ("Sicherheitsunterweisung der Arbeiter vorbereiten", "Arbeitsvorbereitung"),
                            ("Sicherheitseinweisung für die Arbeiter durchführen","Beginn der Baustelle"),
                            ("Abnahmeaufforderung stellen",                      "Abnahme"),
                            ("Abnahme durchführen",                              "Abnahme"),
                        ]
                        for titel, phase in _default_todos:
                            try:
                                db.table("todos").insert({
                                    "projekt_id": new_pid,
                                    "titel": titel,
                                    "phase": phase,
                                    "erledigt": False,
                                }).execute()
                            except Exception:
                                pass
                    st.success(f"'{name}' angelegt!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler: {e}")

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Demo-Daten ────────────────────────────────────────────────
if len(projekte) == 0:
    col_demo, _ = st.columns([3, 7])
    with col_demo:
        if st.button("Demo-Projekt laden", help="Lädt ein realistisches Musterprojekt für die Präsentation"):
            from utils.demo_daten import lade_demo_projekt
            lade_demo_projekt(db)
            st.success("Demo-Projekt geladen!")
            st.rerun()

# ── Projektkacheln ────────────────────────────────────────────
if not projekte:
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem; color: #94a3b8;'>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1"
             stroke-width="1.5" style="margin-bottom:1rem;">
            <rect x="2" y="3" width="20" height="14" rx="2"/>
            <path d="M8 21h8M12 17v4"/>
        </svg>
        <p style='font-size:1rem; font-weight:500; margin:0;'>Noch keine Projekte vorhanden</p>
        <p style='font-size:0.85rem; margin-top:0.3rem;'>Lege oben dein erstes Projekt an.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    if "loesche_projekt" not in st.session_state:
        st.session_state.loesche_projekt = None
    if "bearbeite_projekt" not in st.session_state:
        st.session_state.bearbeite_projekt = None

    # Statistiken für alle Projekte vorladen
    heute_str = str(datetime.date.today())
    in_30_str = str(datetime.date.today() + datetime.timedelta(days=30))
    projekt_stats = {}
    for p in projekte:
        try:
            todos = db.table("todos").select("erledigt").eq("projekt_id", p["id"]).execute().data
            ges = len(todos)
            erl = sum(1 for t in todos if t["erledigt"])
            termine = db.table("kalender").select("id").eq("projekt_id", p["id"]).gte("datum", heute_str).lte("datum", in_30_str).execute().data
            projekt_stats[p["id"]] = {"ges": ges, "erl": erl, "termine": len(termine)}
        except Exception:
            projekt_stats[p["id"]] = {"ges": 0, "erl": 0, "termine": 0}

    # Platzhalter-SVG für Projekte ohne Foto
    PLACEHOLDER_SVG = """
    <div style='background:linear-gradient(135deg,#e2e8f0,#f1f5f9);
         height:140px;display:flex;align-items:center;
         justify-content:center;border-radius:10px;
         margin-bottom:0.5rem;'>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8"
             stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2"/>
            <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
            <line x1="12" y1="12" x2="12" y2="16"/>
            <line x1="10" y1="14" x2="14" y2="14"/>
        </svg>
    </div>"""

    for i in range(0, len(projekte), 3):
        cols = st.columns(3, gap="medium")
        for j in range(3):
            if i + j < len(projekte):
                p = projekte[i + j]
                with cols[j]:
                    with st.container(border=True):
                        # Klickbares Bild: echter HTML-Button mit Query-Param-Navigation
                        pid_safe = html_mod.escape(p["id"])
                        if p.get("foto_url"):
                            btn_content = ""
                            btn_style = ("width:100%;height:148px;border:none;border-radius:10px;"
                                         "cursor:pointer;padding:0;margin:0 0 8px 0;display:block;"
                                         "background-image:url('" + p["foto_url"] + "');"
                                         "background-size:cover;background-position:center;"
                                         "transition:filter 0.2s;")
                        else:
                            btn_content = ('<svg width="48" height="48" viewBox="0 0 24 24" fill="none"'
                                           ' stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"'
                                           ' stroke-linejoin="round">'
                                           '<rect x="2" y="7" width="20" height="14" rx="2"/>'
                                           '<path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>'
                                           '<line x1="12" y1="12" x2="12" y2="16"/>'
                                           '<line x1="10" y1="14" x2="14" y2="14"/>'
                                           '</svg>')
                            btn_style = ("width:100%;height:148px;border:none;border-radius:10px;"
                                         "cursor:pointer;padding:0;margin:0 0 8px 0;"
                                         "display:flex;align-items:center;justify-content:center;"
                                         "background:linear-gradient(135deg,#eaeff5,#dde4ed);"
                                         "transition:filter 0.2s;")
                        st.markdown(
                            "<form method='get' action='' style='margin:0;padding:0;'>"
                            "<input type='hidden' name='open_project' value='" + pid_safe + "'>"
                            "<button type='submit' style='" + btn_style + "'"
                            " onmouseover=\"this.style.filter='brightness(0.92)'\""
                            " onmouseout=\"this.style.filter=''\">"
                            + btn_content +
                            "</button></form>",
                            unsafe_allow_html=True
                        )

                        # Fixer Textblock — immer gleiche Höhe egal wie viel Text
                        pname_safe = html_mod.escape(p['name'])
                        kst  = html_mod.escape(p.get("kostenstelle") or "")
                        adr  = html_mod.escape(p.get("anschrift") or "")
                        von  = html_mod.escape(p.get("bauzeit_von") or "")
                        bis  = html_mod.escape(p.get("bauzeit_bis") or "")
                        meta_html = ""
                        if kst:  meta_html += f"<div style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{kst}</div>"
                        if adr:  meta_html += f"<div style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{adr}</div>"
                        if von or bis: meta_html += f"<div>{von} – {bis}</div>"

                        st.markdown(f"""
                        <div style='padding:0.5rem 0 0.4rem 0;'>
                            <p style='margin:0 0 0.3rem 0; font-weight:700; font-size:0.97rem; color:#1e293b;
                                      overflow:hidden; display:-webkit-box; -webkit-line-clamp:2;
                                      -webkit-box-orient:vertical; min-height:2.4rem; line-height:1.25;'>
                                {pname_safe}
                            </p>
                            <div style='font-size:0.78rem; color:#64748b; min-height:3.6rem;
                                        display:flex; flex-direction:column; gap:2px; justify-content:flex-start;'>
                                {meta_html if meta_html else "<span style='color:#cbd5e1;'>Keine Angaben</span>"}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Stats-Leiste — immer anzeigen für gleiche Höhe
                        s = projekt_stats.get(p["id"], {"ges": 0, "erl": 0, "termine": 0})
                        pct = int(s["erl"] / s["ges"] * 100) if s["ges"] > 0 else 0
                        termin_txt = f"&nbsp;&nbsp;{s['termine']} Termin{'e' if s['termine'] != 1 else ''}" if s["termine"] > 0 else ""
                        todo_txt = f"{s['erl']}/{s['ges']} Aufgaben{termin_txt}" if s["ges"] > 0 else "Noch keine Aufgaben"
                        bar_color = "linear-gradient(90deg,#4CAF50,#66BB6A)" if pct == 100 else "linear-gradient(90deg,#F07030,#F59050)"
                        st.markdown(f"""
                        <div style='margin: 0 0 0.7rem 0;'>
                            <div style='display:flex; align-items:flex-end; justify-content:space-between; margin-bottom:5px;'>
                                <span style='font-size:0.72rem; color:#94a3b8;'>{todo_txt}</span>
                                <span style='font-size:1.45rem; font-weight:800; line-height:1; letter-spacing:-0.04em;
                                             color:{"#4CAF50" if pct==100 else "#F07030"};'>{pct}<span style='font-size:0.68rem; font-weight:600; margin-left:1px; opacity:0.85;'>%</span></span>
                            </div>
                            <div style='background:#f1f5f9; border-radius:999px; height:5px; overflow:hidden;'>
                                <div style='background:{bar_color}; width:{pct}%; height:100%; border-radius:999px;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Aktions-Icons (Bearbeiten / Löschen)
                        ic1, ic2, _ = st.columns([1, 1, 4])
                        with ic1:
                            if st.button("✎", key=f"edit_{p['id']}", help="Bearbeiten", use_container_width=True):
                                st.session_state.bearbeite_projekt = p["id"]
                                st.session_state.loesche_projekt = None
                                st.rerun()
                        with ic2:
                            if st.button("✕", key=f"del_{p['id']}", help="Löschen", use_container_width=True):
                                st.session_state.loesche_projekt = p["id"]
                                st.session_state.bearbeite_projekt = None
                                st.rerun()

                        # ── Bearbeiten-Formular ──────────────────────
                        if st.session_state.get("bearbeite_projekt") == p["id"]:
                            with st.form(f"edit_form_{p['id']}"):
                                e_name = st.text_input("Name", value=p["name"])
                                ec1, ec2 = st.columns(2)
                                with ec1:
                                    e_kst  = st.text_input("Kostenstelle", value=p.get("kostenstelle",""))
                                with ec2:
                                    e_adr  = st.text_input("Anschrift", value=p.get("anschrift",""))
                                ed1, ed2 = st.columns(2)
                                with ed1:
                                    e_von = st.date_input("Baubeginn", value=datetime.date.fromisoformat(p["bauzeit_von"]) if p.get("bauzeit_von") else None, format="DD.MM.YYYY")
                                with ed2:
                                    e_bis = st.date_input("Bauende", value=datetime.date.fromisoformat(p["bauzeit_bis"]) if p.get("bauzeit_bis") else None, format="DD.MM.YYYY")
                                sc1, sc2 = st.columns(2)
                                with sc1:
                                    if st.form_submit_button("Speichern", type="primary", use_container_width=True):
                                        upd = {"name": e_name.strip(), "kostenstelle": e_kst.strip(), "anschrift": e_adr.strip()}
                                        if e_von: upd["bauzeit_von"] = str(e_von)
                                        if e_bis: upd["bauzeit_bis"] = str(e_bis)
                                        db.table("projekte").update(upd).eq("id", p["id"]).execute()
                                        st.session_state.bearbeite_projekt = None
                                        st.rerun()
                                with sc2:
                                    if st.form_submit_button("Abbrechen", use_container_width=True):
                                        st.session_state.bearbeite_projekt = None
                                        st.rerun()

                        # ── Löschen-Bestätigung ──────────────────────
                        if st.session_state.get("loesche_projekt") == p["id"]:
                            st.warning(f"**'{p['name']}'** wirklich löschen?")
                            col_ja, col_nein = st.columns(2)
                            with col_ja:
                                if st.button("Ja, löschen", key=f"ja_{p['id']}", type="primary"):
                                    try:
                                        db.table("projekte").delete().eq("id", p["id"]).execute()
                                    except Exception:
                                        pass
                                    st.session_state.loesche_projekt = None
                                    st.rerun()
                            with col_nein:
                                if st.button("Abbrechen", key=f"nein_{p['id']}"):
                                    st.session_state.loesche_projekt = None
                                    st.rerun()
