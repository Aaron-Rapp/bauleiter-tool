# Bauleiter-Tool — Startanleitung

## Schritt 1: Supabase Datenbank anlegen (einmalig, ~3 Min.)

1. `supabase.com` → dein Projekt → **SQL Editor** (links)
2. Inhalt von `supabase_schema.sql` kopieren (alle 4 Tabellen)
3. In SQL Editor einfügen → **Run**
4. Grüner Haken = fertig

---

## Schritt 2: GitHub Remote verbinden (einmalig)

Im Terminal:
```
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/HTWG/Semester\ 1/Digitalisierung\ im\ Bauwesen/bauleiter-tool
git remote add origin https://github.com/Aaron-Rapp/bauleiter-tool.git
git push -u origin main
```

---

## Schritt 3: App auf Streamlit Cloud deployen (für Handy-Zugriff, einmalig)

1. `share.streamlit.io` aufrufen → mit GitHub anmelden
2. **"New app"** → Repository: `Aaron-Rapp/bauleiter-tool` → Branch: `main` → File: `app.py`
3. **"Advanced settings"** → Secrets einfügen:
   ```
   GEMINI_API_KEY = "dein-gemini-key"
   SUPABASE_URL = "https://deine-id.supabase.co"
   SUPABASE_KEY = "dein-anon-key"
   ```
4. **Deploy** → App bekommt eine URL (z.B. `aaron-rapp-bauleiter.streamlit.app`)
5. Diese URL auf PC + Handy aufrufen = synchron

---

## App lokal starten (täglich)

```
/Users/aaronrapp/Library/Python/3.9/bin/streamlit run app.py
```
→ **http://localhost:8501**

---

## Demo-Test

- `demo/DEMO_Bauvertrag.pdf` — Testvertrag für KI-Chat
- Test-Fragen: "Schulde ich das Baumfällen?" → erwartet: NEIN
- Test-Fragen: "Wer ist für die Verkehrssicherung zuständig?" → erwartet: Auftraggeber

---

## Projektstruktur

```
bauleiter-tool/
├── app.py                       Startseite + Navigation
├── pages/
│   ├── 1_Baustellen.py          Baustellen verwalten
│   ├── 2_Dokumente.py           Dokumente hochladen + KI-Chat
│   ├── 3_Aufgaben.py            Checkliste (3 Phasen)
│   └── 4_Nachtrag.py            Foto → Mehrkostenanzeige (.docx Download)
├── utils/
│   ├── config.py                API-Keys (lokal + Cloud)
│   ├── gemini_helper.py         Gemini 2.0 Flash KI
│   ├── supabase_client.py       Datenbankverbindung
│   └── nachtrag_export.py       Word-Export
├── demo/
│   └── DEMO_Bauvertrag.pdf      Testvertrag für Präsentation
├── .env                         API-Keys lokal (NICHT auf GitHub)
├── supabase_schema.sql          Datenbankschema
└── PRAESENTATION_DEMO.md        Demo-Skript für 18.06.2026
```

---

## KI-Modelle

| Funktion | Modell | Kosten |
|---|---|---|
| Dokument-Chat (RAG) | Gemini 2.0 Flash | kostenlos |
| Foto-Analyse → Nachtrag | Gemini 2.0 Flash Vision | kostenlos |
