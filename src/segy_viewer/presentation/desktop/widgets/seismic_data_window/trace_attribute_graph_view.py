# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_attribute_graph_view.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que cria o TraceAttributeGraphView filho de HSynchronizedSeismicDataWidget,
     este widget é responsável por representar, ao longo das posições dos traços visíveis,
     o valor de um atributo ou header na forma de um gráfico de linha.

Histórico:
       15/09/2026 - Início da criação do Widget
===============================================================================
"""
import numpy as np
import math

from PySide6.QtCore import QPointF, QRectF, Signal
from PySide6.QtGui import QPainter, QPaintEvent, Qt, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget
from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget


class TraceAttributeGraphView(HSynchronizedSeismicDataWidget):
    #signal emitido quando o mouse massa pelo grafico
    graphMouseMoved = Signal(str)

    def __init__(self,  viewport: SeismicViewport,   parent: QWidget | None = None):
        super().__init__(viewport=viewport, parent=parent)

        self._mouse_pos = None #Posição do mouse para fazer o Mouse Tracker
        self._mouse_tracking_on = True #Asssim pode ser configurável mostrar ou nao as linhas do tracking
        self.setMouseTracking(True)

        # self.viewport.trace_count=800  #Vai para a configuracao
        self._trace_positions: np.ndarray = np.empty(0, dtype=np.int64)
        self._trace_indices: np.ndarray = np.empty(0, dtype=np.int64)
        self._graph_header_values: dict[str, np.ndarray] = {}
        self._header_key:str = ""
        self._header_values : np.ndarray = np.empty(0, dtype=np.int64)
        self._position_to_array_index: dict[int, int] = {}

        self._y_axis_zero_fixed: bool = False  #Mantém o ínicio do eixo X fixo no zero, se Falso o inicio depende do _minimum_value
        self._y_tick_interval: float = 1.0

        self._minimum_value: float | None = None
        self._maximum_value: float | None = None

        self._top_margin: float = 5.0
        self._bottom_margin: float = 5.0

    def mouseMoveEvent(self, event):
        screen_point = event.position()
        self._mouse_pos = screen_point.toPoint()
        trace_position = self.x_to_trace_position(screen_point.x())

        if trace_position is None:
            return

        if self._header_key is None:
            return

        if self._header_values is None:
            return

        array_index = self._position_to_array_index.get(trace_position)
        if array_index is None:
            return

        if not 0 <= array_index < len(self._header_values):
            return

        header_value = float(self._header_values[array_index])

        inverse_transform, ok = self._transform.inverted()
        if not ok:
            return

        data_point = inverse_transform.map(screen_point)
        _value = data_point.y()
        mouse_text = f"Trace: {trace_position} {self._header_key}: {header_value:.2f} - Value: {_value:.2f}"
        #Atualiza o viewport com o traco atual sob o ponteiro do mouse
        self.viewport.trace_under_mouse_position = trace_position
        self.graphMouseMoved.emit(mouse_text)
        self.update()  # Dispara o paintEvent

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return

        screen_point = event.position()

        trace_position = self.x_to_trace_position(
            screen_point.x()
        )

        if trace_position is None:
            return

        array_index = self._position_to_array_index.get(
            trace_position
        )

        if array_index is None:
            return

        trace_index = int(
            self._trace_indices[array_index]
        )

        header_value = float(
            self._header_values[array_index]
        )

        print(
            f"Posição selecionada: {trace_position}, "
            f"índice no SEG-Y: {trace_index}, "
            f"{self._header_key}: {header_value:.2f}"
        )

    def leaveEvent(self, event):
        # Limpa as linhas quando o mouse sai do widget
        self.mouse_pos = None
        self.update()
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.save()

        white_color_background = QColor(255, 255, 255)

        #Desenha um retantulo ao lado esquero, area para plotagem do eixo Y e escreve o nome da variavel
        left_rect =QRectF(0.5, 0.5, self._left_margin-0.5, self.height()-1)
        painter.fillRect(left_rect, white_color_background)
        painter.drawRect(left_rect)
        self._draw_vertical_text_up(painter, self._left_margin/3,self.height()-5,self._header_key)

        #Desenha um retangulo do lado direito, área para plotagem dos dados
        right_rect = QRectF(self._left_margin, 0.5, self.plot_width+0.5, self.height()-1)
        painter.fillRect(right_rect, white_color_background)
        painter.drawRect(right_rect)

        #Escreve no canto inferior esquero da area de plotagem os valores mínimo e máximo dos dados
        font = QFont("Arial", 7, QFont.Weight.Bold) #Vai para a configuracao
        painter.setFont(font)
        texto = f"Min: {self._minimum_value:.2f} - Max: {self._maximum_value:.2f}"
        painter.drawText(right_rect, Qt.AlignRight | Qt.AlignBottom, texto)

        painter.restore()

        painter.save()
        # O clipping restringe os dados à área à direita do eixo Y.
        painter.setClipRect(QRectF(self.plot_left,
                                   self._top_margin,
                                   self.plot_width,
                                   self.height()  - self._top_margin - self._bottom_margin,
                                  )
                            )
        if self._create_cartesian_coord_system(painter):
            self._plot_header_values(painter=painter)

        painter.restore()

        self._draw_y_axis(painter)
        self._draw_y_grid(painter)
        if self._mouse_tracking_on:
            self._draw_trackin_lines(painter)


    def set_data(self, trace_positions: np.ndarray,
                       trace_indices: np.ndarray,
                       graph_header_values: dict[str, np.ndarray]) -> None:

        trace_positions = np.asarray(trace_positions, dtype=np.int64)
        trace_indices = np.asarray(trace_indices, dtype=np.int64)

        if trace_positions.ndim != 1:
            raise ValueError("trace_positions deve ser um array unidimensional.")

        if trace_indices.ndim != 1:
            raise ValueError("trace_indices deve ser um array unidimensional.")

        trace_count = trace_positions.size
        if trace_indices.size != trace_count:
            raise ValueError("trace_positions e trace_indices devem possuir "
                             "a mesma quantidade de elementos.")

        converted_header_values: dict[str, np.ndarray] = {}
        finite_arrays: list[np.ndarray] = []

        for header_key, values in graph_header_values.items():
            header_values = np.asarray(values, dtype=np.float64)

            if header_values.ndim != 1:
                raise ValueError(f"Os valores do header {header_key!r} "
                                  "devem formar um array unidimensional.")

            if header_values.size != trace_count:
                raise ValueError(f"O header {header_key!r} possui "
                                 f"{header_values.size} valores, mas foram recebidas "
                                 f"{trace_count} posições de traço.")

            header_values = header_values.copy()
            converted_header_values[header_key] = header_values
            finite_values = header_values[np.isfinite(header_values)]

            if finite_values.size > 0:
                finite_arrays.append(finite_values)

        self._trace_positions = trace_positions.copy()
        self._trace_indices = trace_indices.copy()
        self._graph_header_values = converted_header_values

        # Separa o header e os valores
        header_key, header_values = next(iter(self._graph_header_values.items()))
        self._header_key = header_key
        self._header_values = header_values
        self._position_to_array_index = {int(trace_position): array_index
                                            for array_index, trace_position in enumerate(
                                                self._trace_positions
                                            )
                                        }
        # print(self._graph_header_values)

        self._minimum_value = None
        self._maximum_value = None

        if finite_arrays:
            self._minimum_value = min(float(values.min())
                                        for values in finite_arrays
                                     )

            self._maximum_value = max(float(values.max())
                                      for values in finite_arrays
                                     )

        self.update()

    @staticmethod
    def _calculate_nice_interval(value: float) -> float:
        """
        Converte um intervalo qualquer em um intervalo adequado
        para as divisões do eixo.

        Exemplos aproximados:
            0.7  -> 0.5
            3.2  -> 5.0
            12.0 -> 10.0
            37.0 -> 50.0
        """
        if not math.isfinite(value) or value <= 0.0:
            return 1.0

        exponent = math.floor(math.log10(value))
        magnitude = 10.0 ** exponent
        normalized_value = value / magnitude

        if normalized_value < 1.5:
            nice_value = 1.0
        elif normalized_value < 3.0:
            nice_value = 2.0
        elif normalized_value < 7.0:
            nice_value = 5.0
        else:
            nice_value = 10.0

        return nice_value * magnitude

    def _calculate_y_axis_limits(self) -> tuple[float, float]:
        """
        Calcula os limites arredondados do eixo Y.

        Quando _y_axis_zero_fixed for True, o zero é mantido como
        primeira marca do eixo, com uma pequena margem gráfica abaixo.

        Caso contrário, o eixo começa em um valor arredondado
        imediatamente abaixo de _minimum_value.
        """
        if self._minimum_value is None:
            return 0.0, 1.0

        if self._maximum_value is None:
            return 0.0, 1.0

        minimum_value = float(self._minimum_value)
        maximum_value = float(self._maximum_value)

        if not math.isfinite(minimum_value):
            return 0.0, 1.0

        if not math.isfinite(maximum_value):
            return 0.0, 1.0

        if minimum_value > maximum_value:
            minimum_value, maximum_value = (maximum_value, minimum_value)

        if self._y_axis_zero_fixed:
            provisional_minimum = 0.0
        else:
            provisional_minimum = minimum_value

        data_range = maximum_value - provisional_minimum

        # Trata headers em que todos os traços possuem o mesmo valor.
        if data_range <= 0.0:
            reference_value = max(abs(minimum_value), abs(maximum_value), 1.0)

            data_range = reference_value * 0.1

        desired_interval_count = 5

        tick_interval = self._calculate_nice_interval(data_range / desired_interval_count)

        if self._y_axis_zero_fixed:
            # Mantém o zero ligeiramente acima da borda inferior.
            bottom_padding = tick_interval * 0.25
            y_axis_minimum = -bottom_padding

        else:
            y_axis_minimum = (math.floor(minimum_value / tick_interval) * tick_interval)

            # Evita que o menor valor fique exatamente sobre a borda.
            if math.isclose(minimum_value, y_axis_minimum, abs_tol=tick_interval * 0.01 ):
                y_axis_minimum -= tick_interval * 0.25

        y_axis_maximum = (math.ceil(maximum_value / tick_interval) * tick_interval)

        # Garante uma faixa vertical válida.
        if y_axis_maximum <= y_axis_minimum:
            y_axis_maximum = (y_axis_minimum + tick_interval)

        self._y_tick_interval = tick_interval

        return (float(y_axis_minimum), float(y_axis_maximum))

    def _create_cartesian_coord_system(self, painter: QPainter) -> bool:
        """
        Configura o QPainter para trabalhar com:
            X = posição global de visualização do traço
            Y = valor do hea
        Retorna False quando não for possível criar a transformação.
        """
        if self.trace_count <= 0:
            return False

        if self.x_scale <= 0.0:
            return False

        if self._minimum_value is None:
            return False

        if self._maximum_value is None:
            return False

        plot_top = self._top_margin
        plot_bottom = self.height() - self._bottom_margin

        plot_height = max(0.0, plot_bottom - plot_top)

        if plot_height <= 0.0:
            return False

        y_axis_minimum, y_axis_maximum = (self._calculate_y_axis_limits())

        y_range = y_axis_maximum - y_axis_minimum

        if y_range <= 0.0:
            return False

        y_scale = plot_height / y_range

        # Faz a posição global first_trace_position aparecer no centro
        # do primeiro espaço horizontal reservado aos traços.
        x_origin = (  self.plot_left
                    + self.x_scale / 2.0
                    - self.first_trace_position * self.x_scale
                   )

        # Faz y_axis_minimum aparecer sobre a linha inferior do gráfico.
        y_origin = ( plot_bottom + y_axis_minimum * y_scale)

        painter.translate(x_origin,  y_origin)
        painter.scale(self.x_scale, -y_scale)

        self._transform = painter.transform()
        self._y_axis_minimum = y_axis_minimum
        self._y_axis_maximum = y_axis_maximum
        self._y_scale = y_scale

        return True

    def _draw_vertical_text_up(self, painter, x, y, text):
        """Desenha o texto verticalmente de baixo para cima."""
        painter.save()
        font = QFont("Arial", 7, QFont.Weight.Bold)
        painter.setFont(font)
        painter.translate(x, y)
        painter.rotate(-90)  # Rotaciona 90 graus no sentido anti-horário
        painter.drawText(0, 0, text)
        painter.restore()


    def _draw_y_axis(self, painter: QPainter) -> None:
        if self._minimum_value is None:
            return

        if self._maximum_value is None:
            return

        if self._y_tick_interval <= 0.0:
            return

        if self._y_scale <= 0.0:
            return

        plot_top = self._top_margin
        plot_bottom = self.height() - self._bottom_margin
        plot_height = plot_bottom - plot_top

        if plot_height <= 0.0:
            return

        axis_x = self.plot_left
        painter.save()

        # --------------------------------------------------------------
        # Linha principal do eixo Y
        # --------------------------------------------------------------
        axis_pen = QPen(QColor("#202020"))
        axis_pen.setWidthF(1.0)
        axis_pen.setCosmetic(True)
        painter.setPen(axis_pen)

        painter.drawLine(QPointF(axis_x, plot_top), QPointF(axis_x, plot_bottom))

        # --------------------------------------------------------------
        # Fonte dos valores
        # --------------------------------------------------------------
        font = QFont("Arial", 8)
        painter.setFont(font)

        font_metrics = painter.fontMetrics()
        text_height = float(font_metrics.height())

        # Reserva o lado mais à esquerda para o título vertical.
        label_left = 16.0
        label_right = axis_x - 5.0
        label_width = max(0.0, label_right - label_left)

        # --------------------------------------------------------------
        # Primeiro valor divisível pelo intervalo
        # --------------------------------------------------------------
        first_tick = (
                math.ceil(
                    self._y_axis_minimum
                    / self._y_tick_interval
                )
                * self._y_tick_interval
        )

        tick_count = int(
            math.floor(
                (
                        self._y_axis_maximum
                        - first_tick
                )
                / self._y_tick_interval
            )
        ) + 1

        if tick_count <= 0:
            painter.restore()
            return

        # Limita a quantidade de textos para evitar sobreposição.
        maximum_label_count = max(2, int(plot_height / 22.0) + 1)

        label_stride = max(1,
                            math.ceil(
                                (tick_count - 1)
                                / max(1, maximum_label_count - 1)
                            ),
                        )

        # Número de casas decimais apropriado ao intervalo.
        if self._y_tick_interval >= 1.0:
            decimal_places = 0
        else:
            decimal_places = max(0,
                                int(
                                    math.ceil(
                                        -math.log10(self._y_tick_interval)
                                    )
                                ),
                            )

        # --------------------------------------------------------------
        # Marcas e valores
        # --------------------------------------------------------------
        for tick_index in range(tick_count):
            tick_value = (
                    first_tick
                    + tick_index * self._y_tick_interval
            )

            screen_y = (
                    plot_bottom
                    - (
                            tick_value
                            - self._y_axis_minimum
                    )
                    * self._y_scale
            )

            if screen_y < plot_top - 0.5:
                continue

            if screen_y > plot_bottom + 0.5:
                continue

            is_labeled_tick = (
                    tick_index % label_stride == 0
                    or tick_index == tick_count - 1
            )

            tick_length = 5.0 if is_labeled_tick else 3.0

            painter.drawLine(
                QPointF(
                    axis_x - tick_length,
                    screen_y,
                ),
                QPointF(
                    axis_x,
                    screen_y,
                ),
            )

            if not is_labeled_tick:
                continue

            if math.isclose(
                    tick_value,
                    0.0,
                    abs_tol=1e-12,
            ):
                tick_value = 0.0

            label = (
                f"{tick_value:.{decimal_places}f}"
            )

            text_rect = QRectF(
                label_left,
                screen_y - text_height / 2.0,
                label_width,
                text_height,
            )

            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter,
                label,
            )

        painter.restore()

    def _draw_y_grid(self, painter: QPainter) -> None:
        """
        Desenha as linhas horizontais da grade do eixo Y dentro
        da área útil de plotagem.
        """
        if self._y_tick_interval <= 0.0:
            return

        if self._y_scale <= 0.0:
            return

        plot_top = self._top_margin
        plot_bottom = self.height() - self._bottom_margin

        if plot_bottom <= plot_top:
            return

        first_tick = (
                math.ceil(
                    self._y_axis_minimum
                    / self._y_tick_interval
                )
                * self._y_tick_interval
        )

        grid_pen = QPen(QColor("#707070"))
        grid_pen.setWidthF(0.8)
        grid_pen.setStyle(Qt.PenStyle.DashLine)
        grid_pen.setCosmetic(True)

        painter.save()
        painter.setPen(grid_pen)

        tick_value = first_tick
        tolerance = self._y_tick_interval * 1e-9

        while tick_value <= self._y_axis_maximum + tolerance:
            screen_y = (
                    plot_bottom
                    - (
                            tick_value
                            - self._y_axis_minimum
                    )
                    * self._y_scale
            )

            if plot_top - 0.5 <= screen_y <= plot_bottom + 0.5:
                painter.drawLine(
                    QPointF(self.plot_left, screen_y),
                    QPointF(self.plot_right, screen_y),
                )

            tick_value += self._y_tick_interval

        painter.restore()

    def _plot_header_values(self, painter : QPainter):
        point_pen = QPen(Qt.GlobalColor.darkRed) #Vai para a configuracao
        point_pen.setWidthF(4.0)
        point_pen.setCosmetic(True)
        point_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(point_pen)
        points = []
        for trace_position, header_value in zip(self._trace_positions, self._header_values):
            if not np.isfinite(header_value):
                continue
            point = QPointF(float(trace_position), float(header_value))
            painter.drawPoint(point) #Vai para a configuracao
            points.append(point)

        line_pen = QPen(Qt.GlobalColor.darkBlue) #Vai para a configuracao
        line_pen.setWidthF(1.0)
        line_pen.setStyle(Qt.PenStyle.SolidLine)
        line_pen.setCosmetic(True)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(line_pen)
        painter.drawPolyline(points) #Vai para a configuracao

    def _draw_trackin_lines(self, painter):
        if self._mouse_pos is not None:
            # Configura a caneta (cor vermelha, espessura 1, linha tracejada)
            pen = QPen(QColor("#ff4757"), 1, Qt.DashLine)
            painter.setPen(pen)

            # Desenha a linha horizontal (da esquerda até a direita na altura Y do mouse)
            painter.drawLine(0, self._mouse_pos.y(), self.width(), self._mouse_pos.y())

            # Desenha a linha vertical (do topo até a base na largura X do mouse)
            painter.drawLine(self._mouse_pos.x(), 0, self._mouse_pos.x(), self.height())
