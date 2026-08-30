# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : __main__.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Rotina main() da aplicação segu_viewer

       Para executar
       python -m segy_viewer

Histórico:
       28/08/2026 - Implementação da main()
===============================================================================
"""
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from segy_viewer.bootstrap import create_application
from segy_viewer import __version__
_BASE_DIR = Path(__file__).resolve().parents[2]
_APP_ICON = _BASE_DIR / "resources" / "icons" / "segyFile.ico"

def main() -> int:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(_APP_ICON)))

    app_name = f"Segy Viewer (Version {__version__})"
    app.setApplicationName(app_name)
    app.setApplicationDisplayName(app_name)
    app.setOrganizationName(app_name)

    main_window = create_application()
    main_window.setWindowTitle(app_name)
    main_window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())