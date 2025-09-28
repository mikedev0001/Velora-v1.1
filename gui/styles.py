from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class ModernStyles:
    @staticmethod
    def setup_dark_theme(app):
        app.setStyle('Fusion')
        
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(35, 35, 35))
        
        app.setPalette(dark_palette)
    
    @staticmethod
    def setup_light_theme(app):
        app.setStyle('Fusion')
        
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 163, 224))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        
        app.setPalette(light_palette)
    
    @staticmethod
    def get_stylesheet():
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #353535;
            border-radius: 5px;
        }
        
        QTabBar::tab {
            background-color: #404040;
            color: white;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            font-weight: bold;
        }
        
        QTabBar::tab:selected {
            background-color: #2a82da;
            color: white;
        }
        
        QTabBar::tab:hover {
            background-color: #505050;
        }
        
        QPushButton {
            background-color: #404040;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #505050;
        }
        
        QPushButton:pressed {
            background-color: #2a82da;
        }
        
        QPushButton:disabled {
            background-color: #303030;
            color: #666;
        }
        
        QListWidget {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            outline: none;
        }
        
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #555;
        }
        
        QListWidget::item:selected {
            background-color: #2a82da;
        }
        
        QTextEdit {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
            font-family: 'Consolas', monospace;
        }
        
        QLineEdit {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
        }
        
        QLineEdit:focus {
            border: 1px solid #2a82da;
        }
        
        QComboBox {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox QAbstractItemView {
            background-color: #404040;
            color: white;
            selection-background-color: #2a82da;
        }
        
        QProgressBar {
            border: 1px solid #555;
            border-radius: 4px;
            text-align: center;
            color: white;
        }
        
        QProgressBar::chunk {
            background-color: #2a82da;
            border-radius: 3px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 1px solid #555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QTreeWidget {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
        }
        
        QTreeWidget::item {
            padding: 5px;
        }
        
        QTreeWidget::item:selected {
            background-color: #2a82da;
        }
        
        QHeaderView::section {
            background-color: #505050;
            color: white;
            padding: 5px;
            border: none;
        }
        
        QTableWidget {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            gridline-color: #555;
        }
        
        QTableWidget::item {
            padding: 5px;
            border-bottom: 1px solid #555;
        }
        
        QTableWidget::item:selected {
            background-color: #2a82da;
        }
        
        QCheckBox {
            color: white;
            spacing: 5px;
        }
        
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 1px solid #555;
            background-color: #404040;
            border-radius: 2px;
        }
        
        QCheckBox::indicator:checked {
            border: 1px solid #2a82da;
            background-color: #2a82da;
            border-radius: 2px;
        }
        """