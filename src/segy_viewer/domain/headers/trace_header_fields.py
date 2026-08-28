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
       28/08/2026 - Tradução dos Descriptions para Ingles
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
        "Trace sequence number within line.",
    ),

    trace_field(
        "trace_sequence_file",
        5, 8,
        HeaderDataType.INT32,
        "Trace sequence number within SEG-Y file.",
    ),

    trace_field(
        "field_record_number",
        9, 12,
        HeaderDataType.INT32,
        "Original field record number.",
    ),

    trace_field(
        "trace_number_field_record",
        13, 16,
        HeaderDataType.INT32,
        "Trace number within the original field record.",
    ),

    trace_field(
        "energy_source_point_number",
        17, 20,
        HeaderDataType.INT32,
        "Energy source point number.",
    ),

    trace_field(
        "ensemble_number",
        21, 24,
        HeaderDataType.INT32,
        "Ensemble number.",
    ),

    trace_field(
        "trace_number_ensemble",
        25, 28,
        HeaderDataType.INT32,
        "Trace number within the ensemble.",
    ),

    trace_field(
        "trace_identification_code",
        29, 30,
        HeaderDataType.INT16,
        "Trace identification code.",
    ),

    trace_field(
        "vertically_summed_traces",
        31, 32,
        HeaderDataType.INT16,
        "Number of vertically summed traces yielding this trace.",
    ),

    trace_field(
        "horizontally_stacked_traces",
        33, 34,
        HeaderDataType.INT16,
        "Number of horizontally stacked traces yielding this trace.",
    ),

    trace_field(
        "data_use",
        35, 36,
        HeaderDataType.INT16,
        "Data use.",
    ),

    trace_field(
        "source_receiver_offset",
        37, 40,
        HeaderDataType.INT32,
        "Distance from center of source point to center of receiver group.",
    ),

    trace_field(
        "receiver_group_elevation",
        41, 44,
        HeaderDataType.INT32,
        "Receiver group elevation.",
    ),

    trace_field(
        "source_surface_elevation",
        45, 48,
        HeaderDataType.INT32,
        "Surface elevation at source.",
    ),

    trace_field(
        "source_depth",
        49, 52,
        HeaderDataType.INT32,
        "Source depth below surface.",
    ),

    trace_field(
        "receiver_datum_elevation",
        53, 56,
        HeaderDataType.INT32,
        "Datum elevation at receiver group.",
    ),

    trace_field(
        "source_datum_elevation",
        57, 60,
        HeaderDataType.INT32,
        "Datum elevation at source.",
    ),

    trace_field(
        "source_water_depth",
        61, 64,
        HeaderDataType.INT32,
        "Water depth at source.",
    ),

    trace_field(
        "receiver_water_depth",
        65, 68,
        HeaderDataType.INT32,
        "Water depth at group.",
    ),

    trace_field(
        "elevation_scalar",
        69, 70,
        HeaderDataType.INT16,
        "Scalar to be applied to all elevations and depths specified in bytes 41–68.",
    ),

    trace_field(
        "coordinate_scalar",
        71, 72,
        HeaderDataType.INT16,
        "Scalar to be applied to all coordinates specified in bytes 73–88 and 181–188.",
    ),

    trace_field(
        "source_x",
        73, 76,
        HeaderDataType.INT32,
        "Source coordinate X.",
    ),

    trace_field(
        "source_y",
        77, 80,
        HeaderDataType.INT32,
        "Source coordinate Y.",
    ),

    trace_field(
        "group_x",
        81, 84,
        HeaderDataType.INT32,
        "Group coordinate X.",
    ),

    trace_field(
        "group_y",
        85, 88,
        HeaderDataType.INT32,
        "Group coordinate Y.",
    ),

    trace_field(
        "coordinate_units",
        89, 90,
        HeaderDataType.INT16,
        "Coordinate units.",
    ),

    trace_field(
        "weathering_velocity",
        91, 92,
        HeaderDataType.INT16,
        "Weathering velocity.",
    ),

    trace_field(
        "subweathering_velocity",
        93, 94,
        HeaderDataType.INT16,
        "Subweathering velocity.",
    ),

    trace_field(
        "uphole_time_source",
        95, 96,
        HeaderDataType.INT16,
        "Uphole time at source.",
        unit="ms",
    ),

    trace_field(
        "uphole_time_group",
        97, 98,
        HeaderDataType.INT16,
        "Uphole time at group.",
        unit="ms",
    ),

    trace_field(
        "source_static_correction",
        99, 100,
        HeaderDataType.INT16,
        "Source static correction.",
        unit="ms",
    ),

    trace_field(
        "group_static_correction",
        101, 102,
        HeaderDataType.INT16,
        "Group static correction.",
        unit="ms",
    ),

    trace_field(
        "total_static_applied",
        103, 104,
        HeaderDataType.INT16,
        "Total static applied.",
        unit="ms",
    ),

    trace_field(
        "lag_time_a",
        105, 106,
        HeaderDataType.INT16,
        "Lag time A.",
        unit="ms",
    ),

    trace_field(
        "lag_time_b",
        107, 108,
        HeaderDataType.INT16,
        "Lag time B.",
        unit="ms",
    ),

    trace_field(
        "delay_recording_time",
        109, 110,
        HeaderDataType.INT16,
        "Delay recording time.",
        unit="ms",
    ),

    trace_field(
        "mute_time_start",
        111, 112,
        HeaderDataType.INT16,
        "Mute time — start time.",
        unit="ms",
    ),

    trace_field(
        "mute_time_end",
        113, 114,
        HeaderDataType.INT16,
        "Mute time — end time.",
        unit="ms",
    ),

    trace_field(
        "samples_in_trace",
        115, 116,
        HeaderDataType.UINT16,
        "Number of samples in this trace.",
        required=True,
    ),

    trace_field(
        "sample_interval",
        117, 118,
        HeaderDataType.UINT16,
        "Sample interval in microseconds for this trace.",
        required=True,
    ),

    trace_field(
        "gain_type",
        119, 120,
        HeaderDataType.INT16,
        "Gain type of field instruments.",
    ),

    trace_field(
        "instrument_gain_constant",
        121, 122,
        HeaderDataType.INT16,
        "Instrument gain constant.",
        unit="dB",
    ),

    trace_field(
        "instrument_initial_gain",
        123, 124,
        HeaderDataType.INT16,
        "Instrument early or initial gain.",
        unit="dB",
    ),

    trace_field(
        "correlated",
        125, 126,
        HeaderDataType.INT16,
        "Correlated.",
    ),

    trace_field(
        "sweep_frequency_start",
        127, 128,
        HeaderDataType.INT16,
        "Sweep frequency at start.",
        unit="Hz",
    ),

    trace_field(
        "sweep_frequency_end",
        129, 130,
        HeaderDataType.INT16,
        "Sweep frequency at end.",
        unit="Hz",
    ),

    trace_field(
        "sweep_length",
        131, 132,
        HeaderDataType.INT16,
        "Sweep length.",
        unit="ms",
    ),

    trace_field(
        "sweep_type",
        133, 134,
        HeaderDataType.INT16,
        "Sweep type.",
    ),

    trace_field(
        "sweep_trace_taper_length_start",
        135, 136,
        HeaderDataType.INT16,
        "Sweep trace taper length at start.",
        unit="ms",
    ),

    trace_field(
        "sweep_trace_taper_length_end",
        137, 138,
        HeaderDataType.INT16,
        "Sweep trace taper length at end.",
        unit="ms",
    ),

    trace_field(
        "taper_type",
        139, 140,
        HeaderDataType.INT16,
        "Taper type.",
    ),

    trace_field(
        "alias_filter_frequency",
        141, 142,
        HeaderDataType.INT16,
        "Alias filter frequency.",
        unit="Hz",
    ),

    trace_field(
        "alias_filter_slope",
        143, 144,
        HeaderDataType.INT16,
        "Alias filter slope.",
        unit="dB/octave",
    ),

    trace_field(
        "notch_filter_frequency",
        145, 146,
        HeaderDataType.INT16,
        "Notch filter frequency.",
        unit="Hz",
    ),

    trace_field(
        "notch_filter_slope",
        147, 148,
        HeaderDataType.INT16,
        "Notch filter slope.",
        unit="dB/octave",
    ),

    trace_field(
        "low_cut_frequency",
        149, 150,
        HeaderDataType.INT16,
        "Low-cut frequency.",
        unit="Hz",
    ),

    trace_field(
        "high_cut_frequency",
        151, 152,
        HeaderDataType.INT16,
        "High-cut frequency.",
        unit="Hz",
    ),

    trace_field(
        "low_cut_slope",
        153, 154,
        HeaderDataType.INT16,
        "Low-cut slope.",
        unit="dB/octave",
    ),

    trace_field(
        "high_cut_slope",
        155, 156,
        HeaderDataType.INT16,
        "High-cut slope.",
        unit="dB/octave",
    ),

    trace_field(
        "year_data_recorded",
        157, 158,
        HeaderDataType.INT16,
        "Year data recorded.",
    ),

    trace_field(
        "day_of_year",
        159, 160,
        HeaderDataType.INT16,
        "Day of year.",
    ),

    trace_field(
        "hour_of_day",
        161, 162,
        HeaderDataType.INT16,
        "Hour of day.",
    ),

    trace_field(
        "minute_of_hour",
        163, 164,
        HeaderDataType.INT16,
        "Minute of hour.",
    ),

    trace_field(
        "second_of_minute",
        165, 166,
        HeaderDataType.INT16,
        "Second of minute.",
    ),

    trace_field(
        "time_basis_code",
        167, 168,
        HeaderDataType.INT16,
        "Time basis code.",
    ),

    trace_field(
        "trace_weighting_factor",
        169, 170,
        HeaderDataType.INT16,
        "Trace weighting factor.",
    ),

    trace_field(
        "geophone_group_roll_switch",
        171, 172,
        HeaderDataType.INT16,
        "Geophone group number of roll switch position one.",
    ),

    trace_field(
        "geophone_group_trace_number_one",
        173, 174,
        HeaderDataType.INT16,
        "Geophone group number of trace number one within original field record.",
    ),

    trace_field(
        "geophone_group_last_trace",
        175, 176,
        HeaderDataType.INT16,
        "Geophone group number of last trace within original field record.",
    ),

    trace_field(
        "gap_size",
        177, 178,
        HeaderDataType.INT16,
        "Gap size — total number of groups dropped.",
    ),

    trace_field(
        "over_travel",
        179, 180,
        HeaderDataType.INT16,
        "Over travel associated with taper at beginning or end of line.",
    ),

    # ----------------------------------------------------------
    # Campos adicionados/definidos nas revisões posteriores
    # ----------------------------------------------------------

    trace_field(
        "ensemble_x",
        181, 184,
        HeaderDataType.INT32,
        "X coordinate of ensemble (CDP) position of this trace.",
    ),

    trace_field(
        "ensemble_y",
        185, 188,
        HeaderDataType.INT32,
        "Y coordinate of ensemble (CDP) position of this trace.",
    ),

    trace_field(
        "inline_number",
        189, 192,
        HeaderDataType.INT32,
        "For 3-D poststack data, in-line number.",
    ),

    trace_field(
        "crossline_number",
        193, 196,
        HeaderDataType.INT32,
        "For 3-D poststack data, cross-line number.",
    ),

    trace_field(
        "shotpoint_number",
        197, 200,
        HeaderDataType.INT32,
        "Shotpoint number.",
    ),

    trace_field(
        "shotpoint_scalar",
        201, 202,
        HeaderDataType.INT16,
        "Scalar to be applied to the shotpoint number.",
    ),

    # ----------------------------------------------------------
    # SEG-Y Rev 2.x
    # ----------------------------------------------------------

    trace_field(
        "trace_value_measurement_unit",
        203, 204,
        HeaderDataType.INT16,
        "Trace value measurement unit.",
    ),

    trace_field(
        "transduction_constant",
        205, 210,
        HeaderDataType.RAW_BYTES,
        "Transduction constant used to convert Data Trace samples to the transduction units.",
    ),

    trace_field(
        "transduction_units",
        211, 212,
        HeaderDataType.INT16,
        "Transduction units.",
    ),

    trace_field(
        "device_trace_identifier",
        213, 214,
        HeaderDataType.INT16,
        "Device/Trace identifier.",
    ),

    trace_field(
        "time_scalar",
        215, 216,
        HeaderDataType.INT16,
        "Scalar to be applied to times specified in Trace Header bytes 95–114.",
    ),

    trace_field(
        "source_type_orientation",
        217, 218,
        HeaderDataType.INT16,
        "Source type/orientation.",
    ),

    trace_field(
        "source_energy_direction",
        219, 224,
        HeaderDataType.RAW_BYTES,
        "Source energy direction with respect to source orientation.",
    ),

    trace_field(
        "source_measurement",
        225, 230,
        HeaderDataType.RAW_BYTES,
        "Source measurement.",
    ),

    trace_field(
        "source_measurement_unit",
        231, 232,
        HeaderDataType.INT16,
        "Source measurement unit.",
    ),

    trace_field(
        "trace_header_name",
        233, 240,
        HeaderDataType.RAW_BYTES,
        "Trace Header name.",
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
