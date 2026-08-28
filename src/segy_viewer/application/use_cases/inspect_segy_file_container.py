# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : inspect_segy_file_container.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Container de use cases do widget SegyFileInspector
           Use Cases:
                  SegyFileInspectorUseCases: “O usuário selecionou um arquivo SEG-Y e quer inspecionar suas informações.”

Histórico:
       17/08/2026 - Criação do container SegyFileInspectorUseCases, que conscentra todas
                  as use cases do Widget SegyFileInspector
       27/08/2026 - Inlcusão do use case ImportTextHeaderFromTxtFile
===============================================================================
"""
from collections.abc import Callable
from pathlib import Path

from segy_viewer.domain.files import SeismicFile
from .inspect_segy_file import InspectSegyFile
from .export_segy_inspection_dto import ExportSegyDTO
from .import_text_header_from_txt_file import ImportTextHeaderFromTxtFile
# from segy_viewer.application.use_cases import InspectSegyFile, ExportSegyDTO

#=============================================
class SegyFileInspectorUseCases:
    def __init__(self, file_factory: Callable[[Path], SeismicFile] ) -> None:
        self.inspect_segy_file:InspectSegyFile = InspectSegyFile(file_factory = file_factory)
        self.export_segy_dto:ExportSegyDTO = ExportSegyDTO()
        self.text_header_from_txt_file = ImportTextHeaderFromTxtFile(file_factory = file_factory)



