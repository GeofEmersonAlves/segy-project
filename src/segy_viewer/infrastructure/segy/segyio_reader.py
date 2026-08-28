# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyio_reader.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que faz a leitura do arquivo segy utilizando a biblioteca segyio
    esta classe é uma implementação da Interface SeismicReader

Histórico:
       07/08/2026 - Início da implementação da Classe
       09/08/2026 - Implementação dos metodos read_trace_header, read_trace, read_traces e read_trace_headers
       10/08/2026 - Implementação do metodo read_samples_matrix, pensei neste método pois com uma matrix
                 será mais fácil e perfomático fazer cálculos com as amostras dos traços
===============================================================================
"""
import segyio
import numpy as np
from numpy.typing import NDArray
from collections.abc import Iterator
from typing import Self
from pathlib import Path
from segy_viewer.domain.files.seismic_reader import SeismicReader
from segy_viewer.domain.headers import ByteOrder, SegyBinaryHeader, SegyTextHeader, SegyTraceHeader, HeaderDataType
from segy_viewer.domain.headers.trace_header_fields import TRACE_HEADER_FIELDS
from segy_viewer.domain.traces.seismic_trace import SeismicTrace
from segy_viewer.infrastructure.segy import SegyRawReader

class SegyioReader(SeismicReader):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._segy_file: segyio.SegyFile | None = None
        self._raw_reader:SeismicReader = SegyRawReader(self._path)

    @property
    def is_open(self) -> bool:
        return self._segy_file is not None

    @property
    def trace_count(self) -> int:
        segy_file = self._require_open()
        return segy_file.tracecount

    def open(self) -> None:
        if self.is_open:
            return

        if not self._path.exists():
            raise FileNotFoundError(
                f"Arquivo SEG-Y não encontrado: {self._path}"
            )

        self._segy_file = segyio.open(
            str(self._path),
            mode="r",
            strict=False,
            ignore_geometry=True,
        )

    def close(self) -> None:
        if self._segy_file is None:
            return

        self._segy_file.close()
        self._segy_file = None

    def read_text_header(self) -> SegyTextHeader:
        _segy_file = self._require_open()
        self._raw_reader.open()
        segy_text_header = None
        try:
            segy_text_header: SegyTextHeader = self._raw_reader.read_text_header()
        finally:
            self._raw_reader.close()

            if segy_text_header is None:
                text = bytes(_segy_file.text[0]).decode("ascii")
                cards = tuple(text[i:i + 80] for i in range(0, 3200, 80))
                segy_text_header = SegyTextHeader(cards)

            return segy_text_header

    def read_binary_header(self) -> SegyBinaryHeader:
        _segy_file = self._require_open()

        binary = _segy_file.bin
        values = {
            # ----------------------------------------------------------
            # Bytes 3201-3212
            # Identificação
            # ----------------------------------------------------------
            "job_id":
                binary[segyio.BinField.JobID],

            "line_number":
                binary[segyio.BinField.LineNumber],

            "reel_number":
                binary[segyio.BinField.ReelNumber],

            # ----------------------------------------------------------
            # Bytes 3213-3224
            # Traços e amostragem
            # ----------------------------------------------------------
            "data_traces_per_ensemble":
                binary[segyio.BinField.Traces],

            "auxiliary_traces_per_ensemble":
                binary[segyio.BinField.AuxTraces],

            "sample_interval":
                binary[segyio.BinField.Interval],

            "original_sample_interval":
                binary[segyio.BinField.IntervalOriginal],

            "samples_per_trace":
                binary[segyio.BinField.Samples],

            "original_samples_per_trace":
                binary[segyio.BinField.SamplesOriginal],

            # ----------------------------------------------------------
            # Bytes 3225-3232
            # Formato, fold e ordenação
            # ----------------------------------------------------------
            "sample_format_code":
                binary[segyio.BinField.Format],

            "ensemble_fold":
                binary[segyio.BinField.EnsembleFold],

            "trace_sorting_code":
                binary[segyio.BinField.SortingCode],

            "vertical_sum_code":
                binary[segyio.BinField.VerticalSum],

            # ----------------------------------------------------------
            # Bytes 3233-3248
            # Sweep
            # ----------------------------------------------------------
            "sweep_frequency_start":
                binary[segyio.BinField.SweepFrequencyStart],

            "sweep_frequency_end":
                binary[segyio.BinField.SweepFrequencyEnd],

            "sweep_length":
                binary[segyio.BinField.SweepLength],

            "sweep_type_code":
                binary[segyio.BinField.Sweep],

            "sweep_trace_number":
                binary[segyio.BinField.SweepChannel],

            "sweep_taper_length_start":
                binary[segyio.BinField.SweepTaperStart],

            "sweep_taper_length_end":
                binary[segyio.BinField.SweepTaperEnd],

            "taper_type_code":
                binary[segyio.BinField.Taper],

            # ----------------------------------------------------------
            # Bytes 3249-3260
            # Correlação, ganho, amplitude, unidades e polaridade
            # ----------------------------------------------------------
            "correlated_data_traces":
                binary[segyio.BinField.CorrelatedTraces],

            "binary_gain_recovered":
                binary[segyio.BinField.BinaryGainRecovery],

            "amplitude_recovery_method":
                binary[segyio.BinField.AmplitudeRecovery],

            "measurement_system":
                binary[segyio.BinField.MeasurementSystem],

            "impulse_signal_polarity":
                binary[segyio.BinField.ImpulseSignalPolarity],

            "vibratory_polarity_code":
                binary[segyio.BinField.VibratoryPolarity],

            # ----------------------------------------------------------
            # Bytes 3501-3506
            # Revisão SEG-Y
            # ----------------------------------------------------------
            "revision_major":
                binary[segyio.BinField.SEGYRevision],

            "revision_minor":
                binary[segyio.BinField.SEGYRevisionMinor],

            "fixed_length_trace_flag":
                binary[segyio.BinField.TraceFlag],

            "extended_textual_header_count":
                binary[segyio.BinField.ExtendedHeaders],
        }

        return SegyBinaryHeader(values=values, byte_order=ByteOrder.BIG_ENDIAN, validate_revision=False)

    def read_trace_header(self,index: int) -> SegyTraceHeader:
        """Lê somente o header do traço."""
        segy_file = self._require_open()

        if not 0 <= index < segy_file.tracecount:
            raise IndexError(f"Índice de traço fora do intervalo: {index}. "
                             f"O arquivo possui {segy_file.tracecount} traços.")

        header = segy_file.header[index]
        values = {}

        for field in TRACE_HEADER_FIELDS:
            if field.data_type is HeaderDataType.RAW_BYTES:
                values[field.name] = None
                continue

            values[field.name] = header[field.byte_start]

        return SegyTraceHeader(values=values, byte_order=ByteOrder.BIG_ENDIAN)

    def read_samples(self, index: int) -> np.ndarray:
        segy_file = self._require_open()
        return segy_file.trace[index]

    def read_samples_matrix(self, start: int, stop: int) -> NDArray[np.float32]:
        """
        Retorna uma Matrix com as amostras de vários traços.
        Cada coluna da matriz representa um traço e cada linha representa uma amostra.
                                TRAÇOS
                     100    101    102    103
                   ┌───────────────────────────
        amostra 0  │ 1.2    0.9    1.0    1.3
        amostra 1  │ 1.4    1.1    0.7    1.2
        amostra 2  │ 0.8    1.5    0.3    0.9
        amostra 3  │ 0.2    0.6    0.8    1.1
           ...     │ ...    ...    ...    ...
        amostra N  │ ...
                   └───────────────────────────
        """
        if not 0 <= start < stop <= self.trace_count:
            raise IndexError(
                             f"Intervalo de traços inválido: [{start}, {stop}). "
                             f"O arquivo possui {self.trace_count} traços."
                            )

        traces = [self.read_samples(index) for index in range(start, stop) ]

        return np.column_stack(traces)

    def read_trace(self, index: int) -> SeismicTrace:
        """Lê um traço completo: header + samples."""
        return SeismicTrace(index = index,
                            header=self.read_trace_header(index),
                            samples=self.read_samples(index))

    def read_traces(self, start: int, stop: int) -> list[SeismicTrace]:
        """Lê vários traços completos: headers + samples."""

        if not 0 <= start < stop <= self.trace_count:
            raise IndexError(f"Intervalo de traços inválido: [{start}, {stop})."
                             f"O arquivo possui {self.trace_count} traços.")

        traces = []
        for index in range(start, stop):
            trace = self.read_trace(index)
            traces.append(trace)

        return traces

    def read_trace_headers(self, start: int, stop: int ) -> list[SegyTraceHeader]:
        """Lê somente os headers dos traços."""

        if not 0 <= start < stop <= self.trace_count:
            raise IndexError(f"Intervalo de traços inválido: [{start}, {stop})."
                             f"O arquivo possui {self.trace_count} traços.")
        headers = []
        for index in range(start, stop):
            header = self.read_trace_header(index)
            headers.append(header)

        return headers

    def iter_traces(self, start: int = 0, stop: int | None = None, ) -> Iterator[SeismicTrace]:
        if stop is None:
            stop = self.trace_count

        for index in range(start, stop):
            yield self.read_trace(index)

    def _require_open(self) -> segyio.SegyFile:
        if self._segy_file is None:
            raise RuntimeError(
                f"O arquivo {self._path} não está aberto. "
                "Execute open() antes da leitura."
            )

        return self._segy_file

    #Métodos do protocolo de context manager
    # Com esses dois metodos abaixo  posso fazer
    # with SegyioReader(path) as reader:
    #      binary_header = reader.read_binary_header()
    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

