# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : import_text_header_from_txt_file.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Use case  ImportTextHeaderFromTxtFile, recebe um path e retorna o txt de um arquivo para text header
        Valida o texto lido do txt para verificar se tem 40 linha com 80 colunas cada
        Grava o texto lido no arquivo SGY

Histórico:
       26/08/2026 - Criação da use case
===============================================================================
"""
from pathlib import Path
from collections.abc import Callable
from segy_viewer.application.dto import CheckResponseDto
from segy_viewer.domain.exceptions.segy_file_exceptions import SegyFileInUseError
from segy_viewer.domain.files import SeismicFile

class ImportTextHeaderFromTxtFile:
    def __init__(self, file_factory: Callable[[Path], SeismicFile]) -> None:
        self._file_factory = file_factory

    def validate_text(self, text: str) -> CheckResponseDto:
        lines = text.splitlines()
        if len(lines) != 40:
            return CheckResponseDto(False, f"Text Header has {len(lines)} lines, expected: 40.")

        for line_number, line in enumerate(lines, start=1):
            if len(line) > 80:
                return  CheckResponseDto(False, f"Line {line_number} has {len(line)} characters expected: 80.")

        return CheckResponseDto(True, text)

    def read_text_header_from_file(self, txt_path: Path)->str:
        text = txt_path.read_text(encoding = "ascii")
        return text


    def write_text_header_into_segy(self, segy_path: Path, text: str) -> CheckResponseDto:
        segy_file: SeismicFile = self._file_factory(segy_path)

        try:
            segy_file.writer.write_text_header(text)
            return CheckResponseDto(True, text)

        except (SegyFileInUseError) as error:
            return CheckResponseDto(False, str(error))
