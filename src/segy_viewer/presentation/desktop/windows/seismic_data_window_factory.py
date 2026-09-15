# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window_factory.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Factory que cria uma SeismicDataWindow
Histórico:
       14/09/2026 - Criação da Tool Bar
===============================================================================
"""
from pathlib import Path
from PySide6.QtCore import QRect
from segy_viewer import AppConfig
from segy_viewer.application.headers import SegyViewerHeaderDictionary
from segy_viewer.application.seismic_data_window import TraceBuffer, TraceOrderIndex
from segy_viewer.application.seismic_data_window.seismic_data_window_use_cases import SeismicDataWindowUseCases
from segy_viewer.application.seismic_data_window.services import SeismicDataSession
from segy_viewer.infrastructure.segy.segy_data_source import SegyDataSource
from segy_viewer.presentation.desktop.windows import SeismicDataWindow

class SeismicDataWindowFactory:
    def create(self, path: Path, config: AppConfig, initial_geometry: QRect) -> SeismicDataWindow:
        # --------------------------------------------------------------
        # Infrastructure
        # --------------------------------------------------------------
        data_source = SegyDataSource()

        # --------------------------------------------------------------
        # Application
        # --------------------------------------------------------------
        trace_buffer = TraceBuffer(buffer_ratio=0.10)
        trace_order_index = TraceOrderIndex()
        header_dictionary = SegyViewerHeaderDictionary()
        session = SeismicDataSession(data_source=data_source,
                                     trace_order_index=trace_order_index,
                                     trace_buffer=trace_buffer,
                                     header_dictionary=header_dictionary)

        use_cases = SeismicDataWindowUseCases(session=session)

        # --------------------------------------------------------------
        # Presentation
        # --------------------------------------------------------------
        return SeismicDataWindow(path=path,
                                 config=config,
                                 use_cases=use_cases,
                                 initial_geometry=initial_geometry)