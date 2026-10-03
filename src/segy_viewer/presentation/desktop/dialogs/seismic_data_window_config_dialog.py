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
       26/29/2026 - Finalização do layout e funcionalidades
       01/10/2026 - Inclusão das opções para desenho das amostras sísmicas
       02/10/2026 - Inclusão das propriedades para o calculo das amplitudes dos tracos
       02/10/2026 - Inclusão da Aba Scale
==============================================================================
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox,
                               QHBoxLayout,
                               QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QSpinBox, QTabWidget,
                               QVBoxLayout, QWidget, QFrame, QDoubleSpinBox)

from segy_viewer.presentation.desktop.windows.data_window.seismic_data_window_config import (AVAILABLE_GRAPH_HEADERS,
                                                                                             AVAILABLE_HEADERS,
                                                                                             TRACEDRAWINGMODES,
                                                                                             SeismicDisplaySettings,
                                                                                             AMPLITUDE_SCALE_CALCULATIONS)
class SeismicDataWindowConfigDialog(QDialog):
    """
    Permite editar as configurações da Seismic Data Window.

    OK: aplica e fecha.
    Apply: aplica e permanece aberto.
    Cancel: fecha sem aplicar as edições pendentes.
    """

    # O bool informa se number_traces_to_show mudou.
    settings_applied = Signal(bool)
    recalc_scale = Signal()

    def __init__(self,  settings: SeismicDisplaySettings,   parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._settings = settings

        # Cópias locais: escolher uma cor não altera settings antes de OK ou Apply.
        self._point_color = QColor(settings.graph_point_color)
        self._line_color = QColor(settings.graph_line_color)
        self._background_color = QColor(settings.background_color)
        self._wiggle_color = QColor(settings.wiggle_color)
        self._positive_fill_color=QColor(settings.positive_fill_color)
        self._negative_fill_color=QColor(settings.negative_fill_color)
        self._dead_trace_color=QColor(settings.dead_trace_wiggle_color)

        self.setWindowTitle("Seismic Data Window Settings")
                         #  w, h
        self.setFixedSize(500, 430)

        tabs = QTabWidget(self)
        tabs.addTab(self._create_seismic_tab(), "Plot Parameters")
        tabs.addTab(self._create_pre_process_tab(), "Pré-Process")
        tabs.addTab(self._create_scale_tab(), "Scale")
        tabs.addTab(self._create_headers_tab(), "Trace Headers")
        tabs.addTab(self._create_graph_tab(), "Attribute Graph")

        # Configuração geral da janela, fora das abas.
        self._trace_count_spinbox = QSpinBox()
        self._trace_count_spinbox.setRange(1, 10_000)
        self._trace_count_spinbox.setValue(settings.number_traces_to_show)

        window_group = QGroupBox("Seismic Display")
        window_layout = QFormLayout(window_group)
        window_layout.addRow("Max Traces in Display:",self._trace_count_spinbox)

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
        self._change_tab_background(tab)
        layout = QVBoxLayout(tab)

        self._show_headers_checkbox = QCheckBox("Show Trace Headers")
        self._show_headers_checkbox.setChecked(self._settings.show_trace_headers)
        layout.addWidget(self._show_headers_checkbox)

        layout.addWidget(QLabel("Select and order the Trace Headers:"))

        self._headers_list = QListWidget()

        # Os headers já selecionados aparecem primeiro,
        # preservando a ordem atual de exibição.
        selected_labels = [label
                           for label in self._settings.header_keys_to_show
                         if label in AVAILABLE_HEADERS]

        remaining_labels = [label
                            for label in AVAILABLE_HEADERS
                            if label not in selected_labels]

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
        self._change_tab_background(tab)
        layout = QFormLayout(tab)

        self._drawing_mode_combo = QComboBox()
        for trc_drw_mode  in TRACEDRAWINGMODES:
            self._drawing_mode_combo.addItem(trc_drw_mode.value, trc_drw_mode.name)

        index = self._drawing_mode_combo.findData(self._settings.trace_drawing_mode)
        if index >= 0:
            self._drawing_mode_combo.setCurrentIndex(index)

        layout.addRow("Drawing Mode:", self._drawing_mode_combo)

        self._add_separator(layout)

        bck_label = QLabel("Background Color:")
        self._background_color_button = QPushButton()
        self._update_color_button(self._background_color_button, self._background_color)
        self._background_color_button.clicked.connect(self._choose_background_color)
        bk_color_h_layout = QHBoxLayout()
        bk_color_h_layout.addWidget(bck_label)
        bk_color_h_layout.addWidget(self._background_color_button)

        wiggle_color_label = QLabel("Wiggle Color:")
        self._wiggle_color_button = QPushButton()
        self._update_color_button(self._wiggle_color_button, self._wiggle_color)
        self._wiggle_color_button.clicked.connect(self._choose_wiggle_color)
        wgl_color_h_layout = QHBoxLayout()
        wgl_color_h_layout.addWidget(wiggle_color_label, alignment=Qt.AlignmentFlag.AlignRight)
        wgl_color_h_layout.addWidget(self._wiggle_color_button)

        _color_h_layout = QHBoxLayout()
        _color_h_layout.addLayout(bk_color_h_layout)
        _color_h_layout.addLayout(wgl_color_h_layout)
        layout.addRow(_color_h_layout)

        self._trace_excursion_spinbox = QDoubleSpinBox()
        self._trace_excursion_spinbox.setRange(0.01, 100)
        self._trace_excursion_spinbox.setSingleStep(0.05)
        self._trace_excursion_spinbox.setDecimals(2)
        self._trace_excursion_spinbox.setValue(self._settings.trace_excursion)
        trace_excursion_label = QLabel("Trace Excursion:")
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(trace_excursion_label)
        h_layout1.addWidget(self._trace_excursion_spinbox)

        self._max_clip_excursion_spinbox = QDoubleSpinBox()
        self._max_clip_excursion_spinbox.setRange(0.01, 100)
        self._max_clip_excursion_spinbox.setSingleStep(0.05)
        self._max_clip_excursion_spinbox.setDecimals(2)
        self._max_clip_excursion_spinbox.setValue(self._settings.max_clip_excursion)
        max_clip_excursion_label = QLabel("Max. Clip Excursion:")
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(max_clip_excursion_label)
        h_layout2.addWidget(self._max_clip_excursion_spinbox)

        self._variable_area_bias_spinbox = QSpinBox()
        self._variable_area_bias_spinbox.setRange(1, 100)
        self._variable_area_bias_spinbox.setSingleStep(1)
        self._variable_area_bias_spinbox.setValue(self._settings.variable_area_bias)
        variable_area_bias_spinbox_label = QLabel("Variable Area Bias:")
        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(variable_area_bias_spinbox_label)
        h_layout3.addWidget(self._variable_area_bias_spinbox)

        trace_excursion_v_layout = QVBoxLayout()
        trace_excursion_v_layout.addLayout(h_layout1)
        trace_excursion_v_layout.addLayout(h_layout2)
        trace_excursion_v_layout.addLayout(h_layout3)

        self._positive_fill_color_button = QPushButton()
        self._update_color_button(self._positive_fill_color_button, self._positive_fill_color)
        self._positive_fill_color_button.clicked.connect(self._choose_positive_fill_color)

        self._negative_fill_color_button = QPushButton()
        self._update_color_button(self._negative_fill_color_button, self._negative_fill_color)
        self._negative_fill_color_button.clicked.connect(self._choose_negative_fill_color)

        self._fill_negative_va_checkbox = QCheckBox("Fill Negative Variable Area")
        self._fill_negative_va_checkbox.setChecked(self._settings.fill_negative_va)

        positive_color_label = QLabel("POSITIVE")
        negative_color_label = QLabel("NEGATIVE")

        # Grupo com título
        fill_color_group = QGroupBox("Fill Color")
        fill_color_h_layout = QVBoxLayout(fill_color_group)
        fill_color_h_layout.addWidget(positive_color_label, alignment=Qt.AlignmentFlag.AlignCenter)
        fill_color_h_layout.addWidget(self._positive_fill_color_button)
        fill_color_h_layout.addWidget(negative_color_label, alignment=Qt.AlignmentFlag.AlignCenter)
        fill_color_h_layout.addWidget(self._negative_fill_color_button)
        fill_color_h_layout.addWidget(self._fill_negative_va_checkbox)

        wiggle_final_h_layout = QHBoxLayout()
        wiggle_final_h_layout.addLayout(trace_excursion_v_layout)
        wiggle_final_h_layout.addWidget(fill_color_group)

        layout.addRow(wiggle_final_h_layout)

        return tab

    # ==============================================================
    # ABA OPCOES DE PRE PROCESSAMENTO
    # ==============================================================
    def _create_pre_process_tab(self) -> QWidget:
        tab = QWidget()
        self._change_tab_background(tab)
        layout = QFormLayout(tab)

        # Grupo com título
        dead_trace_group = QGroupBox("Dead Traces")
        dead_trace_v_layout = QVBoxLayout(dead_trace_group)

        self._display_dead_traces_checkbox = QCheckBox("Display Dead Traces")
        self._display_dead_traces_checkbox.setChecked(self._settings.display_dead_traces)

        self._dead_trace_rms_limit_spinbox = QDoubleSpinBox()
        self._dead_trace_rms_limit_spinbox.setRange(0, 10_000)
        self._dead_trace_rms_limit_spinbox.setSingleStep(1)
        self._dead_trace_rms_limit_spinbox.setDecimals(8)
        self._dead_trace_rms_limit_spinbox.setValue(self._settings.dead_trace_rms_limit)
        m_dead_trace_rms_limit_label = QLabel("Dead Trace RMS Limit:")
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(m_dead_trace_rms_limit_label)
        h_layout1.addWidget(self._dead_trace_rms_limit_spinbox)

        self._dead_trace_color_button = QPushButton()
        self._update_color_button(self._dead_trace_color_button, self._dead_trace_color)
        self._dead_trace_color_button.clicked.connect(self._choose_dead_trace_color)
        m_dead_trace_color_label = QLabel("Dead Trace Wiggle Color:")
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(m_dead_trace_color_label)
        h_layout2.addWidget(self._dead_trace_color_button)

        dead_trace_v_layout.addWidget(self._display_dead_traces_checkbox)
        dead_trace_v_layout.addLayout(h_layout1)
        dead_trace_v_layout.addLayout(h_layout2)

        layout.addRow(dead_trace_group)

        self._add_separator(layout)

        self._reverse_data_polarity_checkbox = QCheckBox("Reverse Data Polarity")
        self._reverse_data_polarity_checkbox.setChecked(self._settings.reverse_data_polarity)
        layout.addRow(self._reverse_data_polarity_checkbox)

        self._add_separator(layout)

        self._amplitude_scale_db_spinbox = QSpinBox()
        self._amplitude_scale_db_spinbox.setRange(-500, 500)
        self._amplitude_scale_db_spinbox.setSingleStep(1)
        self._amplitude_scale_db_spinbox.setValue(self._settings.amplitude_scale_db)
        _amplitude_scale_db_spinbox_label = QLabel("Amplitude Scale DB:")
        h_layout = QHBoxLayout()
        h_layout.addWidget(_amplitude_scale_db_spinbox_label)
        h_layout.addWidget(self._amplitude_scale_db_spinbox)
        layout.addRow(h_layout)

        return tab

    def _create_scale_tab(self) -> QWidget:
        tab = QWidget()
        self._change_tab_background(tab)
        layout = QVBoxLayout(tab)

        # Método de cálculo.
        calculation_group = QGroupBox("Scale Calculation")
        calculation_layout = QFormLayout(calculation_group)

        self._scale_calculation_combo = QComboBox()
        for calculation, (name, description) in AMPLITUDE_SCALE_CALCULATIONS.items():
            self._scale_calculation_combo.addItem(name, calculation)

        index = self._scale_calculation_combo.findData(self._settings.amplitude_scale_calculation)
        if index >= 0:
            self._scale_calculation_combo.setCurrentIndex(index)

        calculation_layout.addRow("Scale Type Calculation:", self._scale_calculation_combo)

        self._scale_calculation_description = QLabel()
        self._scale_calculation_description.setWordWrap(True)
        calculation_layout.addRow("", self._scale_calculation_description)

        self._scale_calculation_combo.currentIndexChanged.connect(self._update_description)
        self._update_description()

        self._calc_scale_num_traces_spinbox = QSpinBox()
        self._calc_scale_num_traces_spinbox.setRange(1, self._settings.number_traces_to_show)
        self._calc_scale_num_traces_spinbox.setValue(self._settings.calc_scale_num_traces)
        calculation_layout.addRow("Calc. Scale Max. Traces:", self._calc_scale_num_traces_spinbox)
        layout.addWidget(calculation_group)

        # Valores de amplitude. "Auto" representa None, antes do cálculo inicial.
        amplitude_group = QGroupBox("Scale Amplitude Settings")
        amplitude_layout = QFormLayout(amplitude_group)

        auto_value = -1e15

        self._min_amp_spinbox = QDoubleSpinBox()
        self._min_amp_spinbox.setRange(auto_value, 1e15)
        self._min_amp_spinbox.setDecimals(12)
        self._min_amp_spinbox.setSpecialValueText("Auto")
        self._min_amp_spinbox.setValue(auto_value if self._settings.mim_amp_value is None
                                                   else self._settings.mim_amp_value)
        amplitude_layout.addRow("Min. Amplitude:", self._min_amp_spinbox)

        self._max_amp_spinbox = QDoubleSpinBox()
        self._max_amp_spinbox.setRange(auto_value, 1e15)
        self._max_amp_spinbox.setDecimals(12)
        self._max_amp_spinbox.setSpecialValueText("Auto")
        self._max_amp_spinbox.setValue(auto_value if self._settings.max_amp_value is None
                                                    else self._settings.max_amp_value)
        amplitude_layout.addRow("Max. Amplitude:", self._max_amp_spinbox)

        _lbl_text = f"{self._settings.calculated_scale_trace_count} traces were used to calculate the amplitudes."
        self._calculated_scale_count_label = QLabel(_lbl_text)

        recalc_button = QPushButton("🔄 Recalculate")
        recalc_button.setFixedWidth(100)
        recalc_button.clicked.connect(lambda: self._recalc_scale_amplitudes)

        amplitude_layout.addRow(self._calculated_scale_count_label, recalc_button)
        amplitude_layout.setAlignment(recalc_button, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(amplitude_group)
        layout.addStretch()

        return tab

    def _recalc_scale_amplitudes(self):
        self.recalc_scale.emit()

    # ==============================================================
    # ABA GRÁFICO
    # ==============================================================
    def _create_graph_tab(self) -> QWidget:
        tab = QWidget()
        self._change_tab_background(tab)
        layout = QFormLayout(tab)

        self._show_graph_checkbox = QCheckBox("Show Graph")
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

        self._keep_yaxis_on_zero_checkbox = QCheckBox("Keep Y Axis Zero Fixed." )
        self._keep_yaxis_on_zero_checkbox.setChecked(self._settings.keep_graph_y_axis_on_zero)
        layout.addRow(self._keep_yaxis_on_zero_checkbox)

        self._show_min_max_checkbox = QCheckBox("Show Min/Max Values.")
        self._show_min_max_checkbox.setChecked(self._settings.show_graph_min_max_values)
        layout.addRow(self._show_min_max_checkbox)

        self._add_separator(layout)

        self._show_points_checkbox = QCheckBox("Plot Points")
        self._show_points_checkbox.setChecked(self._settings.plot_graph_point)

        self._point_color_button = QPushButton()
        self._update_color_button(self._point_color_button, self._point_color)
        self._point_color_button.clicked.connect(self._choose_point_color)

        pt_h_layout = QVBoxLayout()
        pt_label = QLabel("Point Color")
        pt_h_layout.addWidget(pt_label, alignment=Qt.AlignmentFlag.AlignCenter)
        pt_h_layout.addWidget(self._point_color_button)
        layout.addRow(self._show_points_checkbox,pt_h_layout)

        self._add_separator(layout)

        self._show_lines_checkbox = QCheckBox("Plot Lines")
        self._show_lines_checkbox.setChecked(self._settings.plot_graph_line)

        self._line_color_button = QPushButton()
        self._update_color_button(self._line_color_button, self._line_color )
        self._line_color_button.clicked.connect(self._choose_line_color)

        layout.addRow(self._show_lines_checkbox)
        ln_h_layout = QVBoxLayout()
        ln_label = QLabel("Line Color")
        ln_h_layout.addWidget(ln_label, alignment=Qt.AlignmentFlag.AlignCenter)
        ln_h_layout.addWidget(self._line_color_button)

        layout.addRow(self._show_lines_checkbox , ln_h_layout)

        return tab


    def _make_line(self)->QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def _add_separator(self, layout: QFormLayout) -> None:
        line = self._make_line()
        layout.addRow(line)

    def _find_color_name(self, color: QColor)->str:
        # Lista com ~148 nomes de cores do Qt (em inglês)
        for name in QColor.colorNames():
            if QColor(name) == color:
                return name.upper()
        return color.name().upper()


    def _update_color_button(self, button: QPushButton, color: QColor) -> None:
        background = self._find_color_name(color)
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

    def _choose_background_color(self) -> None:
        color = QColorDialog.getColor(self._background_color, self, "Background color")
        if not color.isValid():
            return
        self._background_color = color
        self._update_color_button(self._background_color_button, color)

    def _choose_wiggle_color(self) -> None:
        color = QColorDialog.getColor(self._wiggle_color, self, "Wiggle color")
        if not color.isValid():
            return
        self._wiggle_color = color
        self._update_color_button(self._wiggle_color_button, color)

    def _choose_positive_fill_color(self)-> None:
        color = QColorDialog.getColor(self._positive_fill_color, self, "Positive Fill color")
        if not color.isValid():
            return
        self._positive_fill_color = color
        self._update_color_button(self._positive_fill_color_button, color)

    def _choose_negative_fill_color(self)-> None:
        color = QColorDialog.getColor(self._negative_fill_color, self, "Negative Fill color")
        if not color.isValid():
            return
        self._negative_fill_color = color
        self._update_color_button(self._negative_fill_color_button, color)

    def _choose_dead_trace_color(self)-> None:
        color = QColorDialog.getColor(self._dead_trace_color, self, "Dead Trace color")
        if not color.isValid():
            return
        self._dead_trace_color = color
        self._update_color_button(self._dead_trace_color_button, color)

    def _update_description(self) -> None:
        calculation = self._scale_calculation_combo.currentData()
        self._scale_calculation_description.setText(AMPLITUDE_SCALE_CALCULATIONS[calculation][1])

    # ==============================================================
    # OK / APPLY / CANCEL
    # ==============================================================
    def _validate(self) -> bool:
        if self._show_headers_checkbox.isChecked() and not self._selected_headers():
            QMessageBox.warning(self,  "Trace Headers", "Select at least one Trace Header to display.")
            return False

        if self._calc_scale_num_traces_spinbox.value() > self._trace_count_spinbox.value() :
            QMessageBox.warning( self,"Scale Calculation Error", "Calc. Scale Max. Traces cannot exceed Max Traces in Display.")
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
        settings.trace_excursion = self._trace_excursion_spinbox.value()
        settings.max_clip_excursion=self._max_clip_excursion_spinbox.value()
        settings.variable_area_bias=self._variable_area_bias_spinbox.value()

        # SeismicDataSamplesView - Draw colors
        settings.fill_negative_va= self._fill_negative_va_checkbox.isChecked()
        settings.background_color = QColor(self._background_color)
        settings.wiggle_color = QColor(self._wiggle_color)
        settings.positive_fill_color = QColor(self._positive_fill_color)
        settings.negative_fill_color = QColor(self._negative_fill_color)

        #Pre-Process
        settings.display_dead_traces = self._display_dead_traces_checkbox.isChecked()
        settings.dead_trace_rms_limit = self._dead_trace_rms_limit_spinbox.value()
        settings.dead_trace_wiggle_color = QColor(self._dead_trace_color)
        settings.reverse_data_polarity = self._reverse_data_polarity_checkbox.isChecked()
        settings.amplitude_scale_db = self._amplitude_scale_db_spinbox.value()

        #Scale
        settings.amplitude_scale_calculation = self._scale_calculation_combo.currentData()
        settings.calc_scale_num_traces = self._calc_scale_num_traces_spinbox.value()
        settings.mim_amp_value = None if self._min_amp_spinbox.value() == self._min_amp_spinbox.minimum() \
                                        else self._min_amp_spinbox.value()

        settings.max_amp_value = None if self._max_amp_spinbox.value() == self._max_amp_spinbox.minimum() \
                                        else self._max_amp_spinbox.value()

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

    def _change_tab_background(self, tab):
        tab.setAutoFillBackground(True)
        paleta = self.palette()
        paleta.setColor(QPalette.ColorRole.Window, QColor("#f3f3f3"))
        tab.setPalette(paleta)