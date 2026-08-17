import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from segy_viewer.presentation.desktop.widgets import SegyFileBrowser
from segy_viewer import AppConfig

def _on_segy_file_selected(path: Path):
    print(path)

def _on_path_changed(path: Path):
    print(f'Diretório alterado: {path}')
    # resp = input('Deseja alterar o caminho? [S/N]')
    # if resp.upper() == 'S':
    #     segy_browser.change_path(Path("H:\\")  )

if __name__ == "__main__":
    config = AppConfig()
    segy_extensions = config.segy_extensions
    button_style = config.button_style
    app = QApplication(sys.argv)

    segy_browser = SegyFileBrowser(segy_extensions, button_style)
    segy_browser.file_selected.connect(_on_segy_file_selected)
    segy_browser.path_changed.connect(_on_path_changed)
    segy_browser.show()
    sys.exit(app.exec())
