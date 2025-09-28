from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                           QWidget, QStatusBar, QMessageBox, QMenuBar, QMenu)
from PyQt6.QtCore import Qt, QTimer
from .firewall_panel import FirewallPanel
from .server_panel import ServerPanel
from .storage_panel import StoragePanel
from .launcher_panel import LauncherPanel
from .ai_dashboard import AIDashboard
from .styles import ModernStyles
from utils.config_loader import ConfigLoader
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = ConfigLoader()
        self.ai_learning_active = True
        self.init_ui()
        self.setup_ai_learning()
        
    def init_ui(self):
        self.setWindowTitle("AI Firewall & Server Manager - Advanced")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply styles
        self.setStyleSheet(ModernStyles.get_stylesheet())
        
        # Create menu bar
        self.setup_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create panels
        self.firewall_panel = FirewallPanel(self.config)
        self.server_panel = ServerPanel(self.config)
        self.storage_panel = StoragePanel(self.config)
        self.launcher_panel = LauncherPanel(self.config)
        self.ai_dashboard = AIDashboard(self.config)
        
        # Add tabs
        self.tab_widget.addTab(self.firewall_panel, "🔥 Firewall AI")
        self.tab_widget.addTab(self.server_panel, "🚀 Smart Servers")
        self.tab_widget.addTab(self.storage_panel, "💾 Storage Manager")
        self.tab_widget.addTab(self.launcher_panel, "⚡ App Launcher")
        self.tab_widget.addTab(self.ai_dashboard, "🧠 AI Dashboard")
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("AI System Ready - Learning Active")
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # 30 seconds
        
        self.logger.info("Advanced main window initialized")
    
    def setup_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # File menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        
        save_action = file_menu.addAction("Save Configuration")
        save_action.triggered.connect(self.save_config)
        
        load_action = file_menu.addAction("Load Configuration")
        load_action.triggered.connect(self.load_config)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # AI menu
        ai_menu = QMenu("AI Settings", self)
        menu_bar.addMenu(ai_menu)
        
        self.learning_toggle = ai_menu.addAction("✓ AI Learning Active")
        self.learning_toggle.triggered.connect(self.toggle_ai_learning)
        
        train_action = ai_menu.addAction("Train AI Models")
        train_action.triggered.connect(self.train_ai_models)
        
        # View menu
        view_menu = QMenu("View", self)
        menu_bar.addMenu(view_menu)
        
        theme_menu = QMenu("Themes", view_menu)
        view_menu.addMenu(theme_menu)
        
        dark_action = theme_menu.addAction("Dark Theme")
        dark_action.triggered.connect(lambda: ModernStyles.setup_dark_theme(self))
        
        light_action = theme_menu.addAction("Light Theme")
        light_action.triggered.connect(lambda: ModernStyles.setup_light_theme(self))
    
    def setup_ai_learning(self):
        """Initialize AI learning components"""
        from ai.learning_engine import LearningEngine
        self.learning_engine = LearningEngine()
        self.learning_engine.start_continuous_learning()
    
    def toggle_ai_learning(self):
        self.ai_learning_active = not self.ai_learning_active
        status = "Active" if self.ai_learning_active else "Inactive"
        self.learning_toggle.setText(f"{'✓' if self.ai_learning_active else '✗'} AI Learning {status}")
        self.status_bar.showMessage(f"AI Learning {status}")
        
        if self.ai_learning_active:
            self.learning_engine.start_continuous_learning()
        else:
            self.learning_engine.stop_continuous_learning()
    
    def train_ai_models(self):
        QMessageBox.information(self, "AI Training", "Starting AI model training...")
        self.learning_engine.retrain_models()
        self.status_bar.showMessage("AI Models Training Completed")
    
    def auto_save(self):
        """Auto-save configuration"""
        self.config.save()
        self.logger.debug("Configuration auto-saved")
    
    def save_config(self):
        self.config.save()
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
    
    def load_config(self):
        self.config.load()
        QMessageBox.information(self, "Success", "Configuration loaded successfully!")
    
    def closeEvent(self, event):
        if self.ai_learning_active:
            self.learning_engine.stop_continuous_learning()
        
        reply = QMessageBox.question(self, 'Confirm Exit',
                                   'Are you sure you want to exit?',
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config.save()
            self.logger.info("Application closing")
            event.accept()
        else:
            event.ignore()