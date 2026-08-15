from pathlib import Path

from segy_viewer.domain.traces import SeismicTrace
from segy_viewer.domain.headers import SegyBinaryHeader,SegyTextHeader, SegyTraceHeader
from segy_viewer.infrastructure.segy import SegyioReader

path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"
path_br = Path("E:/") / "BGP" / "04 - MEDICAO 4 - SW17-SW01" / "01 - REMESSA 4" / "01-DADOS" / "0328-SW16_BRV06.sgy"
path_anp = Path("C:/") / "Users" / "Emerson" / "Documents" / "MBA" / "Projetos" / "SEGY_File" / "R0254_RIO_UATUMA_3D.3D.POST-STM.1.sgy"

def faz_reader(path: Path):
    with SegyioReader(path) as reader:
        binary_header = reader.read_binary_header()
        text_header = reader.read_text_header()

        print(text_header, f'Qtde. cartões {len(text_header.cards)}')
        print(binary_header.to_dict())
        print(f"Cobertura {binary_header.ensemble_fold}")
        print(f"SEG-Y Revision: {binary_header.revision_major}.{binary_header.revision_minor}")
        print(f'Sistema de medida: {binary_header.measurement_system_name}')

        assert isinstance(text_header, SegyTextHeader)
        assert isinstance(binary_header, SegyBinaryHeader)
        assert len(text_header.cards) == 40

        print(f"Quantidade de traços: {reader.trace_count}")
        traco1: SeismicTrace = reader.read_trace(0)

        result = traco1.to_dict()
        print(result)

        type
        assert isinstance(traco1, SeismicTrace)
        traco1_trace_header = traco1.header

        assert isinstance(traco1_trace_header, SegyTraceHeader)

        # for traco in reader.iter_traces():
        #     print(traco.index)


def test_segy_reader():
    faz_reader(path_segy_file)
    faz_reader(path_br)
    faz_reader(path_anp)


if __name__ == "__main__":
    test_segy_reader()