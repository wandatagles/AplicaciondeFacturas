# Gestor sencillo de temas para la aplicación FACTUYA
from PySide6.QtWidgets import QApplication

LIGHT_QSS = """
QMainWindow { background: #f4f6f9; }
QToolBar { background: #ffffff; border: 0px; spacing:6px; padding:4px; }
QToolButton { background:#eef2f6; border:1px solid #d0d7e1; border-radius:6px; padding:6px 10px; }
QToolButton:hover { background:#dce6ef; }
QToolButton:pressed { background:#c7d3dd; }
QTreeWidget { background:#ffffff; border:1px solid #d0d7e1; border-radius:6px; }
QTreeWidget::item:selected { background:#2d81d2; color:white; }
QLineEdit { background:#ffffff; border:1px solid #c5ccd3; border-radius:6px; padding:4px 8px; }
QPushButton { background:#2d81d2; color:white; border-radius:6px; padding:8px 14px; font-weight:600; }
QPushButton:hover { background:#3b8fe0; }
QPushButton:pressed { background:#1f5b90; }
QLabel#AppTitle { font-size:32px; font-weight:800; color:#2d81d2; letter-spacing:2px; }
QLabel#OrgSubtitle { font-size:15px; font-weight:500; color:#16a085; letter-spacing:1px; }
QLabel#previewLabel { background:#ffffff; border:1px dashed #c5ccd3; color:#5a6570; border-radius:10px; padding:28px; }
QStatusBar { background:#ffffff; border-top:1px solid #d0d7e1; }
QProgressBar { background:#e5eaf0; border:1px solid #c5ccd3; border-radius:6px; height:18px; }
QProgressBar::chunk { background:#2d81d2; border-radius:6px; }
"""

DARK_QSS = """
QMainWindow { background: #1e242b; }
QToolBar { background:#262e37; border:0px; spacing:6px; padding:4px; }
QToolButton { background:#343e49; border:1px solid #465360; border-radius:6px; padding:6px 10px; color:#f0f3f5; }
QToolButton:hover { background:#40505d; }
QToolButton:pressed { background:#2d3a44; }
QTreeWidget { background:#262e37; border:1px solid #465360; border-radius:6px; color:#e2e6ea; }
QTreeWidget::item:selected { background:#2d81d2; color:white; }
QLineEdit { background:#2a333d; border:1px solid #465360; border-radius:6px; padding:4px 8px; color:#e2e6ea; }
QPushButton { background:#2d81d2; color:white; border-radius:6px; padding:8px 14px; font-weight:600; }
QPushButton:hover { background:#3b8fe0; }
QPushButton:pressed { background:#1f5b90; }
QLabel#AppTitle { font-size:32px; font-weight:800; color:#4fa8ff; letter-spacing:2px; }
QLabel#OrgSubtitle { font-size:15px; font-weight:500; color:#5ed4b9; letter-spacing:1px; }
QLabel#previewLabel { background:#262e37; border:1px dashed #465360; color:#95a2af; border-radius:10px; padding:28px; }
QStatusBar { background:#262e37; border-top:1px solid #465360; color:#d8dde2; }
QProgressBar { background:#343e49; border:1px solid #465360; border-radius:6px; height:18px; }
QProgressBar::chunk { background:#2d81d2; border-radius:6px; }
"""

class ThemeManager:
    def __init__(self):
        self.current = 'light'
    def apply(self, mode: str):
        if mode not in ('light','dark'):
            mode = 'light'
        self.current = mode
        qss = LIGHT_QSS if mode == 'light' else DARK_QSS
        QApplication.instance().setStyleSheet(qss)
    def toggle(self):
        self.apply('dark' if self.current=='light' else 'light')

# Singleton simple
_theme_manager = ThemeManager()

def theme_manager():
    return _theme_manager
