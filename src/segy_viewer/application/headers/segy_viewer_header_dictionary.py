# -*- coding: utf-8 -*-
"""
SegyViewer Header Dictionary.

A nomenclatura é inspirada no VISTA Header Dictionary. Nesta primeira
versão são registrados apenas itens cuja origem é o Trace Header SEG-Y.

Os nomes em `key` usam, quando existe correspondência clara, a mesma
nomenclatura do VISTA Master Dictionary fornecido como referência.
"""

from collections.abc import Iterator
from .segy_viewer_header_item import SegyViewerHeaderItem

TRACE_HEADER = "trace_header"

class SegyViewerHeaderDictionary:

    _items: tuple[SegyViewerHeaderItem, ...] = (

        # --------------------------------------------------------------
        # IDENTIFICAÇÃO / GEOMETRIA BÁSICA
        # --------------------------------------------------------------

        SegyViewerHeaderItem("TRACE_SEQ_NO", "Trace Sequence Number", "TRC", TRACE_HEADER, "trace_sequence_line"),
        SegyViewerHeaderItem("TRACE_SEQ_REEL", "Trace Sequence in File", "TRCF", TRACE_HEADER, "trace_sequence_file"),
        SegyViewerHeaderItem("FIELD_RECORD_NO", "Field Record Number", "FFID", TRACE_HEADER, "field_record_number"),
        SegyViewerHeaderItem("CHANNEL_NO", "Channel Number", "CHAN", TRACE_HEADER, "trace_number_field_record"),
        SegyViewerHeaderItem("SHOT_POINT_NO", "Energy Source Point Number", "SHOT", TRACE_HEADER, "energy_source_point_number"),
        SegyViewerHeaderItem("CMP_NO", "Ensemble Number", "CMP", TRACE_HEADER, "ensemble_number"),
        SegyViewerHeaderItem("CMP_SEQ_NO", "Trace Number in Ensemble", "CMPTR", TRACE_HEADER, "trace_number_ensemble"),
        SegyViewerHeaderItem("TRACE_ID_CODE", "Trace Identification Code", "TID", TRACE_HEADER, "trace_identification_code"),
        SegyViewerHeaderItem("FOLD", "Vertically Summed Traces", "FOLD", TRACE_HEADER, "vertically_summed_traces"),
        SegyViewerHeaderItem("TRACE_HSTACK", "Horizontally Stacked Traces", "HSTK", TRACE_HEADER, "horizontally_stacked_traces"),
        SegyViewerHeaderItem("TEST_CODE", "Data Use", "USE", TRACE_HEADER, "data_use"),
        SegyViewerHeaderItem("OFFSET_SH_REC", "Source-Receiver Offset", "OFF", TRACE_HEADER, "source_receiver_offset"),

        # --------------------------------------------------------------
        # ELEVAÇÕES / PROFUNDIDADES / COORDENADAS
        # --------------------------------------------------------------

        SegyViewerHeaderItem("ELEV_REC", "Receiver Elevation", "RELEV", TRACE_HEADER, "receiver_group_elevation"),
        SegyViewerHeaderItem("ELEV_SHOT", "Source Elevation", "SELEV", TRACE_HEADER, "source_surface_elevation"),
        SegyViewerHeaderItem("DEPTH_SHOT", "Source Depth", "SDEP", TRACE_HEADER, "source_depth"),
        SegyViewerHeaderItem("ELEV_FLOATDATUM_REC", "Receiver Datum Elevation", "RDATE", TRACE_HEADER, "receiver_datum_elevation"),
        SegyViewerHeaderItem("ELEV_FLOATDATUM_SHOT", "Source Datum Elevation", "SDATE", TRACE_HEADER, "source_datum_elevation"),
        SegyViewerHeaderItem("WATER_DEPTH_SHOT", "Source Water Depth", "SWD", TRACE_HEADER, "source_water_depth"),
        SegyViewerHeaderItem("WATER_DEPTH_REC", "Receiver Water Depth", "RWD", TRACE_HEADER, "receiver_water_depth"),
        SegyViewerHeaderItem("ELEV_DEPTH_SCALER", "Elevation/Depth Scalar", "ESCL", TRACE_HEADER, "elevation_scalar"),
        SegyViewerHeaderItem("COORD_SCALER", "Coordinate Scalar", "CSCL", TRACE_HEADER, "coordinate_scalar"),
        SegyViewerHeaderItem("XSHOT", "Source X", "SX", TRACE_HEADER, "source_x"),
        SegyViewerHeaderItem("YSHOT", "Source Y", "SY", TRACE_HEADER, "source_y"),
        SegyViewerHeaderItem("XREC", "Receiver X", "RX", TRACE_HEADER, "group_x"),
        SegyViewerHeaderItem("YREC", "Receiver Y", "RY", TRACE_HEADER, "group_y"),
        SegyViewerHeaderItem("UNITS", "Coordinate Units", "CUNIT", TRACE_HEADER, "coordinate_units"),

        # --------------------------------------------------------------
        # VELOCIDADES / ESTÁTICAS / TEMPOS
        # --------------------------------------------------------------

        SegyViewerHeaderItem("VELOCITY_WEATHER", "Weathering Velocity", "WV", TRACE_HEADER, "weathering_velocity"),
        SegyViewerHeaderItem("REPLACEMENT_VELOCITY", "Subweathering Velocity", "SWV", TRACE_HEADER, "subweathering_velocity"),
        SegyViewerHeaderItem("UPHOLE_SHOT", "Source Uphole Time", "SUP", TRACE_HEADER, "uphole_time_source", "ms"),
        SegyViewerHeaderItem("UPHOLE_REC", "Receiver Uphole Time", "RUP", TRACE_HEADER, "uphole_time_group", "ms"),
        SegyViewerHeaderItem("STATIC_SRC", "Source Static Correction", "SSTAT", TRACE_HEADER, "source_static_correction", "ms"),
        SegyViewerHeaderItem("STATIC_REC", "Receiver Static Correction", "RSTAT", TRACE_HEADER, "group_static_correction", "ms"),
        SegyViewerHeaderItem("STATIC_TOTAL", "Total Static Applied", "TSTAT", TRACE_HEADER, "total_static_applied", "ms"),
        SegyViewerHeaderItem("LAG_TIME_A", "Lag Time A", "LAGA", TRACE_HEADER, "lag_time_a", "ms"),
        SegyViewerHeaderItem("LAG_TIME_B", "Lag Time B", "LAGB", TRACE_HEADER, "lag_time_b", "ms"),
        SegyViewerHeaderItem("DELAY_TIME", "Delay Recording Time", "DELAY", TRACE_HEADER, "delay_recording_time", "ms"),
        SegyViewerHeaderItem("MUTE_TIME_START", "Mute Start Time", "MUTS", TRACE_HEADER, "mute_time_start", "ms"),
        SegyViewerHeaderItem("MUTE_TIME_END", "Mute End Time", "MUTE", TRACE_HEADER, "mute_time_end", "ms"),

        # --------------------------------------------------------------
        # AMOSTRAGEM / AQUISIÇÃO
        # --------------------------------------------------------------

        SegyViewerHeaderItem("NSAMPLES", "Number of Samples", "NS", TRACE_HEADER, "samples_in_trace"),
        SegyViewerHeaderItem("SAMPLERATE", "Sample Interval", "DT", TRACE_HEADER, "sample_interval", "µs"),
        SegyViewerHeaderItem("GAIN_TYPE", "Gain Type", "GTYP", TRACE_HEADER, "gain_type"),
        SegyViewerHeaderItem("GAIN_CONSTANT", "Instrument Gain Constant", "GCON", TRACE_HEADER, "instrument_gain_constant", "dB"),
        SegyViewerHeaderItem("GAIN_INITIAL", "Instrument Initial Gain", "GINI", TRACE_HEADER, "instrument_initial_gain", "dB"),
        SegyViewerHeaderItem("DATA_CORRELATED", "Correlated", "CORR", TRACE_HEADER, "correlated"),
        SegyViewerHeaderItem("SWEEP_FREQ_START", "Sweep Start Frequency", "FS", TRACE_HEADER, "sweep_frequency_start", "Hz"),
        SegyViewerHeaderItem("SWEEP_FREQ_END", "Sweep End Frequency", "FE", TRACE_HEADER, "sweep_frequency_end", "Hz"),
        SegyViewerHeaderItem("SWEEP_LENGTH", "Sweep Length", "SLEN", TRACE_HEADER, "sweep_length", "ms"),
        SegyViewerHeaderItem("SWEEP_TYPE", "Sweep Type", "STYP", TRACE_HEADER, "sweep_type"),
        SegyViewerHeaderItem("SWEEP_TAPERLEN_START", "Sweep Taper Length Start", "TAPS", TRACE_HEADER, "sweep_trace_taper_length_start", "ms"),
        SegyViewerHeaderItem("SWEEP_TAPERLEN_END", "Sweep Taper Length End", "TAPE", TRACE_HEADER, "sweep_trace_taper_length_end", "ms"),
        SegyViewerHeaderItem("SWEEP_TAPERTYPE", "Sweep Taper Type", "TAPT", TRACE_HEADER, "taper_type"),
        SegyViewerHeaderItem("ALIAS_FILTER_FREQ", "Alias Filter Frequency", "AFF", TRACE_HEADER, "alias_filter_frequency", "Hz"),
        SegyViewerHeaderItem("ALIAS_FILTER_SLOPE", "Alias Filter Slope", "AFS", TRACE_HEADER, "alias_filter_slope", "dB/octave"),
        SegyViewerHeaderItem("NOTCH_FILTER_FREQ", "Notch Filter Frequency", "NFF", TRACE_HEADER, "notch_filter_frequency", "Hz"),
        SegyViewerHeaderItem("NOTCH_FILTER_SLOPE", "Notch Filter Slope", "NFS", TRACE_HEADER, "notch_filter_slope", "dB/octave"),
        SegyViewerHeaderItem("LOWCUT_FREQ", "Low-Cut Frequency", "LCF", TRACE_HEADER, "low_cut_frequency", "Hz"),
        SegyViewerHeaderItem("HIGHCUT_FREQ", "High-Cut Frequency", "HCF", TRACE_HEADER, "high_cut_frequency", "Hz"),
        SegyViewerHeaderItem("LOWCUT_SLOPE", "Low-Cut Slope", "LCS", TRACE_HEADER, "low_cut_slope", "dB/octave"),
        SegyViewerHeaderItem("HIGHCUT_SLOPE", "High-Cut Slope", "HCS", TRACE_HEADER, "high_cut_slope", "dB/octave"),

        # --------------------------------------------------------------
        # DATA / HORA
        # --------------------------------------------------------------

        SegyViewerHeaderItem("RECORDED_YEAR", "Recorded Year", "YEAR", TRACE_HEADER, "year_data_recorded"),
        SegyViewerHeaderItem("RECORDED_DAY", "Recorded Day of Year", "JDAY", TRACE_HEADER, "day_of_year"),
        SegyViewerHeaderItem("RECORDED_HOUR", "Recorded Hour", "HOUR", TRACE_HEADER, "hour_of_day"),
        SegyViewerHeaderItem("RECORDED_MINUTE", "Recorded Minute", "MIN", TRACE_HEADER, "minute_of_hour"),
        SegyViewerHeaderItem("RECORDED_SECOND", "Recorded Second", "SEC", TRACE_HEADER, "second_of_minute"),
        SegyViewerHeaderItem("TIME_BASIS_CODE", "Time Basis Code", "TBASE", TRACE_HEADER, "time_basis_code"),

        # --------------------------------------------------------------
        # OUTROS CAMPOS PADRÃO SEG-Y
        # --------------------------------------------------------------

        SegyViewerHeaderItem("TRACE_WEIGHTING_FACTOR", "Trace Weighting Factor", "TWF", TRACE_HEADER, "trace_weighting_factor"),
        SegyViewerHeaderItem("GEOPHONE_GROUP_NUMBER", "Geophone Group Roll Switch", "GGRS", TRACE_HEADER, "geophone_group_roll_switch"),
        SegyViewerHeaderItem("GEOPHONE_GROUP_FIRSTTRACE", "Geophone Group First Trace", "GGFT", TRACE_HEADER, "geophone_group_trace_number_one"),
        SegyViewerHeaderItem("GEOPHONE_GROUP_LASTTRACE", "Geophone Group Last Trace", "GGLT", TRACE_HEADER, "geophone_group_last_trace"),
        SegyViewerHeaderItem("GAP_SIZE", "Gap Size", "GAP", TRACE_HEADER, "gap_size"),

        # Não há um nome inequívoco equivalente no VISTA Master Dictionary
        # fornecido para este campo SEG-Y padrão.
        SegyViewerHeaderItem("OVER_TRAVEL", "Over Travel", "OVTR", TRACE_HEADER, "over_travel"),

        # --------------------------------------------------------------
        # SEG-Y REV 1+
        # --------------------------------------------------------------

        SegyViewerHeaderItem("CMP_XCENTER", "Ensemble X", "CMPX", TRACE_HEADER, "ensemble_x"),
        SegyViewerHeaderItem("CMP_YCENTER", "Ensemble Y", "CMPY", TRACE_HEADER, "ensemble_y"),
        SegyViewerHeaderItem("INLINE", "Inline Number", "IL", TRACE_HEADER, "inline_number"),
        SegyViewerHeaderItem("CROSSLINE", "Crossline Number", "XL", TRACE_HEADER, "crossline_number"),

        # O VISTA usa SHOT_POINT_NO para o campo dos bytes 17-20.
        # Como o Domain também expõe o shotpoint SEG-Y Rev.1 (197-200),
        # usamos uma chave própria para evitar colisão semântica.
        SegyViewerHeaderItem("SEGY_SHOTPOINT_NO", "SEG-Y Shotpoint Number", "SP", TRACE_HEADER, "shotpoint_number"),
        SegyViewerHeaderItem("SHOTPOINT_SCALAR", "Shotpoint Scalar", "SPSCL", TRACE_HEADER, "shotpoint_scalar"),

        # --------------------------------------------------------------
        # SEG-Y REV 2.x
        # Sem equivalentes claros no VISTA Master Dictionary fornecido.
        # Mantêm nomes próprios do Segy Viewer.
        # --------------------------------------------------------------

        SegyViewerHeaderItem("TRACE_VALUE_MEASUREMENT_UNIT", "Trace Value Measurement Unit", "TVMU", TRACE_HEADER, "trace_value_measurement_unit"),
        SegyViewerHeaderItem("TRANSDUCTION_CONSTANT", "Transduction Constant", "TRCON", TRACE_HEADER, "transduction_constant"),
        SegyViewerHeaderItem("TRANSDUCTION_UNITS", "Transduction Units", "TRUNT", TRACE_HEADER, "transduction_units"),
        SegyViewerHeaderItem("DEVICE_TRACE_IDENTIFIER", "Device/Trace Identifier", "DVID", TRACE_HEADER, "device_trace_identifier"),
        SegyViewerHeaderItem("TIME_SCALAR", "Time Scalar", "TSCL", TRACE_HEADER, "time_scalar"),
        SegyViewerHeaderItem("SOURCE_TYPE_ORIENTATION", "Source Type/Orientation", "STOR", TRACE_HEADER, "source_type_orientation"),
        SegyViewerHeaderItem("SOURCE_ENERGY_DIRECTION", "Source Energy Direction", "SEDIR", TRACE_HEADER, "source_energy_direction"),
        SegyViewerHeaderItem("SOURCE_MEASUREMENT", "Source Measurement", "SMEAS", TRACE_HEADER, "source_measurement"),
        SegyViewerHeaderItem("SOURCE_MEASUREMENT_UNIT", "Source Measurement Unit", "SMU", TRACE_HEADER, "source_measurement_unit"),
        SegyViewerHeaderItem("TRACE_HEADER_NAME", "Trace Header Name", "THNAM", TRACE_HEADER, "trace_header_name"),
    )

    _by_key: dict[str, SegyViewerHeaderItem] = {
        item.key: item
        for item in _items
    }

    _by_source_field: dict[str, SegyViewerHeaderItem] = {
        item.source_field: item
        for item in _items
    }

    @classmethod
    def all(cls) -> tuple[SegyViewerHeaderItem, ...]:
        return cls._items

    @classmethod
    def get(cls, key: str) -> SegyViewerHeaderItem:
        try:
            return cls._by_key[key]
        except KeyError as error:
            raise KeyError(
                f"SegyViewer Header Item {key!r} is not defined."
            ) from error

    @classmethod
    def get_by_source_field(
        cls,
        source_field: str,
    ) -> SegyViewerHeaderItem:
        try:
            return cls._by_source_field[source_field]
        except KeyError as error:
            raise KeyError(
                f"No SegyViewer Header Item is mapped to "
                f"source field {source_field!r}."
            ) from error

    @classmethod
    def keys(cls) -> tuple[str, ...]:
        return tuple(item.key for item in cls._items)

    @classmethod
    def names(cls) -> tuple[str, ...]:
        return tuple(item.name for item in cls._items)

    @classmethod
    def acronyms(cls) -> tuple[str, ...]:
        return tuple(item.acronym for item in cls._items)

    @classmethod
    def trace_header_items(
        cls,
    ) -> tuple[SegyViewerHeaderItem, ...]:
        return tuple(
            item
            for item in cls._items
            if item.source == TRACE_HEADER
        )

    @classmethod
    def displayed_headers(
        cls,
        keys: tuple[str, ...] | list[str],
    ) -> dict[str, str]:
        """
        Monta o dicionário usado pelo TraceHeaderView.

        Exemplo
        -------
        >>> SegyViewerHeaderDictionary.displayed_headers(
        ...     ["CHANNEL_NO", "FIELD_RECORD_NO"]
        ... )
        {"CHAN": "CHANNEL_NO", "FFID": "FIELD_RECORD_NO"}
        """
        return {
            cls.get(key).acronym: key
            for key in keys
        }

    @classmethod
    def __iter_items(cls) -> Iterator[SegyViewerHeaderItem]:
        yield from cls._items
