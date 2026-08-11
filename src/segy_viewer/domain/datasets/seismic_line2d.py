# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_line2d.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.
Descrição  :
         Implementação da classe SeismicLine2D.

  SeismicDataset(ABC) dataset_type: 2D
       ▲
       │
 SeismicLine2D

Histórico:
       10/08/2026 - Início da implementação da Classe
===============================================================================
"""
from .seismic_dataset import SeismicDatasetType, SeismicDataset

class SeismicLine2D(SeismicDataset):

    def __init__(self, name: str, line_number: str | int | None = None) -> None:
        super().__init__(name)
        self._line_number = line_number

    @property
    def dataset_type(self) -> SeismicDatasetType:
        return SeismicDatasetType.SEISMIC_2D

    @property
    def line_number(self) -> str | int | None:
        return self._line_number

    def describe(self) -> str:
        if self.line_number is None:
            return f"Seismic line 2D: {self.name}"

        return (
            f"Seismic line 2D: {self.name} "
            f"(Line: {self.line_number})"
        )