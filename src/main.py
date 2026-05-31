"""
Main Application - Thiry Planning Tool
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QTextEdit, QHeaderView,
    QFileDialog, QProgressDialog
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
from src.utils.import_manager import ImportManager

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
        self.current_klanten = []  # Huidy klanten in geheugen
        self.sort_column = None  # Huide sort kolom
        self.sort_ascending = True  # Huide sort richting
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
        import_btn = QPushButton("📥 Importeren uit Excel")
        import_btn.clicked.connect(self.import_klanten)
        
        button_layout.addWidget(new_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(import_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Tabel
        self.klanten_table = QTableWidget()
        self.klanten_table.setColumnCount(6)
        self.klanten_table.setHorizontalHeaderLabels(["ID", "Klantnummer", "Naam", "Telefoon", "Email", "Gemeente"])
        self.klanten_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Sorteer functionaliteit inschakelen
        self.klanten_table.horizontalHeader().sectionClicked.connect(self.on_column_header_clicked)
        
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
        self.current_klanten = self.klant_repo.get_all()
        self.sort_column = None
        self.sort_ascending = True
        self.display_klanten(self.current_klanten)
        self.klanten_count_label.setText(f"Klanten: {len(self.current_klanten)}")
    
    def on_column_header_clicked(self, column):
        """Sorteert tabel als kolom header geklikt wordt"""
        # Bepaal sort richting
        if self.sort_column == column:
            # Als dezelfde kolom: wissel richting
            self.sort_ascending = not self.sort_ascending
        else:
            # Nieuwe kolom: begin met oplopend
            self.sort_column = column
            self.sort_ascending = True
        
        # Sorteer klanten
        self.sort_klanten_by_column(column, self.sort_ascending)
    
    def sort_klanten_by_column(self, column, ascending):
        """Sorteert klanten lijst based op kolom"""
        column_map = {
            0: lambda k: k.id,
            1: lambda k: k.klantnummer.lower(),
            2: lambda k: k.naam.lower(),
            3: lambda k: k.telefoon or "",
            4: lambda k: k.email or "",
            5: lambda k: k.gemeente or ""
        }
        
        if column in column_map:
            self.current_klanten.sort(
                key=column_map[column],
                reverse=not ascending
            )
            self.display_klanten(self.current_klanten)
    
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
            self.current_klanten = self.klant_repo.search(search_term)
            self.sort_column = None  # Reset sorteer
            self.sort_ascending = True
            self.display_klanten(self.current_klanten)
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
    
    def import_klanten(self):
        """Importeert klanten uit CSV/Excel bestand"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Kies Excel of CSV bestand",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;Alle Bestanden (*.*)"
        )
        
        if not file_path:
            return
        
        # Progress dialog
        progress = QProgressDialog(
            "Klanten worden ingeladen...",
            "Annuleren",
            0, 100,
            self
        )
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        try:
            # Lees bestand
            if file_path.endswith('.csv'):
                klanten, fouten = ImportManager.import_csv(file_path)
            else:
                klanten, fouten = ImportManager.import_excel(file_path)
            
            progress.setValue(50)
            
            if not klanten and fouten:
                QMessageBox.critical(
                    self,
                    "Fout bij importeren",
                    f"Geen klanten ingeladen.\n\nFouten:\n" + "\n".join(fouten[:5])
                )
                progress.close()
                return
            
            # Voeg klanten toe aan database
            added = 0
            skipped = 0
            errors = []
            
            for i, klant in enumerate(klanten):
                progress.setValue(50 + (i / len(klanten)) * 50)
                
                # Controleer of klant al bestaat
                existing = self.klant_repo.get_by_klantnummer(klant.klantnummer)
                if existing:
                    skipped += 1
                    continue
                
                if not self.klant_repo.create(klant):
                    errors.append(f"Fout bij toevoegen: {klant.naam}")
                else:
                    added += 1
            
            progress.close()
            
            # Toon resultaat
            message = f"✅ {added} klanten succesvol geïmporteerd!"
            if skipped > 0:
                message += f"\n⏭️ {skipped} klanten waren al aanwezig (overgeslagen)"
            if errors:
                message += f"\n❌ {len(errors)} fouten\n\n" + "\n".join(errors[:5])
            
            QMessageBox.information(self, "Import Compleet", message)
            self.load_klanten()
            
        except Exception as e:
            QMessageBox.critical(self, "Fout", f"Fout bij importeren: {str(e)}")
        finally:
            progress.close()

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
