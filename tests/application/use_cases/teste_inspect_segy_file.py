from pathlib import Path
from pprint import pprint

from segy_viewer.infrastructure.segy import SegyFile
from segy_viewer.application.use_cases import SegyFileInspectorUseCases

path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"

def create_segy_file(path: Path) -> SegyFile:
    return SegyFile(path)

use_cases =  SegyFileInspectorUseCases(file_factory = create_segy_file)
resultado = use_cases.inspect_segy_file.execute(path_segy_file)
print(resultado.summary)
# print(resultado.text_header)
# pprint(resultado.binary_header)
# pprint(resultado.trace_header)
# pprint(resultado.trace_header_index)
# with open("dto.txt", 'w', encoding='utf-8') as file:
#     file.write(str(resultado))

