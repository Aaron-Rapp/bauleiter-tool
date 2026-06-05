-- ============================================================
-- Bauleiter-Tool — Supabase Schema (aktuell)
-- In Supabase → SQL Editor einfügen und ausführen
-- ============================================================

CREATE TABLE IF NOT EXISTS projekte (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    kostenstelle TEXT DEFAULT '',
    anschrift TEXT DEFAULT '',
    bauzeit_von DATE,
    bauzeit_bis DATE,
    foto_url TEXT DEFAULT '',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dateien (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    kategorie TEXT DEFAULT '',
    unterordner TEXT DEFAULT '',
    datei_name TEXT NOT NULL,
    datei_url TEXT NOT NULL,
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS todos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    titel TEXT NOT NULL,
    beschreibung TEXT DEFAULT '',
    erledigt BOOLEAN DEFAULT FALSE,
    phase TEXT DEFAULT 'Allgemein',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kalender (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    titel TEXT NOT NULL,
    datum DATE NOT NULL,
    datum_bis DATE,
    uhrzeit_von TEXT DEFAULT '',
    uhrzeit_bis TEXT DEFAULT '',
    kategorie TEXT DEFAULT 'blau',
    beschreibung TEXT DEFAULT '',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS schriftverkehr (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    projekt_id UUID REFERENCES projekte(id) ON DELETE CASCADE,
    typ TEXT NOT NULL,
    nummer INTEGER DEFAULT 1,
    titel TEXT DEFAULT '',
    inhalt TEXT DEFAULT '',
    meta TEXT DEFAULT '{}',
    erstellt_am TIMESTAMPTZ DEFAULT NOW()
);

-- RLS deaktivieren (für Demo/Präsentation)
ALTER TABLE projekte     DISABLE ROW LEVEL SECURITY;
ALTER TABLE dateien      DISABLE ROW LEVEL SECURITY;
ALTER TABLE todos        DISABLE ROW LEVEL SECURITY;
ALTER TABLE kalender     DISABLE ROW LEVEL SECURITY;
ALTER TABLE schriftverkehr DISABLE ROW LEVEL SECURITY;
