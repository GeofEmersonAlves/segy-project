# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyFile_inspector.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria o Widget SegyFileInpecto, Abas que mostram o resumo e os Header do arquiv

    SegyFileBrowser
    ├── Recebe um nome de um arquivo SEGY
    ├── Solicita as informações do arquivo para um "use case"
    ├── Permite salvar as informações em arquivos
    ├── Quando nao tem arquivo limpa o conteudo das abas e exibe só a sumary
    └── Permite limpar o nome do arquivo, e todas as informações são limpas


Histórico:
       16/08/2026 - Implementação da Classe
===============================================================================
"""
from PySide6.QtWidgets import QWidget, QTabWidget
from pathlib import Path

class SegyFileInspector(QWidget):
    def __init__(self, segy_path: Path | None, parent=None):
        super(SegyFileInspector, self).__init__(parent)
        self._segy_path = segy_path

        self._make_tabs()


#=======================================================================
    @property
    def segy_path(self) -> Path | None:
        return self._segy_path

    @segy_path.setter
    def segy_path(self, segy_path: Path | None) -> None:
        self._segy_path = segy_path
        #-->Chamar um metodo para alterar o conteudo das Tabs

# =======================================================================
    def clear_tabs_content(self):
        ...

# =======================================================================
    def _tab_factory(self,tab_name: str) -> QTabWidget:
        ...

    def _make_tabs(self):
        tabs =["Sumary", "Text Header", "Bin Header", "Trace Header"]

        self._tab_sumary = QTabWidget()
        self._tab_text_header = QTabWidget()
        self._tab_bin_header = QTabWidget()
        self._tab_trace_header = QTabWidget()




