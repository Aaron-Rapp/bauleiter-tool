from google import genai
from utils.config import get_config

MODEL = "gemini-2.5-flash"


def _get_client():
    key = get_config("GEMINI_API_KEY")
    if not key or "hier" in key:
        raise ValueError(
            "Gemini API Key nicht konfiguriert. "
            "Bitte GEMINI_API_KEY in die .env-Datei eintragen."
        )
    return genai.Client(api_key=key)


def frage_an_dokumente(frage: str, dokument_texte: list) -> str:
    client = _get_client()
    kontext = "\n\n---DOKUMENT-TRENNER---\n\n".join(dokument_texte)
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

    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text
