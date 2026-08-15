import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from segy_viewer.presentation.desktop.widgets import SegyFileBrowser
from segy_viewer import AppConfig

def _on_segy_file_selected(path: Path):
    print(path)

def _on_path_changed(path: Path):
    print(f'Diretório alterado: {path}')

if __name__ == "__main__":
    config = AppConfig()
    segy_extensions = config.segy_extensions
    button_style = config.button_style
    app = QApplication(sys.argv)

    browser = SegyFileBrowser(segy_extensions, button_style)
    browser.file_selected.connect(_on_segy_file_selected)
    browser.path_changed.connect(_on_path_changed)
    browser.show()

    sys.exit(app.exec())
