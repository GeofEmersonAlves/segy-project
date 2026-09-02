# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : main_window.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria a MainWindow da aplicação
Histórico:
       28/08/2026 - Implementação da Classe
       01/09/2026 - Criação da Tool Bar
===============================================================================
"""

from pathlib import Path
from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QSplitter, QStatusBar, QLabel, QToolBar, QComboBox
from segy_viewer.presentation.desktop.widgets import SegyFileBrowser, SegyFileInspector

_BASE_DIR = Path(__file__).resolve().parents[5]
_ICON_OPEN_FOLDER = _BASE_DIR / "resources" / "icons" / "open_folder.ico"
_ICON_REFRESH_BUTTON= _BASE_DIR / "resources" / "icons" / "reload_folder.ico"
_EXPORT_ICON = _BASE_DIR / "resources" / "icons" / "export.png"
_DATA_WINDOW_ICON = _BASE_DIR / "resources" / "icons" / "seismicWindow.png"
_TOOL_MD5_ICON = _BASE_DIR / "resources" / "icons" / "MD5Tools.png"
_TOOL_JDC_ICON = _BASE_DIR / "resources" / "icons" / "julian_day.png"
_TOOL_SIZE_CALC_ICON = _BASE_DIR / "resources" / "icons" / "segyfilesizecalculator.png"
_EXIT_ICON = _BASE_DIR / "resources" / "icons" / "exit.png"

class MainWindow(QMainWindow):

    def __init__(self,
                 file_browser: SegyFileBrowser,
                 file_inspector: SegyFileInspector,
                 parent=None):
        super().__init__(parent)

        self._file_browser = file_browser
        self._file_inspector = file_inspector

        self.resize(1200, 750)

        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_central_widget()
        self._create_status_bar()
        self._connect_signals()

        # Estado inicial
        self._file_inspector.clear_tabs_content()
        self._set_segy_actions_enabled(False)

    def _create_central_widget(self) -> None:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        splitter.addWidget(self._file_browser)
        splitter.addWidget(self._file_inspector)

        # largura inicial aproximada
        splitter.setSizes([400, 800])

        # Browser não precisa crescer tanto quanto inspector
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self._file_status_label = QLabel(str(self._file_browser.path))
        status_bar.addWidget(self._file_status_label, 1)

    #Qactions do Menus e Barra de Ferramentas
    def _create_actions(self) -> None:
        # -------------------------
        # File
        self._open_directory_action = QAction(QIcon(str(_ICON_OPEN_FOLDER)),"Open directory", self, toolTip="Open directory to show segy files")
        self._open_directory_action.setShortcut(QKeySequence("Ctrl+O"))
        self._open_directory_action.setStatusTip("Open directory to show segy files")

        self._refresh_directory_action = QAction(QIcon(str(_ICON_REFRESH_BUTTON)),"Reopen directory", self)
        self._refresh_directory_action.setStatusTip("Refresh segy file list")
        self._refresh_directory_action.setShortcut(QKeySequence("Ctrl+R"))
        # -------------------------
        self._export_info_action = QAction(QIcon(str(_EXPORT_ICON)),"Export", self)

        self._export_summary_action = QAction(QIcon(str(_EXPORT_ICON)),"Export Summary", self)
        self._export_summary_action.setStatusTip("Export Segy Summary ")
        self._export_summary_action.setShortcut(QKeySequence("Ctrl+S"))

        self._export_text_header_action = QAction(QIcon(str(_EXPORT_ICON)),"Export Text Header", self)
        self._export_text_header_action.setStatusTip("Export Segy Text Header ")
        self._export_text_header_action.setShortcut(QKeySequence("Ctrl+H"))

        self._export_binary_header_action = QAction(QIcon(str(_EXPORT_ICON)),"Export Bin Header", self)
        self._export_binary_header_action.setStatusTip("Export Segy Binary Header ")
        self._export_binary_header_action.setShortcut(QKeySequence("Ctrl+B"))

        self._export_trace_header_action = QAction(QIcon(str(_EXPORT_ICON)),"Export Trace Header",self)
        self._export_trace_header_action.setStatusTip("Export Segy Trace Header ")
        self._export_trace_header_action.setShortcut(QKeySequence("Ctrl+T"))
        # -------------------------
        self._exit_action = QAction(QIcon(str(_EXIT_ICON)),"Exit", self)
        self._exit_action.setShortcut(QKeySequence("Ctrl+X"))

        # -------------------------
        # View
        self._summary_action = QAction("Summary", self)
        self._text_header_action = QAction("Text Header", self)
        self._binary_header_action = QAction("Binary Header", self)
        self._trace_header_action = QAction("Trace Header", self)
        # -------------------------
        self._data_window_action = QAction(QIcon(str(_DATA_WINDOW_ICON)),"Seismic Data window", self, toolTip="Show Seismic Data window")
        self._data_window_action.setStatusTip("Show Seismic Data window ")
        self._data_window_action.setShortcut(QKeySequence("Ctrl+W"))

        # -------------------------
        # Tools
        self._julian_day_action = QAction(QIcon(str(_TOOL_JDC_ICON)),"Julian day calendar", self)
        self._md5_action = QAction(QIcon(str(_TOOL_MD5_ICON)),"MD5", self)
        self._file_size_calculator_action = QAction(QIcon(str(_TOOL_SIZE_CALC_ICON)),"Segy file size calculator", self)

        # -------------------------
        # Help
        self._manual_pt_action = QAction("User Manual (Português)", self)
        self._manual_en_action = QAction("User Manual (English)", self)
        self._about_action = QAction("About SegyViewer", self)


    def _create_menu_bar(self) -> None:
        # ==================================================
        # File
        # ==================================================
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self._open_directory_action)
        file_menu.addAction(self._refresh_directory_action)
        file_menu.addSeparator()
        file_menu.addAction(self._export_summary_action)
        file_menu.addAction(self._export_text_header_action)
        file_menu.addAction(self._export_binary_header_action)
        file_menu.addAction(self._export_trace_header_action)
        file_menu.addSeparator()
        file_menu.addAction(self._exit_action)

        # ==================================================
        # View
        # ==================================================
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self._summary_action)
        view_menu.addAction(self._text_header_action)
        view_menu.addAction(self._binary_header_action)
        view_menu.addAction(self._trace_header_action)
        view_menu.addSeparator()
        view_menu.addAction(self._data_window_action)

        # ==================================================
        # Tools
        # ==================================================
        tools_menu = self.menuBar().addMenu("&Tools")
        tools_menu.addAction(self._julian_day_action)
        tools_menu.addAction(self._md5_action)
        tools_menu.addAction(self._file_size_calculator_action)

        # ==================================================
        # Help
        # ==================================================
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self._manual_pt_action)
        help_menu.addAction(self._manual_en_action)
        help_menu.addSeparator()
        help_menu.addAction(self._about_action)

    def _create_tool_bar(self) -> None:
        self._main_tool_bar = QToolBar("Main Toolbar", self)
        self._main_tool_bar.setMovable(True)
        self._main_tool_bar.setIconSize(QSize(96, 32))
        self.addToolBar(self._main_tool_bar)

        self._section_view_export_combo = QComboBox()
        for section in self._file_inspector.section_type:
            self._section_view_export_combo.addItem(section.value, section)

        self._main_tool_bar.addSeparator()
        self._main_tool_bar.addAction(self._export_info_action)
        self._main_tool_bar.addWidget(self._section_view_export_combo)
        view_expor_button = self._main_tool_bar.widgetForAction(self._export_info_action)
        view_expor_button.setFixedWidth(40)
        self._main_tool_bar.addSeparator()

        self._main_tool_bar.addAction(self._data_window_action)
        data_window_button = self._main_tool_bar.widgetForAction(self._data_window_action)
        data_window_button.setFixedWidth(100)
        self._main_tool_bar.addSeparator()

        self._tools_tool_bar = QToolBar("Tools Toolbar", self)
        self._tools_tool_bar.setMovable(True)
        self._tools_tool_bar.setIconSize(QSize(32, 32))
        self.addToolBar(self._tools_tool_bar)

        self._tools_tool_bar.addSeparator()
        self._tools_tool_bar.addAction(self._julian_day_action)
        self._tools_tool_bar.addAction(self._md5_action)
        self._tools_tool_bar.addAction(self._file_size_calculator_action)
        self._tools_tool_bar.addSeparator()

    def _connect_signals(self) -> None:
        # Browser -> MainWindow
        self._file_browser.file_selected.connect(self._on_segy_file_selected)
        self._file_browser.path_changed.connect(self._on_directory_changed)

        # Inspector -> MainWindow
        self._file_inspector.segy_inspector_has_data.connect(self._on_inspector_has_data)
        self._file_inspector.segy_inspector_empty.connect(self._on_inspector_empty)
        self._file_inspector.segy_inspector_tab_changed.connect(self._inspector_section_changed)

        # File actions
        self._open_directory_action.triggered.connect(self._file_browser.open_folder_dialog)
        self._refresh_directory_action.triggered.connect(self._file_browser.refresh)
        #-------------------------------------------------------------------------------------------
        self._export_summary_action.triggered.connect(self._file_inspector.export_summary)
        self._export_text_header_action.triggered.connect(self._file_inspector.export_text_header)
        self._export_binary_header_action.triggered.connect(self._file_inspector.export_binary_header)
        self._export_trace_header_action.triggered.connect(self._file_inspector.export_trace_header)
        self._export_info_action.triggered.connect(self._export)
        # -------------------------------------------------------------------------------------------
        self._exit_action.triggered.connect(self.close)

        # View actions
        self._summary_action.triggered.connect(self._file_inspector.show_summary)
        self._text_header_action.triggered.connect(self._file_inspector.show_text_header)
        self._binary_header_action.triggered.connect(self._file_inspector.show_binary_header)
        self._trace_header_action.triggered.connect(self._file_inspector.show_trace_header)
        self._section_view_export_combo.currentTextChanged.connect(self._on_section_changed)


    @Slot(str)
    def _inspector_section_changed(self, section:str)->None:
        if section != self._section_view_export_combo.currentText():
            self._section_view_export_combo.setCurrentText(section)

    @Slot(str)
    def _on_section_changed(self, section: str) -> None:
        if section == self._file_inspector.section_type.SUMMARY:
            self._file_inspector.show_summary()

        elif section == self._file_inspector.section_type.TEXT_HEADER:
            self._file_inspector.show_text_header()

        elif section == self._file_inspector.section_type.BIN_HEADER:
            self._file_inspector.show_binary_header()

        elif section == self._file_inspector.section_type.TRACE_HEADER:
            self._file_inspector.show_trace_header()

    @Slot()
    def _export(self) -> None:
        selected = self._section_view_export_combo.currentText()

        if selected == self._file_inspector.section_type.SUMMARY:
            self._export_summary_action.trigger()

        elif selected == self._file_inspector.section_type.TEXT_HEADER:
            self._export_text_header_action.trigger()

        elif selected == self._file_inspector.section_type.BIN_HEADER:
            self._export_binary_header_action.trigger()

        elif selected == self._file_inspector.section_type.TRACE_HEADER:
            self._export_trace_header_action.trigger()

    @Slot(Path)
    def _on_segy_file_selected(self, path: Path) -> None:
        self._file_inspector.segy_path = path
        self._file_status_label.setText(f"File: {path}")

    @Slot(Path)
    def _on_directory_changed(self, path: Path) -> None:
        # self.statusBar().showMessage(f"Directory: {path}")
        self._file_status_label.setText(f"Directory: {path}")
        self._file_inspector.clear_tabs_content()

    @Slot()
    def _on_inspector_has_data(self) -> None:
        self._set_segy_actions_enabled(True)

    @Slot()
    def _on_inspector_empty(self) -> None:
        self._set_segy_actions_enabled(False)

    def _set_segy_actions_enabled(self, enabled: bool) -> None:
        self._export_info_action.setEnabled(enabled)
        self._section_view_export_combo.setCurrentIndex(0)
        self._section_view_export_combo.setEnabled(enabled)
        self._export_summary_action.setEnabled(enabled)
        self._export_text_header_action.setEnabled(enabled)
        self._export_binary_header_action.setEnabled(enabled)
        self._export_trace_header_action.setEnabled(enabled)

        self._summary_action.setEnabled(enabled)
        self._text_header_action.setEnabled(enabled)
        self._binary_header_action.setEnabled(enabled)
        self._trace_header_action.setEnabled(enabled)

        self._data_window_action.setEnabled(enabled)