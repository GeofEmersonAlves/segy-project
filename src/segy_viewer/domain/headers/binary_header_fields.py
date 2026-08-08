# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : binary_header_fields.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Metadados dos campos atribuídos do Binary File Header conforme
    SEG-Y Revision 2.1.

Histórico:
       06/08/2026 - Início da implementação da Classe
===============================================================================
"""
from .header_field import HeaderDataType, HeaderField

def binary_field(name: str,
                 byte_start: int,
                 byte_end: int,
                 data_type: HeaderDataType,
                 description: str,
                 *,
                 unit: str | None = None,
                 required: bool = False) -> HeaderField:

    """
    Função auxiliar para criar um campo do Binary File Header.
    """

    return HeaderField(name = name, byte_start = byte_start,
                       byte_end = byte_end, data_type=data_type,
                       description = description, unit = unit, required = required)


BINARY_HEADER_FIELDS: tuple[HeaderField, ...] = (
    binary_field(
        "job_id",
        3201,
        3204,
        HeaderDataType.INT32,
        "Número de identificação do trabalho.",
    ),
    binary_field(
        "line_number",
        3205,
        3208,
        HeaderDataType.INT32,
        "Número da linha.",
    ),
    binary_field(
        "reel_number",
        3209,
        3212,
        HeaderDataType.INT32,
        "Número do reel.",
    ),
    binary_field(
        "data_traces_per_ensemble",
        3213,
        3214,
        HeaderDataType.UINT16,
        "Número de traços de dados por ensemble.",
    ),
    binary_field(
        "auxiliary_traces_per_ensemble",
        3215,
        3216,
        HeaderDataType.UINT16,
        "Número de traços auxiliares por ensemble.",
    ),
    binary_field(
        "sample_interval",
        3217,
        3218,
        HeaderDataType.UINT16,
        "Intervalo de amostragem dos traços principais.",
        unit="µs",
        required=True,
    ),
    binary_field(
        "original_sample_interval",
        3219,
        3220,
        HeaderDataType.UINT16,
        "Intervalo de amostragem da gravação original.",
        unit="µs",
    ),
    binary_field(
        "samples_per_trace",
        3221,
        3222,
        HeaderDataType.UINT16,
        "Número de amostras por traço.",
        required=True,
    ),
    binary_field(
        "original_samples_per_trace",
        3223,
        3224,
        HeaderDataType.UINT16,
        "Número de amostras por traço na gravação original.",
    ),
    binary_field(
        "sample_format_code",
        3225,
        3226,
        HeaderDataType.INT16,
        "Código do formato das amostras.",
        required=True,
    ),
    binary_field(
        "ensemble_fold",
        3227,
        3228,
        HeaderDataType.UINT16,
        "Número esperado de traços por ensemble.",
    ),
    binary_field(
        "trace_sorting_code",
        3229,
        3230,
        HeaderDataType.INT16,
        "Código de ordenação dos traços.",
    ),
    binary_field(
        "vertical_sum_code",
        3231,
        3232,
        HeaderDataType.UINT16,
        "Código de soma vertical.",
    ),
    binary_field(
        "sweep_frequency_start",
        3233,
        3234,
        HeaderDataType.UINT16,
        "Frequência inicial do sweep.",
        unit="Hz",
    ),
    binary_field(
        "sweep_frequency_end",
        3235,
        3236,
        HeaderDataType.UINT16,
        "Frequência final do sweep.",
        unit="Hz",
    ),
    binary_field(
        "sweep_length",
        3237,
        3238,
        HeaderDataType.UINT16,
        "Duração do sweep.",
        unit="ms",
    ),
    binary_field(
        "sweep_type_code",
        3239,
        3240,
        HeaderDataType.INT16,
        "Código do tipo de sweep.",
    ),
    binary_field(
        "sweep_trace_number",
        3241,
        3242,
        HeaderDataType.UINT16,
        "Número do canal do sweep.",
    ),
    binary_field(
        "sweep_taper_length_start",
        3243,
        3244,
        HeaderDataType.UINT16,
        "Comprimento do taper no início do sweep.",
        unit="ms",
    ),
    binary_field(
        "sweep_taper_length_end",
        3245,
        3246,
        HeaderDataType.UINT16,
        "Comprimento do taper no final do sweep.",
        unit="ms",
    ),
    binary_field(
        "taper_type_code",
        3247,
        3248,
        HeaderDataType.INT16,
        "Código do tipo de taper.",
    ),
    binary_field(
        "correlated_data_traces",
        3249,
        3250,
        HeaderDataType.INT16,
        "Indicador de traços correlacionados.",
    ),
    binary_field(
        "binary_gain_recovered",
        3251,
        3252,
        HeaderDataType.INT16,
        "Indicador de recuperação do ganho binário.",
    ),
    binary_field(
        "amplitude_recovery_method",
        3253,
        3254,
        HeaderDataType.INT16,
        "Método de recuperação de amplitude.",
    ),
    binary_field(
        "measurement_system",
        3255,
        3256,
        HeaderDataType.INT16,
        "Sistema de medidas: 1 = metros; 2 = pés.",
    ),
    binary_field(
        "impulse_signal_polarity",
        3257,
        3258,
        HeaderDataType.INT16,
        "Polaridade do sinal impulsivo.",
    ),
    binary_field(
        "vibratory_polarity_code",
        3259,
        3260,
        HeaderDataType.INT16,
        "Código de polaridade vibratória.",
    ),

    # Campos estendidos

    binary_field(
        "extended_data_traces_per_ensemble",
        3261,
        3264,
        HeaderDataType.UINT32,
        "Número estendido de traços de dados por ensemble.",
    ),
    binary_field(
        "extended_auxiliary_traces_per_ensemble",
        3265,
        3268,
        HeaderDataType.UINT32,
        "Número estendido de traços auxiliares por ensemble.",
    ),
    binary_field(
        "extended_samples_per_trace",
        3269,
        3272,
        HeaderDataType.UINT32,
        "Número estendido de amostras por traço.",
    ),
    binary_field(
        "extended_sample_interval",
        3273,
        3280,
        HeaderDataType.FLOAT64,
        "Intervalo estendido de amostragem.",
        unit="µs",
    ),
    binary_field(
        "extended_original_sample_interval",
        3281,
        3288,
        HeaderDataType.FLOAT64,
        "Intervalo estendido de amostragem da gravação original.",
        unit="µs",
    ),
    binary_field(
        "extended_original_samples_per_trace",
        3289,
        3292,
        HeaderDataType.UINT32,
        "Número estendido de amostras da gravação original.",
    ),
    binary_field(
        "extended_ensemble_fold",
        3293,
        3296,
        HeaderDataType.UINT32,
        "Fold estendido do ensemble.",
    ),
    binary_field(
        "byte_order_detection_constant",
        3297,
        3300,
        HeaderDataType.UINT32,
        "Constante utilizada para identificação da ordem dos bytes.",
    ),

    binary_field(
        "revision_major",
        3501,
        3501,
        HeaderDataType.UINT8,
        "Número principal da revisão SEG-Y.",
        required=True,
    ),
    binary_field(
        "revision_minor",
        3502,
        3502,
        HeaderDataType.UINT8,
        "Número secundário da revisão SEG-Y.",
        required=True,
    ),
    binary_field(
        "fixed_length_trace_flag",
        3503,
        3504,
        HeaderDataType.INT16,
        "Indicador de traços com comprimento fixo.",
    ),
    binary_field(
        "extended_textual_header_count",
        3505,
        3506,
        HeaderDataType.INT16,
        "Quantidade de Extended Textual File Header records.",
    ),
    binary_field(
        "maximum_additional_trace_headers",
        3507,
        3508,
        HeaderDataType.UINT16,
        "Quantidade máxima de Trace Header Extensions.",
    ),
    binary_field(
        "survey_type",
        3509,
        3510,
        HeaderDataType.UINT16,
        "Código do tipo de levantamento.",
    ),
    binary_field(
        "time_basis_code",
        3511,
        3512,
        HeaderDataType.INT16,
        "Código da base de tempo.",
    ),
    binary_field(
        "trace_count",
        3513,
        3520,
        HeaderDataType.UINT64,
        "Quantidade de traços no arquivo ou stream.",
    ),
    binary_field(
        "first_trace_byte_offset",
        3521,
        3528,
        HeaderDataType.UINT64,
        "Offset do primeiro traço em relação ao início do arquivo.",
        unit="bytes",
    ),
    binary_field(
        "data_trailer_count",
        3529,
        3532,
        HeaderDataType.INT32,
        "Quantidade de Data Trailer Stanza records.",
    ),
)


BINARY_HEADER_FIELDS_BY_NAME: dict[str, HeaderField] = {
    field.name: field
    for field in BINARY_HEADER_FIELDS
}


REQUIRED_BINARY_HEADER_FIELDS: tuple[str, ...] = tuple(
    field.name
    for field in BINARY_HEADER_FIELDS
    if field.required
)