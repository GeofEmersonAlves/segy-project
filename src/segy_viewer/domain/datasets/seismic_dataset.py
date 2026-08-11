# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_reader.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.
Descrição  :
         Implementação da classe abstrata interface SeismicDataset
  um SeismicDataset representa o conteúdo sísmico lógico.

  SeismicFile (ABC)
                  ▲
                  │
             SegyFile
                  │ representa
                  ▼
          SeismicDataset
                  ▲
          ┌───────┴───────┐
          │               │
         2D              3D

Histórico:
       10/08/2026 - Início da implementação da Classe
===============================================================================
"""
from abc import ABC, abstractmethod
from enum import StrEnum

class SeismicDatasetType(StrEnum):
    SEISMIC_2D = "2D"
    SEISMIC_3D = "3D"

class SeismicDataset(ABC):
    def __init__(self, name: str) -> None:
        if not name.strip():
            raise ValueError("O nome do dataset não pode estar vazio." )
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    @abstractmethod
    def dataset_type(self) -> SeismicDatasetType:
        """
        Dimensionalidade do dataset: 2D ou 3D.
        """
        pass

    @abstractmethod
    def describe(self) -> str:
        """
        Retorna uma descrição resumida do dataset.
        """
        pass