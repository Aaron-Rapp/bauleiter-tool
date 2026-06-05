-- ============================================================
-- Bauleiter-Tool v2 — Supabase Schema
-- In Supabase → SQL Editor einfügen und ausführen
-- ============================================================

-- Alte Tabellen löschen
DROP TABLE IF EXISTS kalender CASCADE;
DROP TABLE IF EXISTS todos CASCADE;
DROP TABLE IF EXISTS dateien CASCADE;
DROP TABLE IF EXISTS projekte CASCADE;
DROP TABLE IF EXISTS einstellungen CASCADE;
DROP TABLE IF EXISTS aufgaben CASCADE;
DROP TABLE IF EXISTS baustellen CASCADE;
DROP TABLE IF EXISTS dokumente CASCADE;
DROP TABLE IF EXISTS nachtraege CASCADE;

-- ============================================================
-- Tabellen anlegen
-- ============================================================

CREATE TABLE projekte (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    kostenstelle TEXT DEFAULT '',
    anschrift TEXT DEFAULT '',
    bauzeit_von DATE,
    bauzeit_bis DATE,
    foto_url TEXT DEFAULT '',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE dateien (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    kategorie TEXT NOT NULL CHECK (kategorie IN ('Bilder', 'Plaene', 'Vertraege')),
    unterordner TEXT DEFAULT '',
    datei_name TEXT NOT NULL,
    datei_url TEXT NOT NULL,
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE todos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    titel TEXT NOT NULL,
    beschreibung TEXT DEFAULT '',
    erledigt BOOLEAN DEFAULT FALSE,
    phase TEXT DEFAULT 'Allgemein',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE kalender (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    titel TEXT NOT NULL,
    datum DATE NOT NULL,
    uhrzeit_von TEXT DEFAULT '',
    uhrzeit_bis TEXT DEFAULT '',
    kategorie TEXT NOT NULL CHECK (kategorie IN ('gruen', 'blau', 'orange')),
    beschreibung TEXT DEFAULT '',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Row Level Security deaktivieren + Policies anlegen
-- (doppelte Absicherung damit es in jedem Fall funktioniert)
-- ============================================================

ALTER TABLE projekte DISABLE ROW LEVEL SECURITY;
ALTER TABLE dateien  DISABLE ROW LEVEL SECURITY;
ALTER TABLE todos    DISABLE ROW LEVEL SECURITY;
ALTER TABLE kalender DISABLE ROW LEVEL SECURITY;

-- Erlaubnis für alle Operationen (Fallback falls RLS aktiv bleibt)
DROP POLICY IF EXISTS "allow_all" ON projekte;
DROP POLICY IF EXISTS "allow_all" ON dateien;
DROP POLICY IF EXISTS "allow_all" ON todos;
DROP POLICY IF EXISTS "allow_all" ON kalender;

CREATE POLICY "allow_all" ON projekte FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON dateien  FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON todos    FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON kalender FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- ============================================================
-- Storage Bucket
-- Manuell anlegen: Storage → New Bucket → "bauleiter-dateien" → Public: AN
-- ============================================================
