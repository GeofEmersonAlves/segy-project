# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_order_index.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
    Mantém o mapeamento entre posições de visualização e índices físicos dos traços na fonte de dados.
    A posição de visualização representa a posição do traço na SeismicDataWindow.
    O índice físico representa a posição real do traço na fonte de dados.
    Inicialmente:
        trace_position == trace_index

    Exemplo:
        posição:       0  1  2  3  4
                       │  │  │  │  │
                       ▼  ▼  ▼  ▼  ▼
        índice físico: 0  1  2  3  4

    Futuramente, após uma ordenação:
        posição:       0   1   2   3   4
                       │   │   │   │   │
                       ▼   ▼   ▼   ▼   ▼
        índice físico: 120 121 35  36  400

    Dessa forma, os widgets continuam trabalhando com posições de visualização
sem precisar conhecer a organização física dos dados.

Histórico:

       14/09/2026 - Implementação da classe
===============================================================================
"""
import numpy as np
from numpy.typing import NDArray

class TraceOrderIndex:
    def __init__(self) -> None:
        self._trace_indices: NDArray[np.int64] = np.empty(0,dtype=np.int64)

    # ------------------------------------------------------------------
    # Initialize
    # ------------------------------------------------------------------
    def initialize(self,trace_count: int) -> None:
        if trace_count < 0:
            raise ValueError("trace_count cannot be negative.")

        self._trace_indices = np.arange(trace_count, dtype=np.int64)

    # ------------------------------------------------------------------
    # Resolve position
    # ------------------------------------------------------------------
    def resolve_position(self, trace_position: int) -> int:
        """
        Retorna o índice físico correspondente a uma posição
        de visualização.
        """
        self._validate_position(trace_position)
        return int(self._trace_indices[trace_position])

    # ------------------------------------------------------------------
    # Resolve positions
    # ------------------------------------------------------------------
    def resolve_positions(self, trace_positions: list[int] | NDArray[np.int64]) -> NDArray[np.int64]:
        """
        Retorna os índices físicos correspondentes às posições
        de visualização informadas.
        """
        positions = np.asarray(trace_positions, dtype=np.int64)
        if positions.ndim != 1:
            raise ValueError("trace_positions must be one-dimensional.")

        if positions.size == 0:
            return np.empty(0, dtype=np.int64)

        if np.any(positions < 0):
            raise IndexError("trace_positions contains negative positions.")

        if np.any(positions >= self.trace_count):
            raise IndexError("trace_positions contains positions outside the available range.")

        return self._trace_indices[positions]

    # ------------------------------------------------------------------
    # Set order
    # ------------------------------------------------------------------
    def set_order(self,trace_indices: list[int] | NDArray[np.int64]) -> None:
        """
        Define uma nova ordem de visualização.

        Cada elemento representa o índice físico do traço que deverá
        ocupar aquela posição de visualização.

        Exemplo:

            set_order([120, 121, 35, 36])

        produz:

            position 0 -> trace index 120
            position 1 -> trace index 121
            position 2 -> trace index 35
            position 3 -> trace index 36
        """
        indices = np.asarray(trace_indices, dtype=np.int64)
        if indices.ndim != 1:
            raise ValueError("trace_indices must be one-dimensional.")

        if np.any(indices < 0):
            raise ValueError("trace_indices cannot contain negative indices.")

        self._trace_indices = indices.copy()

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Retorna para a ordem natural dos traços.
        """
        self._trace_indices = np.arange(self.trace_count, dtype=np.int64)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate_position(self, trace_position: int) -> None:
        if trace_position < 0:
            raise IndexError("trace_position cannot be negative.")

        if trace_position >= self.trace_count:
            raise IndexError("trace_position is outside the available range.")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def trace_count(self) -> int:
        return int(self._trace_indices.size)

    @property
    def trace_indices(self) -> NDArray[np.int64]:
        return self._trace_indices.copy()