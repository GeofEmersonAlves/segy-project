import json
import random
from pathlib import Path

from segy_viewer.infrastructure.segy import SegyioReader
from segy_viewer.domain.traces import SeismicTrace


path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"
path_br = Path("E:/") / "BGP" / "04 - MEDICAO 4 - SW17-SW01" / "01 - REMESSA 4" / "01-DADOS" / "0328-SW16_BRV06.sgy"
path_anp = Path("C:/") / "Users" / "Emerson" / "Documents" / "MBA" / "Projetos" / "SEGY_File" / "R0254_RIO_UATUMA_3D.3D.POST-STM.1.sgy"


with SegyioReader(path_br) as reader:
    text_header = reader.read_text_header()
    # print(text_header)
    with open("text_header.txt", "w", encoding="utf-8") as fh:
        fh.write(str(text_header))

    index_traco = random.randint(0, reader.trace_count)
    traco: SeismicTrace = reader.read_trace(index_traco)

    with open("traco.json", "w", encoding="utf-8") as fh:
        json.dump(traco.to_dict(), fh, ensure_ascii=False, indent=4)

print("="*10,"FIM","="*10)



