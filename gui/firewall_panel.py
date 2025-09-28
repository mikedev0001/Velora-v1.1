from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QListWidget, QTextEdit, QLabel, QSplitter, 
                           QGroupBox, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt
from ai.firewall_analyzer import FirewallAnalyzer
from core.firewall_manager import FirewallManager
import logging

class FirewallPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.ai_analyzer = FirewallAnalyzer()
        self.firewall_mgr = FirewallManager()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh Rules")
        self.refresh_btn.clicked.connect(self.refresh_rules)
        
        self.analyze_btn = QPushButton("AI Analyze")
        self.analyze_btn.clicked.connect(self.analyze_firewall)
        
        self.add_rule_btn = QPushButton("Add Rule")
        self.add_rule_btn.clicked.connect(self.add_rule)
        
        controls_layout.addWidget(self.refresh_btn)
        controls_layout.addWidget(self.analyze_btn)
        controls_layout.addWidget(self.add_rule_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Rules list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("Firewall Rules"))
        self.rules_list = QListWidget()
        left_layout.addWidget(self.rules_list)
        
        # Right panel - Analysis and details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # AI Analysis section
        analysis_group = QGroupBox("AI Analysis & Recommendations")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        analysis_layout.addWidget(self.analysis_text)
        
        # Add rule section
        rule_group = QGroupBox("Add New Rule")
        rule_layout = QVBoxLayout(rule_group)
        
        rule_form_layout = QHBoxLayout()
        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("e.g., 80/tcp, 443/tcp")
        self.rule_type = QComboBox()
        self.rule_type.addItems(["ALLOW", "DENY"])
        
        rule_form_layout.addWidget(QLabel("Port/Protocol:"))
        rule_form_layout.addWidget(self.rule_input)
        rule_form_layout.addWidget(QLabel("Action:"))
        rule_form_layout.addWidget(self.rule_type)
        
        rule_layout.addLayout(rule_form_layout)
        
        right_layout.addWidget(analysis_group)
        right_layout.addWidget(rule_group)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        
        self.refresh_rules()
    
    def refresh_rules(self):
        self.rules_list.clear()
        rules = self.firewall_mgr.get_rules()
        for rule in rules:
            self.rules_list.addItem(f"{rule['port']}/{rule['protocol']} - {rule['action']}")
    
    def analyze_firewall(self):
        rules = self.firewall_mgr.get_rules()
        analysis = self.ai_analyzer.analyze_rules(rules)
        self.analysis_text.setText(analysis)
    
    def add_rule(self):
        rule_text = self.rule_input.text()
        action = self.rule_type.currentText()
        
        if rule_text:
            try:
                self.firewall_mgr.add_rule(rule_text, action)
                self.refresh_rules()
                self.rule_input.clear()
            except Exception as e:
                self.logger.error(f"Error adding rule: {e}")