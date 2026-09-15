# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_session.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
      Classe que representa o contrato da sessão de dados da Seismic Data Window
      Contrato da sessão de dados utilizada pela Seismic Data Window.
        A implementação concreta será responsável por:
            - abrir o arquivo sísmico;
            - manter o arquivo aberto;
            - carregar blocos de dados;
            - aplicar buffer/prefetch;
            - resolver posições de visualização em índices físicos;
            - fechar o arquivo.

Histórico:
       14/09/2026 - Início da implementação
===============================================================================
"""
from pathlib import Path

from segy_viewer.application.headers import SegyViewerHeaderDictionary
from segy_viewer.application.seismic_data_window import SeismicViewport, TraceBuffer, TraceOrderIndex, SeismicDataSource
from segy_viewer.application.seismic_data_window.dto import SeismicWindowInfoDTO, SeismicDataBlockDTO

class SeismicDataSession:
    def __init__(self, data_source: SeismicDataSource,
                       trace_order_index: TraceOrderIndex,
                       trace_buffer: TraceBuffer,
                       header_dictionary: SegyViewerHeaderDictionary) -> None:

        self._data_source = data_source
        self._trace_order_index = trace_order_index
        self._trace_buffer = trace_buffer
        self._header_dictionary = header_dictionary
        self._path: Path | None = None
        self._is_open: bool = False
        self._window_info: SeismicWindowInfoDTO | None = None
        self._current_data_block: SeismicDataBlockDTO | None = None

    # ------------------------------------------------------------------
    # Open
    # ------------------------------------------------------------------
    def open(self, path: Path) -> SeismicWindowInfoDTO:
        if self._is_open:
            raise RuntimeError("Seismic data session is already open.")

        self._data_source.open(path)

        try:
            self._path = path
            trace_count = self._data_source.trace_count
            sample_count = self._data_source.sample_count
            sample_interval_us = self._data_source.sample_interval_us
            record_length_ms = (sample_count * sample_interval_us / 1000)
            self._trace_order_index.initialize(trace_count=trace_count)

            self._window_info = SeismicWindowInfoDTO(path=path,
                                                     trace_count=trace_count,
                                                     sample_count=sample_count,
                                                     sample_interval_us=sample_interval_us,
                                                     record_length_ms=record_length_ms)
            self._is_open = True
            return self._window_info

        except Exception:
            self._data_source.close()
            self._path = None
            self._window_info = None
            raise

    # ------------------------------------------------------------------
    # Load data
    # ------------------------------------------------------------------
    def load_data(self, viewport: SeismicViewport,
                        header_keys: tuple[str, ...],
                        graph_header_keys: tuple[str, ...]) -> SeismicDataBlockDTO:

        self._ensure_open()
        # --------------------------------------------------------------
        # Verifica se o bloco atualmente carregado ainda atende
        # completamente ao viewport.
        # --------------------------------------------------------------

        if self._current_block_contains_viewport(viewport):
            return self._current_data_block

        # --------------------------------------------------------------
        # Calcula a faixa de posições que deverá ser carregada.
        #
        # O TraceBuffer decide quanto será carregado além do viewport.
        # --------------------------------------------------------------
        first_position, last_position = (self._trace_buffer.calculate_range(first_trace_position=(viewport.first_trace_position),
                                                                            trace_count=viewport.trace_count,
                                                                            total_trace_count=(self._window_info.trace_count),
                                                                            )
                                        )
        # --------------------------------------------------------------
        # Posições no espaço de visualização.
        # --------------------------------------------------------------
        trace_positions = list( range(first_position, last_position + 1))

        # --------------------------------------------------------------
        # Resolve posição de visualização → índice físico.
        # --------------------------------------------------------------
        trace_indices = (self._trace_order_index.resolve_positions(trace_positions))

        # --------------------------------------------------------------
        # Headers necessários.
        #
        # Não devemos ler duas vezes um header que seja solicitado
        # simultaneamente pelo TraceHeaderView e pelo gráfico.
        # --------------------------------------------------------------
        required_header_keys = tuple(dict.fromkeys(header_keys + graph_header_keys))

        # --------------------------------------------------------------
        # Traduz as chaves amigáveis do SegyViewer para os campos
        # utilizados pela fonte de dados.
        # --------------------------------------------------------------
        source_header_fields = {key: self._resolve_header_source_field(key)
                                for key in required_header_keys}

        # --------------------------------------------------------------
        # Leitura das amostras
        # --------------------------------------------------------------
        samples = self._data_source.read_samples(trace_indices)

        # --------------------------------------------------------------
        # Leitura dos headers
        # --------------------------------------------------------------
        all_header_values = {}

        for key, source_field in (source_header_fields.items()):
            all_header_values[key] = (self._data_source.read_trace_header_values(trace_indices=trace_indices,
                                                                                 field=source_field))

        # --------------------------------------------------------------
        # Separa os headers destinados a cada widget.
        # --------------------------------------------------------------
        trace_header_values = {key: all_header_values[key]
                               for key in header_keys}

        graph_header_values = {key: all_header_values[key]
                               for key in graph_header_keys}

        # --------------------------------------------------------------
        # DTO
        # --------------------------------------------------------------
        self._current_data_block = SeismicDataBlockDTO(trace_positions=trace_positions,
                                                       trace_indices=trace_indices,
                                                       samples=samples,
                                                       trace_header_values= trace_header_values,
                                                       graph_header_values=graph_header_values)

        return self._current_data_block

    # ------------------------------------------------------------------
    # Header dictionary
    # ------------------------------------------------------------------
    def _resolve_header_source_field(self, header_key: str) -> str:
        item = self._header_dictionary.get(header_key)

        if item is None:
            raise KeyError(f"Header key not found: {header_key}")

        if item.source != "trace_header":
            raise ValueError(f"Header '{header_key}' is not provided by the trace header.")

        return item.source_field

    # ------------------------------------------------------------------
    # Current block
    # ------------------------------------------------------------------
    def _current_block_contains_viewport(self, viewport: SeismicViewport) -> bool:
        if self._current_data_block is None:
            return False

        positions = self._current_data_block.trace_positions
        if len(positions) == 0:
            return False

        block_first_position = positions[0]
        block_last_position = positions[-1]
        viewport_first_position = viewport.first_trace_position
        viewport_last_position = viewport.first_trace_position + viewport.trace_count - 1


        return (viewport_first_position >= block_first_position and viewport_last_position<= block_last_position)


    # ------------------------------------------------------------------
    # Close
    # ------------------------------------------------------------------
    def close(self) -> None:
        if not self._is_open:
            return

        try:
            self._data_source.close()

        finally:
            self._is_open = False
            self._path = None
            self._window_info = None
            self._current_data_block = None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _ensure_open(self) -> None:
        if not self._is_open:
            raise RuntimeError("Seismic data session is not open.")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def window_info(self) -> SeismicWindowInfoDTO | None:
        return self._window_info