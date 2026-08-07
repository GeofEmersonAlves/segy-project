# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : headers_exceptions.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Exceções relacionadas aos headers SEG-Y.

Histórico:
       06/08/2026 - Início da implementação da Classe
===============================================================================
"""

class SegyHeaderError(Exception):
    """
    Exceção-base para erros relacionados aos headers SEG-Y.
    """

class SegyTextHeaderError(SegyHeaderError):
    """Erro relacionado ao Text Header SEG-Y."""


class InvalidTextHeaderCardCountError(SegyTextHeaderError):
    """Quantidade inválida de cartões no Textual File Header."""

    def __init__(self, received: int, expected: int = 40) -> None:
        self.received = received
        self.expected = expected

        super().__init__(
            f"O Textual File Header deve conter exatamente "
            f"{expected} cartões, mas recebeu {received}."
        )


class InvalidTextHeaderCardLengthError(SegyTextHeaderError):
    """Um ou mais cartões possuem tamanho diferente de 80 caracteres."""

    def __init__(
        self,
        invalid_cards: tuple[tuple[int, int], ...],
        expected: int = 80,
    ) -> None:
        self.invalid_cards = invalid_cards
        self.expected = expected

        details = ", ".join(
            f"cartão {index}: {length} caracteres"
            for index, length in invalid_cards
        )

        super().__init__(
            f"Todos os cartões do Textual File Header devem possuir "
            f"exatamente {expected} caracteres. "
            f"Cartões inválidos: {details}."
        )


class InvalidHeaderFieldError(SegyHeaderError):
    """
    A definição de um campo do header é inválida.
    """


class UnknownHeaderFieldError(SegyHeaderError, KeyError):
    """
    O campo solicitado não está definido no header.
    """


class MissingHeaderFieldError(SegyHeaderError):
    """
    Um campo obrigatório não foi fornecido pelo leitor.
    """


class InvalidHeaderValueError(SegyHeaderError, ValueError):
    """
    O valor fornecido para um campo é inválido.
    """


class UnsupportedSegyRevisionError(SegyHeaderError):
    """
    O arquivo declara uma revisão SEG-Y diferente da suportada.
    """