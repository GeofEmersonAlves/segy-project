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
       28/08/2026 - Finalização do Summary
===============================================================================
"""
from datetime import datetime
from collections.abc import Callable
from pathlib import Path
from segy_viewer.application.dto import SegyFileInspectionDTO
from segy_viewer.domain.files import SeismicFile
from segy_viewer.domain.headers import ByteOrder, SegyBinaryHeader, SegyTextHeader

SAMPLE_FORMAT_NAMES = {
            1: "IBM Float (32-bit)",
            2: "Signed Integer (32-bit)",
            3: "Signed Integer (16-bit)",
            5: "IEEE Float (32-bit)",
            6: "IEEE Float (64-bit)",
            8: "Signed Integer (8-bit)",
        }
MEASUREMENT_SYSTEM = {
    1: "Meters",
    2: "Feet",
}

class InspectSegyFile:
    def __init__(self, file_factory: Callable[[Path], SeismicFile]) -> None:
        self._file_factory = file_factory

    def execute(self, path: Path) -> SegyFileInspectionDTO:
        self.segy_file: SeismicFile = self._file_factory(path)

        try:
            self.segy_file.open()

            self.text_header:SegyTextHeader  = self.segy_file.text_header
            self.binary_header:SegyBinaryHeader = self.segy_file.binary_header

            trace_header_index = 0
            self.first_trace = self.segy_file.reader.read_trace(trace_header_index)
            self.last_trace = self.segy_file.reader.read_trace(self.segy_file.trace_count-1)
            self.first_trace_header = self.first_trace.header
            self.last_trace_header = self.last_trace.header
            self.text_summary = self._make_summary(path)


            return SegyFileInspectionDTO(self.text_summary,
                                         str(self.text_header),
                                         self.binary_header.to_dict(),
                                         self.first_trace_header.to_dict(),
                                         trace_header_index)
        finally:
            self.segy_file.close()


    def _make_summary(self,path: Path) -> str:

        def _format_file_size(size: int) -> str:
            units = ("B", "KB", "MB", "GB", "TB")
            value = float(size)

            for unit in units:
                if value < 1024 or unit == units[-1]:
                    return f"{value:.1f} {unit}"
                value /= 1024

        linha = "-"*80 + "\n"
        sumary_txt = linha.replace("-","=")
        sumary_txt += "Summary Information".center(80) + "\n"
        sumary_txt += linha.replace("-","=") + "\n"
        sumary_txt += "FILE" + "\n"
        sumary_txt += linha
        sumary_txt += f"File name               : {path.name}" + "\n"
        sumary_txt += f"File size               : {_format_file_size(path.stat().st_size)}" + "\n"
        sumary_txt += f"Path                    : {path.parent}" + "\n"
        timestamp_modificacao = path.stat().st_mtime
        data_modificacao = datetime.fromtimestamp(timestamp_modificacao)
        sumary_txt += f"Last update             : {data_modificacao:%Y-%m-%d %H:%M:%S}"+ "\n"
        sumary_txt +=  "\n"
        #===============================================
        sumary_txt += "SEG-Y" + "\n"
        sumary_txt += linha
        major = self.binary_header.revision_major
        minor = self.binary_header.revision_minor
        byte_order: ByteOrder = self.binary_header.byte_order
        text_enconding = self.text_header.encoding
        sample_format_code = self.binary_header.sample_format_code
        sample_format = SAMPLE_FORMAT_NAMES[sample_format_code]
        sample_interval = self.binary_header.sample_interval
        samples_per_trace = self.binary_header.samples_per_trace
        trace_length_s = samples_per_trace * sample_interval / 1_000
        # fixed_length_trace_flag = self.binary_header.fixed_length_trace_flag
        extended_textual_header_count=self.binary_header.extended_textual_header_count
        measurement_system_cod = self.binary_header.measurement_system_code
        measurement_system =MEASUREMENT_SYSTEM[measurement_system_cod]
        sumary_txt += f"Revision                : SEG-Y Rev {major}.{minor}" + "\n"
        sumary_txt += f"Byte order              : {byte_order.display_name}" + "\n"
        sumary_txt += f"Text Header encoding    : {text_enconding}" + "\n"
        sumary_txt += f"Sample format           : {sample_format}"+ "\n"
        sumary_txt += f"Sample interval         : {sample_interval:.0f} µs" + "\n"
        sumary_txt += f"Samples per trace       : {samples_per_trace}" + "\n"
        sumary_txt += f"Trace length            : {trace_length_s:.0f} ms" + "\n"
        # sumary_txt += f"Fixed-length traces     : {fixed_length_trace_flag}" + "\n"
        sumary_txt += f"Extended text headers   : {extended_textual_header_count}" + "\n"
        sumary_txt += f"Measurement system      : {measurement_system}" + "\n"
        sumary_txt += "\n"
        # ===============================================
        sumary_txt += "DATA" + "\n"
        sumary_txt += linha
        #O arquivo ainda esta aberto aqyu
        trace_count = self.segy_file.trace_count
        samples_in_trace = self.first_trace_header.samples_in_trace
        sample_interval = self.first_trace_header.sample_interval
        record_length = self.first_trace_header.trace_duration_seconds * 1_000
        sumary_txt += f"Traces                  : {trace_count:,.0f}" + "\n"
        sumary_txt += f"Samples/trace           : {samples_in_trace}" + "\n"
        sumary_txt += f"Sample interval         : {sample_interval} µs" + "\n"
        sumary_txt += f"Record length           : {record_length:.0f} ms" + "\n"
        sumary_txt += "\n"
        # ===============================================
        sumary_txt += "TRACE RANGE" + "\n"
        sumary_txt += linha
        first_sp = self.first_trace_header.energy_source_point_number
        first_cdp =self.first_trace_header.ensemble_number
        first_ffid = self.first_trace_header.field_record_number

        last_sp = self.last_trace_header.energy_source_point_number
        last_cdp =self.last_trace_header.ensemble_number
        last_ffid = self.last_trace_header.field_record_number

        sumary_txt += f"{'':17}{'First Trace':<16}{'Last Trace'}\n"
        sumary_txt += f"{'SP':17}{first_sp:<16}{last_sp}\n"
        sumary_txt += f"{'CDP':17}{first_cdp:<16}{last_cdp}\n"
        sumary_txt +=  f"{'FFID':17}{first_ffid:<16}{last_ffid}\n"

        return sumary_txt