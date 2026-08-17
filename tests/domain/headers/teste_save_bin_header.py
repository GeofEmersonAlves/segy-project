import json
from pathlib import Path

from segy_viewer.infrastructure.segy import SegyioReader
from segy_viewer.domain.headers import SegyBinaryHeader, SegyTraceHeader

path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"

with SegyioReader(path_segy_file) as reader:
    binary_header:SegyBinaryHeader = reader.read_binary_header()
    with open("bin_header.json", "w", encoding="utf-8") as fh:
        json.dump(binary_header.to_dict(), fh, ensure_ascii=False, indent=4)

    trace_header:SegyTraceHeader = reader.read_trace_header(0)
    with open("trace_header.json", "w", encoding="utf-8") as fh:
        json.dump(trace_header.to_dict(), fh, ensure_ascii=False, indent=4)
