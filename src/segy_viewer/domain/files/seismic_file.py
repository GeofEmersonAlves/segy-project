# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_file.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe abstrata SeimicFile

Histórico:
       05/08/2026 - Início da implementação da Classe
===============================================================================
"""
from abc import ABC, abstractmethod
from pathlib import Path

class SeismicFile(ABC):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._path.name

    @property
    def exists(self) -> bool:
        return self._path.exists()

    @property
    @abstractmethod
    def format_name(self) -> str:
        pass
        """Nome do formato do arquivo."""

    @property
    @abstractmethod
    def trace_count(self) -> int:
        pass
        """Quantidade de traços no arquivo."""

    @abstractmethod
    def open(self) -> None:
        pass
        """Abre o arquivo."""

    @abstractmethod
    def close(self) -> None:
        pass
        """Fecha o arquivo."""