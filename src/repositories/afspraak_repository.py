"""
Afspraak Repository
Beheert alle database operaties voor afspraken
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import DatabaseConnection
from src.models.afspraak import Afspraak

class AfspraakRepository:
    """Repository voor afspraak operaties"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self):
        """Haalt alle afspraken op"""
        query = """
            SELECT 
                a.id, a.klant_id, k.naam as klant_naam,
                a.categorie_id, c.naam as categorie_naam,
                a.titel, a.omschrijving, a.start_datetime, a.eind_datetime,
                a.status, a.locatie, a.created_at, a.updated_at
            FROM afspraken a
            JOIN klanten k ON a.klant_id = k.id
            LEFT JOIN categorieen c ON a.categorie_id = c.id
            ORDER BY a.start_datetime DESC
        """
        results = self.db.execute_query(query)
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def get_by_id(self, afspraak_id):
        """Haalt afspraak op via ID"""
        query = """
            SELECT 
                a.id, a.klant_id, k.naam as klant_naam,
                a.categorie_id, c.naam as categorie_naam,
                a.titel, a.omschrijving, a.start_datetime, a.eind_datetime,
                a.status, a.locatie, a.created_at, a.updated_at
            FROM afspraken a
            JOIN klanten k ON a.klant_id = k.id
            LEFT JOIN categorieen c ON a.categorie_id = c.id
            WHERE a.id = %s
        """
        result = self.db.execute_query(query, (afspraak_id,))
        
        if result:
            return self._map_to_afspraak(result[0])
        return None
    
    def get_by_klant(self, klant_id):
        """Haalt alle afspraken voor klant op"""
        query = """
            SELECT 
                a.id, a.klant_id, k.naam as klant_naam,
                a.categorie_id, c.naam as categorie_naam,
                a.titel, a.omschrijving, a.start_datetime, a.eind_datetime,
                a.status, a.locatie, a.created_at, a.updated_at
            FROM afspraken a
            JOIN klanten k ON a.klant_id = k.id
            LEFT JOIN categorieen c ON a.categorie_id = c.id
            WHERE a.klant_id = %s
            ORDER BY a.start_datetime DESC
        """
        results = self.db.execute_query(query, (klant_id,))
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def get_by_date_range(self, start_date, end_date):
        """Haalt afspraken op in bepaalde periode"""
        query = """
            SELECT 
                a.id, a.klant_id, k.naam as klant_naam,
                a.categorie_id, c.naam as categorie_naam,
                a.titel, a.omschrijving, a.start_datetime, a.eind_datetime,
                a.status, a.locatie, a.created_at, a.updated_at
            FROM afspraken a
            JOIN klanten k ON a.klant_id = k.id
            LEFT JOIN categorieen c ON a.categorie_id = c.id
            WHERE a.start_datetime >= %s AND a.start_datetime < %s
            ORDER BY a.start_datetime ASC
        """
        results = self.db.execute_query(query, (start_date, end_date))
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def create(self, afspraak: Afspraak):
        """Voegt nieuwe afspraak toe"""
        query = """
            INSERT INTO afspraken 
            (klant_id, categorie_id, titel, omschrijving, start_datetime, eind_datetime, status, locatie)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        params = (
            afspraak.klant_id,
            afspraak.categorie_id,
            afspraak.titel,
            afspraak.omschrijving,
            afspraak.start_datetime,
            afspraak.eind_datetime,
            afspraak.status,
            afspraak.locatie
        )
        
        result = self.db.execute_query(query, params)
        return result[0]['id'] if result else None
    
    def update(self, afspraak: Afspraak):
        """Werkt afspraak bij"""
        query = """
            UPDATE afspraken 
            SET klant_id = %s, categorie_id = %s, titel = %s, omschrijving = %s,
                start_datetime = %s, eind_datetime = %s, status = %s, 
                locatie = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (
            afspraak.klant_id,
            afspraak.categorie_id,
            afspraak.titel,
            afspraak.omschrijving,
            afspraak.start_datetime,
            afspraak.eind_datetime,
            afspraak.status,
            afspraak.locatie,
            afspraak.id
        )
        
        return self.db.execute_update(query, params)
    
    def delete(self, afspraak_id):
        """Verwijdert afspraak"""
        query = "DELETE FROM afspraken WHERE id = %s"
        return self.db.execute_update(query, (afspraak_id,))
    
    def update_status(self, afspraak_id, status):
        """Wijzigt status van afspraak"""
        query = "UPDATE afspraken SET status = %s, updated_at = NOW() WHERE id = %s"
        return self.db.execute_update(query, (status, afspraak_id))
    
    @staticmethod
    def _map_to_afspraak(row):
        """Converteer database rij naar Afspraak object"""
        return Afspraak(
            id=row['id'],
            klant_id=row['klant_id'],
            klant_naam=row.get('klant_naam', ''),
            categorie_id=row.get('categorie_id'),
            categorie_naam=row.get('categorie_naam', ''),
            titel=row['titel'],
            omschrijving=row.get('omschrijving'),
            start_datetime=row['start_datetime'],
            eind_datetime=row['eind_datetime'],
            status=row['status'],
            locatie=row.get('locatie'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )