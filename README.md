# R·APP Bauleitung Digital

Digitales Bauleiter-Tool für die Baustelle — entwickelt im Rahmen des Moduls  
**Digitalisierung im Bauwesen**, HTWG Konstanz, Masterstudiengang Bauingenieurwesen.

## Features

- **Dashboard** — Projektkacheln mit Foto, Adresse, Kostenstelle, Bauzeit, Todo-Fortschritt
- **Aufgaben** — Todos mit Phasen und Fortschrittsbalken
- **Kalender** — Termin-Übersicht (Info / Bauleiter / Polier), Konflikterkennung
- **KI-Assistent** — Baurechts-Chatbot (VOB/B + BGB) via Google Gemini
- **Verträge & Pläne** — Datei-Upload mit Unterordnern
- **Bilder** — Kamera-Upload mit Unterordner-Struktur
- **VOB-Schriftverkehr** — Mehrkostenanzeige (§2 VOB/B) + Behinderungsanzeige (§6 VOB/B), Word-Export
- **Tagesbericht** — KI-generiert mit Wetter-Vorausfüllung

## Lokaler Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Läuft auf `http://localhost:8507`

## Konfiguration

Erstelle eine `.env` Datei im Projektordner:

```
GEMINI_API_KEY=dein-api-key
```

Gemini API Key kostenlos unter: https://aistudio.google.com/apikey

## Streamlit Cloud Deployment

1. Repo auf [share.streamlit.io](https://share.streamlit.io) verbinden
2. Unter **Settings → Secrets** eintragen:
   ```toml
   GEMINI_API_KEY = "dein-gemini-api-key"
   ```
3. Main file: `app.py`

## Tech Stack

- **Frontend:** Streamlit + Custom CSS (R·APP Design-System)
- **KI:** Google Gemini (google-genai SDK)
- **Datenbank:** SQLite (lokal) / Supabase (optional Cloud)
- **Wetter:** Open-Meteo + Nominatim (kostenlos, kein API-Key)
- **Dokumente:** python-docx (Word-Export)
