# Bauleiter-Tool — Startanleitung

## Einmalige Einrichtung (noch zu erledigen)

### 1. Supabase: Datenbanktabellen anlegen
1. Gehe zu supabase.com → dein Projekt → **SQL Editor**
2. Kopiere den gesamten Inhalt der Datei `supabase_schema.sql`
3. Füge ihn in den SQL Editor ein → **Run**
4. Alle 4 Tabellen werden angelegt

### 2. GitHub: Remote verbinden
```bash
git remote add origin https://github.com/Aaron-Rapp/bauleiter-tool.git
git push -u origin main
```

---

## App starten (täglich)

Terminal öffnen und eingeben:
```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/HTWG/Semester\ 1/Digitalisierung\ im\ Bauwesen/bauleiter-tool
/Users/aaronrapp/Library/Python/3.9/bin/streamlit run app.py
```

→ App öffnet sich unter: **http://localhost:8501**

---

## Projektstruktur

```
bauleiter-tool/
├── app.py                    Startseite
├── pages/
│   ├── 1_Baustellen.py       Baustellen verwalten
│   ├── 2_Dokumente.py        Dokumente hochladen + KI-Chat
│   ├── 3_Aufgaben.py         Checkliste (3 Phasen)
│   └── 4_Nachtrag.py         Foto → Mehrkostenanzeige
├── utils/
│   ├── gemini_helper.py      Gemini KI-Integration
│   ├── supabase_client.py    Datenbankverbindung
│   └── nachtrag_export.py    Word-Export
├── .env                      API-Keys (NICHT auf GitHub)
├── supabase_schema.sql       Datenbankschema
└── requirements.txt          Python-Pakete
```

---

## KI-Modelle verwendet

| Aufgabe | Modell | Anbieter |
|---|---|---|
| Dokument-Chat (RAG) | Gemini 2.0 Flash | Google (kostenlos) |
| Foto-Analyse Nachtrag | Gemini 2.0 Flash Vision | Google (kostenlos) |
