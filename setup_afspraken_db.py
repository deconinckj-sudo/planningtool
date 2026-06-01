"""
Setup script voor afspraken database
Creert tabellen voor afspraken en categorien
"""

import psycopg2
import sys
from config import DB_CONFIG

def setup_afspraken_db():
    """Maak afspraken database tabellen"""
    
    try:
        # Verbind met database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        print("📅 Afspraken database setup...")
        
        # Tabel: afspraak_categorien
        print("  ✓ Creating afspraak_categorien table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS afspraak_categorien (
                id SERIAL PRIMARY KEY,
                naam VARCHAR(100) NOT NULL UNIQUE,
                kleur VARCHAR(7) DEFAULT '#3498db',
                beschrijving TEXT,
                custom_velden JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel: afspraken
        print("  ✓ Creating afspraken table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS afspraken (
                id SERIAL PRIMARY KEY,
                klant_id INTEGER NOT NULL,
                categorie_id INTEGER NOT NULL,
                datum DATE NOT NULL,
                tijd TIME,
                opmerkingen TEXT,
                custom_data JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (klant_id) REFERENCES klanten(id) ON DELETE CASCADE,
                FOREIGN KEY (categorie_id) REFERENCES afspraak_categorien(id) ON DELETE RESTRICT,
                UNIQUE(klant_id, categorie_id, datum, tijd)
            )
        """)
        
        # Indexes voor sneller zoeken
        print("  ✓ Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_afspraken_klant_id ON afspraken(klant_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_afspraken_categorie_id ON afspraken(categorie_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_afspraken_datum ON afspraken(datum)")
        
        # Standaard categorien toevoegen
        print("  ✓ Adding default categories...")
        cursor.execute("SELECT COUNT(*) FROM afspraak_categorien")
        if cursor.fetchone()[0] == 0:
            categories = [
                ('Reparatie', '#e74c3c', 'Machine reparatie in garage'),
                ('Afhalen', '#3498db', 'Machine afhalen bij klant'),
                ('Retour', '#2ecc71', 'Machine retourneren naar klant'),
                ('Inspectie', '#f39c12', 'Machine inspectie/onderhoud'),
                ('Afspraak', '#9b59b6', 'Algemene afspraak/meeting'),
            ]
            
            for naam, kleur, beschrijving in categories:
                cursor.execute(
                    """INSERT INTO afspraak_categorien (naam, kleur, beschrijving) 
                       VALUES (%s, %s, %s) ON CONFLICT (naam) DO NOTHING""",
                    (naam, kleur, beschrijving)
                )
                print(f"    • {naam} ({kleur})")
        
        conn.commit()
        print("\n✅ Afspraken database setup compleet!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"\n❌ Database fout: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_afspraken_db()
