# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_cursor_info.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Data Class que guarda informações sobre a posição do cursor dentro da Data Window

Histórico:
       16/08/2026 - Implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class TraceCursorInfo:
    trace_index: int
    sample_index: int

    time_ms: float
    amplitude: float

    headers: Mapping[str, int | float | str]