# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segy_file.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe  SegyFile, representa um arquivo SEGY de dados sísmicos
         Se não for designado um SeismicReader na criação da classe, por padrão ela assume o SegyioReader.

SegyFile
   │
   ├── informações do arquivo
   │      ├── path
   │      ├── name
   │      ├── trace_count
   │      ├── text_header
   │      └── binary_header

   │
   └── reader
          │
          ├── read_samples()
          ├── read_trace_header()
          ├── read_trace_headers()
          ├── read_trace()
          ├── read_traces()
          └── iter_traces()


Histórico:
       10/08/2026 - Início da implementação da Classe
       27/08/2026 - Inclusão do Writer
===============================================================================
"""
from segy_viewer.domain.files import SeismicFile, SeismicReader, SeismicWriter
from segy_viewer.domain.datasets import SeismicDataset
from segy_viewer.domain.headers import SegyTextHeader, SegyBinaryHeader
from segy_viewer.infrastructure.segy import SegyioReader
from segy_viewer.infrastructure.segy import SegyioWriter

class SegyFile(SeismicFile):
    def __init__(self, path: str,
                 dataset: SeismicDataset | None = None,
                 reader: SeismicReader | None = None,
                 writer: SeismicWriter | None = None) -> None:
        super().__init__(path)

        self._reader = SegyioReader(path)  if reader is None else reader
        self._writer = SegyioWriter(path) if writer is None else writer

        self._dataset = dataset

    @property
    def dataset(self) -> SeismicDataset | None:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: SeismicDataset | None) :
        self._dataset = dataset

    @property
    def reader(self) -> SeismicReader:
        return self._reader

    @reader.setter
    def reader(self, reader: SeismicReader) :
        self._reader = reader

    @property
    def writer(self) -> SeismicWriter:
        return self._writer

    @writer.setter
    def writer(self, writer: SeismicWriter) :
        self._writer = writer

    @property
    def format_name(self) -> str:
        return 'SEGY'

    @property
    def trace_count(self) -> int:
        return self.reader.trace_count

    @property
    def text_header(self) -> SegyTextHeader:
        return self.reader.read_text_header()

    @property
    def binary_header(self) -> SegyBinaryHeader:
        return self.reader.read_binary_header()

    @property
    def is_open(self) -> bool:
        return self.reader.is_open

    @property
    def exists(self) -> bool:
        return self.reader.p

    def open(self) -> None:
       self.reader.open()

    def close(self) -> None:
        self.reader.close()

