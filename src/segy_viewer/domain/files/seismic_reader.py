# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_reader.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Implementação da interface SeismicReader

Histórico:
       05/08/2026 - Início da implementação da Classe
       10/08/2026 - Atualização da classe com inclusão de alguns metodos abstrados
===============================================================================
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator
from segy_viewer.domain.headers import SegyTextHeader, SegyBinaryHeader
from segy_viewer.domain.traces.seismic_trace import SeismicTrace

class SeismicReader(ABC):
    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Indica se o arquivo está aberto."""
        ...

    @property
    @abstractmethod
    def trace_count(self) -> int:
        """Quantidade de traços disponíveis."""
        ...

    @abstractmethod
    def open(self) -> None:
        """Abre o arquivo sísmico."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Fecha o arquivo sísmico."""
        ...

    @abstractmethod
    def read_text_header(self) -> SegyTextHeader:
        ...

    @abstractmethod
    def read_binary_header(self) -> SegyBinaryHeader:
        ...

    @abstractmethod
    def read_trace(self, index: int) -> SeismicTrace:
        """Lê um traço pelo índice."""
        ...

    @abstractmethod
    def iter_traces(self, start: int = 0, stop: int | None = None) -> Iterator[SeismicTrace]:
        """Percorre os traços de um intervalo."""
        ...