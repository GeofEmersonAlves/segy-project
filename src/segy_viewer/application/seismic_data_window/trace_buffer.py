# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_buffer.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Calcula a faixa de posições de traços que deve ser mantida carregada
    para atender ao viewport da SeismicDataWindow.
        O buffer adiciona uma quantidade extra de traços antes e depois da
    região visível, reduzindo a necessidade de novas leituras durante
    pequenos deslocamentos horizontais.

        Esta classe trabalha exclusivamente com posições de visualização
    (trace positions), e não com índices físicos dos traços no arquivo.

Histórico:

       14/09/2026 - Implementação da classe
===============================================================================
"""

class TraceBuffer:
    def __init__(self, buffer_ratio: float = 0.10) -> None:
        if buffer_ratio < 0:
            raise ValueError("buffer_ratio must be greater than or equal to zero.")
        self._buffer_ratio = buffer_ratio

    # ------------------------------------------------------------------
    # Calculate range
    # ------------------------------------------------------------------
    def calculate_range(self,first_trace_position: int,
                             trace_count: int,
                             total_trace_count: int,) -> tuple[int, int]:
        """
        Calcula a faixa de posições que deverá ser carregada.
        Parameters
        ----------
        first_trace_position:
            Primeira posição visível no viewport.
        trace_count:
            Quantidade de traços visíveis no viewport.
        total_trace_count:
            Quantidade total de posições disponíveis.

        Returns
        -------
        tuple[int, int]
            (first_position, last_position)
            Os limites são inclusivos.

        Example
        -------
        Para:
            first_trace_position = 1000
            trace_count = 300
            buffer_ratio = 0.10
        o viewport ocupa:
            1000 ... 1299
        e o buffer solicitado será aproximadamente:

            970 ... 1329
        """

        self._validate(first_trace_position=first_trace_position,
                       trace_count=trace_count,
                       total_trace_count=total_trace_count)

        # --------------------------------------------------------------
        # Última posição visível
        # --------------------------------------------------------------
        last_trace_position = (first_trace_position + trace_count - 1)

        # --------------------------------------------------------------
        # Quantidade de traços adicionais em cada lado
        # --------------------------------------------------------------
        buffer_size = round(trace_count * self._buffer_ratio)

        # --------------------------------------------------------------
        # Expande o viewport
        # --------------------------------------------------------------
        first_buffer_position = (first_trace_position - buffer_size)
        last_buffer_position = (last_trace_position + buffer_size)

        # --------------------------------------------------------------
        # Limita ao início e ao final dos dados
        # --------------------------------------------------------------
        first_buffer_position = max(0, first_buffer_position)
        last_buffer_position = min(total_trace_count - 1,last_buffer_position)

        return (first_buffer_position, last_buffer_position)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    @staticmethod
    def _validate(first_trace_position: int, trace_count: int, total_trace_count: int) -> None:
        if total_trace_count <= 0:
            raise ValueError("total_trace_count must be greater than zero.")

        if trace_count <= 0:
            raise ValueError("trace_count must be greater than zero.")

        if first_trace_position < 0:
            raise ValueError("first_trace_position cannot be negative.")

        if first_trace_position >= total_trace_count:
            raise ValueError("first_trace_position is outside the available trace range.")

        last_trace_position = (first_trace_position + trace_count - 1)

        if last_trace_position >= total_trace_count:
            raise ValueError("The viewport extends beyond the available trace range.")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def buffer_ratio(self) -> float:
        return self._buffer_ratio