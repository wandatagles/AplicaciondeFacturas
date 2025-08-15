
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
import sys
import logging
from src.core.config import get_settings

def _configure_logging():
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def main():
    _configure_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
