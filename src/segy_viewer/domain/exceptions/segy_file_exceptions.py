# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segy_file_exceptions.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Exceções relacionadas aos arquivos SEG-Y.

Histórico:
       27/08/2026 - Implementação da Classe
===============================================================================
"""

class SegyFileInUseError(OSError):
    """
    Exceção-base para erros relacionados aos headers SEG-Y.
    """