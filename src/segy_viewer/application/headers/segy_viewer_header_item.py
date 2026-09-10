# -*- coding: utf-8 -*-
"""
SegyViewer Header Item.

Representa um item do dicionário de headers conhecido pela aplicação
Segy Viewer. O item descreve a informação; ele não é responsável por
obter ou calcular seu valor.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SegyViewerHeaderItem:
    key: str
    name: str
    acronym: str
    source: str
    source_field: str
    unit: str | None = None
