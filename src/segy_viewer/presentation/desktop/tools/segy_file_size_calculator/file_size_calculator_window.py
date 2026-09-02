# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : file_size_calculator_window.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria a janela da Segy file size calculator
Histórico:
       02/09/2026 - Inicio da implementacao da classe
===============================================================================
"""
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

_BASE_DIR = Path(__file__).resolve().parents[6]
_UNDER_CONSTRUCTION_IMG = _BASE_DIR / "resources" / "images" / "under_construction.png"
class SegyFileSizeCalculatorWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Segy file size calculator")
        label = QLabel(self)
        pixmap = QPixmap(_UNDER_CONSTRUCTION_IMG)
        pixmap = pixmap.scaled(
            pixmap.width() // 2,
            pixmap.height() // 2,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(pixmap)
        close_button = QPushButton(self)
        close_button.setText("Close")
        close_button.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(close_button)


