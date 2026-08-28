# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : inspect_segy_file.py
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
from segy_viewer.domain.files import SeismicFile

class InspectSegyFile:
    def __init__(self, file_factory: Callable[[Path], SeismicFile]) -> None:
        self._file_factory = file_factory

    def execute(self, path: Path) -> SegyFileInspectionDTO:
        segy_file: SeismicFile = self._file_factory(path)

        try:
            segy_file.open()

            text_summary = self._make_summary(path)
            text_header = str(segy_file.text_header)
            binary_header = segy_file.binary_header.to_dict()
            trace_header_index = 0
            trace = segy_file.reader.read_trace(trace_header_index)
            trace_header = trace.header
            trace_header = trace_header.to_dict()

            return SegyFileInspectionDTO(text_summary,
                                         text_header,
                                         binary_header,
                                         trace_header,
                                         trace_header_index)
        finally:
            segy_file.close()


    def _make_summary(self,path: Path) -> str:
        def _format_file_size(size: int) -> str:
            units = ("B", "KB", "MB", "GB", "TB")
            value = float(size)

            for unit in units:
                if value < 1024 or unit == units[-1]:
                    return f"{value:.1f} {unit}"
                value /= 1024

        linha = "-"*50 + "\n"
        sumary_txt = linha
        sumary_txt += "Summary Information".center(50) + "\n"
        sumary_txt += linha
        sumary_txt += "FILE" + "\n"
        sumary_txt += linha
        sumary_txt += f"File name       : {path.name}" + "\n"
        sumary_txt += f"File size       : {_format_file_size(path.stat().st_size)}" + "\n"
        sumary_txt += f"Path            : {path.parent}" + "\n"
        sumary_txt +=  "\n"
        sumary_txt += "SEG-Y" + "\n"
        sumary_txt += linha
        sumary_txt += "\n"
        sumary_txt += "DATA" + "\n"
        sumary_txt += linha
        sumary_txt += f"Traces          : {_format_file_size(path.stat().st_size)}" + "\n"


        return sumary_txt