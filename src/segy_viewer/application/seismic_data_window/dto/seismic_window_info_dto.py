# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_window_info_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Data Class que guarda informações gerais do conjunto de dados sísmicos aberto
    pela SeismicDataWindow.
       Esses dados pertencem à sessão de visualização e permanecem constantes durante
    a navegação entre os traços.

Histórico:
       14/09/2026 - Implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class SeismicWindowInfoDTO:
    path: Path
    trace_count: int
    sample_count: int
    sample_interval_us: int
    record_length_ms: float