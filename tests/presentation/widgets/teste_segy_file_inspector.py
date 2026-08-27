import sys
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication
from setuptools.command.setopt import config_file

from segy_viewer.presentation.desktop.widgets import SegyFileInspector
from segy_viewer.infrastructure.segy import SegyFile
from segy_viewer.application.use_cases import SegyFileInspectorUseCases
from segy_viewer import AppConfig

path_segy_file = Path("C:/") / "Users" /"Emerson" / "Documents" / "ANP" /  "SEGY" / "SISMICA" /"0328-SW036.sgy"
# path_segy_file2 = Path("H:/") / "ENTREGA - ANP" / "SISMICA" / "0328-SW033.sgy"

def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

def inspector_is_empty():
    print("Não há dados para mostar")

def inspetor_not_empty():
    print("agora tem valores")

if __name__ == "__main__":

    app = QApplication(sys.argv)
    use_cases = SegyFileInspectorUseCases(file_factory=create_segy_file)
    status_bar_button_style = AppConfig.status_bar_button_style

    segy_inspector = SegyFileInspector(inspector_use_cases=use_cases, status_bar_button_style=status_bar_button_style)
    segy_inspector.segy_inspector_empty.connect(inspector_is_empty)
    segy_inspector.segy_inspector_has_data.connect(inspetor_not_empty)

    segy_inspector.segy_path = None
    segy_inspector.segy_path = path_segy_file

    segy_inspector.show()

    sys.exit(app.exec())