# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : check_response_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Data Class guarda o resultado de checagens


Histórico:
       26/08/2026 - Implementação da Classe
===============================================================================
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class CheckResponseDto:
    checked_pass: bool
    message: str
