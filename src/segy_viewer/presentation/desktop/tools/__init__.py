from .julian_day_calendar.julian_day_calendar_window import JulianDayCalendarWindow
from .hash_md5.hash_md5_window import HashMD5Window
from .segy_file_size_calculator.file_size_calculator_window import SegyFileSizeCalculatorWindow

def _create_julian_day_window(*args, **kwargs):
    return JulianDayCalendarWindow(*args, **kwargs)

def _create_hash_md5_window(*args, **kwargs):
    return HashMD5Window(*args, **kwargs)

def _create_segy_size_calculator_window(*args, **kwargs):
    return SegyFileSizeCalculatorWindow(*args, **kwargs)

class SegyTools:
    def __init__(self):
        self.julian_day_calendar = _create_julian_day_window
        self.hash_md5 =  _create_hash_md5_window
        self.file_size_calculator = _create_segy_size_calculator_window

