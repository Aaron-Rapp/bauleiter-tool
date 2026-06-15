# Präsentation 25.06.2026 — Demo-Skript (online)

## Aufbau der Präsentation (ca. 15–20 Min.)

---

### Teil 1: Problem (2 Min.)

"Als Bauleiter steht man täglich vor dem gleichen Problem: Man ist auf der Baustelle,
der Auftraggeber bestreitet eine Leistung — und der Vertrag liegt im Büro.
Oder man vergisst beim Baustart die Beweissicherung und verliert später den Nachtrag.
Diese App löst genau das: alle Baustellen-Infos, der Baurechts-Chatbot und der Nachtrag-Generator
in einem Tool, das auf dem Handy läuft."

---

### Teil 2: Live-Demo (10–12 Min.)

**Demo-Schritt 1 — Startseite & Projekt anlegen (2 Min.)**
- App öffnen → Rolle "Bauleiter" + Name eingeben → Auswählen
- Zeigen: Projektkacheln mit Fortschrittsbalken und Wetter
- Neues Projekt anlegen: "Kanalbau Hauptstraße", Auftraggeber: "Stadt Konstanz", KST-2026-042
- Alternativ: **"Demo-Projekt laden"** klicken → realistisches Musterprojekt sofort verfügbar

**Demo-Schritt 2 — Aufgaben-Tab (2 Min.)**
- Projekt öffnen → Tab ✅ Aufgaben
- Zeigen: 3 Phasen (Arbeitsvorbereitung / Bauausführung / Abnahme), Fortschrittsbalken
- Zwei Aufgaben abhaken
- Eigenes Todo hinzufügen: "Beweissicherung Nachbargebäude"
- "Die App erinnert mich an alles — vom ersten Tag bis zur Abnahme"

**Demo-Schritt 3 — KI-Assistent (3 Min.)**
- Tab 🤖 KI-Assistent
- Frage stellen: **"Muss ich den Nachtrag vor Ausführung anzeigen?"**
  → KI: JA + §2 Abs. 6 VOB/B Erklärung
- Zweite Frage: **"Was passiert wenn ich die Behinderungsanzeige vergesse?"**
- "Das hätte mir früher auf der Baustelle 20 Minuten Suchen gespart"

**Demo-Schritt 4 — VOB-Schriftverkehr (3 Min.)**
- Tab ⚖️ VOB
- Mehrkostenanzeige auswählen
- Felder ausfüllen: Auftraggeber, Beschreibung ("Felsschichten Bodenklasse 7 statt 5")
- "Mehrkostenanzeige generieren" klicken → vollständiger Rechtsbref erscheint
- Word-Download zeigen: professioneller Brief sofort fertig
- "Das hat früher 2 Stunden gedauert — jetzt 30 Sekunden"

**Demo-Schritt 5 — Verträge + Briefkopf (1 Min.)**
- Tab 📄 Verträge
- Briefkopf-Vorlage: "Wenn ich hier meine Firmen-Word-Vorlage hochlade, nutzt die App sie für alle VOB-Dokumente"
- Vertrag hochladen zeigen (demo/DEMO_Bauvertrag.pdf)

**Demo-Schritt 6 — Kalender (1 Min.)**
- Tab 📅 Kalender
- Zeigen: 3 Farben (Info / Bauleiter-Termin / Polier-Termin)
- Termin eintragen → Konflikt-Erkennung erklären (Bauleiter kann nicht an zwei Stellen gleichzeitig sein)

---

### Teil 3: Rückblick / Lernreise (3–4 Min.)

"Was ich gelernt habe — und welche Probleme aufgetreten sind:"

1. **GitHub** — Versionskontrolle, strukturiertes Arbeiten mit KI als Co-Entwickler
2. **Google Gemini API** — kostenloses KI-Modell, Wechsel von 2.0-Flash auf 2.5-Flash (Quota-Problem gelöst)
3. **Supabase** — kostenlose Cloud-Datenbank, RLS-Konfiguration war die größte Hürde
4. **Streamlit** — aus Python-Code wird in Minuten eine Web-App mit mobilem Zugriff
5. **Problem:** KI-Modell-Name hat sich geändert → App war kaputt → git push → fix in 10 Min.
6. **Erkenntnis:** KI schreibt ~80% des Codes, aber man muss verstehen was dahintersteckt
7. **Was ich jetzt kann:** Ich kann eigenständig KI-gestützte Web-Apps bauen und deployen

---

### Teil 4: Ausblick (1 Min.)

"Nächster Schritt: Mengenermittlung aus Bauplänen.
Foto eines Rohrleitungsplans → KI erkennt Leitungsführung und Formstücke → automatische Bestellliste.
Das würde in der Arbeitsvorbereitung täglich Stunden sparen."

---

## Checkliste vor der Präsentation

- [ ] App auf Streamlit Cloud geöffnet (URL im Browser bereit)
- [ ] Streamlit Secrets: `GEMINI_API_KEY` korrekt eingetragen
- [ ] Demo-Projekt per "Demo-Projekt laden" vorgeladen
- [ ] Tab VOB: Mehrkostenanzeige einmal testweise generiert
- [ ] Backup: App auch lokal lauffähig auf http://localhost:8501
- [ ] Handy: gleiche Streamlit-URL getestet

---

## Demo-Dateien

- `demo/DEMO_Bauvertrag.pdf` — Testvertrag für Vertrag-Upload
- `demo/Briefkopf_Vorlage.docx` — Vorlage für Briefkopf-Demo

---

## Technische Daten

| Komponente | Eingesetzt | Kosten |
|---|---|---|
| UI | Streamlit | kostenlos |
| KI | Google Gemini 2.5 Flash | kostenlos (Free Tier) |
| Datenbank | SQLite (lokal) / Supabase (Cloud) | kostenlos |
| Wetter | Open-Meteo + Nominatim | kostenlos |
| Hosting | Streamlit Cloud | kostenlos |
| Dokumente | python-docx (Word-Export) | kostenlos |
</content>
