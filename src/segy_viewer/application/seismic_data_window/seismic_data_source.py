# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window_use_cases.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Contrato para acesso aos dados necessários pela SeismicDataSession.
        A SeismicDataSource abstrai a origem física dos dados sísmicos.
        A camada application utiliza este contrato sem precisar conhecer o
    formato do arquivo, biblioteca utilizada para leitura ou mecanismo de
    armazenamento dos dados.
    Uma implementação concreta pode utilizar, por exemplo:
        - SEG-Y através do SegyioReader;
        - outro formato sísmico;
        - banco de dados;
        - cache persistente;
        - outra fonte de dados.

Histórico:
       14/09/2026 - Criação da classe
===============================================================================
"""
from pathlib import Path
from typing import Protocol
import numpy as np
from numpy.typing import NDArray


class SeismicDataSource(Protocol):
    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def open(self, path: Path) -> None:
        """
        Abre a fonte de dados.
        """
        ...

    def close(self) -> None:
        """
        Fecha a fonte de dados.
        """
        ...

    # ------------------------------------------------------------------
    # General information
    # ------------------------------------------------------------------
    @property
    def trace_count(self) -> int:
        """
        Quantidade total de traços disponíveis.
        """
        ...

    @property
    def sample_count(self) -> int:
        """
        Quantidade de amostras por traço.
        """
        ...

    @property
    def sample_interval_us(self) -> int:
        """
        Intervalo de amostragem em microssegundos.
        """
        ...

    # ------------------------------------------------------------------
    # Samples
    # ------------------------------------------------------------------
    def read_samples(self, trace_indices: NDArray[np.int64]) -> NDArray[np.float32]:
        """
        Lê as amostras dos índices físicos informados.

        Parameters
        ----------
        trace_indices:
            Índices físicos dos traços na fonte de dados.

        Returns
        -------
        NDArray[np.float32]
            Matriz contendo as amostras dos traços.
        """
        ...

    # ------------------------------------------------------------------
    # Trace header
    # ------------------------------------------------------------------
    def read_trace_header_values(self, trace_indices: NDArray[np.int64], field: str) -> NDArray:
        """
        Lê um campo do trace header para os índices físicos informados.
        Parameters
        ----------
        trace_indices:
            Índices físicos dos traços.
        field:
            Nome do campo na fonte de dados.
            Exemplo:

                "receiver_group_elevation"
        Returns
        -------
        NDArray
            Valores do campo solicitado na mesma ordem dos
            trace_indices recebidos.
        """
        ...