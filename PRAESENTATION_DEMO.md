# Präsentation 18.06.2026 — Demo-Skript

## Aufbau der Präsentation (ca. 15–20 Min.)

### Teil 1: Problem (2 Min.)
"Als Bauleiter hat man täglich das Problem: Man steht auf der Baustelle,
der AG sagt er schuldet eine Leistung nicht — und man hat den Vertrag nicht dabei.
Oder man vergisst beim Baustart die Beweissicherung.
Diese App löst genau das."

---

### Teil 2: Live-Demo (10–12 Min.)

**Demo-Schritt 1 — Baustelle anlegen (1 Min.)**
- Seite "Baustellen" öffnen
- Neue Baustelle anlegen: z.B. "Kanalbau Hauptstraße", Auftraggeber: "Stadt Konstanz"
- Status zeigen: 🟡 Arbeitsvorbereitung

**Demo-Schritt 2 — Aufgaben-Checkliste (2 Min.)**
- Seite "Aufgaben" öffnen
- Zeigen: 3 Phasen, Fortschrittsbalken
- Zwei Aufgaben abhaken: "Leitungsauskunft einholen" + "Beweissicherung"
- "Schaut her — die App erinnert mich an alles, was ich beim Baustart erledigen muss"

**Demo-Schritt 3 — Vertrag hochladen + KI-Chat (5 Min.)**
- Seite "Dokumente" öffnen
- Vertrag hochladen (vorher bereitliegen haben als PDF!)
- Frage stellen: **"Schulde ich das Baumfällen?"**
  → KI antwortet: NEIN / JA + Vertragsstelle
- Zweite Frage: **"Wer ist für die Verkehrssicherung zuständig?"**
- "Das hätte mir früher auf der Baustelle 20 Minuten Suchen gespart"

**Demo-Schritt 4 — Nachtrag-Generator (3 Min.)**
- Seite "Nachtrag-Generator" öffnen
- Foto hochladen (vorher ein Bild bereithalten — z.B. Baustellen-Foto)
- Beschreibung eingeben: "Gasleitung liegt 50 cm tiefer als im Plan eingezeichnet"
- KI-Analyse starten
- Ergebnis zeigen: Sachverhalt, §2 VOB/B Begründung, Kostenschätzung
- Download-Button klicken → Word-Datei

---

### Teil 3: Rückblick / Lernreise (3–4 Min.)
"Was ich gelernt habe und welche Probleme aufgetreten sind:"

1. **GitHub** — Code-Verwaltung, Versionierung, Zusammenarbeit mit KI
2. **Gemini API** (Google) — kostenloses KI-Modell, kann PDFs verstehen
3. **Supabase** — kostenlose Datenbank in der Cloud, PC + Handy synchron
4. **Streamlit** — aus Python-Code wird in Minuten eine Web-App
5. **Problem 1:** Gemini-Modellname hat sich geändert (gemini-pro → gemini-2.0-flash)
6. **Problem 2:** API-Key versehentlich im Chat geteilt → sofort neu erstellt (Lektion: .env-Datei!)
7. **Was ich jetzt kann:** Ich kann eigenständig KI-Tools kombinieren und Apps bauen

---

### Teil 4: Ausblick (1 Min.)
"Nächster Schritt wäre Idee 2: Mengenermittlung aus Plänen.
Foto von einem Rohrleitungsplan → KI erkennt Längen und Formstücke → automatische Bestellliste."

---

## Checkliste vor der Präsentation

- [ ] App auf Streamlit Cloud deployed (URL bereit)
- [ ] Test-Vertrag als PDF vorbereitet (echter Bauvertrag oder Demo-Vertrag)
- [ ] Test-Foto von Baustelle bereit (für Nachtrag-Demo)
- [ ] App auf dem Handy getestet (gleiche URL)
- [ ] Backup: App auch lokal lauffähig
- [ ] Slides mit Projektübersicht (optional)

---

## Demo-Vertrag vorbereiten
Für die KI-Chat-Demo brauchst du eine PDF-Datei mit einem Bauvertrag.
Empfehlung: Einen echten VOB/B-Werkvertrag nehmen (aus deiner Bauleiter-Zeit) 
oder einen anonymisierten Beispielvertrag erstellen.
Wichtig: Der Vertrag sollte klare Leistungsbeschreibungen enthalten (z.B. Baumfällen: NEIN / Verkehrssicherung: AN).
