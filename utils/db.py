"""
Datenbankabstraktion: Supabase (primär) mit SQLite-Fallback (lokal).
Falls Supabase-RLS oder Netzwerkprobleme → SQLite wird automatisch genutzt.
"""
import sqlite3
import uuid
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# SQLite-Pfad: /tmp/ auf Cloud (beschreibbar), lokal im Projektordner
_LOKAL_PFAD = Path(__file__).parent.parent / "bauleiter_lokal.db"
_DB_PFAD = _LOKAL_PFAD if _LOKAL_PFAD.parent.exists() and not str(_LOKAL_PFAD).startswith("/mount") else Path("/tmp/bauleiter_lokal.db")


def _sqlite_conn():
    conn = sqlite3.connect(str(_DB_PFAD))
    conn.row_factory = sqlite3.Row
    return conn


def _init_sqlite():
    """Legt SQLite-Tabellen an falls nicht vorhanden."""
    conn = _sqlite_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS projekte (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            kostenstelle TEXT DEFAULT '',
            anschrift TEXT DEFAULT '',
            auftraggeber TEXT DEFAULT '',
            vertragsnummer TEXT DEFAULT '',
            bauzeit_von TEXT,
            bauzeit_bis TEXT,
            foto_url TEXT DEFAULT '',
            erstellt_am TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS dateien (
            id TEXT PRIMARY KEY,
            projekt_id TEXT,
            kategorie TEXT,
            unterordner TEXT DEFAULT '',
            datei_name TEXT,
            datei_url TEXT,
            erstellt_am TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS todos (
            id TEXT PRIMARY KEY,
            projekt_id TEXT,
            titel TEXT,
            beschreibung TEXT DEFAULT '',
            erledigt INTEGER DEFAULT 0,
            phase TEXT DEFAULT 'Allgemein',
            erstellt_am TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS schriftverkehr (
            id TEXT PRIMARY KEY,
            projekt_id TEXT,
            typ TEXT,
            nummer INTEGER,
            titel TEXT,
            inhalt TEXT,
            meta TEXT DEFAULT '{}',
            erstellt_am TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS kalender (
            id TEXT PRIMARY KEY,
            projekt_id TEXT,
            titel TEXT,
            datum TEXT,
            datum_bis TEXT DEFAULT '',
            uhrzeit_von TEXT DEFAULT '',
            uhrzeit_bis TEXT DEFAULT '',
            kategorie TEXT,
            beschreibung TEXT DEFAULT '',
            erstellt_am TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    # Migration: neue Spalten für bestehende DBs hinzufügen
    for sql in [
        "ALTER TABLE kalender  ADD COLUMN datum_bis     TEXT DEFAULT ''",
        "ALTER TABLE projekte  ADD COLUMN auftraggeber  TEXT DEFAULT ''",
        "ALTER TABLE projekte  ADD COLUMN vertragsnummer TEXT DEFAULT ''",
    ]:
        try:
            conn.execute(sql)
            conn.commit()
        except Exception:
            pass
    conn.close()


_init_sqlite()


class LokalerClient:
    """SQLite-basierter Client mit gleicher API wie Supabase-Client."""

    class _Tabelle:
        def __init__(self, name: str):
            self.name = name
            self._filter: List = []
            self._order_col: Optional[str] = None
            self._order_desc: bool = False
            self._limit_n: Optional[int] = None
            self._sel: str = "*"

        def select(self, cols: str = "*"):
            self._sel = cols
            return self

        def insert(self, data: Dict) -> "LokalerClient._Result":
            conn = _sqlite_conn()
            c = conn.cursor()
            data = dict(data)
            if "id" not in data:
                data["id"] = str(uuid.uuid4())
            if "erstellt_am" not in data:
                data["erstellt_am"] = datetime.datetime.now().isoformat()
            cols = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            c.execute(f"INSERT INTO {self.name} ({cols}) VALUES ({placeholders})", list(data.values()))
            conn.commit()
            # Zurückgeben
            c.execute(f"SELECT * FROM {self.name} WHERE id = ?", [data["id"]])
            row = c.fetchone()
            conn.close()
            return LokalerClient._Result([dict(row)] if row else [])

        def update(self, data: Dict) -> "LokalerClient._Filterable":
            self._update_data = data
            return self

        def delete(self) -> "LokalerClient._Filterable":
            self._is_delete = True
            return self

        def eq(self, col: str, val: Any):
            self._filter.append(("eq", col, val))
            return self

        def neq(self, col: str, val: Any):
            self._filter.append(("neq", col, val))
            return self

        def gte(self, col: str, val: Any):
            self._filter.append(("gte", col, val))
            return self

        def lte(self, col: str, val: Any):
            self._filter.append(("lte", col, val))
            return self

        def gt(self, col: str, val: Any):
            self._filter.append(("gt", col, val))
            return self

        def order(self, col: str, desc: bool = False):
            self._order_col = col
            self._order_desc = desc
            return self

        def limit(self, n: int):
            self._limit_n = n
            return self

        def _build_where(self):
            parts = []
            vals = []
            for op, col, val in self._filter:
                if op == "eq":
                    parts.append(f"{col} = ?")
                    vals.append(val)
                elif op == "neq":
                    parts.append(f"{col} != ?")
                    vals.append(val)
                elif op == "gte":
                    parts.append(f"{col} >= ?")
                    vals.append(val)
                elif op == "lte":
                    parts.append(f"{col} <= ?")
                    vals.append(val)
                elif op == "gt":
                    parts.append(f"{col} > ?")
                    vals.append(val)
            where = " WHERE " + " AND ".join(parts) if parts else ""
            return where, vals

        def execute(self) -> "LokalerClient._Result":
            conn = _sqlite_conn()
            c = conn.cursor()
            where, vals = self._build_where()

            # DELETE
            if hasattr(self, "_is_delete") and self._is_delete:
                c.execute(f"DELETE FROM {self.name}{where}", vals)
                # CASCADE für projekte: abhängige Tabellen mitlöschen
                if self.name == "projekte" and "projekt_id" not in str(where):
                    for dep in ["todos", "kalender", "dateien", "schriftverkehr"]:
                        c.execute(f"DELETE FROM {dep} WHERE projekt_id NOT IN (SELECT id FROM projekte)")
                conn.commit()
                conn.close()
                return LokalerClient._Result([])

            # UPDATE
            if hasattr(self, "_update_data"):
                data = self._update_data
                sets = ", ".join([f"{k} = ?" for k in data.keys()])
                c.execute(f"UPDATE {self.name} SET {sets}{where}", list(data.values()) + vals)
                conn.commit()
                conn.close()
                return LokalerClient._Result([])

            # SELECT
            order = ""
            if self._order_col:
                order = f" ORDER BY {self._order_col} {'DESC' if self._order_desc else 'ASC'}"
            limit = f" LIMIT {self._limit_n}" if self._limit_n else ""
            c.execute(f"SELECT * FROM {self.name}{where}{order}{limit}", vals)
            rows = [dict(r) for r in c.fetchall()]
            conn.close()
            return LokalerClient._Result(rows)

    class _Result:
        def __init__(self, data: List):
            self.data = data

        def execute(self):
            return self

    def table(self, name: str) -> "_Tabelle":
        t = LokalerClient._Tabelle(name)
        return t

    class _FakeStorage:
        class _Bucket:
            def upload(self, *args, **kwargs):
                pass
            def get_public_url(self, path: str) -> str:
                return ""
        def from_(self, bucket: str):
            return self._Bucket()

    @property
    def storage(self):
        return self._FakeStorage()


def get_db_client():
    """
    Gibt Supabase-Client zurück wenn verfügbar und funktionierend,
    sonst lokalen SQLite-Client.
    Prüft auch Schreibzugriff: RLS-gesperrte Supabase-Projekte fallen auf SQLite zurück.
    """
    try:
        from utils.supabase_client import get_client
        import uuid as _uuid
        db = get_client()
        # SELECT-Test
        db.table("projekte").select("id").limit(1).execute()
        # Schreibzugriff-Test: Mini-INSERT + DELETE mit ungültiger ID
        # Schlägt bei RLS-Sperre mit 42501 fehl → SQLite-Fallback
        _test_id = str(_uuid.uuid4())
        try:
            db.table("projekte").insert({"id": _test_id, "name": "__test__"}).execute()
            db.table("projekte").delete().eq("id", _test_id).execute()
        except Exception as _we:
            if "42501" in str(_we) or "row-level security" in str(_we).lower():
                return LokalerClient(), "lokal"
            # Andere Fehler (NOT NULL etc.) → Schreibzugriff ist da, Schema fehlt
        return db, "supabase"
    except Exception:
        return LokalerClient(), "lokal"
