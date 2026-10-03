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
       27/09/2026 - Criação das configurações apara o desenho do traço sísmico
       01/10/2026 - Adicionado opcoes para configuração do desenho sísmico
       02/10/2026 - Adicionado as configurações para o Scale do traco
       03/10/2026 - Adicionado algumas configurações adicionais para o Plot Parameters
===============================================================================
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# tuple(self._display_state.displayed_headers.values())
AVAILABLE_HEADERS = {"FFID": "FIELD_RECORD_NO",
                     "CHAN": "CHANNEL_NO",
                     "TRC": "TRACE_SEQ_REEL",
                     "SP_NO": "SHOT_POINT_NO",
                     "CMP_NO":"CMP_NO",
                     "INLINE":"INLINE",
                     "CROSSL": "CROSSLINE"}

AVAILABLE_GRAPH_HEADERS =("ELEV_REC","ELEV_SHOT","DEPTH_SHOT",
                          "ELEV_FLOATDATUM_REC","ELEV_FLOATDATUM_SHOT",
                          "WATER_DEPTH_SHOT","WATER_DEPTH_REC")

class TRACEDRAWINGMODES(Enum):
    WIGGLE = "Wiggle Trace"
    VARIABLE_AREA = "Variable Area"
    WIGGLE_VARIABLE_AREA = "Wiggle/Variable Area"
    VARIABLE_DENSITY = "Variable Density"
    WIGGLE_VARIABLE_DENSITY = "Wiggle/Variable Density"


class AmplitudeScaleCalculation(Enum):
    MEAN_ABSOLUTE_AMPLITUDE = auto()
    MEAN_TRACE_PEAK = auto()

AMPLITUDE_SCALE_CALCULATIONS = {AmplitudeScaleCalculation.MEAN_ABSOLUTE_AMPLITUDE: (
                                    "Scaled Mean Amplitude",
                                    "3.5 times the mean absolute sample amplitude across valid traces.",
                                ),
                                AmplitudeScaleCalculation.MEAN_TRACE_PEAK: (
                                    "Mean trace peak",
                                    "Mean of the absolute peak amplitude of each valid trace.",
                                ),
                            }

@dataclass
class SeismicDisplaySettings:
    #Opções Gerais
    number_traces_to_show: int = 600
    mouse_tracking_on: bool = True

    #=== PLOT PARAMETERS ===#
    #Opções para o Desenho das amotras sismicas
    trace_excursion: float = 1   #largura horizontal correspondente à amplitude de referência, medida em espaços entre traços
    max_clip_excursion: float = 3 #limite máximo da largura horizontal do traco, medida em espacos entre tracos
    variable_area_bias:int = 100  #Área preenchida. 100% usa o centro do traço; valores menores reduzem a área preenchida
    trace_drawing_mode: TRACEDRAWINGMODES  = TRACEDRAWINGMODES.WIGGLE_VARIABLE_AREA.name  #Modo de desenho das amostras

    #Grid
    show_time_grid:bool = True
    time_grid_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.black))

    #Cores para desenho das amostras
    background_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.white))
    wiggle_color : QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.black))
    selected_trace_wiggle_color : QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.darkBlue))
    positive_fill_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.red))
    negative_fill_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.blue))
    fill_negative_va:bool = False
    # === PLOT PARAMETERS ===#

    #Opções para o Scale no desenho das amostras
    calc_scale_num_traces:int = 100  #Mesmo valor inicial do number_traces_to_show, assim uso o set_data para o calculo inicial
    mim_amp_value: float | None = None
    max_amp_value: float | None = None
    #-----------------------------------------
    amplitude_scale_calculation: AmplitudeScaleCalculation = AmplitudeScaleCalculation.MEAN_ABSOLUTE_AMPLITUDE  #Forma de calcular o min/max amp_value
    calculated_scale_trace_count: int = 0 #Quantidade real que foi utilizada pra calcular o min/max amp_value

    #Opções para a aba Pre-Process
    display_dead_traces: bool = True
    dead_trace_rms_limit : float = 0.0 #Limite do RMS para considerar um Traço como morto.
    dead_trace_wiggle_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.red))
    reverse_data_polarity:bool = False
    amplitude_scale_db:int = 0

    #Opcoes para o TraceHeaderView
    show_trace_headers: bool = True
    header_keys_to_show: dict[str, str] = field(default_factory=lambda: {key: AVAILABLE_HEADERS[key]
                                                                         for key in list(AVAILABLE_HEADERS)[:3]
                                                                        }) #seleciona os 3 primeiros como padrao

    #Opcoes para o AttributeGraphView
    show_attribute_graph: bool = True
    graph_header_keys_to_show: tuple[str, ...] = (AVAILABLE_GRAPH_HEADERS[0],)
    keep_graph_y_axis_on_zero: bool = False
    show_graph_min_max_values: bool = True
    plot_graph_point: bool = True
    graph_point_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.darkRed)) #evita que instâncias diferentes compartilhem o mesmo objeto
    plot_graph_line: bool = True
    graph_line_color: QColor = field(default_factory=lambda: QColor(Qt.GlobalColor.darkBlue)) #evita que instâncias diferentes compartilhem o mesmo objeto


    def _headers_from_keys(self, header_keys: tuple[str, ...]) -> dict[str, str]:
        labels_by_key = {key: label  for label, key in AVAILABLE_HEADERS.items() }

        return {labels_by_key[key]: key
                 for key in header_keys
               }


