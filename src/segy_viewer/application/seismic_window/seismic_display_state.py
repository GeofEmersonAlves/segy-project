# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_display_state.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que representa o estado da janela

Histórico:

       04/09/2026 - Início da implementação
===============================================================================
"""

from dataclasses import dataclass

from segy_viewer.application.seismic_window.seismic_viewport import SeismicViewport

@dataclass
class SeismicDisplayState:
    viewport: SeismicViewport

    wiggle: bool = True
    variable_area: bool = False

    header_rows: tuple[str, ...] = ()
    graph_header: str | None = None