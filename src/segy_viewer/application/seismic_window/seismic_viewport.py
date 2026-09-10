# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_viewport.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que é objeto central para representar o viewport, classe que será
    compartilhada pelos 3 widgets da Seismic Data Window, assim os 3 widgets apresentarão
    informações dos mesmos.

Histórico:

       04/09/2026 - Início da implementação
===============================================================================
"""

from dataclasses import dataclass

@dataclass
class SeismicViewport:
    first_trace: int = 0
    trace_count: int = 300

    selected_trace: int | None = None

    time_min_ms: float = 0.0
    time_max_ms: float | None = None
