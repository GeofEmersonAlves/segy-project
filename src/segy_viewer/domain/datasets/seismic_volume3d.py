# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_volume3d.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.
Descrição  :
         Implementação da classe SeismicVolume3D.

  SeismicDataset(ABC) dataset_type: 3D
       ▲
       │
 SeismicVolume3D

Histórico:
       10/08/2026 - Início da implementação da Classe
===============================================================================
"""
from .seismic_dataset import SeismicDatasetType, SeismicDataset

class SeismicVolume3D(SeismicDataset):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @property
    def dataset_type(self) -> SeismicDatasetType:
        return SeismicDatasetType.SEISMIC_3D

    def describe(self) -> str:
        return f"Seismic Volume 3D: {self.name}"