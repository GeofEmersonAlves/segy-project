# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    :  byte_order.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
          Define as ordens de bytes reconhecidas pelo domínio da aplicação

Histórico:
       06/08/2026 - Início da implementação da Classe
===============================================================================
"""
from enum import Enum


class ByteOrder(Enum):
    """
    Ordem dos bytes utilizada pelo arquivo SEG-Y.

    A detecção e a interpretação são responsabilidades do leitor concreto,
    como o SegyioReader. O domínio apenas armazena essa informação.
    """

    BIG_ENDIAN = "big"
    LITTLE_ENDIAN = "little"
    UNKNOWN = "unknown"

    @classmethod
    def from_string(cls, value: str | None) -> "ByteOrder":
        """
        Converte uma string em ByteOrder.

        Parameters
        ----------
        value:
            Valor como "big", "msb", "little" ou "lsb".
        """
        if value is None:
            return cls.UNKNOWN

        normalized = value.strip().lower()

        aliases = {
            "big": cls.BIG_ENDIAN,
            "msb": cls.BIG_ENDIAN,
            ">": cls.BIG_ENDIAN,
            "little": cls.LITTLE_ENDIAN,
            "lsb": cls.LITTLE_ENDIAN,
            "<": cls.LITTLE_ENDIAN,
            "unknown": cls.UNKNOWN,
        }

        try:
            return aliases[normalized]
        except KeyError as error:
            raise ValueError(
                f"Ordem de bytes desconhecida: {value!r}."
            ) from error