"""
Klant Model
Data class voor klanten
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Klant:
    """Klant data model"""
    id: Optional[int] = None
    klantnummer: str = ""
    naam: str = ""
    contactpersoon: Optional[str] = None
    telefoon: Optional[str] = None
    gsm: Optional[str] = None
    email: Optional[str] = None
    straat: Optional[str] = None
    huisnummer: Optional[str] = None
    postcode: Optional[str] = None
    gemeente: Optional[str] = None
    actief: bool = True
    opmerkingen: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __str__(self):
        return f"{self.klantnummer} - {self.naam}"
    
    def to_dict(self):
        """Converteer naar dictionary"""
        return {
            'id': self.id,
            'klantnummer': self.klantnummer,
            'naam': self.naam,
            'contactpersoon': self.contactpersoon,
            'telefoon': self.telefoon,
            'gsm': self.gsm,
            'email': self.email,
            'straat': self.straat,
            'huisnummer': self.huisnummer,
            'postcode': self.postcode,
            'gemeente': self.gemeente,
            'actief': self.actief,
            'opmerkingen': self.opmerkingen,
        }