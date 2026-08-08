# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : binary_header.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Representação do Binary File Header de um arquivo SEG-Y.

    A classe recebe valores já lidos por uma implementação de um SeismicReader, como o SegyioReader.

Histórico:
       06/08/2026 - Início da implementação da Classe
===============================================================================
"""
from collections.abc import Iterator, Mapping
from types import MappingProxyType
from typing import Any, ClassVar

from .binary_header_fields import (
    BINARY_HEADER_FIELDS,
    BINARY_HEADER_FIELDS_BY_NAME,
    REQUIRED_BINARY_HEADER_FIELDS,
)
from .byte_order import ByteOrder
from segy_viewer.domain.exceptions.headers_exceptions import (InvalidHeaderValueError,
                                                                MissingHeaderFieldError,
                                                                UnknownHeaderFieldError,
                                                                UnsupportedSegyRevisionError)
from .header_field import HeaderField, HeaderValue


class SegyBinaryHeader:
    """
    Representa os valores do Binary File Header.

    Parameters
    ----------
    values:
        Mapeamento entre o nome interno do campo e seu valor.

    byte_order:
        Ordem dos bytes utilizada pelo arquivo.

    validate_revision:
        Quando True, exige que o arquivo declare Revision 2.1.
    """

    SUPPORTED_REVISION: ClassVar[tuple[int, int]] = (2, 1)

    def __init__(self, values: Mapping[str, HeaderValue], *,
                       byte_order: ByteOrder = ByteOrder.UNKNOWN,
                       validate_revision: bool = False) -> None:

        self._byte_order = byte_order
        self._values = self._prepare_values(values)

        self._validate_required_fields()
        self._validate_values()

        if validate_revision:
            self.validate_revision()

    @property
    def byte_order(self) -> ByteOrder:
        return self._byte_order

    @property
    def fields(self) -> tuple[HeaderField, ...]:
        return BINARY_HEADER_FIELDS

    @property
    def values(self) -> Mapping[str, HeaderValue]:
        """
        Visualização somente para leitura dos valores.
        """
        return MappingProxyType(self._values)

    @property
    def revision_major(self) -> int:
        return self._int_value("revision_major")

    @property
    def revision_minor(self) -> int:
        return self._int_value("revision_minor")

    @property
    def revision(self) -> tuple[int, int]:
        return self.revision_major, self.revision_minor

    @property
    def revision_name(self) -> str:
        major, minor = self.revision
        return f"SEG-Y Revision {major}.{minor}"

    @property
    def is_supported_revision(self) -> bool:
        return self.revision == self.SUPPORTED_REVISION

    @property
    def sample_interval(self) -> float:
        """
        Intervalo de amostragem efetivo.

        O campo estendido é utilizado quando contém um valor positivo.
        """
        extended = self._float_value(
            "extended_sample_interval",
            default=0.0,
        )

        if extended > 0.0:
            return extended

        return float(self._int_value("sample_interval"))

    @property
    def original_sample_interval(self) -> float:
        extended = self._float_value(
            "extended_original_sample_interval",
            default=0.0,
        )

        if extended > 0.0:
            return extended

        return float(
            self._int_value(
                "original_sample_interval",
                default=0,
            )
        )

    @property
    def samples_per_trace(self) -> int:
        return self._extended_or_legacy_integer(
            extended_name="extended_samples_per_trace",
            legacy_name="samples_per_trace",
        )

    @property
    def original_samples_per_trace(self) -> int:
        return self._extended_or_legacy_integer(
            extended_name="extended_original_samples_per_trace",
            legacy_name="original_samples_per_trace",
        )

    @property
    def data_traces_per_ensemble(self) -> int:
        return self._extended_or_legacy_integer(
            extended_name="extended_data_traces_per_ensemble",
            legacy_name="data_traces_per_ensemble",
        )

    @property
    def auxiliary_traces_per_ensemble(self) -> int:
        return self._extended_or_legacy_integer(
            extended_name="extended_auxiliary_traces_per_ensemble",
            legacy_name="auxiliary_traces_per_ensemble",
        )

    @property
    def ensemble_fold(self) -> int:
        return self._extended_or_legacy_integer(
            extended_name="extended_ensemble_fold",
            legacy_name="ensemble_fold",
        )

    @property
    def sample_format_code(self) -> int:
        return self._int_value("sample_format_code")

    @property
    def measurement_system_code(self) -> int:
        return self._int_value(
            "measurement_system",
            default=0,
        )

    @property
    def measurement_system_name(self) -> str:
        names = {
            0: "não definido",
            1: "metros",
            2: "pés",
        }

        code = self.measurement_system_code
        return names.get(code, f"desconhecido ({code})")

    @property
    def fixed_length_trace_flag(self) -> int:
        return self._int_value(
            "fixed_length_trace_flag",
            default=0,
        )

    @property
    def has_fixed_length_traces(self) -> bool:
        return self.fixed_length_trace_flag == 1

    @property
    def extended_textual_header_count(self) -> int:
        return self._int_value(
            "extended_textual_header_count",
            default=0,
        )

    @property
    def has_extended_textual_headers(self) -> bool:
        return self.extended_textual_header_count != 0

    @property
    def has_variable_extended_textual_headers(self) -> bool:
        return self.extended_textual_header_count == -1

    @property
    def maximum_additional_trace_headers(self) -> int:
        return self._int_value(
            "maximum_additional_trace_headers",
            default=0,
        )

    @property
    def trace_count(self) -> int:
        return self._int_value(
            "trace_count",
            default=0,
        )

    @property
    def first_trace_byte_offset(self) -> int:
        explicit_offset = self._int_value(
            "first_trace_byte_offset",
            default=0,
        )

        if explicit_offset > 0:
            return explicit_offset

        extended_header_count = self.extended_textual_header_count

        if extended_header_count >= 0:
            return 3600 + (extended_header_count * 3200)

        raise InvalidHeaderValueError(
            "O offset do primeiro traço não está definido e não pode "
            "ser calculado porque a quantidade de Extended Textual "
            "Headers é variável."
        )

    @property
    def data_trailer_count(self) -> int:
        return self._int_value(
            "data_trailer_count",
            default=0,
        )

    def get(
        self,
        field_name: str,
        default: Any = None,
    ) -> HeaderValue | Any:
        """
        Retorna o valor bruto fornecido pelo leitor.
        """
        return self._values.get(field_name, default)

    def get_field(self, field_name: str) -> HeaderField:
        """
        Retorna os metadados de um campo.
        """
        try:
            return BINARY_HEADER_FIELDS_BY_NAME[field_name]
        except KeyError as error:
            raise UnknownHeaderFieldError(
                f"O campo {field_name!r} não está definido no "
                "Binary File Header."
            ) from error

    def validate_revision(self) -> None:
        """
        Verifica se o arquivo declara SEG-Y Revision 2.1.
        """
        if self.is_supported_revision:
            return

        expected_major, expected_minor = self.SUPPORTED_REVISION
        actual_major, actual_minor = self.revision

        raise UnsupportedSegyRevisionError(
            "Revisão SEG-Y não suportada. "
            f"Esperado: {expected_major}.{expected_minor}; "
            f"encontrado: {actual_major}.{actual_minor}."
        )

    def raw_items(
        self,
    ) -> Iterator[tuple[HeaderField, HeaderValue]]:
        """
        Percorre os metadados e os valores brutos.
        """
        for field in BINARY_HEADER_FIELDS:
            yield field, self._values[field.name]

    def to_dict(self, *, effective_values: bool = False, include_none: bool = True) -> dict[str, HeaderValue]:
        """
        Converte o header para um novo dicionário.

        Parameters
        ----------
        effective_values:
            Substitui os campos históricos pelos valores efetivos,
            considerando seus equivalentes estendidos.

        include_none:
            Inclui ou remove campos sem valor.
        """
        result = dict(self._values)

        if effective_values:
            result.update(
                {
                    "sample_interval": self.sample_interval,
                    "original_sample_interval": (
                        self.original_sample_interval
                    ),
                    "samples_per_trace": self.samples_per_trace,
                    "original_samples_per_trace": (
                        self.original_samples_per_trace
                    ),
                    "data_traces_per_ensemble": (
                        self.data_traces_per_ensemble
                    ),
                    "auxiliary_traces_per_ensemble": (
                        self.auxiliary_traces_per_ensemble
                    ),
                    "ensemble_fold": self.ensemble_fold,
                }
            )

        if not include_none:
            result = {
                name: value
                for name, value in result.items()
                if value is not None
            }

        return result

    def _prepare_values(self,values: Mapping[str, HeaderValue]) -> dict[str, HeaderValue]:
        """
        Cria uma cópia contendo todos os campos conhecidos.

        Campos não fornecidos recebem None.
        """
        unknown_fields = (
            set(values)
            - set(BINARY_HEADER_FIELDS_BY_NAME)
        )

        if unknown_fields:
            names = ", ".join(sorted(unknown_fields))

            raise UnknownHeaderFieldError(
                f"Campos desconhecidos no Binary Header: {names}."
            )

        return {
            field.name: values.get(field.name)
            for field in BINARY_HEADER_FIELDS
        }

    def _validate_required_fields(self) -> None:
        missing = [
            field_name
            for field_name in REQUIRED_BINARY_HEADER_FIELDS
            if self._values[field_name] is None
        ]

        if missing:
            names = ", ".join(missing)

            raise MissingHeaderFieldError(
                f"Campos obrigatórios não fornecidos: {names}."
            )

    def _validate_values(self) -> None:
        for field in BINARY_HEADER_FIELDS:
            value = self._values[field.name]

            if not field.accepts_value(value):
                raise InvalidHeaderValueError(
                    f"Valor inválido para o campo {field.name!r}: "
                    f"{value!r}. Tipo esperado: "
                    f"{field.data_type.value}."
                )

    def _extended_or_legacy_integer(
        self,
        *,
        extended_name: str,
        legacy_name: str,
    ) -> int:
        extended = self._int_value(
            extended_name,
            default=0,
        )

        if extended > 0:
            return extended

        return self._int_value(
            legacy_name,
            default=0,
        )

    def _int_value(
        self,
        field_name: str,
        *,
        default: int | None = None,
    ) -> int:
        value = self._values.get(field_name)

        if value is None:
            if default is not None:
                return default

            raise MissingHeaderFieldError(
                f"O campo {field_name!r} não possui valor."
            )

        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidHeaderValueError(
                f"O campo {field_name!r} não contém um inteiro."
            )

        return value

    def _float_value(
        self,
        field_name: str,
        *,
        default: float | None = None,
    ) -> float:
        value = self._values.get(field_name)

        if value is None:
            if default is not None:
                return default

            raise MissingHeaderFieldError(
                f"O campo {field_name!r} não possui valor."
            )

        if (
            not isinstance(value, int | float)
            or isinstance(value, bool)
        ):
            raise InvalidHeaderValueError(
                f"O campo {field_name!r} não contém um número."
            )

        return float(value)

    def __getitem__(self, field_name: str) -> HeaderValue:
        try:
            return self._values[field_name]
        except KeyError as error:
            raise UnknownHeaderFieldError(
                f"O campo {field_name!r} não está definido."
            ) from error

    def __contains__(self, field_name: object) -> bool:
        return field_name in self._values

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"revision={self.revision!r}, "
            f"byte_order={self.byte_order.value!r}, "
            f"sample_interval={self.sample_interval!r}, "
            f"samples_per_trace={self.samples_per_trace!r}, "
            f"sample_format_code={self.sample_format_code!r}"
            ")"
        )