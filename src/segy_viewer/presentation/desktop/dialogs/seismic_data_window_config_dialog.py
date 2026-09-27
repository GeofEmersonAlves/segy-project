# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window_config_dialog.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Dialog de configuração da Seismic Data Window

Histórico:
       25/09/2026 - Implementação do Dialog
===============================================================================
"""
from pydoc import text

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox,
                               QHBoxLayout,
                               QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QSpinBox, QTabWidget,
                               QVBoxLayout, QWidget, QFrame)

from segy_viewer.presentation.desktop.windows.data_window.seismic_data_window_config import (AVAILABLE_GRAPH_HEADERS,
                                                                                             AVAILABLE_HEADERS,
                                                                                             SeismicDisplaySettings,
                                                                                             TraceDrawingMode)


class SeismicDataWindowConfigDialog(QDialog):
    """
    Permite editar as configurações da Seismic Data Window.

    OK: aplica e fecha.
    Apply: aplica e permanece aberto.
    Cancel: fecha sem aplicar as edições pendentes.
    """

    # O bool informa se number_traces_to_show mudou.
    settings_applied = Signal(bool)

    def __init__(self,  settings: SeismicDisplaySettings,   parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._settings = settings

        # Cópias locais: escolher uma cor não altera settings
        # antes de OK ou Apply.
        self._point_color = QColor(settings.graph_point_color)
        self._line_color = QColor(settings.graph_line_color)

        self.setWindowTitle("Data Window Settings")
                         #  w, h
        self.setFixedSize(390, 400)

        tabs = QTabWidget(self)
        tabs.addTab(self._create_headers_tab(), "Trace Headers")
        tabs.addTab(self._create_seismic_tab(), "Seismic Plot Parameters")
        tabs.addTab(self._create_graph_tab(), "Attribute Graph")

        # Configuração geral da janela, fora das abas.
        self._trace_count_spinbox = QSpinBox()
        self._trace_count_spinbox.setRange(1, 10_000)
        self._trace_count_spinbox.setValue(settings.number_traces_to_show   )

        window_group = QGroupBox("Seismic Display")
        window_layout = QFormLayout(window_group)
        window_layout.addRow("Max traces in display:",self._trace_count_spinbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                 | QDialogButtonBox.StandardButton.Apply
                                 | QDialogButtonBox.StandardButton.Close)

        buttons.accepted.connect(self._on_ok)
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._on_apply)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(window_group)
        layout.addWidget(buttons)

    # ==============================================================
    # ABA HEADERS
    # ==============================================================

    def _create_headers_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self._show_headers_checkbox = QCheckBox("Show Trace Headers")
        self._show_headers_checkbox.setChecked(self._settings.show_trace_headers)
        layout.addWidget(self._show_headers_checkbox)

        layout.addWidget(QLabel("Select and order the Trace Headers:"))

        self._headers_list = QListWidget()

        # Os headers já selecionados aparecem primeiro,
        # preservando a ordem atual de exibição.
        selected_labels = [
            label
            for label in self._settings.header_keys_to_show
            if label in AVAILABLE_HEADERS
        ]

        remaining_labels = [
                            label
                            for label in AVAILABLE_HEADERS
                            if label not in selected_labels
                         ]

        for label in selected_labels + remaining_labels:
            item = QListWidgetItem(str(AVAILABLE_HEADERS[label]))
            item.setData(Qt.ItemDataRole.UserRole, label)

            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if label in selected_labels
                                                        else Qt.CheckState.Unchecked)
            self._headers_list.addItem(item)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self._headers_list)

        up_button = QPushButton("⬆️\nUP")
        down_button = QPushButton("DOWN\n ⬇️")
        up_button.clicked.connect(lambda: self._move_header(-1))
        down_button.clicked.connect(lambda: self._move_header(1))
        v_layout = QVBoxLayout()
        v_layout.addWidget(up_button)
        v_layout.addWidget(down_button)
        h_layout.addLayout(v_layout)
        layout.addLayout(h_layout)
        return tab

    def _move_header(self, step: int) -> None:
        current_row = self._headers_list.currentRow()
        target_row = current_row + step

        if current_row < 0:
            return

        if not 0 <= target_row < self._headers_list.count():
            return

        item = self._headers_list.takeItem(current_row)
        self._headers_list.insertItem(target_row, item)
        self._headers_list.setCurrentRow(target_row)

    def _selected_headers(self) -> dict[str, str]:
        selected: dict[str, str] = {}

        for row in range(self._headers_list.count()):
            item = self._headers_list.item(row)

            if item.checkState() == Qt.CheckState.Checked:
                label = item.text()
                header_key = item.data(Qt.ItemDataRole.UserRole)
                selected[header_key] = label
        return selected

    # ==============================================================
    # ABA DESENHO SÍSMICO
    # ==============================================================
    def _create_seismic_tab(self) -> QWidget:
        tab = QWidget()
        layout = QFormLayout(tab)

        self._drawing_mode_combo = QComboBox()
        self._drawing_mode_combo.addItem("Wiggle", TraceDrawingMode.WIGGLE)
        self._drawing_mode_combo.addItem("Variable Area", TraceDrawingMode.VARIABLE_AREA)

        index = self._drawing_mode_combo.findData(self._settings.trace_drawing_mode)
        if index >= 0:
            self._drawing_mode_combo.setCurrentIndex(index)

        layout.addRow("Dwawing mode:", self._drawing_mode_combo)

        return tab

    # ==============================================================
    # ABA GRÁFICO
    # ==============================================================
    def _create_graph_tab(self) -> QWidget:
        tab = QWidget()
        layout = QFormLayout(tab)

        self._show_graph_checkbox = QCheckBox("Show graph")
        self._show_graph_checkbox.setChecked(self._settings.show_attribute_graph)

        self._graph_header_combo = QComboBox()
        for header_key in AVAILABLE_GRAPH_HEADERS:
            self._graph_header_combo.addItem(header_key, header_key)

        if self._settings.graph_header_keys_to_show:
            index = self._graph_header_combo.findData(self._settings.graph_header_keys_to_show[0])
            if index >= 0:
                self._graph_header_combo.setCurrentIndex(index)
        h_attr_layout = QHBoxLayout()
        label = QLabel("Attribute:")
        h_attr_layout.addWidget(label)
        h_attr_layout.addWidget(self._graph_header_combo)
        layout.addRow(self._show_graph_checkbox, h_attr_layout)

        self._add_separator(layout)

        self._keep_yaxis_on_zero_checkbox = QCheckBox("Keep Y axis zero fixed." )
        self._keep_yaxis_on_zero_checkbox.setChecked(self._settings.keep_graph_y_axis_on_zero)
        layout.addRow(self._keep_yaxis_on_zero_checkbox)

        self._show_min_max_checkbox = QCheckBox("Show min/max values.")
        self._show_min_max_checkbox.setChecked(self._settings.show_graph_min_max_values)
        layout.addRow(self._show_min_max_checkbox)

        self._add_separator(layout)

        self._show_points_checkbox = QCheckBox("Plot points")
        self._show_points_checkbox.setChecked(self._settings.plot_graph_point)

        self._point_color_button = QPushButton()
        self._update_color_button(self._point_color_button, self._point_color)
        self._point_color_button.clicked.connect(self._choose_point_color)

        pt_h_layout = QVBoxLayout()
        pt_label = QLabel("Point color")
        pt_h_layout.addWidget(pt_label, alignment=Qt.AlignmentFlag.AlignCenter)
        pt_h_layout.addWidget(self._point_color_button)
        layout.addRow(self._show_points_checkbox,pt_h_layout)

        self._add_separator(layout)

        self._show_lines_checkbox = QCheckBox("Plot line")
        self._show_lines_checkbox.setChecked(self._settings.plot_graph_line)

        self._line_color_button = QPushButton()
        self._update_color_button(self._line_color_button, self._line_color )
        self._line_color_button.clicked.connect(self._choose_line_color)

        layout.addRow(self._show_lines_checkbox)
        ln_h_layout = QVBoxLayout()
        ln_label = QLabel("Line color")
        ln_h_layout.addWidget(ln_label, alignment=Qt.AlignmentFlag.AlignCenter)
        ln_h_layout.addWidget(self._line_color_button)

        layout.addRow(self._show_lines_checkbox , ln_h_layout)

        return tab

    @staticmethod
    def _add_separator(layout: QFormLayout) -> None:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addRow(line)

    @staticmethod
    def _update_color_button(button: QPushButton, color: QColor) -> None:
        background = color.name()
        foreground = ("white" if color.lightness() < 128 else "black" )

        button.setText(background)
        button.setStyleSheet(f"background-color: {background};"
                             f"color: {foreground};")

    def _choose_point_color(self) -> None:
        color = QColorDialog.getColor(self._point_color, self, "Points color")
        if not color.isValid():
            return
        self._point_color = color
        self._update_color_button(self._point_color_button, color)

    def _choose_line_color(self) -> None:
        color = QColorDialog.getColor(self._line_color, self, "Line color")
        if not color.isValid():
            return
        self._line_color = color
        self._update_color_button(self._line_color_button, color)


    # ==============================================================
    # OK / APPLY / CANCEL
    # ==============================================================

    def _validate(self) -> bool:
        if self._show_headers_checkbox.isChecked() and not self._selected_headers():
            QMessageBox.warning(self,  "Trace Headers", "Select at least one Trace Header to display.")
            return False

        return True

    def _apply_changes(self) -> bool:
        if not self._validate():
            return False

        settings = self._settings
        trace_count_changed = settings.number_traces_to_show != self._trace_count_spinbox.value()

        # Configurações gerais.
        settings.number_traces_to_show = self._trace_count_spinbox.value()

        # TraceHeaderView.
        settings.show_trace_headers = self._show_headers_checkbox.isChecked()
        settings.header_keys_to_show = self._selected_headers()

        # SeismicDataSamplesView.
        settings.trace_drawing_mode = self._drawing_mode_combo.currentData()

        # TraceAttributeGraphView.
        settings.show_attribute_graph = self._show_graph_checkbox.isChecked()
        settings.graph_header_keys_to_show =  (self._graph_header_combo.currentData(),)
        settings.keep_graph_y_axis_on_zero = self._keep_yaxis_on_zero_checkbox.isChecked()
        settings.show_graph_min_max_values =   self._show_min_max_checkbox.isChecked()
        settings.plot_graph_point = self._show_points_checkbox.isChecked()
        settings.graph_point_color = QColor(self._point_color)
        settings.plot_graph_line =  self._show_lines_checkbox.isChecked()
        settings.graph_line_color = QColor(self._line_color)

        self.settings_applied.emit(trace_count_changed)

        return True

    def _on_apply(self) -> None:
        self._apply_changes()

    def _on_ok(self) -> None:
        if self._apply_changes():
            self.accept()