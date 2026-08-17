# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyFile_inspection_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Data Class que guarda as infomacões de um arquivo segy,

Histórico:
       16/08/2026 - Implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
from segy_viewer.domain.headers import HeaderDict

@dataclass(frozen=True)
class SegyFileInspectionDTO:
    summary: str
    text_header: str
    binary_header: HeaderDict
    trace_header: HeaderDict
    trace_header_index: int