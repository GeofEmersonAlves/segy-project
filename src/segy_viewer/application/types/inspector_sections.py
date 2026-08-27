# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : inspector_sections.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Tipo de dados do para as abas, usecase e window

Histórico:
       17/08/2026 - Criação do tipo
===============================================================================
"""

from enum import StrEnum

class InspectorSectionType(StrEnum):
    SUMMARY = "Summary"
    TEXT_HEADER = "Text Header"
    BIN_HEADER = "Bin Header"
    TRACE_HEADER = "Trace Header"