"""
Konfiguration aus Streamlit Secrets (Cloud) oder .env (lokal).
Rolle wird lokal gespeichert — kein Datenbankzugriff nötig.
"""
import os
import json
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Pfad für lokale Rolle (liegt im Projektordner, nicht in der Cloud)
_ROLLE_PFAD = Path(__file__).parent.parent / ".bauleiter_rolle.json"


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
    """Liest gespeicherte Rolle: session_state (primär) oder lokale Datei (Fallback)."""
    try:
        import streamlit as st
        if "bauleiter_rolle" in st.session_state:
            return st.session_state["bauleiter_rolle"]
    except Exception:
        pass
    try:
        if _ROLLE_PFAD.exists():
            data = json.loads(_ROLLE_PFAD.read_text(encoding="utf-8"))
            return data.get("rolle")
    except Exception:
        pass
    return None


def set_rolle(rolle: str):
    """Speichert Rolle in session_state und (wenn möglich) auf Disk."""
    try:
        import streamlit as st
        st.session_state["bauleiter_rolle"] = rolle
    except Exception:
        pass
    try:
        _ROLLE_PFAD.write_text(json.dumps({"rolle": rolle}), encoding="utf-8")
    except Exception:
        pass


def reset_rolle():
    """Löscht gespeicherte Rolle."""
    try:
        import streamlit as st
        st.session_state.pop("bauleiter_rolle", None)
        st.session_state.pop("bauleiter_name", None)
    except Exception:
        pass
    try:
        if _ROLLE_PFAD.exists():
            _ROLLE_PFAD.unlink()
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
