# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_samples_view.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Componente responsável pelo desenho do traco sismico

Histórico:
       27/09/2026 - Início da criação do Widget
       28/09/2026 - Criação dos metodos para desenhar o eixo Y e a grade da area dos dados.
       30/09/2026 - Criação do sistema de coordenadas dos tracos, criacao do metodo mouseMoveEvent
       01/10/2026 - Inclusão no set_data do calculo do RMS do traço e da lista de traços mortos
                 traço morto -> rms <= _dead_trace_rms_limit
       02/10/2026 - Finalização do _draw_trace
       03/10/2026 - Alterações para melhorar a performance apos o desenho das amostras
===============================================================================
"""
import math
import numpy as np
from numpy._typing import NDArray
from typing import NamedTuple
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen, QFont, QPainterPath, QPixmap
from PySide6.QtCore import QLineF, QRectF, Qt, Signal
from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget
from segy_viewer.presentation.desktop.windows.data_window.seismic_data_window_config import (SeismicDisplaySettings,
                                                                                             TRACEDRAWINGMODES,
                                                                                             AmplitudeScaleCalculation)

class TimeTick(NamedTuple):
    time_ms: float
    y: float
    is_major: bool

class SeismicDataSamplesView(HSynchronizedSeismicDataWidget):
    samplesMouseMoved = Signal(str)

    # Signal emitido quando o usuário clicar em um traco
    mouseTraceSelected = Signal(object)

    def __init__(self, viewport: SeismicViewport, display_settings: SeismicDisplaySettings, parent=None):
        super().__init__(viewport=viewport, display_settings=display_settings, parent=parent)

        # Posição do mouse para fazer o Mouse Tracker
        self._data_samples = None
        self._mouse_pos = None
        self.setMouseTracking(True)

        self._samples: NDArray[np.float32] | None = None
        self._sample_interval_us : int = 0
        self._record_length_ms: float = 0
        self._samples_count: int = 0

        # Mapeia trace_position -> índice nos arrays carregados
        self._position_to_array_index: dict[int, int] = {}

        self._trace_rms: NDArray[np.float64] = np.empty(0, dtype=np.float64)  #Valor do RMS de cada traço na tela
        self._dead_traces: NDArray[np.bool_] = np.empty(0, dtype=np.bool_) #Mapeia os traços mortos

        #Cache de imagem para melhorar a performance
        self._plot_cache: QPixmap | None = None
        self._plot_cache_key = None


    def paintEvent(self, event:QPaintEvent) -> None:
        dpr = self.devicePixelRatioF()
        cache_key = (self.width(),
                    self.height(),
                    dpr,
                    self.viewport.first_trace_position,
                    self.viewport.trace_count,
                    self.viewport.selected_trace,
                    self._display_settings.show_time_grid)

        if self._plot_cache is None or cache_key != self._plot_cache_key:
            pixmap = QPixmap(round(self.width() * dpr), round(self.height() * dpr))
            pixmap.setDevicePixelRatio(dpr)
            pixmap.fill(Qt.GlobalColor.transparent)
            cache_painter = QPainter(pixmap)

            try:
                self._draw_static_plot(cache_painter)
            finally:
                cache_painter.end()

            self._plot_cache = pixmap
            self._plot_cache_key = cache_key

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._plot_cache)

        if self.display_settings.mouse_tracking_on:
            self._draw_trackin_lines(painter)

    def mouseMoveEvent(self, event):
        mouse_pos = event.position().toPoint()
        self._mouse_pos = mouse_pos
        trace_position = self.x_to_trace_position(mouse_pos.x())

        if trace_position is None:
            self._mouse_pos = None
            self.viewport.trace_under_mouse_position = None
            self.samplesMouseMoved.emit("")
            return

        array_index = self._position_to_array_index.get(trace_position)

        if array_index is None or self._data_samples is None:
            self.samplesMouseMoved.emit("")
            return

        samples = self._data_samples[:, array_index]
        trace_index = int(self._trace_indices[array_index])  # Numero do traço dentro do arquivo
        trace_rms = float(self._trace_rms[array_index])

        inverse_transform, ok = self._transform.inverted()
        if not ok:
            return

        data_point = inverse_transform.map(mouse_pos)
        _time = data_point.y()
        sample_value= None

        if 0 <= _time < self._record_length_ms and len(samples) > 0:
            sample_interval_ms = self._sample_interval_us / 1000.0
            sample_index = round(_time / sample_interval_ms)

            # O limite do eixo pode estar uma amostra depois da última amostra real.
            sample_index = min(sample_index, len(samples) - 1)
            sample_value = float(samples[sample_index])

        if sample_value is None:
            sample_text = "—"
        else:
            sample_text = f"{sample_value:.8g}"

        trace_text = f"Trace: {trace_index+ 1} - RMS: {trace_rms:.8g} | Time: {_time:.2f} ms | Sample value: {sample_text}"

        self.viewport.trace_under_mouse_position = trace_index
        self.samplesMouseMoved.emit(trace_text)

    def leaveEvent(self, event):
        # Limpa as linhas quando o mouse sai do widget
        self._mouse_pos = None
        self.viewport.trace_under_mouse_position = None
        self.samplesMouseMoved.emit("")
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return

        screen_point = event.position()  #Pega a posição que foi clicada na tela
        trace_position = self.x_to_trace_position(screen_point.x()) #Com a coordenada x converte para o numero do traço dentro do viewport

        if trace_position is None:
            return

        array_index = self._position_to_array_index.get(trace_position)
        if array_index is None:
            return

        trace_index = int(self._trace_indices[array_index])  #Numero do traço dentro do arquivo
        if self.viewport.selected_trace == trace_index:
            trace_index = None

        self.viewport.selected_trace = trace_index
        self.mouseTraceSelected.emit(self.viewport.selected_trace_number)

    def set_data(self, trace_positions: NDArray[np.int64],
                 trace_indices: NDArray[np.int64],
                 samples: NDArray[np.float32],
                 sample_interval_us: int) -> None:

        trace_positions = np.asarray(trace_positions, dtype=np.int64)
        trace_indices = np.asarray(trace_indices, dtype=np.int64)
        sample_data:NDArray = np.asarray(samples)

        if trace_positions.ndim != 1 or trace_positions.ndim != 1:
            raise ValueError("The positions and indices of the traces must be vectors.")

        if sample_data.ndim != 2:
            raise ValueError("The samples must form a 2D matrix.")

        #sample_data.shape = (n_amostras, n_tracos)
        if not (len(trace_positions) == len(trace_positions) == sample_data.shape[1]):
            raise ValueError("Each trace position and index must correspond to a column of the sample matrix.")

        if sample_interval_us <= 0:
            raise ValueError("Sample interval must be greater than zero.")

        self._trace_positions = trace_positions.copy()
        self._trace_indices = trace_indices.copy()
        self._data_samples = sample_data.copy()

        self._position_to_array_index = {int(trace_position): array_index
                                         for array_index, trace_position in enumerate(self._trace_positions)}

        self._samples_count = len(self._data_samples)
        self._sample_interval_us = sample_interval_us
        self._record_length_ms =  (self._samples_count * self._sample_interval_us / 1000)


        #Detecção dos traços mortos pelo RMS do traço
        self._trace_rms = np.sqrt(np.mean(self._data_samples.astype(np.float64) ** 2, axis=0))  #Cálculo do RMS do dos traços
        self._dead_traces = (self._trace_rms <= self.display_settings.dead_trace_rms_limit)  #Compara o RMS com o limite estabelecido, resultado uma matriz com Trues se for morto e False se for vivo
        self._calculate_amplitude_scale() #Calcula os valores da aba Scale para a escala do desenho do traço

        self._plot_cache = None


    def recalculate_amplitude_scale(self, force: bool = False) -> None:
        self._calculate_amplitude_scale(force=force)

    def invalidate_plot(self) -> None:
        self._plot_cache = None
        self.update()

    def _draw_static_plot(self, painter: QPainter) -> None:
        self.draw_box_data_area_fill_color(painter, self.display_settings.background_color)

        # Desenha um retangulo branco na area do eixo y
        white_color_background = QColor(255, 255, 255)
        self.draw_box_y_axis_area_fill_color(painter, white_color_background)

        # Calcula as marcas do eixo de tempo
        ticks = self._calculate_time_ticks()

        # Desenha o eixo Y do lado esquerdo
        self._draw_y_axis(painter, ticks)

        # Desenha a grade do lado direito, na area dos dados
        if self.display_settings.show_time_grid:
            self._draw_time_grid(painter, ticks)

        painter.save()
        try:
            if self._create_cartesian_coord_system(painter):
                self._draw_samples(painter)
        finally:
            painter.restore()


    def _calculate_time_ticks(self) -> list[TimeTick]:
        """Calcula as marcas do eixo de tempo nas coordenadas do widget."""

        duration_ms = self._record_length_ms

        if (not math.isfinite(duration_ms)
            or duration_ms <= 0
            or self.right_rect.height() <= 0):

            return []

        target_step = duration_ms / 6   #9 da um resultado interessante
        # magnitude = 10 ** math.floor(math.log10(target_step))

        candidates = [
            factor * (10 ** exponent)
            for exponent in (
                math.floor(math.log10(target_step)) - 1,
                math.floor(math.log10(target_step)),
                math.floor(math.log10(target_step)) + 1,
            )
            for factor in (1, 2, 5)
        ]

        major_step = min(candidates,   key=lambda step: abs(duration_ms / step - 6))
        minor_step = major_step / 5

        top = self.right_rect.top()
        height = self.right_rect.height()
        ticks: list[TimeTick] = []

        minor_count = math.floor(duration_ms / minor_step)

        for index in range(minor_count + 1):
            time_ms = index * minor_step

            if time_ms > duration_ms:
                break

            y = top + (time_ms / duration_ms) * height

            ticks.append(TimeTick(time_ms=time_ms,  y=y,  is_major=(index % 5 == 0)))

        # Inclui o limite real quando ele não coincide com uma marca,
        # evitando dois rótulos quase sobrepostos no fim do eixo.
        last_major_time = (
                math.floor(duration_ms / major_step) * major_step
        )

        if (
                not ticks
                or (
                not math.isclose(ticks[-1].time_ms, duration_ms, abs_tol=1e-9)
                and duration_ms - last_major_time >= minor_step / 2)):
            ticks.append(TimeTick(time_ms=duration_ms, y=self.right_rect.bottom(),is_major=True))

        return ticks


    def _draw_y_axis(self, painter: QPainter, ticks: list[TimeTick]) -> None:
        """Desenha as marcas e os rótulos do eixo de tempo."""

        if not ticks:
            return

        painter.save()
        font = QFont("Arial", 8)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))

        axis_x = self.right_rect.left()
        label_height = painter.fontMetrics().height() + 2

        # Reserva a parte esquerda para o título vertical.
        label_left = self.left_rect.left() + 10
        label_right = axis_x - 9
        label_width = label_right - label_left

        for tick in ticks:
            tick_length = 7 if tick.is_major else 3

            painter.drawLine(QLineF(axis_x - tick_length, tick.y, axis_x, tick.y))

            if not tick.is_major or label_width <= 0:
                continue

            # Mantém os rótulos extremos dentro da faixa do eixo.
            label_top = max(self.left_rect.top(), min(tick.y - label_height / 2,  self.left_rect.bottom() - label_height))

            painter.drawText(QRectF(label_left, label_top, label_width, label_height),
                             Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                            f"{tick.time_ms:.0f}"
                            )

        # Título centralizado e girado, sem alterar o painter externo.
        painter.save()

        painter.translate(self.left_rect.left() + 10, self.right_rect.center().y() )
        painter.rotate(-90)
        font = QFont("Arial", 9)
        painter.setFont(font)

        painter.drawText(QRectF(-self.right_rect.height() / 2, -label_height / 2, self.right_rect.height(), label_height),
                        Qt.AlignmentFlag.AlignCenter,  "Time (ms)")

        painter.restore()
        painter.restore()

    def _draw_time_grid(self, painter: QPainter, ticks: list[TimeTick] ) -> None:
        """Desenha a grade horizontal na área dos traços."""

        if not ticks or self.right_rect.isEmpty():
            return

        painter.save()
        painter.setClipRect(self.right_rect)

        minor_pen = QPen(QColor(0, 0, 0))
        minor_pen.setWidthF(1)
        minor_pen.setColor(self.display_settings.time_grid_color)

        major_pen = QPen(QColor(0, 0, 0))
        major_pen.setWidthF(2)
        major_pen.setColor(self.display_settings.time_grid_color)

        x_start = self.right_rect.left()
        x_end = self.right_rect.right()

        for tick in ticks:
            painter.setPen(major_pen if tick.is_major else minor_pen)
            painter.drawLine(QLineF(x_start, tick.y, x_end, tick.y))

        painter.restore()

    def _create_cartesian_coord_system(self, painter: QPainter) -> bool:
        """Configura Y em milissegundos, com tempo crescente para baixo."""

        duration_ms = self._record_length_ms

        if (not math.isfinite(duration_ms)
                or duration_ms <= 0
                or self.right_rect.isEmpty()):
            return False

        # Definido antes da transformação: limita o desenho à área dos traços.
        painter.setClipRect(self.right_rect)

        # y = 0 ms fica no topo da área; x permanece em pixels do widget.
        painter.translate(0, self.right_rect.top())
        painter.scale(1.0, self.right_rect.height() / duration_ms)

        self._transform = painter.transform()

        return True

    def _draw_trackin_lines(self, painter):
        # Configura a caneta (cor vermelha, espessura 1, linha tracejada)
        pen = QPen(QColor("#ff4757"), 1, Qt.DashLine)
        painter.setPen(pen)

        if self._mouse_pos is not None:
            # Desenha a linha horizontal (da esquerda até a direita na altura Y do mouse)

            painter.drawLine(self._left_margin - 5, self._mouse_pos.y(), self.plot_width + self._left_margin, self._mouse_pos.y())

            # Desenha a linha vertical (do topo até a base na largura X do mouse)
            painter.drawLine(self._mouse_pos.x(), 0, self._mouse_pos.x(), self.height())

        else:
            if self.viewport.trace_under_mouse_position is not None:
                # Desenha a linha vertical (do topo até a base na largura X do mouse)
                _mouse_pos_x = self.trace_to_x(self.viewport.trace_under_mouse_position)
                painter.drawLine(_mouse_pos_x, 0, _mouse_pos_x, self.height())


    def _draw_samples(self, painter: QPainter) -> None:
        if self._data_samples is None or self._data_samples.size == 0:
            return

        settings = self.display_settings
        mode = settings.trace_drawing_mode

        draw_density = mode in (TRACEDRAWINGMODES.VARIABLE_DENSITY.name, TRACEDRAWINGMODES.WIGGLE_VARIABLE_DENSITY.name)
        draw_area = mode in (TRACEDRAWINGMODES.VARIABLE_AREA.name, TRACEDRAWINGMODES.WIGGLE_VARIABLE_AREA.name)
        draw_wiggle = mode in (TRACEDRAWINGMODES.WIGGLE.name, TRACEDRAWINGMODES.WIGGLE_VARIABLE_AREA.name, TRACEDRAWINGMODES.WIGGLE_VARIABLE_DENSITY.name)

        # A imagem de densidade será desenhada primeiro.
        if draw_density:
            # self._draw_variable_density(painter)
            pass

        if not (draw_area or draw_wiggle):
            return

        amplitude_factor = 10.0 ** (settings.amplitude_scale_db / 20.0) #Cálculo do fator de amplitude, ver documentacao
        if settings.reverse_data_polarity:
            amplitude_factor = -amplitude_factor

        first_position = self.viewport.first_trace_position
        last_position = first_position + self.viewport.trace_count

        for trace_position in range(first_position, last_position):
            array_index = self._position_to_array_index.get(trace_position)
            if array_index is None:
                continue

            is_dead = self._dead_traces[array_index]

            if is_dead and not settings.display_dead_traces:
                continue

            samples = self._data_samples[:, array_index]

            if amplitude_factor != 1.0:
                samples = samples * amplitude_factor

            self._draw_trace(painter,  trace_position, samples, is_dead=is_dead,
                                                                draw_area=draw_area,
                                                                draw_wiggle=draw_wiggle)


    def _calculate_amplitude_scale(self, force: bool = False) -> bool:
        settings = self._display_settings
        if (not force
                and settings.mim_amp_value is not None
                and settings.max_amp_value is not None):
            return False

        if self._data_samples is None or self._data_samples.size == 0:
            return False

        # Colunas da matriz = traços do datablock.
        # Percorre os traços na ordem e usa até o máximo configurado de válidos.
        valid_traces = (~self._dead_traces & np.all(np.isfinite(self._data_samples), axis=0))

        qtde_traces_to_calculate = settings.calc_scale_num_traces
        #Se a quantidade para calculo for maior que a quanditade de tracos carregados, uso 20% dos carregados
        if qtde_traces_to_calculate > settings.number_traces_to_show:
            qtde_traces_to_calculate = settings.number_traces_to_show * 0.20

        indices = np.flatnonzero(valid_traces)[:qtde_traces_to_calculate]

        if indices.size == 0:
            return False

        samples = np.asarray( self._data_samples[:, indices], dtype=np.float64)

        match settings.amplitude_scale_calculation:
            case AmplitudeScaleCalculation.MEAN_ABSOLUTE_AMPLITUDE:
                reference = 3.5 * float(np.mean(np.abs(samples), dtype=np.float64))

            case AmplitudeScaleCalculation.MEAN_TRACE_PEAK:
                peaks = np.max(np.abs(samples), axis=0)
                reference = float(np.mean(peaks, dtype=np.float64))
            case _:
                raise ValueError("Unsupported amplitude scale calculation method.")

        if not np.isfinite(reference) or reference <= 0:
            return False

        if force or settings.mim_amp_value is None:
            settings.mim_amp_value = -reference

        if force or settings.max_amp_value is None:
            settings.max_amp_value = reference

        settings.calculated_scale_trace_count = int(indices.size)
        return True

    def _draw_trace(self, painter, trace_position, samples, is_dead, draw_area, draw_wiggle):
        painter.save()
        try:
            plot_samples = self._configure_trace_coordinates(painter, trace_position, samples)
            if plot_samples is None:
                return

            if is_dead:
                self._draw_wiggle(painter, plot_samples, color=self.display_settings.dead_trace_wiggle_color, trace_width = 1.0)
                return

            if draw_area:
                self._draw_variable_area(painter, plot_samples)

            if draw_wiggle:
                if trace_position == self.viewport.selected_trace:
                    _trace_color = self.display_settings.selected_trace_wiggle_color
                    _trace_width = 2.0
                else:
                    _trace_color = self.display_settings.wiggle_color
                    _trace_width = 1.0

                self._draw_wiggle(painter, plot_samples, color = _trace_color, trace_width = _trace_width)

        finally:
            painter.restore()

    def _configure_trace_coordinates(self, painter: QPainter, trace_position: 
                                           int, samples: NDArray[np.float32]) -> NDArray[np.float64] | None:
        settings = self._display_settings

        min_amp = settings.mim_amp_value
        max_amp = settings.max_amp_value

        if (
                min_amp is None
                or max_amp is None
                or not np.isfinite(min_amp)
                or not np.isfinite(max_amp)
                or min_amp >= 0
                or max_amp <= 0
                or settings.trace_excursion <= 0
                or settings.max_clip_excursion <= 0
                or self.viewport.trace_count <= 0
                or self.right_rect.isEmpty()
        ):
            return None

        # Uma unidade horizontal passa a representar a excursão configurada,
        # medida em espaços entre os centros de traços vizinhos.
        trace_spacing = self.right_rect.width() / self.viewport.trace_count
        amplitude_width = trace_spacing * settings.trace_excursion

        # Cada lado usa seu próprio limite de referência. Isso também permite
        # que o usuário informe limites de amplitudes assimétricos.
        values = np.asarray(samples, dtype=np.float64)
        normalized = np.empty_like(values)

        positive = values >= 0
        normalized[positive] = values[positive] / max_amp
        normalized[~positive] = values[~positive] / abs(min_amp)

        # A configuração de clip é expressa em espaços entre traços.
        # Converte esse limite para as unidades horizontais locais.
        clip_limit = settings.max_clip_excursion / settings.trace_excursion
        plot_samples = np.clip(normalized, -clip_limit, clip_limit)

        painter.translate(self.trace_to_x(trace_position), 0)
        painter.scale(amplitude_width, 1.0)

        return plot_samples

    def _draw_wiggle(self, painter: QPainter, plot_samples: NDArray[np.float64], color: QColor, trace_width:float) -> None:
        if plot_samples.size == 0 or self._sample_interval_us <= 0:
            return

        sample_interval_ms = self._sample_interval_us / 1000.0
        path = QPainterPath()
        segment_started = False

        for index, amplitude in enumerate(plot_samples):
            if not np.isfinite(amplitude):
                segment_started = False
                continue

            x = float(amplitude)
            y = index * sample_interval_ms

            if segment_started:
                path.lineTo(x, y)
            else:
                path.moveTo(x, y)
                segment_started = True

        pen = QPen(QColor(color))
        pen.setWidthF(trace_width)
        pen.setCosmetic(True)  # Mantém 1 pixel apesar da escala X e Y do painter.

        painter.save()
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.drawPath(path)
        painter.restore()

    def _draw_variable_area(self, painter: QPainter, plot_samples: NDArray[np.float64]) -> None:
        if plot_samples.size == 0 or self._sample_interval_us <= 0:
            return

        settings = self.display_settings
        bias = max(0.0, min(100.0, float(settings.variable_area_bias)))

        if bias == 0.0:
            return

        # As amplitudes já estão normalizadas por _configure_trace_coordinates().
        # 100%: referência no centro (x = 0).
        # Valores menores: preenche apenas a parte mais externa dos picos.
        threshold = 1.0 - bias / 100.0
        sample_interval_ms = self._sample_interval_us / 1000.0
        finite = np.isfinite(plot_samples)

        def draw_side(baseline: float, positive: bool, color: QColor) -> None:
            active = finite & (
                (plot_samples > baseline) if positive
                else (plot_samples < baseline)
            )

            if not np.any(active):
                return

            # Encontra o início e o fim de cada trecho contínuo a preencher.
            changes = np.diff(
                np.concatenate(([False], active, [False])).astype(np.int8)
            )
            starts = np.flatnonzero(changes == 1)
            ends = np.flatnonzero(changes == -1) - 1

            path = QPainterPath()

            for start, end in zip(starts, ends):
                start_y = start * sample_interval_ms

                # Interpola onde o traço cruzou a linha de referência.
                if start > 0 and finite[start - 1]:
                    previous = float(plot_samples[start - 1])
                    current = float(plot_samples[start])
                    fraction = (baseline - previous) / (current - previous)
                    start_y = (start - 1 + fraction) * sample_interval_ms

                path.moveTo(baseline, start_y)

                for index in range(start, end + 1):
                    path.lineTo(
                        float(plot_samples[index]),
                        index * sample_interval_ms,
                    )

                end_y = end * sample_interval_ms

                if end + 1 < plot_samples.size and finite[end + 1]:
                    current = float(plot_samples[end])
                    following = float(plot_samples[end + 1])
                    fraction = (baseline - current) / (following - current)
                    end_y = (end + fraction) * sample_interval_ms

                path.lineTo(baseline, end_y)
                path.closeSubpath()

            painter.setBrush(QColor(color))
            painter.drawPath(path)

        painter.save()
        try:
            painter.setPen(Qt.PenStyle.NoPen)

            draw_side(
                baseline=threshold,
                positive=True,
                color=settings.positive_fill_color,
            )

            if settings.fill_negative_va:
                draw_side(
                    baseline=-threshold,
                    positive=False,
                    color=settings.negative_fill_color,
                )
        finally:
            painter.restore()