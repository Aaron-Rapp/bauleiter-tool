"""
Konfiguration aus Streamlit Secrets (Cloud) oder .env (lokal).
Rolle wird pro Sitzung gespeichert (session_state) — NICHT auf Disk.
Wichtig: Auf Streamlit Cloud teilen sich alle Nutzer denselben Server.
Eine Datei-Speicherung würde die Rolle des einen Nutzers allen anderen
aufzwingen (Onboarding würde übersprungen). Daher rein session-basiert.
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_config(key: str) -> str:
    """Liest Konfigurationswert aus Streamlit Secrets oder .env"""
    try:
        import streamlit as st
        wert = st.secrets.get(key, "")
        if wert and "hier" not in str(wert):
            return str(wert)
    except Exception:
        pass
    return os.getenv(key, "")


def get_rolle() -> Optional[str]:
    """Liest die Rolle der aktuellen Sitzung (pro Nutzer, nicht geteilt)."""
    try:
        import streamlit as st
        return st.session_state.get("bauleiter_rolle")
    except Exception:
        return None


def set_rolle(rolle: str):
    """Speichert Rolle nur in der aktuellen Sitzung."""
    try:
        import streamlit as st
        st.session_state["bauleiter_rolle"] = rolle
    except Exception:
        pass


def reset_rolle():
    """Löscht Rolle + Name aus der aktuellen Sitzung."""
    try:
        import streamlit as st
        st.session_state.pop("bauleiter_rolle", None)
        st.session_state.pop("bauleiter_name", None)
    except Exception:
        pass


def get_name() -> str:
    """Liest den Namen aus der aktuellen Sitzung (wird nicht dauerhaft gespeichert)."""
    try:
        import streamlit as st
        return st.session_state.get("bauleiter_name", "")
    except Exception:
        return ""


def set_name(name: str):
    """Speichert den Namen nur für die aktuelle Sitzung."""
    try:
        import streamlit as st
        st.session_state["bauleiter_name"] = name
    except Exception:
        pass
