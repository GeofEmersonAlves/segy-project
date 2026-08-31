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
       29/08/2026 - Inclusão da main window
===============================================================================
"""
from pathlib import Path

from setuptools.command.setopt import config_file

from segy_viewer import AppConfig
from segy_viewer.presentation.desktop import MainWindow
from segy_viewer.presentation.desktop.widgets import SegyFileInspector, SegyFileBrowser
from segy_viewer.application.use_cases import SegyFileInspectorUseCases
from segy_viewer.infrastructure.segy import SegyFile

#Factory que cria um segy file
def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

def create_application():
    #CONFIG
    config = AppConfig()
    segy_extensions = config.segy_extensions
    button_style = config.button_style
    tree_style = config.tree_browser_style
    inspec_status_bar_button_style = AppConfig.status_bar_button_style

    #USE CASES
    inspector_use_cases = SegyFileInspectorUseCases(file_factory = create_segy_file)

    # WIDGETS
    segy_file_inspector = SegyFileInspector(inspector_use_cases = inspector_use_cases,
                                            status_bar_button_style = inspec_status_bar_button_style)

    segy_file_browser = SegyFileBrowser(segy_extensions = segy_extensions,
                                        button_style = button_style,
                                        tree_style = tree_style)

    # Main Window
    main_window = MainWindow(file_browser = segy_file_browser,
                             file_inspector = segy_file_inspector
                             )

    return main_window