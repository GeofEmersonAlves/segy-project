# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segy_raw_reader.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que faz a leitura dos bytes fisicos arquivo segy
    esta classe é uma implementação da Interface SeismicReader

Histórico:
       28/08/2026 - Implementação da Classe
===============================================================================
"""
from pathlib import Path
from collections.abc import Iterator

from segy_viewer.domain.files import SeismicReader
from segy_viewer.domain.headers import SegyTextHeader, SegyBinaryHeader, TextHeaderEncoding
from segy_viewer.domain.traces.seismic_trace import SeismicTrace

class SegyRawReader(SeismicReader):

    TEXT_HEADER_SIZE = 3200

    def __init__(self, path: Path) -> None:
        self._path = path
        self._file = None

    @property
    def is_open(self) -> bool:
        return self._file is not None

    def open(self) -> None:
        if self.is_open:
            return

        self._file = self._path.open("rb")

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

    def _require_open(self):
        if self._file is None:
            raise RuntimeError(
                f"O arquivo {self._path} não está aberto. "
                "Execute open() antes da leitura."
            )

        return self._file

    def read_text_header(self) -> SegyTextHeader:
        file = self._require_open()

        file.seek(0)
        raw_text = file.read(self.TEXT_HEADER_SIZE)

        encoding = self._detect_text_header_encoding(raw_text)

        if encoding == TextHeaderEncoding.ASCII:
            text = raw_text.decode("ascii")

        elif encoding == TextHeaderEncoding.EBCDIC:
            text = raw_text.decode("cp500")

        else:
            raise ValueError("Unable to determine Text Header encoding.")

        cards = tuple(
            text[i:i + 80]
            for i in range(0, 3200, 80)
        )

        return SegyTextHeader(cards=cards,
                              encoding=encoding
                             )

    @property
    def trace_count(self) -> int:
        raise NotImplementedError

    def read_binary_header(self) -> SegyBinaryHeader:
        raise NotImplementedError

    def read_trace(self, index: int) -> SeismicTrace:
        raise NotImplementedError

    def iter_traces(
        self,
        start: int = 0,
        stop: int | None = None,
    ) -> Iterator[SeismicTrace]:
        raise NotImplementedError

    def _decode_text_header(self, raw_text: bytes,) -> tuple[str, TextHeaderEncoding]:
        encoding = self._detect_text_header_encoding(raw_text)

        match encoding:

            case TextHeaderEncoding.ASCII:
                text = raw_text.decode("ascii")

            case TextHeaderEncoding.EBCDIC:
                text = raw_text.decode("cp500")

            case _:
                raise ValueError(
                    "Unable to determine Text Header encoding."
                )

        return text, encoding

    @staticmethod
    def _detect_text_header_encoding(raw_text: bytes) -> TextHeaderEncoding:

        try:
            text = raw_text.decode("ascii")

            if text.startswith("C"):
                return TextHeaderEncoding.ASCII

        except UnicodeDecodeError:
            pass

        try:
            text = raw_text.decode("cp500")

            if text.startswith("C"):
                return TextHeaderEncoding.EBCDIC

        except UnicodeDecodeError:
            pass

        return TextHeaderEncoding.UNKNOWN