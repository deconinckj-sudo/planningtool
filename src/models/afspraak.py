"""
Afspraak Model
Data class voor afspraken
"""

from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional
import json

@dataclass
class Afspraak:
    """Afspraak data model"""
    id: Optional[int] = None
    klant_id: int = 0
    categorie_id: int = 0
    datum: Optional[date] = None
    tijd: Optional[time] = None
    opmerkingen: Optional[str] = None
    custom_data: dict = None  # Dynamische velden per categorie
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.custom_data is None:
            self.custom_data = {}
    
    def __str__(self):
        tijd_str = self.tijd.strftime("%H:%M") if self.tijd else "Geen tijd"
        datum_str = self.datum.strftime("%d-%m-%Y") if self.datum else "Geen datum"
        return f"{datum_str} {tijd_str}"
    
    def to_dict(self):
        """Converteer naar dictionary"""
        return {
            'id': self.id,
            'klant_id': self.klant_id,
            'categorie_id': self.categorie_id,
            'datum': self.datum.isoformat() if self.datum else None,
            'tijd': self.tijd.isoformat() if self.tijd else None,
            'opmerkingen': self.opmerkingen,
            'custom_data': json.dumps(self.custom_data),
        }
