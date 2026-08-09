# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_header_fields.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Metadados dos campos atribuídos ao Trace Header conforme  SEG-Y Revision 2.1.

Histórico:
       08/08/2026 - Início da implementação da Classe
===============================================================================
"""
from .header_field import HeaderDataType, HeaderField

def trace_field(name: str,
                byte_start: int,
                byte_end: int,
                data_type: HeaderDataType,
                description: str,
                *,
                unit: str | None = None,
                required: bool = False) -> HeaderField:
    """
    Função auxiliar para criar um campo do Trace Header.
    """

    return HeaderField(name=name,
                       byte_start=byte_start,
                       byte_end=byte_end,
                       data_type=data_type,
                       description=description,
                       unit=unit,
                       required=required,
                      )


TRACE_HEADER_FIELDS: tuple[HeaderField, ...] = (

    trace_field(
        "trace_sequence_line",
        1, 4,
        HeaderDataType.INT32,
        "Número sequencial do traço dentro da linha.",
    ),

    trace_field(
        "trace_sequence_file",
        5, 8,
        HeaderDataType.INT32,
        "Número sequencial do traço dentro do arquivo SEG-Y.",
    ),

    trace_field(
        "field_record_number",
        9, 12,
        HeaderDataType.INT32,
        "Número do registro de campo original.",
    ),

    trace_field(
        "trace_number_field_record",
        13, 16,
        HeaderDataType.INT32,
        "Número do traço dentro do registro de campo original.",
    ),

    trace_field(
        "energy_source_point_number",
        17, 20,
        HeaderDataType.INT32,
        "Número do ponto de fonte de energia.",
    ),

    trace_field(
        "ensemble_number",
        21, 24,
        HeaderDataType.INT32,
        "Número do ensemble (CDP, CMP, CRP etc.).",
    ),

    trace_field(
        "trace_number_ensemble",
        25, 28,
        HeaderDataType.INT32,
        "Número do traço dentro do ensemble.",
    ),

    trace_field(
        "trace_identification_code",
        29, 30,
        HeaderDataType.INT16,
        "Código de identificação do traço.",
    ),

    trace_field(
        "vertically_summed_traces",
        31, 32,
        HeaderDataType.INT16,
        "Número de traços somados verticalmente para formar este traço.",
    ),

    trace_field(
        "horizontally_stacked_traces",
        33, 34,
        HeaderDataType.INT16,
        "Número de traços empilhados horizontalmente para formar este traço.",
    ),

    trace_field(
        "data_use",
        35, 36,
        HeaderDataType.INT16,
        "Tipo de uso do dado: produção ou teste.",
    ),

    trace_field(
        "source_receiver_offset",
        37, 40,
        HeaderDataType.INT32,
        "Distância entre o centro da fonte e o centro do grupo receptor.",
    ),

    trace_field(
        "receiver_group_elevation",
        41, 44,
        HeaderDataType.INT32,
        "Elevação do grupo receptor.",
    ),

    trace_field(
        "source_surface_elevation",
        45, 48,
        HeaderDataType.INT32,
        "Elevação da superfície na posição da fonte.",
    ),

    trace_field(
        "source_depth",
        49, 52,
        HeaderDataType.INT32,
        "Profundidade da fonte abaixo da superfície.",
    ),

    trace_field(
        "receiver_datum_elevation",
        53, 56,
        HeaderDataType.INT32,
        "Elevação do datum sísmico no grupo receptor.",
    ),

    trace_field(
        "source_datum_elevation",
        57, 60,
        HeaderDataType.INT32,
        "Elevação do datum sísmico na fonte.",
    ),

    trace_field(
        "source_water_depth",
        61, 64,
        HeaderDataType.INT32,
        "Altura da coluna d'água na posição da fonte.",
    ),

    trace_field(
        "receiver_water_depth",
        65, 68,
        HeaderDataType.INT32,
        "Altura da coluna d'água na posição do grupo receptor.",
    ),

    trace_field(
        "elevation_scalar",
        69, 70,
        HeaderDataType.INT16,
        "Escalar aplicado às elevações e profundidades dos bytes 41–68.",
    ),

    trace_field(
        "coordinate_scalar",
        71, 72,
        HeaderDataType.INT16,
        "Escalar aplicado às coordenadas dos bytes 73–88 e 181–188.",
    ),

    trace_field(
        "source_x",
        73, 76,
        HeaderDataType.INT32,
        "Coordenada X da fonte.",
    ),

    trace_field(
        "source_y",
        77, 80,
        HeaderDataType.INT32,
        "Coordenada Y da fonte.",
    ),

    trace_field(
        "group_x",
        81, 84,
        HeaderDataType.INT32,
        "Coordenada X do grupo receptor.",
    ),

    trace_field(
        "group_y",
        85, 88,
        HeaderDataType.INT32,
        "Coordenada Y do grupo receptor.",
    ),

    trace_field(
        "coordinate_units",
        89, 90,
        HeaderDataType.INT16,
        "Unidade das coordenadas.",
    ),

    trace_field(
        "weathering_velocity",
        91, 92,
        HeaderDataType.INT16,
        "Velocidade da camada de intemperismo.",
    ),

    trace_field(
        "subweathering_velocity",
        93, 94,
        HeaderDataType.INT16,
        "Velocidade abaixo da camada de intemperismo.",
    ),

    trace_field(
        "uphole_time_source",
        95, 96,
        HeaderDataType.INT16,
        "Tempo de uphole na fonte.",
        unit="ms",
    ),

    trace_field(
        "uphole_time_group",
        97, 98,
        HeaderDataType.INT16,
        "Tempo de uphole no grupo receptor.",
        unit="ms",
    ),

    trace_field(
        "source_static_correction",
        99, 100,
        HeaderDataType.INT16,
        "Correção estática da fonte.",
        unit="ms",
    ),

    trace_field(
        "group_static_correction",
        101, 102,
        HeaderDataType.INT16,
        "Correção estática do grupo receptor.",
        unit="ms",
    ),

    trace_field(
        "total_static_applied",
        103, 104,
        HeaderDataType.INT16,
        "Correção estática total aplicada.",
        unit="ms",
    ),

    trace_field(
        "lag_time_a",
        105, 106,
        HeaderDataType.INT16,
        "Lag Time A.",
        unit="ms",
    ),

    trace_field(
        "lag_time_b",
        107, 108,
        HeaderDataType.INT16,
        "Lag Time B.",
        unit="ms",
    ),

    trace_field(
        "delay_recording_time",
        109, 110,
        HeaderDataType.INT16,
        "Tempo entre a iniciação da fonte e o início da gravação.",
        unit="ms",
    ),

    trace_field(
        "mute_time_start",
        111, 112,
        HeaderDataType.INT16,
        "Tempo inicial do mute.",
        unit="ms",
    ),

    trace_field(
        "mute_time_end",
        113, 114,
        HeaderDataType.INT16,
        "Tempo final do mute.",
        unit="ms",
    ),

    trace_field(
        "samples_in_trace",
        115, 116,
        HeaderDataType.UINT16,
        "Número de amostras neste traço.",
        required=True,
    ),

    trace_field(
        "sample_interval",
        117, 118,
        HeaderDataType.UINT16,
        "Intervalo de amostragem deste traço.",
        required=True,
    ),

    trace_field(
        "gain_type",
        119, 120,
        HeaderDataType.INT16,
        "Tipo de ganho do instrumento de campo.",
    ),

    trace_field(
        "instrument_gain_constant",
        121, 122,
        HeaderDataType.INT16,
        "Constante de ganho do instrumento.",
        unit="dB",
    ),

    trace_field(
        "instrument_initial_gain",
        123, 124,
        HeaderDataType.INT16,
        "Ganho inicial do instrumento.",
        unit="dB",
    ),

    trace_field(
        "correlated",
        125, 126,
        HeaderDataType.INT16,
        "Indica se o traço foi correlacionado.",
    ),

    trace_field(
        "sweep_frequency_start",
        127, 128,
        HeaderDataType.INT16,
        "Frequência inicial do sweep.",
        unit="Hz",
    ),

    trace_field(
        "sweep_frequency_end",
        129, 130,
        HeaderDataType.INT16,
        "Frequência final do sweep.",
        unit="Hz",
    ),

    trace_field(
        "sweep_length",
        131, 132,
        HeaderDataType.INT16,
        "Duração do sweep.",
        unit="ms",
    ),

    trace_field(
        "sweep_type",
        133, 134,
        HeaderDataType.INT16,
        "Tipo de sweep.",
    ),

    trace_field(
        "sweep_trace_taper_length_start",
        135, 136,
        HeaderDataType.INT16,
        "Comprimento do taper no início do sweep.",
        unit="ms",
    ),

    trace_field(
        "sweep_trace_taper_length_end",
        137, 138,
        HeaderDataType.INT16,
        "Comprimento do taper no final do sweep.",
        unit="ms",
    ),

    trace_field(
        "taper_type",
        139, 140,
        HeaderDataType.INT16,
        "Tipo de taper.",
    ),

    trace_field(
        "alias_filter_frequency",
        141, 142,
        HeaderDataType.INT16,
        "Frequência do filtro anti-alias.",
        unit="Hz",
    ),

    trace_field(
        "alias_filter_slope",
        143, 144,
        HeaderDataType.INT16,
        "Inclinação do filtro anti-alias.",
        unit="dB/octave",
    ),

    trace_field(
        "notch_filter_frequency",
        145, 146,
        HeaderDataType.INT16,
        "Frequência do filtro notch.",
        unit="Hz",
    ),

    trace_field(
        "notch_filter_slope",
        147, 148,
        HeaderDataType.INT16,
        "Inclinação do filtro notch.",
        unit="dB/octave",
    ),

    trace_field(
        "low_cut_frequency",
        149, 150,
        HeaderDataType.INT16,
        "Frequência de low-cut.",
        unit="Hz",
    ),

    trace_field(
        "high_cut_frequency",
        151, 152,
        HeaderDataType.INT16,
        "Frequência de high-cut.",
        unit="Hz",
    ),

    trace_field(
        "low_cut_slope",
        153, 154,
        HeaderDataType.INT16,
        "Inclinação do filtro low-cut.",
        unit="dB/octave",
    ),

    trace_field(
        "high_cut_slope",
        155, 156,
        HeaderDataType.INT16,
        "Inclinação do filtro high-cut.",
        unit="dB/octave",
    ),

    trace_field(
        "year_data_recorded",
        157, 158,
        HeaderDataType.INT16,
        "Ano em que o dado foi registrado.",
    ),

    trace_field(
        "day_of_year",
        159, 160,
        HeaderDataType.INT16,
        "Dia do ano.",
    ),

    trace_field(
        "hour_of_day",
        161, 162,
        HeaderDataType.INT16,
        "Hora do dia.",
    ),

    trace_field(
        "minute_of_hour",
        163, 164,
        HeaderDataType.INT16,
        "Minuto da hora.",
    ),

    trace_field(
        "second_of_minute",
        165, 166,
        HeaderDataType.INT16,
        "Segundo do minuto.",
    ),

    trace_field(
        "time_basis_code",
        167, 168,
        HeaderDataType.INT16,
        "Código da base de tempo.",
    ),

    trace_field(
        "trace_weighting_factor",
        169, 170,
        HeaderDataType.INT16,
        "Fator de ponderação do traço.",
    ),

    trace_field(
        "geophone_group_roll_switch",
        171, 172,
        HeaderDataType.INT16,
        "Número do grupo de geofones do roll switch.",
    ),

    trace_field(
        "geophone_group_trace_number_one",
        173, 174,
        HeaderDataType.INT16,
        "Número do grupo de geofones do traço número um.",
    ),

    trace_field(
        "geophone_group_last_trace",
        175, 176,
        HeaderDataType.INT16,
        "Número do grupo de geofones do último traço.",
    ),

    trace_field(
        "gap_size",
        177, 178,
        HeaderDataType.INT16,
        "Tamanho do gap: número total de grupos descartados.",
    ),

    trace_field(
        "over_travel",
        179, 180,
        HeaderDataType.INT16,
        "Over travel associado ao taper no início ou fim da linha.",
    ),

    # ----------------------------------------------------------
    # Campos adicionados/definidos nas revisões posteriores
    # ----------------------------------------------------------

    trace_field(
        "ensemble_x",
        181, 184,
        HeaderDataType.INT32,
        "Coordenada X da posição do ensemble (CDP) deste traço.",
    ),

    trace_field(
        "ensemble_y",
        185, 188,
        HeaderDataType.INT32,
        "Coordenada Y da posição do ensemble (CDP) deste traço.",
    ),

    trace_field(
        "inline_number",
        189, 192,
        HeaderDataType.INT32,
        "Número de inline para dados 3-D pós-stack.",
    ),

    trace_field(
        "crossline_number",
        193, 196,
        HeaderDataType.INT32,
        "Número de crossline para dados 3-D pós-stack.",
    ),

    trace_field(
        "shotpoint_number",
        197, 200,
        HeaderDataType.INT32,
        "Número do shotpoint.",
    ),

    trace_field(
        "shotpoint_scalar",
        201, 202,
        HeaderDataType.INT16,
        "Escalar aplicado ao número do shotpoint.",
    ),

    # ----------------------------------------------------------
    # SEG-Y Rev 2.x
    # ----------------------------------------------------------

    trace_field(
        "trace_value_measurement_unit",
        203, 204,
        HeaderDataType.INT16,
        "Unidade de medida dos valores das amostras do traço.",
    ),

    trace_field(
        "transduction_constant",
        205, 210,
        HeaderDataType.RAW_BYTES,
        "Constante de transdução usada para converter as amostras "
        "para as unidades de transdução.",
    ),

    trace_field(
        "transduction_units",
        211, 212,
        HeaderDataType.INT16,
        "Unidade de medida após aplicação da constante de transdução.",
    ),

    trace_field(
        "device_trace_identifier",
        213, 214,
        HeaderDataType.INT16,
        "Identificador da unidade ou dispositivo associado ao traço.",
    ),

    trace_field(
        "time_scalar",
        215, 216,
        HeaderDataType.INT16,
        "Escalar aplicado aos tempos especificados nos bytes 95–114.",
    ),

    trace_field(
        "source_type_orientation",
        217, 218,
        HeaderDataType.INT16,
        "Tipo e orientação da fonte de energia.",
    ),

    trace_field(
        "source_energy_direction",
        219, 224,
        HeaderDataType.RAW_BYTES,
        "Direção da energia da fonte para as orientações vertical, "
        "cross-line e in-line.",
    ),

    trace_field(
        "source_measurement",
        225, 230,
        HeaderDataType.RAW_BYTES,
        "Medição do esforço da fonte usado para gerar o traço.",
    ),

    trace_field(
        "source_measurement_unit",
        231, 232,
        HeaderDataType.INT16,
        "Unidade utilizada para a medição da fonte.",
    ),

    trace_field(
        "trace_header_name",
        233, 240,
        HeaderDataType.RAW_BYTES,
        "Zeros binários ou nome de oito caracteres do Trace Header "
        "(por exemplo, 'SEG00000').",
    ),
)


TRACE_HEADER_FIELDS_BY_NAME: dict[str, HeaderField] = {
    field.name: field
    for field in TRACE_HEADER_FIELDS
}

REQUIRED_TRACE_HEADER_FIELDS: tuple[str, ...] = tuple(
    field.name
    for field in TRACE_HEADER_FIELDS
    if field.required
)