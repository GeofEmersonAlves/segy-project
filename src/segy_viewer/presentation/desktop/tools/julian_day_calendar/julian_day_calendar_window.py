# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : julian_day_calendar_window.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria a janela da ferramenta Julian Day Calendar
Histórico:
       02/09/2026 - Inicio da implementacao da classe
===============================================================================
"""
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from segy_viewer.resources import resource_path

_UNDER_CONSTRUCTION_IMG = resource_path("resources/images/under_construction.png")

class JulianDayCalendarWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Julian Day Calendar")
        label = QLabel(self)

        pixmap = QPixmap(_UNDER_CONSTRUCTION_IMG)
        pixmap = pixmap.scaled(
            pixmap.width() // 2,
            pixmap.height() // 2,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        label.setPixmap(pixmap)
        close_button  = QPushButton(self)
        close_button .setText("Close")
        close_button.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(close_button)



