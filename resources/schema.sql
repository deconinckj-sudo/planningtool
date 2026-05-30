-- ============================================
-- THIRY PLANNING - DATABASE SCHEMA
-- Klanten en Afspraken Management
-- ============================================

-- Bedrijfsinstellingen
CREATE TABLE IF NOT EXISTS bedrijfsinstellingen (
    id SERIAL PRIMARY KEY,
    bedrijfsnaam VARCHAR(255) NOT NULL,
    telefoon VARCHAR(50),
    email VARCHAR(255),
    btw_nummer VARCHAR(50),
    logo_pad TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Klanten (max 1100+)
CREATE TABLE IF NOT EXISTS klanten (
    id SERIAL PRIMARY KEY,
    klantnummer VARCHAR(50) UNIQUE NOT NULL,
    naam VARCHAR(255) NOT NULL,
    contactpersoon VARCHAR(255),
    telefoon VARCHAR(50),
    gsm VARCHAR(50),
    email VARCHAR(255),
    straat VARCHAR(255),
    huisnummer VARCHAR(10),
    postcode VARCHAR(20),
    gemeente VARCHAR(255),
    actief BOOLEAN DEFAULT TRUE,
    opmerkingen TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categorieën (soorten afspraken: Onderhoud, Reparatie, etc.)
CREATE TABLE IF NOT EXISTS categorieen (
    id SERIAL PRIMARY KEY,
    naam VARCHAR(255) NOT NULL,
    kleur VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Afspraken (geplande bezoeken)
CREATE TABLE IF NOT EXISTS afspraken (
    id SERIAL PRIMARY KEY,
    klant_id INTEGER NOT NULL REFERENCES klanten(id) ON DELETE CASCADE,
    categorie_id INTEGER REFERENCES categorieen(id) ON DELETE SET NULL,
    titel VARCHAR(255) NOT NULL,
    omschrijving TEXT,
    start_datetime TIMESTAMP NOT NULL,
    eind_datetime TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'geplanned', -- geplanned, in_uitvoering, afgerond, geannuleerd
    locatie VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexen voor snelle zoekopdrachten (belangrijk met 1100 klanten!)
CREATE INDEX IF NOT EXISTS idx_klanten_naam ON klanten(naam);
CREATE INDEX IF NOT EXISTS idx_klanten_klantnummer ON klanten(klantnummer);
CREATE INDEX IF NOT EXISTS idx_klanten_actief ON klanten(actief);
CREATE INDEX IF NOT EXISTS idx_afspraken_klant ON afspraken(klant_id);
CREATE INDEX IF NOT EXISTS idx_afspraken_start ON afspraken(start_datetime);
CREATE INDEX IF NOT EXISTS idx_afspraken_status ON afspraken(status);

-- Insert bedrijfsgegevens
INSERT INTO bedrijfsinstellingen (bedrijfsnaam, telefoon, email) 
VALUES ('Thiry Planning', '', '')
ON CONFLICT DO NOTHING;

-- Insert standaard categorieën
INSERT INTO categorieen (naam, kleur) VALUES
('Onderhoud', '#4CAF50'),
('Reparatie', '#FF9800'),
('Inspectie', '#2196F3'),
('Installatie', '#9C27B0'),
('Overig', '#757575')
ON CONFLICT DO NOTHING;