# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_coordinate_transform.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe faz a transformação das coordenadas de tela

Histórico:

       04/09/2026 - Início da implementação da classe
===============================================================================
"""

class SeismicCoordinateTransform:

    def trace_to_x(self, trace_index: int) -> float:
        ...

    def sample_to_y(self, sample_index: int) -> float:
        ...

    def x_to_trace(self, x: float) -> int:
        ...

    def y_to_sample(self, y: float) -> int:
        ...