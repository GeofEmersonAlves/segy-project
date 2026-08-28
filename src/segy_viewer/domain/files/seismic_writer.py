# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_writer.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Implementação da interface SeismicWriter

Histórico:
       27/08/2026 - Implementação da classe
===============================================================================
"""
from abc import ABC, abstractmethod
from pathlib import Path


class SeismicWriter(ABC):

    @abstractmethod
    def write_text_header(self, text_header: str) -> None:
        ...