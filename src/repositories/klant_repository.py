"""
Klant Repository
Beheert alle database operaties voor klanten
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import DatabaseConnection
from src.models.klant import Klant

class KlantRepository:
    """Repository voor klant operaties"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self, actief_only=True):
        """Haalt alle klanten op"""
        query = "SELECT * FROM klanten"
        if actief_only:
            query += " WHERE actief = TRUE"
        query += " ORDER BY naam ASC"
        
        results = self.db.execute_query(query)
        return [self._map_to_klant(row) for row in results] if results else []
    
    def get_by_id(self, klant_id):
        """Haalt klant op via ID"""
        query = "SELECT * FROM klanten WHERE id = %s"
        result = self.db.execute_query(query, (klant_id,))
        
        if result:
            return self._map_to_klant(result[0])
        return None
    
    def search(self, search_term):
        """Zoekt klanten op naam, email of klantnummer"""
        search_term = f"%{search_term}%"
        query = """
            SELECT * FROM klanten 
            WHERE naam ILIKE %s 
               OR email ILIKE %s 
               OR klantnummer ILIKE %s
               OR postcode ILIKE %s
            ORDER BY naam ASC
            LIMIT 100
        """
        results = self.db.execute_query(query, (search_term, search_term, search_term, search_term))
        return [self._map_to_klant(row) for row in results] if results else []
    
    def create(self, klant: Klant):
        """Voegt nieuwe klant toe"""
        query = """
            INSERT INTO klanten 
            (klantnummer, naam, contactpersoon, telefoon, gsm, email, straat, huisnummer, postcode, gemeente, opmerkingen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        params = (
            klant.klantnummer,
            klant.naam,
            klant.contactpersoon,
            klant.telefoon,
            klant.gsm,
            klant.email,
            klant.straat,
            klant.huisnummer,
            klant.postcode,
            klant.gemeente,
            klant.opmerkingen
        )
        
        result = self.db.execute_query(query, params)
        return result[0]['id'] if result else None
    
    def update(self, klant: Klant):
        """Werkt klant bij"""
        query = """
            UPDATE klanten 
            SET naam = %s, contactpersoon = %s, telefoon = %s, gsm = %s, 
                email = %s, straat = %s, huisnummer = %s, postcode = %s, 
                gemeente = %s, actief = %s, opmerkingen = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (
            klant.naam,
            klant.contactpersoon,
            klant.telefoon,
            klant.gsm,
            klant.email,
            klant.straat,
            klant.huisnummer,
            klant.postcode,
            klant.gemeente,
            klant.actief,
            klant.opmerkingen,
            klant.id
        )
        
        return self.db.execute_update(query, params)
    
    def delete(self, klant_id):
        """Verwijdert klant (soft delete - zet op inactief)"""
        query = "UPDATE klanten SET actief = FALSE, updated_at = NOW() WHERE id = %s"
        return self.db.execute_update(query, (klant_id,))
    
    def count(self):
        """Telt totaal actieve klanten"""
        query = "SELECT COUNT(*) as total FROM klanten WHERE actief = TRUE"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def _map_to_klant(row):
        """Converteer database rij naar Klant object"""
        return Klant(
            id=row['id'],
            klantnummer=row['klantnummer'],
            naam=row['naam'],
            contactpersoon=row.get('contactpersoon'),
            telefoon=row.get('telefoon'),
            gsm=row.get('gsm'),
            email=row.get('email'),
            straat=row.get('straat'),
            huisnummer=row.get('huisnummer'),
            postcode=row.get('postcode'),
            gemeente=row.get('gemeente'),
            actief=row['actief'],
            opmerkingen=row.get('opmerkingen'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )