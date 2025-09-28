from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTreeWidget, QTreeWidgetItem, QLabel, QGroupBox,
                           QLineEdit, QComboBox, QProgressBar, QFileDialog,
                           QSplitter, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from core.storage_manager import StorageManager
import logging
import os

class StoragePanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.storage_mgr = StorageManager(config)
        self.init_ui()
        self.refresh_storage_info()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Storage controls
        controls_layout = QHBoxLayout()
        
        self.add_location_btn = QPushButton("Add Storage Location")
        self.add_location_btn.clicked.connect(self.add_storage_location)
        
        self.cleanup_btn = QPushButton("Cleanup Storage")
        self.cleanup_btn.clicked.connect(self.cleanup_storage)
        
        self.analyze_btn = QPushButton("AI Analyze Storage")
        self.analyze_btn.clicked.connect(self.analyze_storage)
        
        controls_layout.addWidget(self.add_location_btn)
        controls_layout.addWidget(self.cleanup_btn)
        controls_layout.addWidget(self.analyze_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Storage locations
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("Storage Locations"))
        self.storage_tree = QTreeWidget()
        self.storage_tree.setHeaderLabels(["Location", "Type", "Usage", "Free Space"])
        self.storage_tree.itemDoubleClicked.connect(self.on_location_selected)
        left_layout.addWidget(self.storage_tree)
        
        # Add location form
        add_group = QGroupBox("Add New Location")
        add_layout = QVBoxLayout(add_group)
        
        form_layout = QHBoxLayout()
        self.location_path = QLineEdit()
        self.location_path.setPlaceholderText("Path or select directory...")
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_directory)
        
        self.location_type = QComboBox()
        self.location_type.addItems(["Server Storage", "Backup", "Logs", "Temporary"])
        
        form_layout.addWidget(QLabel("Path:"))
        form_layout.addWidget(self.location_path)
        form_layout.addWidget(self.browse_btn)
        form_layout.addWidget(QLabel("Type:"))
        form_layout.addWidget(self.location_type)
        
        add_layout.addLayout(form_layout)
        
        add_btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Location")
        self.add_btn.clicked.connect(self.add_new_location)
        add_btn_layout.addWidget(self.add_btn)
        add_btn_layout.addStretch()
        
        add_layout.addLayout(add_btn_layout)
        left_layout.addWidget(add_group)
        
        # Right panel - Storage details and AI analysis
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Storage info
        info_group = QGroupBox("Storage Information")
        info_layout = QVBoxLayout(info_group)
        
        self.usage_bar = QProgressBar()
        self.usage_bar.setFormat("Overall Usage: %p%")
        info_layout.addWidget(self.usage_bar)
        
        info_details_layout = QVBoxLayout()
        self.total_space_label = QLabel("Total Space: Calculating...")
        self.used_space_label = QLabel("Used Space: Calculating...")
        self.free_space_label = QLabel("Free Space: Calculating...")
        
        info_details_layout.addWidget(self.total_space_label)
        info_details_layout.addWidget(self.used_space_label)
        info_details_layout.addWidget(self.free_space_label)
        
        info_layout.addLayout(info_details_layout)
        right_layout.addWidget(info_group)
        
        # AI Analysis
        analysis_group = QGroupBox("AI Storage Analysis & Recommendations")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        analysis_layout.addWidget(self.analysis_text)
        
        right_layout.addWidget(analysis_group)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([500, 700])
        
        layout.addWidget(splitter)
        
        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_storage_info)
        self.refresh_timer.start(10000)  # Refresh every 10 seconds
    
    def refresh_storage_info(self):
        """Refresh storage information display"""
        self.storage_tree.clear()
        
        locations = self.storage_mgr.get_storage_locations()
        for location in locations:
            item = QTreeWidgetItem([
                location['path'],
                location['type'],
                f"{location['usage_gb']:.1f} GB",
                f"{location['free_gb']:.1f} GB"
            ])
            self.storage_tree.addTopLevelItem(item)
        
        # Update overall usage
        overall_usage = self.storage_mgr.get_overall_usage()
        self.usage_bar.setValue(int(overall_usage['percent_used']))
        self.total_space_label.setText(f"Total Space: {overall_usage['total_gb']:.1f} GB")
        self.used_space_label.setText(f"Used Space: {overall_usage['used_gb']:.1f} GB")
        self.free_space_label.setText(f"Free Space: {overall_usage['free_gb']:.1f} GB")
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Storage Directory")
        if directory:
            self.location_path.setText(directory)
    
    def add_new_location(self):
        path = self.location_path.text()
        location_type = self.location_type.currentText()
        
        if path and os.path.exists(path):
            self.storage_mgr.add_storage_location(path, location_type)
            self.location_path.clear()
            self.refresh_storage_info()
            self.logger.info(f"Added storage location: {path}")
        else:
            self.logger.warning("Invalid storage path")
    
    def add_storage_location(self):
        # Implementation for adding predefined locations
        pass
    
    def cleanup_storage(self):
        """AI-powered storage cleanup"""
        cleanup_report = self.storage_mgr.ai_cleanup()
        self.analysis_text.setText(cleanup_report)
    
    def analyze_storage(self):
        """AI analysis of storage patterns"""
        analysis = self.storage_mgr.ai_analyze_storage()
        self.analysis_text.setText(analysis)
    
    def on_location_selected(self, item, column):
        """Handle storage location selection"""
        path = item.text(0)
        details = self.storage_mgr.get_location_details(path)
        
        detail_text = f"""
=== Storage Location Analysis ===
Path: {details['path']}
Type: {details['type']}
Total Size: {details['total_gb']:.1f} GB
Used: {details['used_gb']:.1f} GB
Free: {details['free_gb']:.1f} GB
Usage: {details['percent_used']:.1f}%

File Types Distribution:
"""
        for file_type, count in details['file_types'].items():
            detail_text += f"{file_type}: {count} files\n"
        
        self.analysis_text.setText(detail_text)