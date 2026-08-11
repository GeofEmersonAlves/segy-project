# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_swath3d.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.
Descrição  :
         Implementação da classe SeismicSwath3D.

  SeismicDataset(ABC) dataset_type: 3D
       ▲
       │
 SeismicSwath3D

Histórico:
       10/08/2026 - Início da implementação da Classe
===============================================================================
"""
from .seismic_dataset import SeismicDatasetType, SeismicDataset

class SeismicSwath3D(SeismicDataset):

    def __init__(self, name: str, swath_number: str | int | None = None) -> None:
        super().__init__(name)
        self._swath_number = swath_number

    @property
    def dataset_type(self) -> SeismicDatasetType:
        return SeismicDatasetType.SEISMIC_3D

    @property
    def swath_number(self) -> str | int | None:
        return self._swath_number

    def describe(self) -> str:
        if self.swath_number is None:
            return f"Swath 3D: {self.name}"

        return (
            f"Swath 3D: {self.name} "
            f"(swath: {self.swath_number})"
        )