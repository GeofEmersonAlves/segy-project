from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.presentation.desktop.widgets.seismic_data_window import HSynchronizedSeismicDataWidget

class SeismicDataSamplesView(HSynchronizedSeismicDataWidget):
    def __init__(self, viewport: SeismicViewport, parent=None):
        super().__init__(viewport=viewport, parent=parent,)