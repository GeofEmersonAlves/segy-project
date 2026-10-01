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
===============================================================================
"""
import math
import numpy as np
from numpy._typing import NDArray
from typing import NamedTuple
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen, QFont
from PySide6.QtCore import QLineF, QRectF, Qt, Signal
from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget
from segy_viewer.presentation.desktop.windows.data_window.seismic_data_window_config import SeismicDisplaySettings

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


    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.save()

        _color_background =  QColor(255, 255, 255)
        # Desenha um retantulo preenchido na area do widget
        self.draw_boxes_xy_axes_fill_color(painter, _color_background)

        #Calcula as marcas do eixo de tempo
        ticks = self._calculate_time_ticks()

        #Desenha o eixo Y do lado esquerdo
        self._draw_y_axis(painter, ticks)

        #Desenha a grade do lado direito, na area dos dados
        self._draw_time_grid(painter, ticks)

        if self._create_cartesian_coord_system(painter):
            pass
            # self._draw_samples(painter)

        painter.restore()

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

        trace_text = f"Trace: {trace_index+ 1} | Time: {_time:.2f} ms | Sample value: {sample_text}"

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

        self.update()


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

        major_pen = QPen(QColor(0, 0, 0))
        major_pen.setWidthF(2)

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
