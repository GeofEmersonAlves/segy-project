# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : trace_header_view.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
         Classe que cria o TraceHeaderView filho de HSynchronizedSeismicDataWidget, responsável por mostrar os headers
    dos dados contitidos em um segy. Inicialmente os tracos aparecem somente com o Channel no cabeçalho

    Channel: trace_number_field_record (bytes 13-16)
Histórico:
       05/09/2026 - Início da criação do Widget
       09/09/2026 - Inicio da implementação do método paintEvent()
       21/09/2026 - Retomada do widget depois da decisao de criar o HSynchronizedSeismicDataWidget
       22/09/2026 - Finalização com todas as funcionalidades prontas
===============================================================================
"""
import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QPaintEvent, QPainter, Qt, QColor, QPen, QFont, QBrush
from numpy._typing import NDArray

from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget

class TraceHeaderView(HSynchronizedSeismicDataWidget):
    ROW_HEIGHT = 20
    headerMouseMoved = Signal(str)

    # Signal emitido quando o usuário clicar em um traco
    mouseTraceSelected = Signal(object)

    def __init__(self, viewport: SeismicViewport, parent=None):
        super().__init__(viewport=viewport,parent=parent)

        self._displayed_headers: dict[str, str] = {"FFID": "FIELD_RECORD_NO",
                                                   "TRC":"TRACE_SEQ_REEL",
                                                   "CHAN": "CHANNEL_NO"}

        self._trace_positions: NDArray[np.int64] = np.empty(0, dtype=np.int64)
        self._trace_indices: NDArray[np.int64] = np.empty(0, dtype=np.int64)
        self._header_values: dict[str, NDArray] = {}
        # Mapeia trace_position -> índice nos arrays carregados
        self._position_to_array_index: dict[int, int] = {}

        self._mouse_pos = None  # Posição do mouse para fazer o Mouse Tracker
        self._mouse_tracking_on = True  # Asssim pode ser configurável mostrar ou nao as linhas do tracking
        self.setMouseTracking(True)

        self._update_view_height()

    def set_data(self, trace_positions: NDArray[np.int64],
                       trace_indices: NDArray[np.int64],
                       header_values: dict[str, NDArray]) -> None:

        trace_positions = np.asarray(trace_positions, dtype=np.int64)
        trace_indices = np.asarray(trace_indices, dtype=np.int64)

        if trace_positions.ndim != 1:
            raise ValueError("trace_positions must be a 1D array.")

        if trace_indices.ndim != 1:
            raise ValueError("trace_indices must be a 1D array.")

        if trace_positions.size != trace_indices.size:
            raise ValueError("trace_positions and trace_indices must have the same size.")

        trace_count = trace_positions.size
        for header_key, values in header_values.items():
            values = np.asarray(values)
            if values.ndim != 1:
                raise ValueError(f"Header '{header_key}' values must be a 1D array.")

            if values.size != trace_count:
                raise ValueError(f"Header '{header_key}' has "
                                 f"{values.size} values, expected "
                                 f"{trace_count}."
                                 )

        self._trace_positions = trace_positions.copy()
        self._trace_indices = trace_indices.copy()

        self._header_values = {
                                key: np.asarray(values).copy()
                                for key, values in header_values.items()
                             }

        self._position_to_array_index = {int(trace_position): array_index
                                         for array_index, trace_position
                                         in enumerate(self._trace_positions)
                                        }
        # print(self._header_values)
        self.update()

    @property
    def displayed_headers(self) -> dict[str, str]:
        return self._displayed_headers.copy()

    @displayed_headers.setter
    def displayed_headers(self, headers: dict[str, str] ) -> None:
        self._displayed_headers = headers.copy()
        self._update_view_height()
        self.update()

    def mouseMoveEvent(self, event) -> None:
        mouse_pos = event.position()
        self._mouse_pos = mouse_pos.toPoint()
        trace_position = self.x_to_trace_position(mouse_pos.x())

        if trace_position is None:
            self._mouse_pos = None
            self.viewport.trace_under_mouse_position = None
            self.headerMouseMoved.emit("")
            return

        array_index = self._position_to_array_index.get(trace_position       )

        if array_index is None:
            self.headerMouseMoved.emit("")
            return

        header_texts: list[str] = []
        for label, header_key in self._displayed_headers.items():
            values = self._header_values.get(header_key)

            if values is None:
                continue

            value = values[array_index]
            header_texts.append(f"{label} {value}")

        array_index = self._position_to_array_index.get(trace_position)
        if array_index is None:
            return

        trace_index = int(self._trace_indices[array_index])  # Numero do traço dentro do arquivo
        texto_saida=" | ".join(header_texts)
        # print(texto_saida)
        self.viewport.trace_under_mouse_position = trace_index
        self.headerMouseMoved.emit(texto_saida)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return

        screen_point = event.position()  # Pega a posição que foi clicada na tela
        trace_position = self.x_to_trace_position(screen_point.x())  # Com a coordenada x converte para o numero do traço dentro do viewport

        if trace_position is None:
            return

        array_index = self._position_to_array_index.get(trace_position)
        if array_index is None:
            return

        trace_index = int(self._trace_indices[array_index])  # Numero do traço dentro do arquivo


        if self.viewport.selected_trace == trace_index:
            trace_index = None

        self.viewport.selected_trace = trace_index
        self.mouseTraceSelected.emit(self.viewport.selected_trace_number)

    def leaveEvent(self, event):
        # Limpa as linhas quando o mouse sai do widget
        self._mouse_pos = None
        self.viewport.trace_under_mouse_position = None
        self.headerMouseMoved.emit("")
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.save()

        white_color_background = QColor(255, 255, 255)
        # Desenha um retantulo preenchido na area do widget
        self.draw_boxes_xy_axes_fill_color(painter, white_color_background)
        self._draw_header_labels(painter) #Escreve do lado esquedo o label dos header exibidos
        painter.restore()

        painter.save()
        self._create_cartesian_coord_system(painter)
        self._draw_header_values(painter)
        self._draw_selected_trace_header_values(painter)

        painter.restore()

        if self.mouse_tracking_on:
            self._draw_trackin_lines(painter)

    def _draw_trackin_lines(self, painter):
        # Configura a caneta (cor vermelha, espessura 1, linha tracejada)
        pen = QPen(QColor("#ff4757"), 1, Qt.DashLine)
        painter.setPen(pen)
        if self._mouse_pos is not None:
           # Desenha a linha vertical (do topo até a base na largura X do mouse)
            painter.drawLine(self._mouse_pos.x(), 0, self._mouse_pos.x(), self.height())

        else:  #O mouse esta fora deste widget mas esta em outro apontando para um traco
            if self.viewport.trace_under_mouse_position is not None:
                # Desenha a linha vertical (do topo até a base na largura X do mouse)
                _mouse_pos_x = self.trace_to_x(self.viewport.trace_under_mouse_position)
                painter.drawLine(_mouse_pos_x, 0, _mouse_pos_x, self.height())

    def _update_view_height(self) -> None:
        header_count = len(self._displayed_headers)
        height = header_count * self.ROW_HEIGHT +1
        self.setFixedHeight(height)

    def _create_cartesian_coord_system(self, painter: QPainter) -> None:
        painter.translate(self.plot_left, 0.0)
        painter.scale(self.trace_spacing,  1.0)
        painter.translate(-self.viewport.first_trace_position, 0.0)


    def _draw_header_labels(self, painter: QPainter) -> None:
        if not self._displayed_headers:
            return
        painter.save()
        painter.resetTransform()

        font = QFont("Arial")
        font.setPixelSize(11)
        painter.setFont(font)

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidthF(1.0)
        painter.setPen(pen)

        label_width = self.left_margin
        for row, label in enumerate(self._displayed_headers):
            y = row * self.ROW_HEIGHT
            rect = QRectF(0.0, y, label_width, self.ROW_HEIGHT)
            # Nome do header
            painter.drawText(rect.adjusted(3.0, 0.0, -2.0, 0.0),  Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)

            # Linha horizontal superior da linha
            painter.drawLine(QPointF(0.0, y), QPointF(label_width, y))

        bottom = len(self._displayed_headers) * self.ROW_HEIGHT

        # Linha horizontal inferior
        painter.drawLine( QPointF(0.0, bottom), QPointF(label_width, bottom))

        painter.restore()

    def _draw_header_values(self, painter: QPainter) -> None:
        if not self._displayed_headers:
            return

        if not self._position_to_array_index:
            return

        font = QFont("Arial")
        font.setPixelSize(10)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        label_step = max(1, round(self.viewport.trace_count / 10))

        for row, (_, header_key) in enumerate(self._displayed_headers.items()):
            values = self._header_values.get(header_key)

            if values is None:
                continue

            # ---------------------------------------------------------
            # Geometria vertical da linha
            # ---------------------------------------------------------
            row_top = row * self.ROW_HEIGHT
            row_bottom = (row + 1) * self.ROW_HEIGHT

            # ---------------------------------------------------------
            # Linha horizontal inferior
            # Coordenadas de tela, portanto não deve sofrer a
            # transformação horizontal dos trace positions.
            # ---------------------------------------------------------
            painter.save()
            painter.resetTransform()
            painter.drawLine(QPointF(self.plot_left, row_bottom), QPointF(self.plot_width + self._left_margin, row_bottom))

            painter.restore()

            # ---------------------------------------------------------
            # Valores
            # ---------------------------------------------------------
            first_label = True

            for trace_position in self.visible_trace_range():
                if trace_position % label_step != 0:
                    continue

                array_index = self._position_to_array_index.get(trace_position)

                if array_index is None:
                    continue
                value = values[array_index]

                # -----------------------------------------------------
                # Converte trace position -> coordenada de tela
                # -----------------------------------------------------
                point = QPointF(float(trace_position),   0.0)
                screen_point = painter.transform().map(point)
                x = screen_point.x()

                if first_label: #Se for a primeira etiqueta e estiver muito a esquerda nao mostra
                    first_label = False
                    if 54 < x < 70:
                        continue

                painter.save()
                painter.resetTransform()

                # -----------------------------------------------------
                # Valor centralizado sobre a posição do traço
                # -----------------------------------------------------
                text_rect = QRectF(x - 50.0, row_top,   100.0, self.ROW_HEIGHT )

                painter.drawText(text_rect,  Qt.AlignmentFlag.AlignCenter,  str(value))

                # -----------------------------------------------------
                # Pequeno marcador vertical
                # -----------------------------------------------------
                tick_height = 4.0

                painter.drawLine(QPointF(x+2, row_bottom - tick_height),
                                 QPointF(x+2, row_bottom))

                painter.restore()

    def _draw_selected_trace_header_values(self, painter: QPainter) -> None:
        selected_trace_position = self.viewport.selected_trace
        if selected_trace_position is None:
            return

        array_index = self._position_to_array_index.get(selected_trace_position)

        if array_index is None:
            return

        # Posição X do traço selecionado no sistema cartesiano atual
        point = QPointF(float(selected_trace_position), 0.0)

        screen_point = painter.transform().map(point)
        x = screen_point.x()

        # Evita escrever sobre a área fixa dos labels
        if x <= self.plot_left:
            return

        painter.save()
        painter.resetTransform()

        font = QFont("Arial")
        font.setPixelSize(10)
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.GlobalColor.red)

        tick_height = 4.0

        for row, (_, header_key) in enumerate(self._displayed_headers.items()):
            values = self._header_values.get(header_key)

            if values is None:
                continue

            value = values[array_index]
            row_top = row * self.ROW_HEIGHT
            row_bottom = (row + 1) * self.ROW_HEIGHT

            # Valor centralizado na posição do traço selecionado
            text_rect =  QRectF(x - 50.0, row_top,     100.0,  self.ROW_HEIGHT )
            withe_rect = QRectF(x - 30.0, row_top + 2 , 60.0,  self.ROW_HEIGHT - 2  ) #o retangulo granco é um pouco menor

            #Desenha um retangulo branco transparente, o valor do header fica por cima
            painter.save()
            cor_branca_transparente = QColor(255, 255, 255, 204)  #aprox. 80% de transparencia
            painter.setBrush(QBrush(cor_branca_transparente))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(withe_rect)
            painter.restore()

            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter,  str(value))

            # Tick na mesma posição X
            painter.drawLine(QPointF( x+2, row_bottom - tick_height),
                             QPointF( x+2, row_bottom))

        painter.restore()