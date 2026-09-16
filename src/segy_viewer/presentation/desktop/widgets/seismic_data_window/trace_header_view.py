# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_header_view.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que cria o TraceHeaderView filho de HSynchronizedSeismicDataWidget, responsável por mostrar os headers
    dos dados contitidos em um segy. Inicialmente os tracos aparecem somente com o Channel no cabeçalho

    Channel: trace_number_field_record (bytes 13-16)
Histórico:
       05/09/2026 - Início da criação do Widget
       09/09/2026 - Inicio da implementação do método paintEvent()
===============================================================================
"""
import numpy as np
from PySide6.QtGui import QPaintEvent, QPainter, Qt
from numpy._typing import NDArray

from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget

class TraceHeaderView(HSynchronizedSeismicDataWidget):
    def __init__(self, viewport: SeismicViewport, parent=None):
        super().__init__(viewport=viewport,parent=parent)
        self._displayed_headers: dict[str, str] = {"CHAN": "CHANNEL_NO"}
        self._trace_positions: NDArray[np.int64] = np.empty(0, dtype=np.int64)
        self._trace_indices: NDArray[np.int64] = np.empty(0, dtype=np.int64)
        self._header_values: dict[str, NDArray] = {}

    def set_data(self, trace_positions: NDArray[np.int64],
                       trace_indices: NDArray[np.int64],
                       header_values: dict[str, NDArray]) -> None:

        self._trace_positions = trace_positions
        self._trace_indices = trace_indices
        self._header_values = header_values
        self.update()

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
        painter.drawText(event.rect(), Qt.AlignCenter,
                         f"{self._viewport.first_trace_position} - {self._viewport.time_max_ms}")
