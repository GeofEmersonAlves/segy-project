from pathlib import Path


from segy_viewer.domain.headers import  SegyBinaryHeader
from segy_viewer.infrastructure.segy import SegyioReader


def test_binary_header():
    path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"
    path_br = Path("E:/") / "BGP" / "04 - MEDICAO 4 - SW17-SW01" / "01 - REMESSA 4" / "01-DADOS" / "0328-SW16_BRV06.sgy"
    path_anp = Path("C:/") / "Users" / "Emerson" / "Documents" / "MBA" / "Cursos Complementares" / "SEGY_File" / "R0254_RIO_UATUMA_3D.3D.POST-STM.1.sgy"

    path = path_segy_file

    with SegyioReader(path) as reader:
        binary_header = reader.read_binary_header()

        print(binary_header.to_dict())
        print(f"Cobertura {binary_header.ensemble_fold}")
        print(f"SEG-Y Revision: {binary_header.revision_major}.{binary_header.revision_minor}")
        print(f'Sistema de medida: {binary_header.measurement_system_name}')

        assert isinstance(binary_header, SegyBinaryHeader)


if __name__ == "__main__":
      test_binary_header()

