from pathlib import Path
import segyio
from segy_viewer.domain.exceptions.segy_file_exceptions import SegyFileInUseError
from segy_viewer.domain.files import SeismicWriter

class SegyioWriter(SeismicWriter):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._segy_file: segyio.SegyFile | None = None


    def _prepare_text_header(self, text: str) -> str:
        lines = text.splitlines()
        prepared_lines = []

        for line_number, line in enumerate(lines, start=1):
            prepared_lines.append(line.ljust(80))

        return "".join(prepared_lines)

    def write_text_header(self, text_header: str):
        text_header = self._prepare_text_header(text_header)

        encoded_header = text_header.encode("ascii")
        try:
            with segyio.open(str(self._path), mode="r+", strict=False, ignore_geometry=True) as segy_file:
                segy_file.text[0] = encoded_header
                segy_file.flush()

        except (PermissionError, OSError) as error:
            raise SegyFileInUseError(f"The SEG-Y file could not be opened for writing: "
                                     f"{self._path}") from error