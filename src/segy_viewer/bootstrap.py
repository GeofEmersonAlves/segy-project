# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : bootstrap.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Rotina que monta a aplicacao, importa todas as dependencias e
    retorna pronta para a MainWindow

Histórico:
       16/08/2026 - Início da implementação
===============================================================================
"""
from pathlib import Path

from segy_viewer.presentation.desktop.widgets import SegyFileInspector
from segy_viewer.application.use_cases import SegyFileInspectorUseCases
from segy_viewer.infrastructure.segy import SegyFile

#Factory que cria um segy file
def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

def create_application():
    segy_file_inspector_use_cases = SegyFileInspectorUseCases(file_factory=create_segy_file)
    segy_file_inspector = SegyFileInspector(inspector_use_cases = segy_file_inspector_use_cases)

    # main_window = MainWindow(
    #                          segy_file_inspector=segy_file_inspector
    #                         )
    #
    # return main_window
    ...