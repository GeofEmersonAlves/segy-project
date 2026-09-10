# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Janela responsável pela visualização dos dados sísmicos. A visualização
dos dados é composta por três widgets principais:
           TraceHeaderView
           SeismicDataView
           TraceAttributeGraphView

       A SeismicDataWindow coordena o estado e o sincronismo entre esses componentes,
além da barra de rolagem, menus, toolbars e status bar.
       A janela terá duas barras de ferramentas fixas
       -Main Seismic Toolbar
       -View Seismic Toolbar

Histórico:
       04/09/2026 - Início da implementação da janela
       09/09/2026 - Estrutura inicial da Seismic Data Window
===============================================================================
"""
from pathlib import Path
from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QHBoxLayout, QMainWindow, QScrollBar, QStatusBar, QToolBar, QVBoxLayout, QWidget)
from segy_viewer.application.seismic_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import TraceHeaderView
from segy_viewer.presentation.desktop.widgets.seismic_data_window import SeismicDataView
from segy_viewer.presentation.desktop.widgets.seismic_data_window import TraceAttributeGraphView
from segy_viewer.resources import resource_path
from segy_viewer import AppConfig

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
               # use_cases: SeismicWindowUseCases,
                 config: AppConfig,
                 parent=None):

        super().__init__(parent)
        self._config = config
        self._path = path
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose,True)

        # Quantidade total de traços do conjunto carregado.
        # Isso não pertence ao viewport.
        self._total_trace_count = 0

        # Estado da região atualmente visível.
        self._viewport = SeismicViewport()

        # Widgets principais
        self._header_view = TraceHeaderView(parent=self)
        self._seismic_data_view = SeismicDataView(parent=self)
        self._attribute_view = TraceAttributeGraphView(parent=self)

        # Navegação
        self._horizontal_scrollbar =  QScrollBar(Qt.Orientation.Horizontal)

        # -------------------------------------------------------------
        # Construção da janela
        # -------------------------------------------------------------

        self._build_ui()
        self._create_actions()
        self._create_menu_bar()
        self._create_toolbars()
        self._create_status_bar()
        # self._connect_signals()
        self._configure_scrollbar()
        self._configure_window()
        # self._initialize_display()


    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)

        # Header
        self._header_view.setMinimumHeight(45)
        self._header_view.setMaximumHeight(160)

        # Seismic data
        self._seismic_data_view.setMinimumHeight(200)

        # Attribute graph
        self._attribute_view.setMinimumHeight(60)
        self._attribute_view.setMaximumHeight(180)

        # Layout
        main_layout.addWidget(self._header_view, stretch=0)
        main_layout.addWidget(self._seismic_data_view,stretch=1)
        main_layout.addWidget(self._attribute_view,stretch=0)
        main_layout.addWidget(self._horizontal_scrollbar,stretch=0)

        self.setCentralWidget(central_widget)

    def _create_actions(self):
        # Main seismic tool bar actions
        self._dead_trace_detection_action = QAction(QIcon(str(_DEAD_TRACE_DETECTION_ICON)), "Dead trace auto detection", self,
                                              toolTip="Dead trace auto detection dialog")

        self._processing_tool_action = QAction(QIcon(str(_PROCESSING_TOOL_ICON)), "Processing tools", self,
                                              toolTip="Processing tools dialog")

        #DEMAIS FERRAMENTAS DE PROCESSAMENTO SERÃO IMPLEMENTADAS CONFORME O PROJE CRESCE

        #View Seismic Tool Bar actions
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

    def _create_menu_bar(self):
        # AINDA TO NA DÚVIDA SE COLOCO MENU OU DEIXO TUDO NAS BARRAS DE FERRAMENTAS
        return

    def _create_toolbars(self):
        self._main_seismic_tool_bar = QToolBar("Main Seismic Toolbar", self)
        self._main_seismic_tool_bar.setMovable(False)
        self._main_seismic_tool_bar.setStyleSheet(self._config.SEISMIC_DATA_WINDOW_TOOL_BAR_STYLE)
        self._main_seismic_tool_bar.setIconSize(QSize(25, 25))

        self._main_seismic_tool_bar.addAction(self._exit_action)
        self._main_seismic_tool_bar.addSeparator()
        self._main_seismic_tool_bar.addAction(self._dead_trace_detection_action)
        self._main_seismic_tool_bar.addAction(self._processing_tool_action)
        self.addToolBar(self._main_seismic_tool_bar)

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

    def _create_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def _configure_window(self) -> None:
        self.setWindowTitle(f"Seismic Data Window: {self._path}")
        self.resize(1400, 850)

    def _configure_scrollbar(self) -> None:
        self._horizontal_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        self._horizontal_scrollbar.setStyleSheet(self._config.SEISMIC_SCROLLBAR_STYLE)
        maximum = max(0, self._total_trace_count - self._viewport.trace_count)
        self._horizontal_scrollbar.setRange(0, maximum)
        self._horizontal_scrollbar.setPageStep(self._viewport.trace_count)
        self._horizontal_scrollbar.setSingleStep(1)
        self._horizontal_scrollbar.setValue(self._viewport.first_trace)
