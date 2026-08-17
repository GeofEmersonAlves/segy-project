# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_header.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Representação do Trace Header de um traço SEG-Y.

Histórico:
       08/08/2026 - Início da implementação da Classe
===============================================================================
"""

from collections.abc import Iterator, Mapping
from types import MappingProxyType
from typing import Any

from .byte_order import ByteOrder
from .header_field import HeaderField, HeaderValue
from .trace_header_fields import (
    TRACE_HEADER_FIELDS,
    TRACE_HEADER_FIELDS_BY_NAME,
    REQUIRED_TRACE_HEADER_FIELDS,
)

from segy_viewer.domain.exceptions.headers_exceptions import (
    InvalidHeaderValueError,
    MissingHeaderFieldError,
    UnknownHeaderFieldError,
)


class SegyTraceHeader:
    """
    Representa os valores dos 240 bytes do Trace Header SEG-Y.

    Parameters
    ----------
    values:
        Mapeamento entre o nome interno do campo e seu valor.

    byte_order:
        Ordem dos bytes utilizada pelo arquivo.
    """

    def __init__(self,
                values: Mapping[str, HeaderValue],
                *,
                byte_order: ByteOrder = ByteOrder.UNKNOWN) -> None:

        self._byte_order = byte_order
        self._values = self._prepare_values(values)

        self._validate_required_fields()
        self._validate_values()

    # ==================================================================
    # PROPRIEDADES GERAIS
    # ==================================================================

    @property
    def byte_order(self) -> ByteOrder:
        """
        Ordem de bytes utilizada na interpretação do Trace Header.
        """
        return self._byte_order

    @property
    def fields(self) -> tuple[HeaderField, ...]:
        """
        Definições de todos os campos do Trace Header.
        """
        return TRACE_HEADER_FIELDS

    @property
    def values(self) -> Mapping[str, HeaderValue]:
        """
        Visualização somente para leitura dos valores do header.
        """
        return MappingProxyType(self._values)

    # ==================================================================
    # IDENTIFICAÇÃO DO TRAÇO
    # ==================================================================

    @property
    def trace_sequence_line(self) -> int:
        """
        Número sequencial do traço dentro da linha.
        """
        return self._int_value(
            "trace_sequence_line",
            default=0,
        )

    @property
    def trace_sequence_file(self) -> int:
        """
        Número sequencial do traço dentro do arquivo SEG-Y.
        """
        return self._int_value(
            "trace_sequence_file",
            default=0,
        )

    @property
    def field_record_number(self) -> int:
        """
        Número do registro de campo original.
        """
        return self._int_value(
            "field_record_number",
            default=0,
        )

    @property
    def trace_number_field_record(self) -> int:
        """
        Número do traço dentro do registro de campo.
        """
        return self._int_value(
            "trace_number_field_record",
            default=0,
        )

    @property
    def energy_source_point_number(self) -> int:
        """
        Número do ponto de fonte de energia.
        """
        return self._int_value(
            "energy_source_point_number",
            default=0,
        )

    @property
    def ensemble_number(self) -> int:
        """
        Número do ensemble (CMP, CDP, CRP etc.).
        """
        return self._int_value(
            "ensemble_number",
            default=0,
        )

    @property
    def trace_number_ensemble(self) -> int:
        """
        Número do traço dentro do ensemble.
        """
        return self._int_value(
            "trace_number_ensemble",
            default=0,
        )

    @property
    def trace_identification_code(self) -> int:
        """
        Código de identificação do traço.
        """
        return self._int_value(
            "trace_identification_code",
            default=0,
        )

    # ==================================================================
    # AMOSTRAS
    # ==================================================================

    @property
    def samples_in_trace(self) -> int:
        """
        Número de amostras existentes neste traço.

        Corresponde aos bytes 115-116 do Trace Header.
        """
        return self._int_value("samples_in_trace")

    @property
    def sample_interval(self) -> int:
        """
        Intervalo de amostragem deste traço.

        Corresponde aos bytes 117-118.

        O valor normalmente é expresso em microssegundos.
        """
        return self._int_value("sample_interval")

    @property
    def sample_interval_seconds(self) -> float:
        """
        Intervalo de amostragem convertido para segundos.
        """
        return self.sample_interval / 1_000_000.0

    @property
    def sample_interval_ms(self) -> float:
        """
        Intervalo de amostragem convertido para milissegundos.
        """
        return self.sample_interval / 1_000.0

    @property
    def trace_duration_seconds(self) -> float:
        """
        Duração correspondente às amostras do traço.

        Representa:

            número de amostras × intervalo de amostragem

        É uma informação derivada e não um campo armazenado no header.
        """
        return (
            self.samples_in_trace
            * self.sample_interval_seconds
        )

    # ==================================================================
    # OFFSET
    # ==================================================================

    @property
    def source_receiver_offset(self) -> int:
        """
        Distância fonte-receptor armazenada no Trace Header.
        """
        return self._int_value(
            "source_receiver_offset",
            default=0,
        )

    # ==================================================================
    # ESCALARES
    # ==================================================================

    @property
    def elevation_scalar(self) -> int:
        """
        Escalar aplicado às elevações e profundidades.
        """
        return self._int_value(
            "elevation_scalar",
            default=0,
        )

    @property
    def coordinate_scalar(self) -> int:
        """
        Escalar aplicado às coordenadas.
        """
        return self._int_value(
            "coordinate_scalar",
            default=0,
        )

    @property
    def shotpoint_scalar(self) -> int:
        """
        Escalar aplicado ao número do shotpoint.
        """
        return self._int_value(
            "shotpoint_scalar",
            default=0,
        )

    @property
    def time_scalar(self) -> int:
        """
        Escalar aplicado aos campos de tempo.
        """
        return self._int_value(
            "time_scalar",
            default=0,
        )

    # ==================================================================
    # COORDENADAS BRUTAS
    # ==================================================================

    @property
    def source_x_raw(self) -> int:
        return self._int_value(
            "source_x",
            default=0,
        )

    @property
    def source_y_raw(self) -> int:
        return self._int_value(
            "source_y",
            default=0,
        )

    @property
    def group_x_raw(self) -> int:
        return self._int_value(
            "group_x",
            default=0,
        )

    @property
    def group_y_raw(self) -> int:
        return self._int_value(
            "group_y",
            default=0,
        )

    @property
    def ensemble_x_raw(self) -> int:
        return self._int_value(
            "ensemble_x",
            default=0,
        )

    @property
    def ensemble_y_raw(self) -> int:
        return self._int_value(
            "ensemble_y",
            default=0,
        )

    # ==================================================================
    # COORDENADAS COM ESCALAR APLICADO
    # ==================================================================

    @property
    def source_x(self) -> float:
        """
        Coordenada X efetiva da fonte.
        """
        return self._apply_scalar(
            self.source_x_raw,
            self.coordinate_scalar,
        )

    @property
    def source_y(self) -> float:
        """
        Coordenada Y efetiva da fonte.
        """
        return self._apply_scalar(
            self.source_y_raw,
            self.coordinate_scalar,
        )

    @property
    def group_x(self) -> float:
        """
        Coordenada X efetiva do receptor.
        """
        return self._apply_scalar(
            self.group_x_raw,
            self.coordinate_scalar,
        )

    @property
    def group_y(self) -> float:
        """
        Coordenada Y efetiva do receptor.
        """
        return self._apply_scalar(
            self.group_y_raw,
            self.coordinate_scalar,
        )

    @property
    def ensemble_x(self) -> float:
        """
        Coordenada X efetiva do ensemble.
        """
        return self._apply_scalar(
            self.ensemble_x_raw,
            self.coordinate_scalar,
        )

    @property
    def ensemble_y(self) -> float:
        """
        Coordenada Y efetiva do ensemble.
        """
        return self._apply_scalar(
            self.ensemble_y_raw,
            self.coordinate_scalar,
        )

    # ==================================================================
    # ELEVAÇÕES E PROFUNDIDADES
    # ==================================================================

    @property
    def receiver_group_elevation(self) -> float:
        return self._scaled_integer_value(
            "receiver_group_elevation",
            self.elevation_scalar,
        )

    @property
    def source_surface_elevation(self) -> float:
        return self._scaled_integer_value(
            "source_surface_elevation",
            self.elevation_scalar,
        )

    @property
    def source_depth(self) -> float:
        return self._scaled_integer_value(
            "source_depth",
            self.elevation_scalar,
        )

    @property
    def receiver_datum_elevation(self) -> float:
        return self._scaled_integer_value(
            "receiver_datum_elevation",
            self.elevation_scalar,
        )

    @property
    def source_datum_elevation(self) -> float:
        return self._scaled_integer_value(
            "source_datum_elevation",
            self.elevation_scalar,
        )

    @property
    def source_water_depth(self) -> float:
        return self._scaled_integer_value(
            "source_water_depth",
            self.elevation_scalar,
        )

    @property
    def receiver_water_depth(self) -> float:
        return self._scaled_integer_value(
            "receiver_water_depth",
            self.elevation_scalar,
        )

    # ==================================================================
    # GEOMETRIA 3-D
    # ==================================================================

    @property
    def inline_number(self) -> int:
        """
        Número de inline.
        """
        return self._int_value(
            "inline_number",
            default=0,
        )

    @property
    def crossline_number(self) -> int:
        """
        Número de crossline.
        """
        return self._int_value(
            "crossline_number",
            default=0,
        )

    @property
    def shotpoint_number_raw(self) -> int:
        """
        Número bruto do shotpoint.
        """
        return self._int_value(
            "shotpoint_number",
            default=0,
        )

    @property
    def shotpoint_number(self) -> float:
        """
        Número do shotpoint com seu escalar aplicado.
        """
        return self._apply_scalar(
            self.shotpoint_number_raw,
            self.shotpoint_scalar,
        )

    # ==================================================================
    # UNIDADES
    # ==================================================================

    @property
    def coordinate_units(self) -> int:
        """
        Código da unidade das coordenadas.
        """
        return self._int_value(
            "coordinate_units",
            default=0,
        )

    @property
    def trace_value_measurement_unit(self) -> int:
        """
        Código da unidade dos valores das amostras.
        """
        return self._int_value(
            "trace_value_measurement_unit",
            default=0,
        )

    @property
    def transduction_units(self) -> int:
        """
        Código da unidade física após aplicação da
        constante de transdução.
        """
        return self._int_value(
            "transduction_units",
            default=0,
        )

    # ==================================================================
    # CAMPOS COMPOSTOS / RAW BYTES
    # ==================================================================

    @property
    def transduction_constant_raw(self) -> bytes | None:
        """
        Representação bruta dos bytes 205-210.

        A interpretação em mantissa e expoente deve ser realizada
        pelo reader ou por um Value Object específico.
        """
        return self._bytes_value(
            "transduction_constant",
            default=None,
        )

    @property
    def source_energy_direction_raw(self) -> bytes | None:
        """
        Representação bruta dos bytes 219-224.
        """
        return self._bytes_value(
            "source_energy_direction",
            default=None,
        )

    @property
    def source_measurement_raw(self) -> bytes | None:
        """
        Representação bruta dos bytes 225-230.
        """
        return self._bytes_value(
            "source_measurement",
            default=None,
        )

    @property
    def trace_header_name_raw(self) -> bytes | None:
        """
        Conteúdo bruto dos bytes 233-240.
        """
        return self._bytes_value(
            "trace_header_name",
            default=None,
        )

    @property
    def trace_header_name(self) -> str | None:
        """
        Nome do Trace Header, quando os bytes 233-240 contêm texto.

        Bytes nulos são removidos.
        """
        raw = self.trace_header_name_raw

        if raw is None:
            return None

        cleaned = raw.rstrip(b"\x00")

        if not cleaned:
            return None

        return cleaned.decode(
            "ascii",
            errors="replace",
        )

    # ==================================================================
    # ACESSO GENÉRICO
    # ==================================================================

    def get(
        self,
        field_name: str,
        default: Any = None,
    ) -> HeaderValue | Any:
        """
        Retorna o valor bruto fornecido pelo leitor.
        """
        return self._values.get(
            field_name,
            default,
        )

    def get_field(self,field_name: str) -> HeaderField:
        """
        Retorna os metadados de um campo do Trace Header.
        """
        try:
            return TRACE_HEADER_FIELDS_BY_NAME[field_name]

        except KeyError as error:
            raise UnknownHeaderFieldError(f"O campo {field_name!r} não está definido no "
                                          "Trace Header.") from error

    def raw_items(self) -> Iterator[tuple[HeaderField, HeaderValue]]:
        """
        Percorre os metadados e valores brutos do Trace Header.
        """
        for field in TRACE_HEADER_FIELDS:
            yield field, self._values[field.name]

    def to_dict(self, *, effective_values: bool = False, include_none: bool = True) -> dict[str, dict[str, Any]]:
        """
        Converte o Trace Header para um dicionário contendo
        o valor e os metadados de cada campo.

        Parameters
        ----------
        effective_values:
            Quando True, substitui alguns valores brutos por seus
            valores efetivos após aplicação dos escalares.

        include_none:
            Quando False, remove campos sem valor.
        """

        values = dict(self._values)

        if effective_values:
            values.update(
                {
                    "source_x": self.source_x,
                    "source_y": self.source_y,
                    "group_x": self.group_x,
                    "group_y": self.group_y,
                    "ensemble_x": self.ensemble_x,
                    "ensemble_y": self.ensemble_y,
                    "receiver_group_elevation": (self.receiver_group_elevation),
                    "source_surface_elevation": (self.source_surface_elevation),
                    "source_depth": self.source_depth,
                    "receiver_datum_elevation": (self.receiver_datum_elevation),
                    "source_datum_elevation": (self.source_datum_elevation),
                    "source_water_depth": (self.source_water_depth),
                    "receiver_water_depth": (self.receiver_water_depth),
                    "shotpoint_number": self.shotpoint_number,
                }
            )

        result = {}

        for name, value in values.items():

            if not include_none and value is None:
                continue

            field = TRACE_HEADER_FIELDS_BY_NAME[name]

            result[name] = {
                            "value": value,
                            "trace_header_field": field.to_dict(),
                          }

        return result

    # ==================================================================
    # VALIDAÇÃO
    # ==================================================================

    def _prepare_values(
        self,
        values: Mapping[str, HeaderValue],
    ) -> dict[str, HeaderValue]:
        """
        Cria uma cópia contendo todos os campos conhecidos.

        Campos não fornecidos recebem None.
        """
        unknown_fields = (
            set(values)
            - set(TRACE_HEADER_FIELDS_BY_NAME)
        )

        if unknown_fields:
            names = ", ".join(
                sorted(unknown_fields)
            )

            raise UnknownHeaderFieldError(
                "Campos desconhecidos no Trace Header: "
                f"{names}."
            )

        return {
            field.name: values.get(field.name)
            for field in TRACE_HEADER_FIELDS
        }

    def _validate_required_fields(self) -> None:
        """
        Verifica se todos os campos obrigatórios foram fornecidos.
        """
        missing = [
            field_name
            for field_name in REQUIRED_TRACE_HEADER_FIELDS
            if self._values[field_name] is None
        ]

        if missing:
            names = ", ".join(missing)

            raise MissingHeaderFieldError(
                "Campos obrigatórios não fornecidos no "
                f"Trace Header: {names}."
            )

    def _validate_values(self) -> None:
        """
        Valida os tipos dos valores de acordo com seus HeaderFields.
        """
        for field in TRACE_HEADER_FIELDS:

            value = self._values[field.name]

            if not field.accepts_value(value):
                raise InvalidHeaderValueError(
                    f"Valor inválido para o campo "
                    f"{field.name!r}: {value!r}. "
                    f"Tipo esperado: "
                    f"{field.data_type.value}."
                )

    # ==================================================================
    # MÉTODOS AUXILIARES
    # ==================================================================

    @staticmethod
    def _apply_scalar(
        value: int | float,
        scalar: int,
    ) -> float:
        """
        Aplica um escalar SEG-Y.

        Regras
        ------
        scalar = 0:
            O valor permanece inalterado.

        scalar > 0:
            O valor é multiplicado pelo escalar.

        scalar < 0:
            O valor é dividido pelo valor absoluto do escalar.
        """
        if scalar == 0:
            return float(value)

        if scalar > 0:
            return float(value * scalar)

        return float(
            value / abs(scalar)
        )

    def _scaled_integer_value(
        self,
        field_name: str,
        scalar: int,
    ) -> float:
        """
        Obtém um inteiro e aplica o escalar SEG-Y.
        """
        value = self._int_value(
            field_name,
            default=0,
        )

        return self._apply_scalar(
            value,
            scalar,
        )

    def _int_value(
        self,
        field_name: str,
        *,
        default: int | None = None,
    ) -> int:
        """
        Obtém um valor inteiro do header.
        """
        value = self._values.get(field_name)

        if value is None:

            if default is not None:
                return default

            raise MissingHeaderFieldError(
                f"O campo {field_name!r} não possui valor."
            )

        if (
            not isinstance(value, int)
            or isinstance(value, bool)
        ):
            raise InvalidHeaderValueError(
                f"O campo {field_name!r} "
                "não contém um inteiro."
            )

        return value

    def _float_value(
        self,
        field_name: str,
        *,
        default: float | None = None,
    ) -> float:
        """
        Obtém um valor numérico do header.
        """
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
                f"O campo {field_name!r} "
                "não contém um número."
            )

        return float(value)

    def _bytes_value(
        self,
        field_name: str,
        *,
        default: bytes | None = None,
    ) -> bytes | None:
        """
        Obtém um campo armazenado como bytes brutos.
        """
        value = self._values.get(field_name)

        if value is None:
            return default

        if not isinstance(value, bytes):
            raise InvalidHeaderValueError(
                f"O campo {field_name!r} "
                "não contém bytes."
            )

        return value

    # ==================================================================
    # PROTOCOLO DE CONTAINER
    # ==================================================================

    def __getitem__(
        self,
        field_name: str,
    ) -> HeaderValue:
        try:
            return self._values[field_name]

        except KeyError as error:
            raise UnknownHeaderFieldError(
                f"O campo {field_name!r} "
                "não está definido."
            ) from error

    def __contains__(
        self,
        field_name: object,
    ) -> bool:
        return field_name in self._values

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"trace_sequence_file="
            f"{self.trace_sequence_file!r}, "
            f"field_record_number="
            f"{self.field_record_number!r}, "
            f"samples_in_trace="
            f"{self.samples_in_trace!r}, "
            f"sample_interval="
            f"{self.sample_interval!r}, "
            f"inline="
            f"{self.inline_number!r}, "
            f"crossline="
            f"{self.crossline_number!r}"
            ")"
        )