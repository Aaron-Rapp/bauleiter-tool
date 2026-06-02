import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def frage_an_dokumente(frage: str, dokument_texte: list[str]) -> str:
    kontext = "\n\n---\n\n".join(dokument_texte)
    prompt = f"""Du bist ein Assistent für einen Bauleiter im deutschen Bauwesen.
Dir liegen folgende Dokumente vor (Verträge, Leistungsverzeichnisse, etc.):

{kontext}

Beantworte die folgende Frage ausschließlich auf Basis dieser Dokumente.
Antworte klar mit JA oder NEIN am Anfang, dann erkläre kurz die relevante Vertragsstelle.
Falls die Frage nicht aus den Dokumenten beantwortet werden kann, sage das deutlich.

Frage: {frage}"""

    response = model.generate_content(prompt)
    return response.text


def beschreibe_foto_fuer_nachtrag(bild_bytes: bytes, beschreibung: str) -> dict:
    import PIL.Image
    import io

    bild = PIL.Image.open(io.BytesIO(bild_bytes))

    prompt = f"""Du bist ein Bauleiter-Assistent im deutschen Bauwesen (VOB).
Ein Bauleiter hat folgendes Foto gemacht mit dieser Beschreibung: "{beschreibung}"

Erstelle auf Basis des Fotos und der Beschreibung eine strukturierte Mehrkostenanzeige mit:
1. Kurzbeschreibung der Situation
2. Betroffene Leistungsposition (geschätzt)
3. Begründung warum es sich um eine Nachtragsleistung handelt
4. Geschätzte Mehrkostensumme (Bandbreite angeben)
5. Empfohlene nächste Schritte

Antworte auf Deutsch, professionell und knapp."""

    response = model.generate_content([prompt, bild])
    return {"nachtrag_text": response.text}
