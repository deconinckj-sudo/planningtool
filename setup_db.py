"""
Setup script - voer dit EENMALIG uit!
Maakt database aan en laadt schema
"""

import psycopg2
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import DB_CONFIG

def setup_database():
    """Maakt database aan en laadt schema"""
    
    print("🔧 Database Setup Started...\n")
    
    # Verbind eerst met postgres (standaard database)
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Controleer of database al bestaat
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"✅ Database '{DB_CONFIG['database']}' wordt aangemaakt...")
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' succesvol aangemaakt!\n")
        else:
            print(f"✅ Database '{DB_CONFIG['database']}' bestaat al\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Fout bij database aanmaak: {e}")
        return False
    
    # Nu verbind met de nieuwe database en laad het schema
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Lees schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), 'resources', 'schema.sql')
        
        if not os.path.exists(schema_path):
            print(f"❌ Schema bestand niet gevonden: {schema_path}")
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Voer schema uit
        print("📦 Database schema wordt geladen...")
        cursor.execute(schema_sql)
        conn.commit()
        print("✅ Database schema succesvol geladen!\n")
        
        cursor.close()
        conn.close()
        
        print("✅ DATABASE SETUP VOLTOOID!\n")
        print("📝 Database gegevens:")
        print(f"  Host: {DB_CONFIG['host']}")
        print(f"  Port: {DB_CONFIG['port']}")
        print(f"  Database: {DB_CONFIG['database']}")
        print(f"  User: {DB_CONFIG['user']}")
        print("\n🚀 Je bent klaar om de applicatie te starten!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij schema laden: {e}")
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)