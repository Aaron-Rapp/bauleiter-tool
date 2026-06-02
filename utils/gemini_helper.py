import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY", "")
if _api_key and "hier" not in _api_key:
    genai.configure(api_key=_api_key)

MODEL = "gemini-2.0-flash"


def _get_model():
    key = os.getenv("GEMINI_API_KEY", "")
    if not key or "hier" in key:
        raise ValueError("Gemini API Key nicht konfiguriert. Bitte GEMINI_API_KEY in .env eintragen.")
    genai.configure(api_key=key)
    return genai.GenerativeModel(MODEL)


def frage_an_dokumente(frage: str, dokument_texte: list) -> str:
    model = _get_model()
    kontext = "\n\n---DOKUMENT-TRENNER---\n\n".join(dokument_texte)

    # Kontext auf max. 800.000 Zeichen begrenzen (Gemini 2.0 Flash: 1M Token Context)
    if len(kontext) > 800000:
        kontext = kontext[:800000] + "\n\n[Dokument wurde aus Platzgründen gekürzt]"

    prompt = f"""Du bist ein erfahrener Assistent für einen deutschen Bauleiter (VOB-Kenntnisse).
Dir liegen folgende Vertragsunterlagen vor:

{kontext}

Beantworte die folgende Frage ausschließlich auf Basis dieser Dokumente.

WICHTIG: Beginne deine Antwort immer mit "JA" oder "NEIN" (Großbuchstaben).
Danach: kurze Erklärung (max. 3 Sätze) mit direktem Zitat aus dem Vertrag wenn möglich.
Falls die Frage nicht aus den Dokumenten beantwortet werden kann, antworte mit:
"UNKLAR – Diese Frage kann aus den vorliegenden Dokumenten nicht eindeutig beantwortet werden."

Frage: {frage}"""

    response = model.generate_content(prompt)
    return response.text


def beschreibe_foto_fuer_nachtrag(bild_bytes: bytes, beschreibung: str) -> dict:
    import PIL.Image
    import io

    model = _get_model()
    bild = PIL.Image.open(io.BytesIO(bild_bytes))

    prompt = f"""Du bist ein erfahrener Bauleiter-Assistent im deutschen Bauwesen (VOB/B §2).
Der Bauleiter hat folgende Situation dokumentiert: "{beschreibung}"

Erstelle auf Basis des Fotos und der Beschreibung eine professionelle Mehrkostenanzeige mit diesen Abschnitten:

**1. Sachverhalt**
(Was ist passiert? Kurze, faktische Beschreibung)

**2. Nachtragsbegründung (§2 VOB/B)**
(Warum handelt es sich um eine zusätzliche/geänderte Leistung, die nicht im Vertrag enthalten ist?)

**3. Betroffene Leistungsposition**
(Geschätzte LV-Position oder Beschreibung)

**4. Geschätzte Mehrkosten**
(Bandbreite in Euro, mit kurzer Begründung)

**5. Empfohlene nächste Schritte**
- Sofortmaßnahme
- Schriftliche Ankündigung an AG
- Dokumentation

Antworte auf Deutsch, professionell und sachlich."""

    response = model.generate_content([prompt, bild])
    return {"nachtrag_text": response.text}
