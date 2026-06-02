"""
Liest Konfiguration aus Streamlit Secrets (Cloud) oder .env (lokal).
Streamlit Secrets haben Vorrang.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_config(key: str) -> str:
    # Zuerst Streamlit Secrets versuchen (funktioniert nur wenn Streamlit läuft)
    try:
        import streamlit as st
        wert = st.secrets.get(key, "")
        if wert and "hier" not in str(wert):
            return str(wert)
    except Exception:
        pass

    # Fallback: .env / Umgebungsvariable
    wert = os.getenv(key, "")
    return wert
