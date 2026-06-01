"""
Categorie Model
Data class voor afspraak categorien
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json

@dataclass
class Categorie:
    """Afspraak categorie data model"""
    id: Optional[int] = None
    naam: str = ""
    kleur: str = "#3498db"  # Standaard blauw
    beschrijving: Optional[str] = None
    custom_velden: dict = None  # JSON velden configuratie
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.custom_velden is None:
            self.custom_velden = {}
    
    def __str__(self):
        return f"{self.naam}"
    
    def to_dict(self):
        """Converteer naar dictionary"""
        return {
            'id': self.id,
            'naam': self.naam,
            'kleur': self.kleur,
            'beschrijving': self.beschrijving,
            'custom_velden': json.dumps(self.custom_velden),
        }
