from PySide6.QtGui import QPaintEvent, QPainter, QColor

from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget
from segy_viewer.presentation.desktop.windows.data_window.seismic_data_window_config import SeismicDisplaySettings


class SeismicDataSamplesView(HSynchronizedSeismicDataWidget):
    def __init__(self, viewport: SeismicViewport, display_settings: SeismicDisplaySettings, parent=None):
        super().__init__(viewport=viewport, display_settings=display_settings, parent=parent)


    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.save()

        _color_background =  QColor(255, 255, 255)
        # Desenha um retantulo preenchido na area do widget
        self.draw_boxes_xy_axes_fill_color(painter, _color_background)

        painter.restore()