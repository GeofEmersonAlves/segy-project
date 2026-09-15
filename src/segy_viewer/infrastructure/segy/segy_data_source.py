# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segy_data_source.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
    Fonte de dados sísmicos baseada em arquivo SEG-Y.
    Implementa o contrato esperado por SeismicDataSource e funciona como adaptador
entre a camada application e o SegyioReader.

    Responsabilidades:
        - controlar o ciclo de vida do SegyioReader;
        - fornecer informações gerais necessárias pela sessão;
        - fornecer amostras para índices físicos de traços;
        - fornecer valores de campos específicos dos Trace Headers.

    Esta classe trabalha exclusivamente com índices físicos dos traços.
    Ela não conhece:
        - viewport;
        - posição de visualização;
        - buffer;
        - ordenação;
        - widgets da SeismicDataWindow.

Histórico:
      14/09/2026 - Implementação da classe
===============================================================================
"""
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from segy_viewer.infrastructure.segy import SegyioReader

class SegyDataSource:
    def __init__(self) -> None:
        self._reader: SegyioReader | None = None
        self._path: Path | None = None
        self._sample_count: int | None = None
        self._sample_interval_us: int | None = None

    # ==================================================================
    # LIFECYCLE
    # ==================================================================
    def open(self, path: Path) -> None:
        """
        Abre o arquivo SEG-Y e inicializa as informações gerais
        necessárias pela SeismicDataSession.
        """
        if self.is_open:
            raise RuntimeError("SEG-Y data source is already open.")

        reader = SegyioReader(path)
        reader.open()

        try:
            binary_header = reader.read_binary_header()
            self._reader = reader
            self._path = Path(path)
            self._sample_count = int(binary_header.samples_per_trace)
            self._sample_interval_us = int(binary_header.sample_interval)

        except Exception:
            reader.close()

            self._reader = None
            self._path = None
            self._sample_count = None
            self._sample_interval_us = None

            raise

    def close(self) -> None:
        """
        Fecha o SegyioReader e limpa o estado da fonte de dados.
        """
        if self._reader is None:
            return

        try:
            self._reader.close()

        finally:
            self._reader = None
            self._path = None
            self._sample_count = None
            self._sample_interval_us = None

    # ==================================================================
    # GENERAL INFORMATION
    # ==================================================================
    @property
    def trace_count(self) -> int:
        """
        Quantidade total de traços físicos existentes no arquivo.
        """
        reader = self._require_reader()

        return reader.trace_count

    @property
    def sample_count(self) -> int:
        """
        Quantidade de amostras por traço.
        """
        self._require_reader()
        if self._sample_count is None:
            raise RuntimeError("Sample count is not available.")

        return self._sample_count

    @property
    def sample_interval_us(self) -> int:
        """
        Intervalo de amostragem em microssegundos.
        """
        self._require_reader()
        if self._sample_interval_us is None:
            raise RuntimeError("Sample interval is not available.")

        return self._sample_interval_us

    # ==================================================================
    # SAMPLES
    # ==================================================================
    def read_samples(self, trace_indices: NDArray[np.int64]) -> NDArray[np.float32]:
        """
        Lê as amostras dos índices físicos informados.
        Os índices não precisam ser consecutivos e a ordem recebida é preservada.
        A matriz segue a convenção:
            shape = (sample_count, trace_count)
        Portanto:
            samples[:, i]
        representa todas as amostras do traço localizado na posição i do bloco solicitado.
        """
        reader = self._require_reader()
        indices = self._validate_trace_indices(trace_indices)

        if indices.size == 0:
            return np.empty((self.sample_count, 0), dtype=np.float32)

        return reader.read_samples_by_indices(indices)

    # ==================================================================
    # TRACE HEADER
    # ==================================================================
    def read_trace_header_values(self, trace_indices: NDArray[np.int64], field: str) -> NDArray:
        """
        Lê um campo do Trace Header para os índices físicos informados.
        Quando SegyTraceHeader possui uma propriedade pública com
     o mesmo nome do campo, o valor efetivo dessa propriedade é utilizado.
        Isso permite, por exemplo, que campos dependentes de escalares sejam retornados já convertidos:
            receiver_group_elevation
            source_surface_elevation
            source_depth
            source_x
            source_y
            group_x
            group_y
            shotpoint_number

        Quando não existe uma propriedade correspondente, é utilizado
        o valor bruto armazenado no Trace Header através de get().
        A ordem dos valores retornados é a mesma de trace_indices.
        """

        reader = self._require_reader()
        indices = self._validate_trace_indices(trace_indices)
        values = []

        for index in indices:
            trace_header = reader.read_trace_header(int(index))

            value = self._get_trace_header_value(trace_header, field)

            values.append(value)

        return np.asarray(values)

    # ==================================================================
    # TRACE HEADER VALUE
    # ==================================================================

    @staticmethod
    def _get_trace_header_value(trace_header: Any, field: str) -> Any:
        """
        Retorna preferencialmente o valor efetivo de um campo.

        Se SegyTraceHeader possuir uma propriedade pública com o
        mesmo nome, utiliza essa propriedade.

        Caso contrário, retorna o valor bruto através de get().
        """
        descriptor = getattr(type(trace_header), field, None)
        if isinstance(descriptor, property):
            return getattr(trace_header, field)

        return trace_header.get(field)

    # ==================================================================
    # VALIDATION
    # ==================================================================
    def _validate_trace_indices(self, trace_indices: NDArray[np.int64]) -> NDArray[np.int64]:
        """
        Valida e normaliza os índices físicos recebidos.
        """
        indices = np.asarray(trace_indices, dtype=np.int64)
        if indices.ndim != 1:
            raise ValueError("trace_indices must be one-dimensional.")

        if indices.size == 0:
            return indices

        if np.any(indices < 0):
            raise IndexError("trace_indices contains negative indices.")

        if np.any(indices >= self.trace_count):
            raise IndexError("trace_indices contains indices outside "
                             "the available trace range.")

        return indices

    # ==================================================================
    # INTERNAL
    # ==================================================================
    def _require_reader(self) -> SegyioReader:
        """
        Retorna o reader aberto.
        Raises
        ------
        RuntimeError
            Quando a fonte de dados ainda não foi aberta.
        """
        if self._reader is None:
            raise RuntimeError("SEG-Y data source is not open.")

        if not self._reader.is_open:
            raise RuntimeError("SEG-Y reader is not open.")

        return self._reader

    # ==================================================================
    # PROPERTIES
    # ==================================================================
    @property
    def is_open(self) -> bool:

        return (self._reader is not None
                and self._reader.is_open)

    @property
    def path(self) -> Path | None:
        return self._path