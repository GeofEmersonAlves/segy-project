# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_header_view.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que cria o Widget TraceHeaderView, responsável por mostrar os headers
    dos dados contitidos em um segy. Inicialmente os tracos aparecem somente com o Channel no cabeçalho

    Channel: trace_number_field_record (bytes 13-16)
Histórico:
       05/09/2026 - Início da criação do Widget
       09/09/2026 - Inicio da implementação do método paintEvent()
===============================================================================
"""
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget

class TraceHeaderView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._displayed_headers: dict[str, str] = {"CHAN": "CHANNEL_NO" }


    @property
    def displayed_headers(self) -> dict[str, str]:
        return self._displayed_headers

    @displayed_headers.setter
    def displayed_headers(self, headers: dict[str, str] ) -> None:
        self._displayed_headers = headers
        self.repaint()
        self.update()


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.begin(self)



        painter.end()