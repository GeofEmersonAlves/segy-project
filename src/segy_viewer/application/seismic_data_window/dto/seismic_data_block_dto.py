# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_block_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Bloco de dados sísmicos carregado para atender ao viewport atual.
        O bloco pode conter mais traços que a região visível devido à estratégia
    de buffer/prefetch utilizada pela camada application.
       As posições de visualização não precisam corresponder aos índices físicos
    dos traços no arquivo
    (Preparado para a evolução para o calculo de métricas do dado).
------------------------------------------------------------------------------
    Amostras dos traços.
       Shape: (trace_count, sample_count)

    Valores dos headers solicitados pelo TraceHeaderView.
       Exemplo:{
                "CHANNEL_NO": np.ndarray(...),
                "FIELD_RECORD_NO": np.ndarray(...),
                }

    Valores dos headers/atributos solicitados pelo TraceAttributeGraphView.
       Inicialmente: {"ELEV_REC": np.ndarray(...) }
------------------------------------------------------------------------------

Histórico:
       14/09/2026 - Implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

@dataclass(frozen=True, slots=True)
class SeismicDataBlockDTO:
    trace_positions: NDArray[np.int64]   # Posições dos traços no espaço de visualização.
    trace_indices: NDArray[np.int64]     # Índices físicos dos traços no arquivo SEG-Y.
    samples: NDArray[np.floating]        # O mesmo da camada domain para as amostras
    trace_header_values: dict[str, NDArray]
    graph_header_values: dict[str, NDArray]