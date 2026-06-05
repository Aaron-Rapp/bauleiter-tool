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
    """Liest gespeicherte Rolle aus lokaler JSON-Datei"""
    try:
        if _ROLLE_PFAD.exists():
            data = json.loads(_ROLLE_PFAD.read_text(encoding="utf-8"))
            return data.get("rolle")
    except Exception:
        pass
    return None


def set_rolle(rolle: str):
    """Speichert Rolle in lokaler JSON-Datei"""
    try:
        _ROLLE_PFAD.write_text(json.dumps({"rolle": rolle}), encoding="utf-8")
    except Exception:
        pass


def reset_rolle():
    """Löscht gespeicherte Rolle"""
    try:
        if _ROLLE_PFAD.exists():
            _ROLLE_PFAD.unlink()
    except Exception:
        pass
