from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QListWidget, QGroupBox, QLineEdit, QSpinBox, 
                           QLabel, QTextEdit, QComboBox, QFileDialog)
from PyQt6.QtCore import QThread, pyqtSignal
from core.server_manager import ServerManager
from PyQt6.QtGui import QFont, QColor, QPalette
import logging
from gui.proxy_chain_panel import ProxyChainPanel

class ServerThread(QThread):
    output_signal = pyqtSignal(str)
    
    def __init__(self, server_manager, port, server_type, proxy_chain=None):
        super().__init__()
        self.server_manager = server_manager
        self.port = port
        self.server_type = server_type
        self.proxy_chain = proxy_chain
    
    def run(self):
        try:
            if self.server_type == "HTTP":
                self.server_manager.start_http_server(self.port, self.output_signal.emit)
            elif self.server_type == "HTTP Proxy":
                self.server_manager.start_http_proxy(self.port, self.output_signal.emit, self.proxy_chain)
            # TCP/UDP can be implemented similarly
        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")

class ServerPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.server_mgr = ServerManager()
        self.running_servers = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Advanced Server Manager")
        self.setMinimumSize(800, 600)
        # Modern dark theme
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(dark_palette)
        self.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                font-weight: bold;
                font-size: 15px;
                padding: 8px;
            }
            QPushButton {
                background-color: #232323;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
                border: 1px solid #0078d7;
            }
            QLineEdit, QSpinBox, QComboBox, QTextEdit, QListWidget {
                background-color: #232323;
                border: 1px solid #444;
                border-radius: 4px;
                color: #e0e0e0;
                padding: 4px;
            }
            QTextEdit {
                font-family: 'Consolas', 'Fira Mono', monospace;
                font-size: 13px;
            }
            QListWidget::item:selected {
                background: #0078d7;
                color: #fff;
            }
        ''')
        
        layout = QVBoxLayout(self)
        
        # Server creation controls
        creation_group = QGroupBox("Create Lightweight Server")
        creation_layout = QVBoxLayout(creation_group)
        
        form_layout = QHBoxLayout()
        self.server_type = QComboBox()
        self.server_type.addItems(["HTTP", "TCP", "UDP", "HTTP Proxy"])
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1000, 65535)
        self.port_input.setValue(8080)
        
        self.start_btn = QPushButton("Start Server")
        self.start_btn.clicked.connect(self.start_server)
        
        form_layout.addWidget(QLabel("Type:"))
        form_layout.addWidget(self.server_type)
        form_layout.addWidget(QLabel("Port:"))
        form_layout.addWidget(self.port_input)
        form_layout.addWidget(self.start_btn)
        form_layout.addStretch()
        
        creation_layout.addLayout(form_layout)
        
        # Active servers list
        servers_group = QGroupBox("Active Servers")
        servers_layout = QVBoxLayout(servers_group)
        
        self.servers_list = QListWidget()
        servers_layout.addWidget(self.servers_list)
        
        # Server controls
        controls_layout = QHBoxLayout()
        self.stop_btn = QPushButton("Stop Selected Server")
        self.stop_btn.clicked.connect(self.stop_server)
        self.view_logs_btn = QPushButton("View Logs")
        self.view_logs_btn.clicked.connect(self.view_logs)
        self.launch_btn = QPushButton("Launch Program on Server")
        self.launch_btn.clicked.connect(self.launch_program_on_server)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.view_logs_btn)
        controls_layout.addWidget(self.launch_btn)
        controls_layout.addStretch()
        
        servers_layout.addLayout(controls_layout)
        
        # Server output
        output_group = QGroupBox("Server Output")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        
        layout.addWidget(creation_group)
        layout.addWidget(servers_group)
        layout.addWidget(output_group)
        
        self.proxy_btn = QPushButton("Configure Proxy Chain")
        self.proxy_btn.clicked.connect(self.open_proxy_chain_panel)
        layout.addWidget(self.proxy_btn)
    
    def start_server(self):
        port = self.port_input.value()
        server_type = self.server_type.currentText()
        
        if port in self.running_servers:
            self.output_text.append(f"Server already running on port {port}")
            return
        
        proxy_chain = self.config.get('proxy_chain') if hasattr(self, 'config') else None
        thread = ServerThread(self.server_mgr, port, server_type, proxy_chain)
        thread.output_signal.connect(self.output_text.append)
        thread.start()
        
        self.running_servers[port] = thread
        self.servers_list.addItem(f"{server_type} Server on port {port}")
        
        self.output_text.append(f"Started {server_type} server on port {port}")
    
    def stop_server(self):
        current_row = self.servers_list.currentRow()
        if current_row >= 0:
            item = self.servers_list.takeItem(current_row)
            port = int(item.text().split()[-1])
            
            if port in self.running_servers:
                self.running_servers[port].terminate()
                del self.running_servers[port]
                self.output_text.append(f"Stopped server on port {port}")
    
    def view_logs(self):
        # Implement log viewing functionality
        pass
    
    def launch_program_on_server(self):
        current_row = self.servers_list.currentRow()
        if current_row < 0:
            self.output_text.append("No server selected.")
            return
        item = self.servers_list.item(current_row)
        port = int(item.text().split()[-1])
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Program or Script to Launch")
        if not file_path:
            self.output_text.append("No file selected.")
            return
        # Prompt for arguments
        from PyQt6.QtWidgets import QInputDialog
        args, ok = QInputDialog.getText(self, "Script Arguments", "Enter arguments (optional):")
        if not ok:
            self.output_text.append("Launch cancelled.")
            return
        # Detect script type and adjust command if needed
        import os
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.py':
            cmd = ['python', file_path]
            if args:
                cmd += args.split()
        elif ext in ['.bat', '.cmd']:
            cmd = [file_path]
            if args:
                cmd += args.split()
        elif ext == '.sh':
            cmd = ['bash', file_path]
            if args:
                cmd += args.split()
        else:
            cmd = [file_path]
            if args:
                cmd += args.split()
        # Launch the program on the server
        result = self.server_mgr.launch_program_on_server(port, cmd[0], cmd[1:], self.output_text.append)
        if result:
            self.output_text.append(f"Requested launch of {file_path} on server port {port}")
        else:
            self.output_text.append(f"Failed to launch {file_path} on server port {port}")
    
    def open_proxy_chain_panel(self):
        dlg = ProxyChainPanel(self.config)
        dlg.setWindowModality(True)
        dlg.exec() if hasattr(dlg, 'exec') else dlg.show()
        # Save proxy chain config if needed
        if hasattr(self, 'config'):
            self.config['proxy_chain'] = dlg.get_proxy_chain()