# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : header_field.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Define os metadados dos campos encontrados nos headers SEG-Y.
       HeaderField não realiza leitura de arquivo e não depende de segyio.
       A leitura é responsabilidade das implementações de SeismicReader.

Histórico:
       06/08/2026 - Início da implementação da Classe
===============================================================================
"""
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
from segy_viewer.domain.exceptions.headers_exceptions import InvalidHeaderFieldError

HeaderValue: TypeAlias = int | float | str | bool | bytes | None

class HeaderDataType(Enum):
    """
    Tipo conceitual de um campo do header.

    Esses tipos são usados para documentação, validação e apresentação.
    Não representam diretamente tipos do módulo struct.
    """

    INT8 = "int8"
    UINT8 = "uint8"

    INT16 = "int16"
    UINT16 = "uint16"

    INT32 = "int32"
    UINT32 = "uint32"

    INT64 = "int64"
    UINT64 = "uint64"

    FLOAT32 = "float32"
    FLOAT64 = "float64"

    RAW_BYTES = "raw_bytes"

    @property
    def byte_length(self) -> int | None:
        """
        Tamanho esperado em bytes.

        RAW_BYTES não possui tamanho obrigatório.
        """
        lengths: dict[HeaderDataType, int | None] = {
            HeaderDataType.INT8: 1,
            HeaderDataType.UINT8: 1,
            HeaderDataType.INT16: 2,
            HeaderDataType.UINT16: 2,
            HeaderDataType.INT32: 4,
            HeaderDataType.UINT32: 4,
            HeaderDataType.INT64: 8,
            HeaderDataType.UINT64: 8,
            HeaderDataType.FLOAT32: 4,
            HeaderDataType.FLOAT64: 8,
            HeaderDataType.RAW_BYTES: None,
        }

        return lengths[self]



@dataclass(frozen=True, slots=True)
class HeaderField:
    """
    Metadados de um campo de header SEG-Y.

    Parameters
    ----------
    name:
        Nome interno utilizado pelo domínio.

    byte_start:
        Primeiro byte absoluto do campo na especificação SEG-Y.
        A contagem começa em 1.

    byte_end:
        Último byte absoluto, inclusive.

    data_type:
        Tipo conceitual do campo.

    description:
        Descrição legível do campo.

    unit:
        Unidade do valor, quando aplicável.

    required:
        Indica se o leitor deve obrigatoriamente fornecer o campo.
    """

    name: str
    byte_start: int
    byte_end: int
    data_type: HeaderDataType
    description: str
    unit: str | None = None
    required: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvalidHeaderFieldError(
                "O nome do campo não pode estar vazio."
            )

        if self.byte_start <= 0:
            raise InvalidHeaderFieldError(
                f"O byte inicial de {self.name!r} deve ser maior que zero."
            )

        if self.byte_end < self.byte_start:
            raise InvalidHeaderFieldError(
                f"O byte final de {self.name!r} não pode ser menor "
                "que o byte inicial."
            )

        expected_length = self.data_type.byte_length

        if (
            expected_length is not None
            and self.length != expected_length
        ):
            raise InvalidHeaderFieldError(
                f"O campo {self.name!r} possui {self.length} bytes, "
                f"mas o tipo {self.data_type.value!r} exige "
                f"{expected_length}."
            )

    @property
    def length(self) -> int:
        """
        Quantidade de bytes ocupada pelo campo.
        """
        return self.byte_end - self.byte_start + 1

    @property
    def relative_offset(self) -> int:
        """
        Offset relativo ao início do Binary File Header.

        O Binary File Header começa no byte 3201 do arquivo.
        """
        return self.byte_start - 3201

    @property
    def byte_range(self) -> tuple[int, int]:
        """
        Retorna o intervalo absoluto inclusivo.
        """
        return self.byte_start, self.byte_end

    def accepts_value(self, value: HeaderValue) -> bool:
        """
        Faz uma validação básica do tipo Python recebido.

        A validação não verifica todos os limites numéricos do padrão.
        """
        if value is None:
            return not self.required

        if self.data_type in {
            HeaderDataType.INT8,
            HeaderDataType.UINT8,
            HeaderDataType.INT16,
            HeaderDataType.UINT16,
            HeaderDataType.INT32,
            HeaderDataType.UINT32,
            HeaderDataType.INT64,
            HeaderDataType.UINT64,
        }:
            return isinstance(value, int) and not isinstance(value, bool)

        if self.data_type in {
            HeaderDataType.FLOAT32,
            HeaderDataType.FLOAT64,
        }:
            return (
                isinstance(value, int | float)
                and not isinstance(value, bool)
            )

        if self.data_type is HeaderDataType.RAW_BYTES:
            return isinstance(value, bytes)

        return False