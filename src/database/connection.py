"""
Database Connection Manager
Beheert verbinding met PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os

# Voeg root directory toe aan path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import DB_CONFIG

class DatabaseConnection:
    """Beheert database verbindingen"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Verbind met database"""
        try:
            self._connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            # Enable autocommit voor betere connection handling
            self._connection.autocommit = False
            print("✅ Database verbonden!")
            return True
        except psycopg2.OperationalError as e:
            print(f"❌ Database verbindingsfout: {e}")
            return False
    
    def get_connection(self):
        """Geeft huidige verbinding"""
        if self._connection is None:
            self.connect()
        return self._connection
    
    def execute_query(self, query, params=None):
        """Voert SELECT query uit en geeft resultaten"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.commit()  # Commit ook voor queries (IMPORTANT!)
            return results
        except Exception as e:
            self.get_connection().rollback()
            print(f"❌ Query fout: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def execute_update(self, query, params=None):
        """Voert INSERT/UPDATE/DELETE uit"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows_affected = cursor.rowcount
            conn.commit()
            print(f"✅ {rows_affected} rij(en) gewijzigd")
            return True
        except Exception as e:
            conn = self.get_connection()
            conn.rollback()
            print(f"❌ Update fout: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Sluit database verbinding"""
        if self._connection:
            try:
                self._connection.close()
                print("✅ Database verbinding gesloten")
            except Exception as e:
                print(f"❌ Fout bij sluiten verbinding: {e}")
