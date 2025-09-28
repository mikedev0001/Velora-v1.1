from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal
import json
import os

class SettingsPanel(QWidget):
    settings_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.settings_file = 'config/settings.json'
        self.settings = self.load_settings()
        self.init_ui()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {"server_storage": ""}

    def save_settings(self):
        os.makedirs('config', exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Server storage location
        storage_layout = QHBoxLayout()
        storage_label = QLabel("Server Storage Location:")
        self.storage_edit = QLineEdit(self.settings.get("server_storage", ""))
        storage_browse_btn = QPushButton("Browse")
        storage_browse_btn.clicked.connect(self.browse_storage)

        storage_layout.addWidget(storage_label)
        storage_layout.addWidget(self.storage_edit)
        storage_layout.addWidget(storage_browse_btn)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings_changes)

        layout.addLayout(storage_layout)
        layout.addWidget(save_btn)
        layout.addStretch()

    def browse_storage(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Server Storage Directory")
        if directory:
            self.storage_edit.setText(directory)

    def save_settings_changes(self):
        self.settings["server_storage"] = self.storage_edit.text()
        self.save_settings()
        self.settings_updated.emit(self.settings)
        QMessageBox.information(self, "Settings", "Settings saved successfully!")