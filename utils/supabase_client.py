from supabase import create_client, Client
from utils.config import get_config

from typing import Optional
_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = get_config("SUPABASE_URL")
        key = get_config("SUPABASE_KEY")
        if not url or not key or "hier" in url:
            raise ValueError(
                "Supabase nicht konfiguriert. "
                "Bitte SUPABASE_URL und SUPABASE_KEY in die .env-Datei eintragen."
            )
        _client = create_client(url, key)
    return _client
