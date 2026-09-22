# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Janela responsável pela visualização dos dados sísmicos. A SeismicDataWindow atua como coordenadora
("maestro") dos três componentes principais que são filhos de HSynchronizedSeismicDataWidget  onde esta o
contrato de sincronismo horizontal com da Data Window com o Widget. Os três componentes principais são:
           TraceHeaderView
           SeismicDataView
           TraceAttributeGraphView

       A janela terá duas barras de ferramentas fixas
       -Main Seismic Toolbar
       -View Seismic Toolbar

Responsabilidades principais:

- controlar o SeismicViewport;
- controlar a navegação horizontal;
- solicitar dados à camada application;
- manter aberta a sessão de dados enquanto a janela existir;
- distribuir os dados entre os widgets;
- manter os três widgets horizontalmente sincronizados;
- fechar a sessão de dados quando a janela for encerrada.

Histórico:
       04/09/2026 - Início da implementação da janela
       09/09/2026 - Estrutura inicial da Seismic Data Window
       13/09/2026 - Construção do acesso aos dados contidos nos arquivos Seg-y
       16/09/2026 - Inclusão de labels informativos na statusbar
===============================================================================
"""
from pathlib import Path
from PySide6.QtCore import Qt, Slot, QSize, QRect
from PySide6.QtGui import QAction, QIcon, QKeySequence, QCloseEvent, QFontDatabase
from PySide6.QtWidgets import QMainWindow, QScrollBar, QStatusBar, QToolBar, QVBoxLayout, QWidget, QMessageBox, QLabel, \
    QSizePolicy
from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.application.seismic_data_window.dto import SeismicWindowInfoDTO, SeismicDataBlockDTO
from segy_viewer.application.seismic_data_window.seismic_data_window_use_cases import SeismicDataWindowUseCases
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget
from segy_viewer.presentation.desktop.widgets.seismic_data_window import TraceHeaderView
from segy_viewer.presentation.desktop.widgets.seismic_data_window import SeismicDataSamplesView
from segy_viewer.presentation.desktop.widgets.seismic_data_window import TraceAttributeGraphView
from segy_viewer.resources import resource_path
from segy_viewer import AppConfig

# ============================================================================
# Resources
# ============================================================================
_EXIT_ICON = resource_path("resources/icons/exit.png")
_DEAD_TRACE_DETECTION_ICON = resource_path("resources/icons/dead_trace_detetion.png")
_PROCESSING_TOOL_ICON = resource_path("resources/icons/processing_tool.png")
_DATA_PLOT_PARAMETERS_TOOL_ICON = resource_path("resources/icons/data_plot_parameters.png")
_DATA_SORT_ORDER_TOOL_ICON = resource_path("resources/icons/data_sort_order.png")
_SHOW_TRACES_GRAPH_ORDER_TOOL_ICON = resource_path("resources/icons/show_traces_graph_.png")
_TRACE_HEADER_INFO_TOOL_ICON = resource_path("resources/icons/trace_header_info.png")
_MOUSE_TRACKING_ON_TOOL_ICON = resource_path("resources/icons/mouse_tracking_on.png")
_MOUSE_TRACKING_OFF_TOOL_ICON = resource_path("resources/icons/mouse_tracking_off.png")

class SeismicDataWindow(QMainWindow):
    def __init__(self, path: Path,
                 config: AppConfig,
                 use_cases: SeismicDataWindowUseCases,
                 initial_geometry: QRect | None = None):

        super().__init__(parent=None)
        # ------------------------------------------------------------------
        # Dependencies
        # ------------------------------------------------------------------
        self._config = config
        self._path = path
        self._use_cases = use_cases

        # ------------------------------------------------------------------
        # Window lifetime
        # ------------------------------------------------------------------
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose,True)

        # ------------------------------------------------------------------
        # Data state
        # ------------------------------------------------------------------
        self._data_is_open = False

        # Informações gerais da sessão / arquivo.
        self._window_info: SeismicWindowInfoDTO | None = None

        # Último bloco de dados devolvido pela application.
        self._data_block: SeismicDataBlockDTO | None = None

        # Total de posições de traço disponíveis para navegação.
        self._total_trace_count = 0

        # ------------------------------------------------------------------
        # viewport compartilhado
        # ------------------------------------------------------------------
        self._viewport = SeismicViewport(first_trace_position=0, trace_count=300)


        # Headers mostrados inicialmente no TraceHeaderView.
        self._displayed_header_keys: tuple[str, ...] = ("CHANNEL_NO","TRACE_SEQ_REEL","FIELD_RECORD_NO")

        # Header/atributo exibido no gráfico inferior.
        self._graph_header_keys: tuple[str, ...] = ("ELEV_REC",)

        # Widgets principais. Todos recebem EXATAMENTE o mesmo SeismicViewport.
        self._mouse_tracking_on = True   #Depois mover para um dataclass de configuracao da janela de dados
        self._trace_header_view:HSynchronizedSeismicDataWidget = TraceHeaderView(viewport=self._viewport, parent=self)
        self._seismic_data_samples_view:HSynchronizedSeismicDataWidget = SeismicDataSamplesView(viewport=self._viewport, parent=self)
        self._trace_attribute_graph_view:HSynchronizedSeismicDataWidget = TraceAttributeGraphView(viewport=self._viewport, parent=self)

        # Scrollbar - Navegação pelos traços
        self._horizontal_scrollbar =  QScrollBar(Qt.Orientation.Horizontal)
        self._horizontal_scrollbar.setStyleSheet(self._config.SEISMIC_DATA_WINDOW_SCROLLBAR_STYLE)

        # -------------------------------------------------------------
        # Construção da janela
        # -------------------------------------------------------------
        self._build_ui()
        self._create_actions()
        self._create_menu_bar()
        self._create_toolbars()
        self._create_status_bar()
        self._configure_window(initial_geometry)
        self._connect_signals()

        # ------------------------------------------------------------------
        # Data - O metodo chama o self.update_scrollbar()
        # ------------------------------------------------------------------
        self._initialize_display()


    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)

        # ------------------------------------------------------------------
        # Trace Header View
        # ------------------------------------------------------------------
        self._trace_header_view.mouse_tracking_on = self._mouse_tracking_on
        # self._trace_header_view.setMinimumHeight(45)
        # self._trace_header_view.setMaximumHeight(160)

        # ------------------------------------------------------------------
        # Seismic Data Samples View
        # ------------------------------------------------------------------
        self._seismic_data_samples_view.setMinimumHeight(200)

        # ------------------------------------------------------------------
        # Trace Attribute Graph View
        # ------------------------------------------------------------------
        self._trace_attribute_graph_view.mouse_tracking_on = self._mouse_tracking_on
        self._trace_attribute_graph_view.setMinimumHeight(70)
        self._trace_attribute_graph_view.setMaximumHeight(180)

        # Layout
        main_layout.addWidget(self._trace_header_view, stretch=0)
        main_layout.addWidget(self._seismic_data_samples_view, stretch=1)
        main_layout.addWidget(self._trace_attribute_graph_view, stretch=0)
        main_layout.addWidget(self._horizontal_scrollbar,stretch=0)

        self.setCentralWidget(central_widget)

    # ======================================================================
    # Actions
    # ======================================================================
    def _create_actions(self):
        # ------------------------------------------------------------------
        # Main seismic toolbar
        # ------------------------------------------------------------------
        self._dead_trace_detection_action = QAction(QIcon(str(_DEAD_TRACE_DETECTION_ICON)), "Dead trace auto detection", self,
                                              toolTip="Dead trace auto detection dialog")

        self._processing_tool_action = QAction(QIcon(str(_PROCESSING_TOOL_ICON)), "Processing tools", self,
                                              toolTip="Processing tools dialog")

        #DEMAIS FERRAMENTAS DE PROCESSAMENTO SERÃO IMPLEMENTADAS CONFORME O PROJETO CRESCE

        # ------------------------------------------------------------------
        # View toolbar
        # ------------------------------------------------------------------
        self._data_plot_parameters_action = QAction(QIcon(str(_DATA_PLOT_PARAMETERS_TOOL_ICON)), "Processing tools", self,
                                              toolTip="Processing tools dialog")

        self._data_sort_order_action = QAction(QIcon(str(_DATA_SORT_ORDER_TOOL_ICON)), "Data sort order tools", self,
                                                    toolTip="Data sort order tool dialog")

        self._show_traces_graph_action = QAction(QIcon(str(_SHOW_TRACES_GRAPH_ORDER_TOOL_ICON)), "Show trace(s) Graph", self,
                                               toolTip="Show trace(s) Graph window")

        self._trace_header_info_action = QAction(QIcon(str(_TRACE_HEADER_INFO_TOOL_ICON)), "Trace Header info", self,
                                                 toolTip="Trace Header info dialog")

        self._mouse_tracking_action = QAction(QIcon(str(_MOUSE_TRACKING_ON_TOOL_ICON)), "Mouse tracking ON/OFF", self,
                                                 toolTip="Mouse tracking ON/OFF")

        self._exit_action = QAction(QIcon(str(_EXIT_ICON)), "Exit", self, toolTip="Close Data Seismic Window")
        self._exit_action.setShortcut(QKeySequence("Ctrl+X"))


    # ======================================================================
    # Menu - AINDA TO NA DÚVIDA SE COLOCO MENU OU DEIXO TUDO NAS BARRAS DE FERRAMENTAS
    # ======================================================================
    def _create_menu_bar(self):
        return


    # ======================================================================
    # Toolbars
    # ======================================================================
    def _create_toolbars(self):
        # ------------------------------------------------------------------
        # Main toolbar
        # ------------------------------------------------------------------
        self._main_seismic_tool_bar = QToolBar("Main Seismic Toolbar", self)
        self._main_seismic_tool_bar.setMovable(False)
        self._main_seismic_tool_bar.setStyleSheet(self._config.SEISMIC_DATA_WINDOW_TOOL_BAR_STYLE)
        self._main_seismic_tool_bar.setIconSize(QSize(25, 25))

        self._main_seismic_tool_bar.addAction(self._exit_action)
        self._main_seismic_tool_bar.addSeparator()
        self._main_seismic_tool_bar.addAction(self._dead_trace_detection_action)
        self._main_seismic_tool_bar.addAction(self._processing_tool_action)
        self.addToolBar(self._main_seismic_tool_bar)
        # ------------------------------------------------------------------
        # View toolbar
        # ------------------------------------------------------------------
        self._seismic_view_tool_bar = QToolBar("Seismic View Toolbar", self)
        self._seismic_view_tool_bar.setMovable(False)
        self._seismic_view_tool_bar.setStyleSheet(self._config.SEISMIC_DATA_WINDOW_TOOL_BAR_STYLE)
        self._seismic_view_tool_bar.setIconSize(QSize(25, 25))

        self._seismic_view_tool_bar.addAction(self._data_plot_parameters_action)
        self._seismic_view_tool_bar.addAction(self._data_sort_order_action)
        self._seismic_view_tool_bar.addSeparator()
        self._seismic_view_tool_bar.addAction(self._show_traces_graph_action)
        self._seismic_view_tool_bar.addAction(self._trace_header_info_action)
        self._seismic_view_tool_bar.addSeparator()
        self._seismic_view_tool_bar.addAction(self._mouse_tracking_action)

        self.addToolBar(Qt.LeftToolBarArea, self._seismic_view_tool_bar)


    # ======================================================================
    # Status bar
    # ======================================================================
    def _create_status_bar(self):
        status_bar = QStatusBar(self)

        _font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        _font.setPointSize(8)
        _font.setBold(True)

        self._status_bar_summary_label = QLabel()
        self._status_bar_summary_label.setFont(_font)
        self._status_bar_summary_label.setStyleSheet(self._config.SEISMIC_DATA_WINDOW_STATUS_BAR_LABEL_STYLE)

        self._status_bar_trace_info_label = QLabel()
        # _font.setPointSize(9)
        self._status_bar_trace_info_label.setFont(_font)
        status_bar.addPermanentWidget(self._status_bar_trace_info_label)
        status_bar.addPermanentWidget(self._status_bar_summary_label)

        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Ready")



    # ======================================================================
    # Window configuration
    #      A geometria inicial vem da main window, sempre abre sobre o SegyFileInspector
    # ======================================================================
    def _configure_window(self, initial_geometry: QRect) -> None:
        self.setWindowTitle(f"Seismic Data Window: {self._path}")

        if initial_geometry is not None:
            self.setGeometry(initial_geometry)


    # ======================================================================
    # Scrollbar
    # ======================================================================
    def _update_scrollbar(self) -> None:
        visible_trace_count = min(self._viewport.trace_count, self._total_trace_count)
        maximum = max(0, self._total_trace_count - visible_trace_count)

        self._horizontal_scrollbar.setRange(0, maximum)
        self._horizontal_scrollbar.setPageStep(max(1, visible_trace_count))
        self._horizontal_scrollbar.setSingleStep(max(1, round(visible_trace_count * 0.10)))
        self._horizontal_scrollbar.setValue(min(self._viewport.first_trace_position, maximum))
        self._horizontal_scrollbar.setEnabled(self._total_trace_count > visible_trace_count)


    # ======================================================================
    # Signals
    # ======================================================================
    def _connect_signals(self):
        self._exit_action.triggered.connect(self.close)
        self._horizontal_scrollbar.valueChanged.connect(self._on_horizontal_scroll)
        self._trace_attribute_graph_view.graphMouseMoved.connect(self._update_status_bar_graph_info)
        self._trace_header_view.headerMouseMoved.connect(self._update_status_bar_graph_info)
        self._trace_attribute_graph_view.mouseTraceSelected.connect(self._update_selected_trace)
        self._trace_header_view.mouseTraceSelected.connect(self._update_selected_trace)


    # ======================================================================
    # Initialization
    # ======================================================================
    def _initialize_display(self) -> None:
        """
        Abre a sessão de dados e carrega o primeiro viewport.
        """
        self.statusBar().showMessage(f"Opening {self._path.name}...")

        try:
            # --------------------------------------------------------------
            # Open data session
            # --------------------------------------------------------------
            self._window_info = self._use_cases.open(self._path)
            self._data_is_open = True

            # --------------------------------------------------------------
            # General information
            # --------------------------------------------------------------
            self._total_trace_count = (self._window_info.trace_count)

            # --------------------------------------------------------------
            # Correct viewport for small files
            # --------------------------------------------------------------
            if (self._total_trace_count < self._viewport.trace_count):
                self._viewport.trace_count = self._total_trace_count

            # --------------------------------------------------------------
            # Vertical time range
            # --------------------------------------------------------------
            self._viewport.time_min_ms = 0.0
            self._viewport.time_max_ms = (self._window_info.record_length_ms)

            # --------------------------------------------------------------
            # Scrollbar
            # --------------------------------------------------------------
            self._update_scrollbar()

            # --------------------------------------------------------------
            # First data request
            # --------------------------------------------------------------
            self._request_current_data()
            self._status_bar_summary_label.setText((f"{self._total_trace_count:,} traces | "
                                                    f"{self._window_info.sample_count} samples/trace | "
                                                    f"{self._window_info.sample_interval_us} µs"
                                                  ))

            self.statusBar().showMessage("Ready - SEG-Y file opened.")

        except Exception as error:
            if self._data_is_open:
                self._use_cases.close()
                self._data_is_open = False

            QMessageBox.critical(self, "Attention, error!", "The Data Window could not access segy file data.\n\n"
                                             f"{type(error).__name__}: {error}")
            self.close()


    # ======================================================================
    # Data request
    # ======================================================================
    def _request_current_data(self) -> None:
        """
           Solicita à application os dados necessários para o viewport atual.
           A SeismicDataWindow informa apenas o viewport desejado. A decisão
        de carregar uma região maior que o viewport (buffer/prefetch) pertence
        à camada application.
        """
        if not self._data_is_open:
            return

        self._data_block = self._use_cases.load_data(viewport=self._viewport,
                                                     header_keys=self._displayed_header_keys,
                                                     graph_header_keys=self._graph_header_keys)
        self._distribute_data(data_block=self._data_block)


    # ======================================================================
    # Data distribution
    # ======================================================================
    def _distribute_data(self, data_block: SeismicDataBlockDTO,) -> None:
        """
        Distribui o bloco de dados carregado para os widgets.
        Cada widget recebe somente os dados pelos quais é responsável.
        """
        if self._data_block is None:
            return


        self._trace_header_view.set_data(trace_positions=data_block.trace_positions,
                                         trace_indices=data_block.trace_indices,
                                         header_values=data_block.trace_header_values)

        # self._seismic_data_samples_view.set_data(
        #     trace_positions=data_block.trace_positions,
        #     trace_indices=data_block.trace_indices,
        #     samples=data_block.samples,
        # )
        #
        self._trace_attribute_graph_view.set_data(trace_positions=data_block.trace_positions,
                                                  trace_indices=data_block.trace_indices,
                                                  graph_header_values=data_block.graph_header_values)
        self._refresh_hsynchronized_widgets()


    # ======================================================================
    # Refresh
    # ======================================================================
    def _refresh_hsynchronized_widgets(self) -> None:
        self._trace_header_view.refresh()
        self._seismic_data_samples_view.refresh()
        self._trace_attribute_graph_view.refresh()

    # ======================================================================
    # status Bar
    # ======================================================================
    @Slot(str)
    def _update_status_bar_graph_info(self, message: str) -> None:
        self._status_bar_trace_info_label.setText(message)
        #atualiza os Widgets pois a o traco sob o mouse mudou
        self._trace_attribute_graph_view.refresh()
        self._trace_header_view.refresh()
        self._seismic_data_samples_view.refresh()

    # ======================================================================
    # Trace Selected
    # ======================================================================
    @Slot(int)
    def _update_selected_trace(self, trace_selected: int | None) -> None:
        # atualiza os  Widgets
        if trace_selected is None:
            self.statusBar().showMessage("Ready - SEG-Y file opened.")
        else:
            self.statusBar().showMessage(f"Selected trace: {trace_selected}")

        self._trace_attribute_graph_view.refresh()
        self._trace_header_view.refresh()
        self._seismic_data_samples_view.refresh()


    # ======================================================================
    # Horizontal navigation
    # ======================================================================
    @Slot(int)
    def _on_horizontal_scroll(self, first_trace: int) -> None:
        """
        Atualiza a posição horizontal do viewport, first_trace representa uma posição no espaço de visualização.
        Atualmente:
            posição visual == índice físico.
        """
        if first_trace == self._viewport.first_trace_position:
            return

        self._viewport.first_trace_position = first_trace
        self._request_current_data()


    # ======================================================================
    # Change visible trace count
    # ======================================================================
    def set_visible_trace_count(self, trace_count: int) -> None:
        if trace_count <= 0:
            QMessageBox.critical(self,"Attention, error!", "The trace_count must be greater than zero.")

        if self._total_trace_count > 0:
            trace_count = min(trace_count, self._total_trace_count)

        self._viewport.trace_count = trace_count

        # Garante que o último viewport continue válido.
        maximum_first_trace = max(0, self._total_trace_count - self._viewport.trace_count)
        self._viewport.first_trace_position = min(self._viewport.first_trace_position, maximum_first_trace)
        self._update_scrollbar()
        self._request_current_data()


    # ======================================================================
    # Displayed headers - Define os headers apresentados pelo TraceHeaderView.
    # ======================================================================
    def set_displayed_headers(self, header_keys: tuple[str, ...] | list[str]) -> None:
        self._displayed_header_keys = tuple(header_keys)
        self._request_current_data()


    # ======================================================================
    # Attribute graph -Define os header/atributo mostrados no gráfico inferior
    # ======================================================================
    def set_graph_headers(self, header_keys: tuple[str, ...] | list[str]) -> None:
        self._graph_header_keys = tuple(header_keys)
        self._request_current_data()


    # ======================================================================
    # Selected trace - Atualiza o traço selecionado compartilhado pelos três widgets.
    # ======================================================================
    def select_trace(self, trace_index: int | None) -> None:
       self._viewport.selected_trace = trace_index
       self._refresh_hsynchronized_widgets()


    # ======================================================================
    # Finaliza a sessão de dados pertencente exclusivamente a esta janela.
    # ======================================================================
    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            if self._data_is_open:
                self._use_cases.close()
                self._data_is_open = False
        finally:
            super().closeEvent(event)
            event.accept()




