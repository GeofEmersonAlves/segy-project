# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : resources.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Metodo para trazer o path das imagens do projeto,
    pois depois de empacotado o Path(__file__).resolve().parents[5] não funciona
Histórico:
       28/08/2026 - Implementação da Classe
       01/09/2026 - Criação da Tool Bar
===============================================================================
"""
from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parents[2]

    return base_dir / relative_path
