"""
Categorie Repository
Beheert alle database operaties voor afspraak categorien
"""

import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import DatabaseConnection
from src.models.categorie import Categorie

class CategorieRepository:
    """Repository voor categorie operaties"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self):
        """Haalt alle categorien op"""
        query = "SELECT * FROM afspraak_categorien ORDER BY naam ASC"
        results = self.db.execute_query(query)
        return [self._map_to_categorie(row) for row in results] if results else []
    
    def get_by_id(self, categorie_id):
        """Haalt categorie op via ID"""
        query = "SELECT * FROM afspraak_categorien WHERE id = %s"
        result = self.db.execute_query(query, (categorie_id,))
        
        if result:
            return self._map_to_categorie(result[0])
        return None
    
    def create(self, categorie: Categorie):
        """Voegt nieuwe categorie toe"""
        query = """
            INSERT INTO afspraak_categorien 
            (naam, kleur, beschrijving, custom_velden)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        custom_velden_json = json.dumps(categorie.custom_velden)
        params = (
            categorie.naam,
            categorie.kleur,
            categorie.beschrijving,
            custom_velden_json
        )
        
        result = self.db.execute_query(query, params)
        return result[0]['id'] if result else None
    
    def update(self, categorie: Categorie):
        """Werkt categorie bij"""
        query = """
            UPDATE afspraak_categorien 
            SET naam = %s, kleur = %s, beschrijving = %s, 
                custom_velden = %s, updated_at = NOW()
            WHERE id = %s
        """
        custom_velden_json = json.dumps(categorie.custom_velden)
        params = (
            categorie.naam,
            categorie.kleur,
            categorie.beschrijving,
            custom_velden_json,
            categorie.id
        )
        
        return self.db.execute_update(query, params)
    
    def delete(self, categorie_id):
        """Verwijdert categorie"""
        query = "DELETE FROM afspraak_categorien WHERE id = %s"
        return self.db.execute_update(query, (categorie_id,))
    
    def count(self):
        """Telt totaal categorien"""
        query = "SELECT COUNT(*) as total FROM afspraak_categorien"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def _map_to_categorie(row):
        """Converteer database rij naar Categorie object"""
        custom_velden = {}
        if row.get('custom_velden'):
            try:
                custom_velden = json.loads(row['custom_velden'])
            except:
                custom_velden = {}
        
        return Categorie(
            id=row['id'],
            naam=row['naam'],
            kleur=row['kleur'],
            beschrijving=row.get('beschrijving'),
            custom_velden=custom_velden,
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
