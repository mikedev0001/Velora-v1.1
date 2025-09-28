from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QListWidget, QGroupBox, QLineEdit, QLabel,
                           QTextEdit, QComboBox, QFileDialog, QCheckBox)
from PyQt6.QtCore import QProcess, QTimer
from core.launcher_manager import LauncherManager
import logging
import os

class LauncherPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.launcher_mgr = LauncherManager(config)
        self.running_processes = {}
        self.init_ui()
        self.load_applications()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Application controls
        controls_layout = QHBoxLayout()
        
        self.add_app_btn = QPushButton("Add Application")
        self.add_app_btn.clicked.connect(self.add_application)
        
        self.import_btn = QPushButton("Import from System")
        self.import_btn.clicked.connect(self.import_system_apps)
        
        self.ai_optimize_btn = QPushButton("AI Optimize Launch")
        self.ai_optimize_btn.clicked.connect(self.ai_optimize_launch)
        
        controls_layout.addWidget(self.add_app_btn)
        controls_layout.addWidget(self.import_btn)
        controls_layout.addWidget(self.ai_optimize_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Main content
        main_layout = QHBoxLayout()
        
        # Left panel - Applications list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("Applications"))
        self.apps_list = QListWidget()
        self.apps_list.itemDoubleClicked.connect(self.launch_application)
        left_layout.addWidget(self.apps_list)
        
        # Application controls
        app_controls_layout = QHBoxLayout()
        self.launch_btn = QPushButton("Launch Selected")
        self.launch_btn.clicked.connect(self.launch_application)
        
        self.stop_btn = QPushButton("Stop Selected")
        self.stop_btn.clicked.connect(self.stop_application)
        
        self.edit_btn = QPushButton("Edit Application")
        self.edit_btn.clicked.connect(self.edit_application)
        
        app_controls_layout.addWidget(self.launch_btn)
        app_controls_layout.addWidget(self.stop_btn)
        app_controls_layout.addWidget(self.edit_btn)
        app_controls_layout.addStretch()
        
        left_layout.addLayout(app_controls_layout)
        
        # Right panel - Application details and AI
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Add application form
        add_group = QGroupBox("Add/Edit Application")
        add_layout = QVBoxLayout(add_group)
        
        # Form fields
        form_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.app_name = QLineEdit()
        self.app_name.setPlaceholderText("Application name")
        name_layout.addWidget(self.app_name)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Path:"))
        self.app_path = QLineEdit()
        self.app_path.setPlaceholderText("Executable path")
        self.browse_app_btn = QPushButton("Browse")
        self.browse_app_btn.clicked.connect(self.browse_application)
        path_layout.addWidget(self.app_path)
        path_layout.addWidget(self.browse_app_btn)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.app_type = QComboBox()
        self.app_type.addItems(["Executable", "Script", "Web Service", "System Tool"])
        type_layout.addWidget(self.app_type)
        
        args_layout = QHBoxLayout()
        args_layout.addWidget(QLabel("Arguments:"))
        self.app_args = QLineEdit()
        self.app_args.setPlaceholderText("Command line arguments (optional)")
        args_layout.addWidget(self.app_args)
        
        self.auto_start = QCheckBox("Start automatically with system")
        
        form_layout.addLayout(name_layout)
        form_layout.addLayout(path_layout)
        form_layout.addLayout(type_layout)
        form_layout.addLayout(args_layout)
        form_layout.addWidget(self.auto_start)
        
        add_layout.addLayout(form_layout)
        
        # Form buttons
        form_btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Application")
        self.save_btn.clicked.connect(self.save_application)
        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        
        form_btn_layout.addWidget(self.save_btn)
        form_btn_layout.addWidget(self.clear_btn)
        form_btn_layout.addStretch()
        
        add_layout.addLayout(form_btn_layout)
        right_layout.addWidget(add_group)
        
        # Running processes
        running_group = QGroupBox("Running Processes")
        running_layout = QVBoxLayout(running_group)
        
        self.running_processes_text = QTextEdit()
        self.running_processes_text.setReadOnly(True)
        running_layout.addWidget(self.running_processes_text)
        
        right_layout.addWidget(running_group)
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_layout.setStretchFactor(left_widget, 1)
        main_layout.setStretchFactor(right_widget, 2)
        
        layout.addLayout(main_layout)
        
        # Setup process monitor timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_running_processes)
        self.monitor_timer.start(2000)  # Update every 2 seconds
    
    def load_applications(self):
        """Load applications from configuration"""
        self.apps_list.clear()
        applications = self.launcher_mgr.get_applications()
        for app in applications:
            status = "✅" if app.get('running', False) else "⏹️"
            self.apps_list.addItem(f"{status} {app['name']} ({app['type']})")
    
    def browse_application(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Application")
        if file_path:
            self.app_path.setText(file_path)
            if not self.app_name.text():
                self.app_name.setText(os.path.basename(file_path))
    
    def add_application(self):
        self.clear_form()
    
    def save_application(self):
        name = self.app_name.text()
        path = self.app_path.text()
        app_type = self.app_type.currentText()
        args = self.app_args.text()
        auto_start = self.auto_start.isChecked()
        
        if name and path and os.path.exists(path):
            app_data = {
                'name': name,
                'path': path,
                'type': app_type,
                'arguments': args,
                'auto_start': auto_start
            }
            
            self.launcher_mgr.add_application(app_data)
            self.load_applications()
            self.clear_form()
            self.logger.info(f"Added application: {name}")
        else:
            self.logger.warning("Invalid application data")
    
    def clear_form(self):
        self.app_name.clear()
        self.app_path.clear()
        self.app_args.clear()
        self.auto_start.setChecked(False)
    
    def launch_application(self, item=None):
        if not item:
            item = self.apps_list.currentItem()
        
        if item:
            app_name = item.text().split(' ')[1]  # Extract name from display
            success, message = self.launcher_mgr.launch_application(app_name)
            
            if success:
                self.logger.info(f"Launched application: {app_name}")
            else:
                self.logger.error(f"Failed to launch {app_name}: {message}")
            
            self.load_applications()
    
    def stop_application(self):
        item = self.apps_list.currentItem()
        if item:
            app_name = item.text().split(' ')[1]
            success = self.launcher_mgr.stop_application(app_name)
            
            if success:
                self.logger.info(f"Stopped application: {app_name}")
            else:
                self.logger.error(f"Failed to stop application: {app_name}")
            
            self.load_applications()
    
    def edit_application(self):
        item = self.apps_list.currentItem()
        if item:
            app_name = item.text().split(' ')[1]
            app_data = self.launcher_mgr.get_application(app_name)
            
            if app_data:
                self.app_name.setText(app_data['name'])
                self.app_path.setText(app_data['path'])
                self.app_type.setCurrentText(app_data['type'])
                self.app_args.setText(app_data.get('arguments', ''))
                self.auto_start.setChecked(app_data.get('auto_start', False))
    
    def import_system_apps(self):
        """Import applications from system"""
        imported = self.launcher_mgr.import_system_applications()
        self.load_applications()
        self.logger.info(f"Imported {imported} system applications")
    
    def ai_optimize_launch(self):
        """AI optimization for application launching"""
        optimization = self.launcher_mgr.ai_optimize_launch_order()
        self.running_processes_text.setText(optimization)
    
    def update_running_processes(self):
        """Update running processes display"""
        running_apps = self.launcher_mgr.get_running_applications()
        display_text = "=== Running Applications ===\n\n"
        
        for app in running_apps:
            display_text += f"🔵 {app['name']}\n"
            display_text += f"   PID: {app['pid']} | CPU: {app.get('cpu', 'N/A')}% | Memory: {app.get('memory', 'N/A')}MB\n"
            display_text += f"   Uptime: {app.get('uptime', 'N/A')}\n\n"
        
        self.running_processes_text.setText(display_text)