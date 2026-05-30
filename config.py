"""
Configuatie voor Thiry Planning Tool
Pas dit aan met jouw PostgreSQL gegevens
"""

# Database Configuratie
DB_CONFIG = {
    'host': 'localhost',           # Of het IP adres van jouw server
    'port': 5432,                  # Standaard PostgreSQL poort
    'database': 'thiry_planning',  # Databasenaam
    'user': 'postgres',            # PostgreSQL gebruiker (standaard)
    'password': 'JOUW_WACHTWOORD',  # ⚠️ VERVANG MET JE WACHTWOORD
}

# Applicatie Instellingen
APP_TITLE = 'Thiry Planning Tool'
APP_VERSION = '1.0.0'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Kleuren voor UI
COLORS = {
    'primary': '#2196F3',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'light': '#F5F5F5',
    'dark': '#424242'
}