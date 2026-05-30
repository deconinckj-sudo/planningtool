"""
Main Application - Thiry Planning Tool
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QTextEdit, QHeaderView
)
from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtGui import QIcon, QFont
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import APP_TITLE, APP_VERSION, COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from src.database.connection import DatabaseConnection
from src.repositories.klant_repository import KlantRepository
from src.repositories.afspraak_repository import AfspraakRepository
from src.models.klant import Klant
from src.models.afspraak import Afspraak

class KlantDialog(QDialog):
    """Dialog voor klant toevoegen/bewerken"""
    
    def __init__(self, klant=None, parent=None):
        super().__init__(parent)
        self.klant = klant or Klant()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Klant" if self.klant.id else "Nieuwe Klant")
        self.setGeometry(100, 100, 500, 400)
        
        layout = QFormLayout()
        
        # Klantnummer
        self.klantnummer_input = QLineEdit()
        self.klantnummer_input.setText(self.klant.klantnummer)
        self.klantnummer_input.setEnabled(not self.klant.id)  # Niet wijzigen na aanmaak
        layout.addRow("Klantnummer:", self.klantnummer_input)
        
        # Naam
        self.naam_input = QLineEdit()
        self.naam_input.setText(self.klant.naam)
        layout.addRow("Naam:", self.naam_input)
        
        # Contactpersoon
        self.contactpersoon_input = QLineEdit()
        self.contactpersoon_input.setText(self.klant.contactpersoon or "")
        layout.addRow("Contactpersoon:", self.contactpersoon_input)
        
        # Telefoon
        self.telefoon_input = QLineEdit()
        self.telefoon_input.setText(self.klant.telefoon or "")
        layout.addRow("Telefoon:", self.telefoon_input)
        
        # GSM
        self.gsm_input = QLineEdit()
        self.gsm_input.setText(self.klant.gsm or "")
        layout.addRow("GSM:", self.gsm_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setText(self.klant.email or "")
        layout.addRow("Email:", self.email_input)
        
        # Adres
        self.straat_input = QLineEdit()
        self.straat_input.setText(self.klant.straat or "")
        layout.addRow("Straat:", self.straat_input)
        
        self.huisnummer_input = QLineEdit()
        self.huisnummer_input.setText(self.klant.huisnummer or "")
        layout.addRow("Huisnummer:", self.huisnummer_input)
        
        self.postcode_input = QLineEdit()
        self.postcode_input.setText(self.klant.postcode or "")
        layout.addRow("Postcode:", self.postcode_input)
        
        self.gemeente_input = QLineEdit()
        self.gemeente_input.setText(self.klant.gemeente or "")
        layout.addRow("Gemeente:", self.gemeente_input)
        
        # Opmerkingen
        self.opmerkingen_input = QTextEdit()
        self.opmerkingen_input.setText(self.klant.opmerkingen or "")
        layout.addRow("Opmerkingen:", self.opmerkingen_input)
        
        # Knoppen
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Opslaan")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annuleren")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow("", button_layout)
        self.setLayout(layout)
    
    def get_klant(self):
        """Geeft ingevulde klantgegevens"""
        self.klant.klantnummer = self.klantnummer_input.text()
        self.klant.naam = self.naam_input.text()
        self.klant.contactpersoon = self.contactpersoon_input.text()
        self.klant.telefoon = self.telefoon_input.text()
        self.klant.gsm = self.gsm_input.text()
        self.klant.email = self.email_input.text()
        self.klant.straat = self.straat_input.text()
        self.klant.huisnummer = self.huisnummer_input.text()
        self.klant.postcode = self.postcode_input.text()
        self.klant.gemeente = self.gemeente_input.text()
        self.klant.opmerkingen = self.opmerkingen_input.toPlainText()
        return self.klant

class MainWindow(QMainWindow):
    """Hoofd applicatievenster"""
    
    def __init__(self):
        super().__init__()
        self.klant_repo = KlantRepository()
        self.afspraak_repo = AfspraakRepository()
        self.init_ui()
        self.load_klanten()
    
    def init_ui(self):
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Hoofd widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel(APP_TITLE)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        klanten_count = QLabel()
        klanten_count.setText(f"Klanten: {self.klant_repo.count()}")
        klanten_count.setFont(QFont("Arial", 12))
        self.klanten_count_label = klanten_count
        header_layout.addWidget(klanten_count)
        
        main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        
        # Klanten Tab
        klanten_widget = self.create_klanten_tab()
        tabs.addTab(klanten_widget, "Klanten")
        
        # Afspraken Tab
        afspraken_widget = self.create_afspraken_tab()
        tabs.addTab(afspraken_widget, "Afspraken")
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
    
    def create_klanten_tab(self):
        """Maakt klanten tabblad"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Zoekbalk
        search_layout = QHBoxLayout()
        search_label = QLabel("Zoeken:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Naam, email, klantnummer of postcode...")
        self.search_input.textChanged.connect(self.search_klanten)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        new_btn = QPushButton("➕ Nieuwe Klant")
        new_btn.clicked.connect(self.add_klant)
        edit_btn = QPushButton("✏️ Bewerken")
        edit_btn.clicked.connect(self.edit_klant)
        delete_btn = QPushButton("🗑️ Verwijderen")
        delete_btn.clicked.connect(self.delete_klant)
        refresh_btn = QPushButton("🔄 Vernieuwen")
        refresh_btn.clicked.connect(self.load_klanten)
        
        button_layout.addWidget(new_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Tabel
        self.klanten_table = QTableWidget()
        self.klanten_table.setColumnCount(6)
        self.klanten_table.setHorizontalHeaderLabels(["ID", "Klantnummer", "Naam", "Telefoon", "Email", "Gemeente"])
        self.klanten_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.klanten_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_afspraken_tab(self):
        """Maakt afspraken tabblad"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Afspraken Management (Binnenkort beschikbaar)"))
        
        widget.setLayout(layout)
        return widget
    
    def load_klanten(self):
        """Laadt alle klanten in tabel"""
        klanten = self.klant_repo.get_all()
        self.display_klanten(klanten)
        self.klanten_count_label.setText(f"Klanten: {len(klanten)}")
    
    def display_klanten(self, klanten):
        """Toont klanten in tabel"""
        self.klanten_table.setRowCount(len(klanten))
        
        for row, klant in enumerate(klanten):
            self.klanten_table.setItem(row, 0, QTableWidgetItem(str(klant.id)))
            self.klanten_table.setItem(row, 1, QTableWidgetItem(klant.klantnummer))
            self.klanten_table.setItem(row, 2, QTableWidgetItem(klant.naam))
            self.klanten_table.setItem(row, 3, QTableWidgetItem(klant.telefoon or ""))
            self.klanten_table.setItem(row, 4, QTableWidgetItem(klant.email or ""))
            self.klanten_table.setItem(row, 5, QTableWidgetItem(klant.gemeente or ""))
    
    def search_klanten(self):
        """Zoekt klanten"""
        search_term = self.search_input.text()
        if search_term:
            klanten = self.klant_repo.search(search_term)
            self.display_klanten(klanten)
        else:
            self.load_klanten()
    
    def add_klant(self):
        """Voegt nieuwe klant toe"""
        dialog = KlantDialog(parent=self)
        if dialog.exec():
            klant = dialog.get_klant()
            if not klant.naam or not klant.klantnummer:
                QMessageBox.warning(self, "Fout", "Naam en klantnummer zijn verplicht!")
                return
            
            if self.klant_repo.create(klant):
                QMessageBox.information(self, "Succes", "Klant succesvol toegevoegd!")
                self.load_klanten()
            else:
                QMessageBox.critical(self, "Fout", "Fout bij toevoegen klant")
    
    def edit_klant(self):
        """Bewerkt geselecteerde klant"""
        selected = self.klanten_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Fout", "Selecteer eerst een klant!")
            return
        
        klant_id = int(self.klanten_table.item(selected[0].row(), 0).text())
        klant = self.klant_repo.get_by_id(klant_id)
        
        dialog = KlantDialog(klant, parent=self)
        if dialog.exec():
            klant = dialog.get_klant()
            if self.klant_repo.update(klant):
                QMessageBox.information(self, "Succes", "Klant succesvol bijgewerkt!")
                self.load_klanten()
    
    def delete_klant(self):
        """Verwijdert geselecteerde klant"""
        selected = self.klanten_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Fout", "Selecteer eerst een klant!")
            return
        
        reply = QMessageBox.question(self, "Bevestiging", "Weet je zeker dat je deze klant wilt verwijderen?")
        if reply == QMessageBox.Yes:
            klant_id = int(self.klanten_table.item(selected[0].row(), 0).text())
            if self.klant_repo.delete(klant_id):
                QMessageBox.information(self, "Succes", "Klant verwijderd!")
                self.load_klanten()

def main():
    app = QApplication(sys.argv)
    
    # Verbind met database
    db = DatabaseConnection()
    if not db.connect():
        QMessageBox.critical(None, "Fout", "Kan niet verbinden met database!\n\nVoer eerst setup_db.py uit.")
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()