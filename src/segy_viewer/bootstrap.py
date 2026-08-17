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
from segy_viewer.infrastructure.segy import SegyFile

def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

def create_application():
    ...