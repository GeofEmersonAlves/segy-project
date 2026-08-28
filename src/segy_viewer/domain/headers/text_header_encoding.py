# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : text_header_encoding.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
          Define a decodificação do Trace Header

Histórico:
       28/08/2026 - Implementação da Classe
===============================================================================
"""

from enum import Enum


class TextHeaderEncoding(Enum):
    ASCII = "ASCII"
    EBCDIC = "EBCDIC"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return self.value