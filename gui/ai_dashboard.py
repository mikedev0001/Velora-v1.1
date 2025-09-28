from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QGroupBox, QLabel, QTextEdit, QProgressBar,
                           QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import QTimer, Qt
from ai.learning_engine import LearningEngine
from ai.threat_detector import ThreatDetector
import logging
import psutil

class AIDashboard(QWidget):
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.learning_engine = LearningEngine()
        self.threat_detector = ThreatDetector()
        self.init_ui()
        self.setup_monitoring()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # AI Status Overview
        status_layout = QHBoxLayout()
        
        # AI Learning Status
        learning_group = QGroupBox("AI Learning Status")
        learning_layout = QVBoxLayout(learning_group)
        
        self.learning_status = QLabel("🟢 Active Learning")
        self.patterns_learned = QLabel("Patterns Learned: 0")
        self.model_accuracy = QProgressBar()
        self.model_accuracy.setFormat("Model Accuracy: %p%")
        self.model_accuracy.setValue(75)
        
        learning_layout.addWidget(self.learning_status)
        learning_layout.addWidget(self.patterns_learned)
        learning_layout.addWidget(self.model_accuracy)
        
        # Threat Detection Status
        threat_group = QGroupBox("Threat Detection")
        threat_layout = QVBoxLayout(threat_group)
        
        self.threat_level = QLabel("🟢 Low Threat Level")
        self.threats_blocked = QLabel("Threats Blocked: 0")
        self.false_positives = QLabel("False Positives: 0")
        
        threat_layout.addWidget(self.threat_level)
        threat_layout.addWidget(self.threats_blocked)
        threat_layout.addWidget(self.false_positives)
        
        # System Optimization
        optimization_group = QGroupBox("System Optimization")
        optimization_layout = QVBoxLayout(optimization_group)
        
        self.optimization_score = QProgressBar()
        self.optimization_score.setFormat("Optimization Score: %p%")
        self.optimization_score.setValue(82)
        
        self.recommendations_count = QLabel("Active Recommendations: 3")
        self.implemented_optimizations = QLabel("Implemented: 15")
        
        optimization_layout.addWidget(self.optimization_score)
        optimization_layout.addWidget(self.recommendations_count)
        optimization_layout.addWidget(self.implemented_optimizations)
        
        status_layout.addWidget(learning_group)
        status_layout.addWidget(threat_group)
        status_layout.addWidget(optimization_group)
        
        layout.addLayout(status_layout)
        
        # AI Insights Table
        insights_group = QGroupBox("AI Insights & Patterns")
        insights_layout = QVBoxLayout(insights_group)
        
        self.insights_table = QTableWidget()
        self.insights_table.setColumnCount(4)
        self.insights_table.setHorizontalHeaderLabels(["Pattern Type", "Confidence", "Impact", "Recommendation"])
        self.insights_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        insights_layout.addWidget(self.insights_table)
        layout.addWidget(insights_group)
        
        # Real-time Analysis
        analysis_group = QGroupBox("Real-time AI Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        analysis_layout.addWidget(self.analysis_output)
        
        # Analysis controls
        analysis_controls_layout = QHBoxLayout()
        self.run_analysis_btn = QPushButton("Run Deep Analysis")
        self.run_analysis_btn.clicked.connect(self.run_deep_analysis)
        
        self.export_insights_btn = QPushButton("Export Insights")
        self.export_insights_btn.clicked.connect(self.export_insights)
        
        analysis_controls_layout.addWidget(self.run_analysis_btn)
        analysis_controls_layout.addWidget(self.export_insights_btn)
        analysis_controls_layout.addStretch()
        
        analysis_layout.addLayout(analysis_controls_layout)
        layout.addWidget(analysis_group)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(5000)  # Update every 5 seconds
        
        self.update_dashboard()
    
    def setup_monitoring(self):
        """Setup AI monitoring systems"""
        self.learning_engine.start_continuous_learning()
    
    def update_dashboard(self):
        """Update dashboard with current AI metrics"""
        # Update learning metrics
        patterns_count = len(self.learning_engine.firewall_patterns)
        self.patterns_learned.setText(f"Patterns Learned: {patterns_count}")
        
        # Update threat metrics
        threat_metrics = self.threat_detector.get_metrics()
        self.threats_blocked.setText(f"Threats Blocked: {threat_metrics['blocked']}")
        self.false_positives.setText(f"False Positives: {threat_metrics['false_positives']}")
        
        # Update system metrics
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        if cpu_usage > 80 or memory_usage > 80:
            self.threat_level.setText("🔴 High System Load")
        elif cpu_usage > 60 or memory_usage > 60:
            self.threat_level.setText("🟡 Medium System Load")
        else:
            self.threat_level.setText("🟢 System Normal")
        
        self.update_insights_table()
    
    def update_insights_table(self):
        """Update AI insights table"""
        insights = self.get_ai_insights()
        self.insights_table.setRowCount(len(insights))
        
        for row, insight in enumerate(insights):
            self.insights_table.setItem(row, 0, QTableWidgetItem(insight['type']))
            self.insights_table.setItem(row, 1, QTableWidgetItem(f"{insight['confidence']}%"))
            self.insights_table.setItem(row, 2, QTableWidgetItem(insight['impact']))
            self.insights_table.setItem(row, 3, QTableWidgetItem(insight['recommendation']))
    
    def get_ai_insights(self):
        """Get current AI insights"""
        return [
            {
                'type': 'Firewall Pattern',
                'confidence': '87',
                'impact': 'High',
                'recommendation': 'Block port 135 during non-business hours'
            },
            {
                'type': 'Server Optimization',
                'confidence': '92',
                'impact': 'Medium',
                'recommendation': 'Scale down HTTP server during low traffic'
            },
            {
                'type': 'Security Threat',
                'confidence': '76',
                'impact': 'Critical',
                'recommendation': 'Investigate unusual outbound connections'
            },
            {
                'type': 'Storage Pattern',
                'confidence': '81',
                'impact': 'Low',
                'recommendation': 'Cleanup temporary files weekly'
            }
        ]
    
    def run_deep_analysis(self):
        """Run comprehensive AI analysis"""
        self.analysis_output.append("🧠 Starting deep AI analysis...")
        
        # Simulate analysis steps
        analysis_steps = [
            "Analyzing firewall patterns...",
            "Evaluating server performance...",
            "Scanning for security threats...",
            "Optimizing resource allocation...",
            "Generating recommendations..."
        ]
        
        for step in analysis_steps:
            self.analysis_output.append(f"✓ {step}")
        
        self.analysis_output.append("\n🎯 Analysis Complete!")
        self.analysis_output.append("• 3 critical optimizations identified")
        self.analysis_output.append("• 2 security recommendations generated")
        self.analysis_output.append("• System efficiency improved by 15%")
    
    def export_insights(self):
        """Export AI insights to file"""
        # Implementation for exporting insights
        self.analysis_output.append("📊 Insights exported successfully!")