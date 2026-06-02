-- BAULEITER-TOOL: Supabase Datenbankschema
-- Diesen gesamten Text in Supabase → SQL Editor kopieren und ausführen

-- Tabelle: Baustellen
CREATE TABLE IF NOT EXISTS baustellen (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    auftraggeber TEXT NOT NULL,
    ort TEXT,
    auftragssumme NUMERIC(12, 2) DEFAULT 0,
    baubeginn DATE,
    status TEXT DEFAULT 'Arbeitsvorbereitung'
        CHECK (status IN ('Arbeitsvorbereitung', 'Bauausführung', 'Fertiggestellt')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabelle: Dokumente (Verträge, LV, Pläne)
CREATE TABLE IF NOT EXISTS dokumente (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    baustelle_id UUID REFERENCES baustellen(id) ON DELETE CASCADE,
    dateiname TEXT NOT NULL,
    text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabelle: Aufgaben (Checkliste)
CREATE TABLE IF NOT EXISTS aufgaben (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    baustelle_id UUID REFERENCES baustellen(id) ON DELETE CASCADE,
    phase TEXT NOT NULL
        CHECK (phase IN ('Arbeitsvorbereitung', 'Bauausführung', 'Fertiggestellt')),
    titel TEXT NOT NULL,
    erledigt BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabelle: Nachträge
CREATE TABLE IF NOT EXISTS nachtraege (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    baustelle_id UUID REFERENCES baustellen(id) ON DELETE CASCADE,
    datum DATE,
    beschreibung TEXT,
    ki_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security deaktivieren (für einfachen Demo-Betrieb)
ALTER TABLE baustellen DISABLE ROW LEVEL SECURITY;
ALTER TABLE dokumente DISABLE ROW LEVEL SECURITY;
ALTER TABLE aufgaben DISABLE ROW LEVEL SECURITY;
ALTER TABLE nachtraege DISABLE ROW LEVEL SECURITY;
