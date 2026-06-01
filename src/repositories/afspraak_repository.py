"""
Afspraak Repository
Beheert alle database operaties voor afspraken
"""

import sys
import os
from datetime import datetime, date, time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import DatabaseConnection
from src.models.afspraak import Afspraak

class AfspraakRepository:
    """Repository voor afspraak operaties"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self):
        """Haalt alle afspraken op"""
        query = "SELECT * FROM afspraken ORDER BY datum DESC, tijd DESC"
        results = self.db.execute_query(query)
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def get_by_id(self, afspraak_id):
        """Haalt afspraak op via ID"""
        query = "SELECT * FROM afspraken WHERE id = %s"
        result = self.db.execute_query(query, (afspraak_id,))
        
        if result:
            return self._map_to_afspraak(result[0])
        return None
    
    def get_by_klant_id(self, klant_id):
        """Haalt alle afspraken voor een klant op"""
        query = "SELECT * FROM afspraken WHERE klant_id = %s ORDER BY datum DESC, tijd DESC"
        results = self.db.execute_query(query, (klant_id,))
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def get_by_datum(self, datum):
        """Haalt alle afspraken voor een specifieke datum op"""
        query = "SELECT * FROM afspraken WHERE datum = %s ORDER BY tijd ASC"
        results = self.db.execute_query(query, (datum,))
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def get_by_datum_range(self, start_datum, eind_datum):
        """Haalt afspraken op tussen twee datums"""
        query = "SELECT * FROM afspraken WHERE datum >= %s AND datum <= %s ORDER BY datum ASC, tijd ASC"
        results = self.db.execute_query(query, (start_datum, eind_datum))
        return [self._map_to_afspraak(row) for row in results] if results else []
    
    def create(self, afspraak: Afspraak):
        """Voegt nieuwe afspraak toe"""
        query = """
            INSERT INTO afspraken 
            (klant_id, categorie_id, datum, tijd, opmerkingen, custom_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        custom_data_json = json.dumps(afspraak.custom_data)
        params = (
            afspraak.klant_id,
            afspraak.categorie_id,
            afspraak.datum,
            afspraak.tijd,
            afspraak.opmerkingen,
            custom_data_json
        )
        
        result = self.db.execute_query(query, params)
        return result[0]['id'] if result else None
    
    def update(self, afspraak: Afspraak):
        """Werkt afspraak bij"""
        query = """
            UPDATE afspraken 
            SET klant_id = %s, categorie_id = %s, datum = %s, tijd = %s, 
                opmerkingen = %s, custom_data = %s, updated_at = NOW()
            WHERE id = %s
        """
        custom_data_json = json.dumps(afspraak.custom_data)
        params = (
            afspraak.klant_id,
            afspraak.categorie_id,
            afspraak.datum,
            afspraak.tijd,
            afspraak.opmerkingen,
            custom_data_json,
            afspraak.id
        )
        
        return self.db.execute_update(query, params)
    
    def delete(self, afspraak_id):
        """Verwijdert afspraak"""
        query = "DELETE FROM afspraken WHERE id = %s"
        return self.db.execute_update(query, (afspraak_id,))
    
    def copy_afspraak(self, afspraak_id, new_datum, new_tijd=None):
        """Kopieert afspraak naar nieuwe datum/tijd"""
        afspraak = self.get_by_id(afspraak_id)
        if not afspraak:
            return None
        
        # Maak kopie met nieuwe datum/tijd
        new_afspraak = Afspraak(
            klant_id=afspraak.klant_id,
            categorie_id=afspraak.categorie_id,
            datum=new_datum,
            tijd=new_tijd or afspraak.tijd,
            opmerkingen=afspraak.opmerkingen,
            custom_data=afspraak.custom_data.copy()
        )
        
        return self.create(new_afspraak)
    
    def count(self):
        """Telt totaal afspraken"""
        query = "SELECT COUNT(*) as total FROM afspraken"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def _map_to_afspraak(row):
        """Converteer database rij naar Afspraak object"""
        custom_data = {}
        if row.get('custom_data'):
            try:
                custom_data = json.loads(row['custom_data'])
            except:
                custom_data = {}
        
        # Parse datum en tijd
        datum = row.get('datum')
        if isinstance(datum, str):
            datum = datetime.fromisoformat(datum).date()
        
        tijd = row.get('tijd')
        if isinstance(tijd, str):
            # Probeer als ISO format te parsen
            try:
                tijd = datetime.fromisoformat(f"2000-01-01T{tijd}").time()
            except:
                tijd = None
        
        return Afspraak(
            id=row['id'],
            klant_id=row['klant_id'],
            categorie_id=row['categorie_id'],
            datum=datum,
            tijd=tijd,
            opmerkingen=row.get('opmerkingen'),
            custom_data=custom_data,
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
