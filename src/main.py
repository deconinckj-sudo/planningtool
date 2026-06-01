"""
Main Application - Thiry Planning Tool
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QTextEdit, QHeaderView,
    QFileDialog, QProgressDialog, QCheckBox, QScrollArea
)
from PySide6.QtCore import Qt, QDateTime, QDate, QSize
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

class ColumnPickerDialog(QDialog):
    """Dialog om kolommen te kiezen"""
    
    def __init__(self, available_columns, visible_columns, parent=None):
        super().__init__(parent)
        self.available_columns = available_columns
        self.visible_columns = visible_columns
        self.checkboxes = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Kolommen Selecteren")
        self.setGeometry(100, 100, 300, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Selecteer welke kolommen zichtbaar zijn:"))
        
        # Scrollable area met checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()
        
        for col in self.available_columns:
            checkbox = QCheckBox(col)
            checkbox.setChecked(col in self.visible_columns)
            self.checkboxes[col] = checkbox
            container_layout.addWidget(checkbox)
        
        container.setLayout(container_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Knoppen
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annuleren")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_visible_columns(self):
        """Geeft geselecteerde kolommen"""
        return [col for col, checkbox in self.checkboxes.items() if checkbox.isChecked()]

class MainWindow(QMainWindow):
    """Hoofd applicatievenster"""
    
    def __init__(self):
        super().__init__()
        self.klant_repo = KlantRepository()
        self.afspraak_repo = AfspraakRepository()
        self.current_klanten = []
        self.sort_column = None
        self.sort_ascending = True
        
        # Beschikbare en zichtbare kolommen
        self.available_columns = ["ID", "Klantnummer", "Naam", "Adres", "Telefoon", "Email", "Gemeente"]
        self.visible_columns = ["ID", "Klantnummer", "Naam", "Adres", "Telefoon", "Email", "Gemeente"]
        
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
        columns_btn = QPushButton("⚙️ Kolommen")
        columns_btn.clicked.connect(self.show_column_picker)
        
        button_layout.addWidget(new_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(import_btn)
        button_layout.addWidget(columns_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Tabel
        self.klanten_table = QTableWidget()
        self.update_table_columns()
        
        # Sorteer functionaliteit inschakelen
        self.klanten_table.horizontalHeader().sectionClicked.connect(self.on_column_header_clicked)
        
        layout.addWidget(self.klanten_table)
        
        widget.setLayout(layout)
        return widget
    
    def update_table_columns(self):
        """Update tabel kolommen op basis van visible_columns"""
        self.klanten_table.setColumnCount(len(self.visible_columns))
        self.klanten_table.setHorizontalHeaderLabels(self.visible_columns)
        
        # Zet kolom breedtes op basis van content
        for i in range(len(self.visible_columns)):
            if self.visible_columns[i] in ["ID", "Klantnummer"]:
                self.klanten_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                self.klanten_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    def show_column_picker(self):
        """Toont dialog om kolommen te kiezen"""
        dialog = ColumnPickerDialog(self.available_columns, self.visible_columns, self)
        if dialog.exec():
            self.visible_columns = dialog.get_visible_columns()
            self.update_table_columns()
            self.display_klanten(self.current_klanten)
    
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
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True
        
        self.sort_klanten_by_column(column, self.sort_ascending)
    
    def sort_klanten_by_column(self, column, ascending):
        """Sorteert klanten lijst based op kolom"""
        col_name = self.visible_columns[column]
        
        column_map = {
            "ID": lambda k: int(k.id) if k.id else 0,
            "Klantnummer": lambda k: int(k.klantnummer) if k.klantnummer.isdigit() else k.klantnummer.lower(),
            "Naam": lambda k: k.naam.lower(),
            "Adres": lambda k: f"{k.straat or ''} {k.huisnummer or ''}".lower(),
            "Telefoon": lambda k: k.telefoon or "",
            "Email": lambda k: k.email or "",
            "Gemeente": lambda k: k.gemeente or ""
        }
        
        if col_name in column_map:
            self.current_klanten.sort(
                key=column_map[col_name],
                reverse=not ascending
            )
            self.display_klanten(self.current_klanten)
    
    def display_klanten(self, klanten):
        """Toont klanten in tabel"""
        self.klanten_table.setRowCount(len(klanten))
        
        for row, klant in enumerate(klanten):
            for col_idx, col_name in enumerate(self.visible_columns):
                if col_name == "ID":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(str(klant.id)))
                elif col_name == "Klantnummer":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(klant.klantnummer))
                elif col_name == "Naam":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(klant.naam))
                elif col_name == "Adres":
                    adres = f"{klant.straat or ''} {klant.huisnummer or ''}".strip()
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(adres))
                elif col_name == "Telefoon":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(klant.telefoon or ""))
                elif col_name == "Email":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(klant.email or ""))
                elif col_name == "Gemeente":
                    self.klanten_table.setItem(row, col_idx, QTableWidgetItem(klant.gemeente or ""))
    
    def search_klanten(self):
        """Zoekt klanten"""
        search_term = self.search_input.text()
        if search_term:
            self.current_klanten = self.klant_repo.search(search_term)
            self.sort_column = None
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
        
        progress = QProgressDialog(
            "Klanten worden ingeladen...",
            "Annuleren",
            0, 100,
            self
        )
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        try:
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
            
            added = 0
            skipped = 0
            errors = []
            
            for i, klant in enumerate(klanten):
                progress.setValue(50 + (i / len(klanten)) * 50)
                
                existing = self.klant_repo.get_by_klantnummer(klant.klantnummer)
                if existing:
                    skipped += 1
                    continue
                
                if not self.klant_repo.create(klant):
                    errors.append(f"Fout bij toevoegen: {klant.naam}")
                else:
                    added += 1
            
            progress.close()
            
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
    
    db = DatabaseConnection()
    if not db.connect():
        QMessageBox.critical(None, "Fout", "Kan niet verbinden met database!\n\nVoer eerst setup_db.py uit.")
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
