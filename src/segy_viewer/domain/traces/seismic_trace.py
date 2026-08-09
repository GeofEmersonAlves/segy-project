# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_trace.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que representa um traço sismico.

Histórico:
       08/08/2026 - Início da implementação da Classe
===============================================================================
"""
import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from typing import Self
from segy_viewer.domain.headers.trace_header import SegyTraceHeader

@dataclass(slots=True)
class SeismicTrace:
    """
        Representa um traço sísmico composto por seu Trace Header
        e suas amostras de amplitude.
    """
    index: int
    header: SegyTraceHeader
    samples:  NDArray[np.float32]

    @property
    def sample_interval_us(self) -> int:
        return self.header.sample_interval

    @property
    def sample_count(self) -> int:
        return self.samples.size

    @property
    def rms(self) -> float:
        return float(np.sqrt(np.mean(self.samples ** 2) ) )

    @property
    def maximum_amplitude(self) -> float:
        return float(np.max(self.samples))

    @property
    def minimum_amplitude(self) -> float:
        return float(np.min(self.samples))

    @property
    def duration_ms(self) -> float:
        if self.sample_count == 0:
            return 0.0

        return (
                (self.sample_count - 1) * self.header.sample_interval_ms
              )

    def copy(self) -> "SeismicTrace":
        return SeismicTrace(
            index=self.index,
            header=self.header,
            samples=self.samples.copy(),
        )