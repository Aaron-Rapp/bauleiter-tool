# CLAUDE.md — Bauleiter-Tool (Aaron Rapp, HTWG Konstanz)

## Wer du bist und was du machst
Du bist Claude Code und arbeitest autonom an einer Streamlit Web-App für Bauleiter.
Aaron Rapp ist Masterstudent Bauingenieurwesen an der HTWG Konstanz.
Präsentation der App: **25.06.2026** (online) in der Vorlesung "Digitalisierung im Bauwesen" bei Prof. Dr. Bühler.

## Was die App ist
Ein Bauleiter-Tool mit:
- Projektverwaltung (Foto, Name, Kostenstelle, Adresse, Bauzeit)
- 7 Tabs pro Projekt: Bilder / Pläne / Verträge / KI-Chat / To-Do / Kalender / Nachtrag
- Farbiger Kalender (🟢 läuft alleine / 🔵 Bauleiter / 🟠 Polier)
- Konflikt-Erkennung bei Blau-Terminen über mehrere Projekte
- Rollen: Bauleiter / Polier / Außenstehend

## Tech-Stack
- **Streamlit** (UI) — Python 3.9
- **Supabase** (Datenbank) — mit SQLite-Fallback falls RLS blockiert
- **Gemini 2.0 Flash** (KI-Chat + Nachtrag-Generator)
- **python-dotenv** (.env für API-Keys)

## Wichtigste Dateien
- `app.py` — Startseite mit Projektkacheln + Onboarding
- `pages/1_Projekt.py` — Projektdetail (7 Tabs)
- `utils/db.py` — Datenbankabstraktion (Supabase + SQLite-Fallback)
- `utils/config.py` — Konfiguration + lokale Rolle-Speicherung
- `utils/supabase_client.py` — Supabase-Verbindung
- `supabase_schema.sql` — Datenbankschema (einmalig in Supabase ausführen)
- `.env` — API-Keys (nie in Git pushen!)

## App starten (Terminal 1)
```bash
/Users/aaronrapp/Library/Python/3.9/bin/streamlit run app.py
```
→ http://localhost:8501

## Regeln — IMMER einhalten
1. **Nur kostenfreie Lösungen** — keine kostenpflichtigen APIs oder Services
2. **Alles was du selbst fixen kannst, fixst du** — Aaron nicht unnötig fragen
3. **Nie Git-Push ohne Aarons explizites OK**
4. **Kein Ruhezustand** — `caffeinate -d &` wenn lange Arbeit
5. **Screenshots liest du selbst** — `ls -lt ~/Desktop/*.png | head -3` dann Read

## Aktueller Stand
- ✅ Onboarding (Rolle lokal gespeichert)
- ✅ Projektkacheln mit Foto/Name/KST/Adresse/Bauzeit
- ✅ Projekt anlegen + löschen
- ✅ 7 Tabs in Projektdetail
- ✅ Supabase + SQLite-Fallback
- ⚠️ Supabase Storage Bucket "bauleiter-dateien" muss Public sein
- ⚠️ Supabase RLS: Schema-SQL einmalig in SQL Editor ausführen

## Was als nächstes zu tun ist
1. App vollständig testen
2. Deployment auf Streamlit Cloud für Handy-Zugriff
3. GitHub Remote einrichten: `git remote add origin https://github.com/Aaron-Rapp/bauleiter-tool.git`
4. UI-Polish für Präsentation
