"""
Afspraak Model
Data class voor afspraken
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Afspraak:
    """Afspraak data model"""
    id: Optional[int] = None
    klant_id: int = 0
    klant_naam: str = ""
    categorie_id: Optional[int] = None
    categorie_naam: str = ""
    titel: str = ""
    omschrijving: Optional[str] = None
    start_datetime: Optional[datetime] = None
    eind_datetime: Optional[datetime] = None
    status: str = "geplanned"  # geplanned, in_uitvoering, afgerond, geannuleerd
    locatie: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __str__(self):
        return f"{self.titel} - {self.klant_naam}"
    
    def to_dict(self):
        """Converteer naar dictionary"""
        return {
            'id': self.id,
            'klant_id': self.klant_id,
            'categorie_id': self.categorie_id,
            'titel': self.titel,
            'omschrijving': self.omschrijving,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'eind_datetime': self.eind_datetime.isoformat() if self.eind_datetime else None,
            'status': self.status,
            'locatie': self.locatie,
        }