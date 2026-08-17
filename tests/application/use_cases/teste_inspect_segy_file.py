from pathlib import Path

from segy_viewer.application import use_cases
from segy_viewer.infrastructure.segy import SegyFile
from segy_viewer.application.use_cases import InspectSegyFile

path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"


def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

use_case = InspectSegyFile(file_factory = create_segy_file)
resultado = use_case.execute(path_segy_file)
with open("dto.txt", 'w', encoding='utf-8') as file:
    file.write(str(resultado))

