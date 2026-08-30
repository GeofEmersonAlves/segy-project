# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : export_segy_inspection_dto.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Use case  ExportSegyDTO, recebe um SegyFileInspectionDTO e salva em um arquivo o
    o dto field que foi idicado, permite 4 formatos para o Binary e Trace Header (.txt/.csv/.json/.xlsx)
    e para o Summary e Text Header permite salvar em .txt
        A use case expoe FILE_FILTERS

Histórico:
       17/08/2026 - Criação da use case
       19/08/2026 - Continuação da construção da classe
===============================================================================
"""
from pathlib import Path
import json
import pandas as pd
from segy_viewer.application.dto import SegyFileInspectionDTO
from segy_viewer.application.types import InspectorSectionType

class ExportSegyDTO:
    def __init__(self) -> None:
        self._FILE_FILTERS = ("Text Files (*.txt)",
                              "CSV Files (*.csv)",
                              "Json Files (*.json)",
                              "Excel Files (*.xlsx)",
                              "All files (*.*)"
                              )

        self._TXT_FILTER, self._CSV_FILTER, self._JSON_FILTER, self._XLSX_FILTER, self._ALL_FILES_FILTER = self._FILE_FILTERS

    @property
    def FILE_FILTERS(self) -> str:
        return self._FILE_FILTERS
    @property
    def TXT_FILTER(self) -> str:
        return self._TXT_FILTER
    @property
    def CSV_FILTER(self) -> str:
        return self._CSV_FILTER
    @property
    def JSON_FILTER(self) -> str:
        return self._JSON_FILTER
    @property
    def XLSX_FILTER(self) -> str:
        return self._XLSX_FILTER
    @property
    def ALL_FILES_FILTER(self) -> str:
        return self._ALL_FILES_FILTER
    @property
    def DICT_FILES_FILTER(self) -> str:
        _dict_filter = self.JSON_FILTER + ";;"
        _dict_filter += self.CSV_FILTER + ";;"
        _dict_filter += self.XLSX_FILTER
        return _dict_filter


    @property
    def allowed_filters(self, section_name : InspectorSectionType) -> tuple:
        filters = ()

        if section_name in (InspectorSectionType.SUMMARY, InspectorSectionType.TEXT_HEADER):
            filters = (self._TXT_FILTER)

        elif section_name in (InspectorSectionType.BIN_HEADER, InspectorSectionType.TRACE_HEADER):
            filters = self._FILE_FILTERS  #por enquanto permito todos os formatos, depois eu revejo

        return filters


    def execute(self, segy_inspetion_dto: SegyFileInspectionDTO,
                section_name : InspectorSectionType,
                file_path: Path,
                file_filter: str) -> bool:

        if file_filter == self.TXT_FILTER:
            return self._save_info_text_file(segy_inspetion_dto, section_name, file_path)

        elif file_filter == self.CSV_FILTER:
            self._save_info_csv_file(segy_inspetion_dto, section_name, file_path)

        elif file_filter == self.JSON_FILTER:
            self._save_info_json_file(segy_inspetion_dto, section_name, file_path)

        elif file_filter == self.XLSX_FILTER:
            self._save_info_xlsx_file(segy_inspetion_dto, section_name, file_path)

        return True

    def _save_info_text_file(self, segy_inspection_dto: SegyFileInspectionDTO,
                                   section_name: InspectorSectionType,
                                   file_path: Path)->bool:
        if section_name == InspectorSectionType.SUMMARY:
            text_to_save = segy_inspection_dto.summary
        elif section_name == InspectorSectionType.TEXT_HEADER:
            text_to_save = segy_inspection_dto.text_header
        elif section_name == InspectorSectionType.BIN_HEADER:
            text_to_save = str(segy_inspection_dto.binary_header)

        try:
            file_path.write_text(text_to_save, encoding="utf-8")
            return True

        except OSError:
            return False

    def _save_info_csv_file(self, segy_inspection_dto: SegyFileInspectionDTO,
                            section_name: InspectorSectionType,
                            file_path: Path)->bool:

        if section_name == InspectorSectionType.BIN_HEADER:
            table_to_save = self._header_to_table(segy_inspection_dto.binary_header)

        elif section_name == InspectorSectionType.TRACE_HEADER:
            table_to_save =  self._header_to_table(segy_inspection_dto.trace_header)

        try:
            df_to_save = pd.DataFrame(table_to_save)
            df_to_save.to_csv(file_path, encoding="utf-8",index=False)
            return True

        except OSError:
            return False

    def _save_info_xlsx_file(self, segy_inspection_dto: SegyFileInspectionDTO,
                             section_name: InspectorSectionType,
                             file_path: Path)->bool:

        if section_name == InspectorSectionType.BIN_HEADER:
            table_to_save = self._header_to_table(segy_inspection_dto.binary_header)

        elif section_name == InspectorSectionType.TRACE_HEADER:
            table_to_save = self._header_to_table(segy_inspection_dto.trace_header)

        try:
            df_to_save = pd.DataFrame(table_to_save)
            df_to_save.to_excel(file_path, index=False)
            return True

        except OSError:
            return False


    def _save_info_json_file(self, segy_inspection_dto: SegyFileInspectionDTO,
                             section_name: InspectorSectionType,
                             file_path: Path)->bool:
        dict_to_save = {}
        if section_name == InspectorSectionType.BIN_HEADER:
            dict_to_save = segy_inspection_dto.binary_header

        elif section_name == InspectorSectionType.TRACE_HEADER:
            dict_to_save = segy_inspection_dto.trace_header

        try:
            with open(file_path, "w", encoding="utf-8")as file:
                json.dump(dict_to_save, file, ensure_ascii=False, indent=4)

            return True

        except OSError:
            return False

    def _header_to_table(self, data: dict) -> list[dict]:
        rows = []

        for item in data.values():

            if "bin_header_field" in item:
                field = item["bin_header_field"]

            elif "trace_header_field" in item:
                field = item["trace_header_field"]

            else:
                raise ValueError(
                    "Invalid header data: field definition not found."
                )

            rows.append({
                "Bytes": f'{field["byte_start"]} - {field["byte_end"]}',
                "Description": field["description"],
                "Value": item["value"],
                "Data Type": field["data_type"],
            })

        return rows