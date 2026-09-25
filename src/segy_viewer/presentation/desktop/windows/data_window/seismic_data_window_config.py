"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window_config.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que representa as configurações da Seismic Data Window
    esta classe é compartilhada com todos os HSynchronizedSeismicDataWidget's

Histórico:
       24/09/2026 - Início da implementação
       25/09/2026 - Correcoes
===============================================================================
"""
from dataclasses import dataclass, field

from enum import Enum
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# tuple(self._display_state.displayed_headers.values())
AVAILABLE_HEADERS = {"FFID": "FIELD_RECORD_NO",
                     "CHAN": "CHANNEL_NO",
                     "TRC": "TRACE_SEQ_REEL",
                     "SP": "SHOT_POINT_NO",
                     "CMP":"CMP_NO",
                     "INLI":"INLINE",
                     "CROS": "CROSSLINE"}

AVAILABLE_GRAPH_HEADERS =("ELEV_REC","ELEV_SHOT","DEPTH_SHOT",
                          "ELEV_FLOATDATUM_REC","ELEV_FLOATDATUM_SHOT",
                          "WATER_DEPTH_SHOT","WATER_DEPTH_REC")

class TraceDrawingMode(Enum):
    WIGGLE = "wiggle"
    VARIABLE_AREA = "variable_area"


@dataclass
class SeismicDisplaySettings:
    trace_drawing_mode: TraceDrawingMode = TraceDrawingMode.WIGGLE
    number_traces_to_show: int = 300
    mouse_tracking_on: bool = False

    #Opcies para o TraceHeaderView
    show_trace_headers: bool = True
    header_keys_to_show: dict[str, str] = field(default_factory=lambda: {key: AVAILABLE_HEADERS[key]
                                                                         for key in list(AVAILABLE_HEADERS)[:3]
                                                                        }) #seleciona os 3 primeiros como padrao

    #Opcoes para o AttributeGraphView
    show_attribute_graph: bool = True
    graph_header_keys_to_show: tuple[str, ...] = (AVAILABLE_GRAPH_HEADERS[0],)
    keep_yaxis_on_zero: bool = False
    show_min_max_values: bool = True
    show_point: bool = True
    point_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.darkRed)) #evita que instâncias diferentes compartilhem o mesmo objeto
    show_lines: bool = True
    line_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.darkBlue) ) #evita que instâncias diferentes compartilhem o mesmo objeto




