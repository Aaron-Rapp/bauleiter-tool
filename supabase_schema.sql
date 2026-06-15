-- ============================================================
-- Bauleiter-Tool — Supabase Schema (aktuell)
-- In Supabase → SQL Editor einfügen und ausführen
-- ============================================================

CREATE TABLE IF NOT EXISTS projekte (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    kostenstelle TEXT DEFAULT '',
    anschrift TEXT DEFAULT '',
    auftraggeber TEXT DEFAULT '',
    vertragsnummer TEXT DEFAULT '',
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
    erstellt_am TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT dateien_kategorie_check CHECK (kategorie IN ('Bilder', 'Plaene', 'Vertraege', 'Briefkopf', ''))
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

-- Kategorie-Constraint aktualisieren (Briefkopf + Vertraege ergänzen)
ALTER TABLE dateien DROP CONSTRAINT IF EXISTS dateien_kategorie_check;
ALTER TABLE dateien ADD CONSTRAINT dateien_kategorie_check
  CHECK (kategorie IN ('Bilder', 'Plaene', 'Vertraege', 'Briefkopf', ''));

-- Migration: auftraggeber + vertragsnummer für bestehende Supabase-Datenbanken
ALTER TABLE projekte ADD COLUMN IF NOT EXISTS auftraggeber TEXT DEFAULT '';
ALTER TABLE projekte ADD COLUMN IF NOT EXISTS vertragsnummer TEXT DEFAULT '';
