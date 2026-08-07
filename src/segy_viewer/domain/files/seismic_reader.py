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
===============================================================================
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator

class SeismicReader(ABC):

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Indica se o arquivo está aberto."""
        raise NotImplementedError

    @property
    @abstractmethod
    def trace_count(self) -> int:
        """Quantidade de traços disponíveis."""
        raise NotImplementedError

    @abstractmethod
    def open(self) -> None:
        """Abre o arquivo sísmico."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Fecha o arquivo sísmico."""
        raise NotImplementedError

    @abstractmethod
    def read_trace(self, index: int) -> "SeismicTrace":
        """Lê um traço pelo índice."""
        raise NotImplementedError

    @abstractmethod
    def iter_traces(
        self,
        start: int = 0,
        stop: int | None = None,
    ) -> Iterator["SeismicTrace"]:
        """Percorre os traços de um intervalo."""
        raise NotImplementedError