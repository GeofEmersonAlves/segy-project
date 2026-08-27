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

Histórico:
       26/08/2026 - Criação da use case
===============================================================================
"""
from pathlib import Path
from urllib import response

from segy_viewer.application.dto import CheckResponseDto

class ImportTextHeaderFromTxtFile:

    def validate_text(self, text: str) -> CheckResponseDto:
        lines = text.splitlines()
        if len(lines) != 40:
            return CheckResponseDto(False, f"Text Header has {len(lines)} lines, expected: 40.")

        for line_number, line in enumerate(lines, start=1):
            if len(line) > 80:
                return  CheckResponseDto(False, f"Line {line_number} has {len(line)} characters expected: 80.")


        return CheckResponseDto(True, text)

    def read_text(self, txt_path: Path)->str:
        text = txt_path.read_text(encoding="ascii")
        return text