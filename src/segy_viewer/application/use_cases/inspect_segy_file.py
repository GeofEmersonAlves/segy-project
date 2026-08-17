# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyFile_inspection_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Use case :“O usuário selecionou um arquivo SEG-Y e quer inspecionar suas informações.”

Histórico:
       16/08/2026 - Implementação do Use Case
===============================================================================
"""
from collections.abc import Callable
from pathlib import Path

from segy_viewer.application.dto import SegyFileInspectionDTO
from segy_viewer.infrastructure.segy import SegyFile

class InspectSegyFile:
    def __init__(self, file_factory: Callable[[Path], SegyFile]) -> None:
        self._file_factory = file_factory

    def execute(self, path: Path) -> SegyFileInspectionDTO:
        segy_file: SegyFile = self._file_factory(path)

        try:
            segy_file.open()

            summary="Falta implementar"
            text_header = str(segy_file.text_header)
            binary_header = segy_file.binary_header.to_dict()
            trace_header_index = 0
            trace = segy_file.reader.read_trace(trace_header_index)
            trace_header = trace.header
            trace_header = trace_header.to_dict()

            return SegyFileInspectionDTO(summary,
                                         text_header,
                                         binary_header,
                                         trace_header,
                                         trace_header_index)
        finally:
            segy_file.close()