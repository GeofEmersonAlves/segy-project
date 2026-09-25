from PySide6.QtGui import QPaintEvent, QPainter, QColor

from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget

class SeismicDataSamplesView(HSynchronizedSeismicDataWidget):
    def __init__(self, viewport: SeismicViewport, parent=None):
        super().__init__(viewport=viewport, parent=parent,)


    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.save()

        _color_background =  QColor(255, 255, 255)
        # Desenha um retantulo preenchido na area do widget
        self.draw_boxes_xy_axes_fill_color(painter, _color_background)

        painter.restore()