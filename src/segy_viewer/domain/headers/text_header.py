# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : text_header.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que  representa o Text Header

Histórico:
       05/08/2026 - Início da implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
from typing import ClassVar
from segy_viewer.domain.exceptions.headers_exceptions import (InvalidTextHeaderCardCountError,
                                                              InvalidTextHeaderCardLengthError)
from segy_viewer.domain.headers import TextHeaderEncoding


@dataclass(frozen=True)
class SegyTextHeader:
    cards: tuple[str, ...]
    encoding: TextHeaderEncoding = TextHeaderEncoding.UNKNOWN

    CARD_COUNT: ClassVar[int] = 40
    CARD_LENGTH: ClassVar[int] = 80

    def __post_init__(self) -> None:
        self._validate_card_count()
        self._validate_card_lengths()

    def _validate_card_count(self) -> None:
        if len(self.cards) != self.CARD_COUNT:
            raise InvalidTextHeaderCardCountError(
                received=len(self.cards),
                expected=self.CARD_COUNT,
            )

    def _validate_card_lengths(self) -> None:
        invalid_cards = tuple(
            (index, len(card))
            for index, card in enumerate(self.cards, start=1)
            if len(card) != self.CARD_LENGTH
        )

        if invalid_cards:
            raise InvalidTextHeaderCardLengthError(
                invalid_cards=invalid_cards,
                expected=self.CARD_LENGTH,
            )

    def card(self, number: int) -> str:
        if not 1 <= number <= self.CARD_COUNT:
            raise IndexError(
                f"O número do cartão deve estar entre "
                f"1 e {self.CARD_COUNT}."
            )

        return self.cards[number - 1]

    def __str__(self) -> str:
        return "\n".join(self.cards)