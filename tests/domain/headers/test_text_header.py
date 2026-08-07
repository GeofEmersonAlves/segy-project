from operator import ifloordiv
from pathlib import Path
import segyio

from segy_viewer.domain.exceptions.headers_exceptions import SegyTextHeaderError
from segy_viewer.domain.headers.text_header import SegyTextHeader

BASE_DIR = Path(__file__).parent.parent
path_segy_file =  Path("F:/") / "ENTREGA - ANP"  / "SÍSMICA"  / "0328-SW0001.sgy"
path_br = Path("E:/")  / "BGP" / "04 - MEDICAO 4 - SW17-SW01" / "01 - REMESSA 4" / "01-DADOS" / "0328-SW16_BRV06.sgy"
path_anp = Path("C:/") / "Users" / "Emerson"  / "Documents" / "MBA" / "Cursos Complementares" / "SEGY_File" / "R0254_RIO_UATUMA_3D.3D.POST-STM.1.sgy"

def file_text_header_reader(path : Path)-> tuple[str, ...]:
    with segyio.open(path, ignore_geometry=True) as segy:
        text = bytes(segy.text[0]).decode("ascii")
        cards = tuple(text[i:i + 80] for i in range(0, 3200, 80))

        return cards


def test_text_header():
        cards1 = file_text_header_reader(path_segy_file)
        cards2 = file_text_header_reader(path_br)
        cards3 = file_text_header_reader(path_anp)

        # Aqui tem 39 cartões, propositalmente para gerar um SegyTextHeaderError
        cards4 = tuple(x for i, x in  enumerate(cards3) if i != 30 )

        # Aqui os cartões possuem 50 caracteres, propositalmente para gerar um SegyTextHeaderError
        cards5 = tuple(x[0:50] for i, x in enumerate(cards3) )

        text_header1 = SegyTextHeader(cards1)
        text_header2 = SegyTextHeader(cards2)
        text_header3 = SegyTextHeader(cards3)

        try:
                text_header4 = SegyTextHeader(cards4)

        except SegyTextHeaderError as e:
                print(f"SegyTextHeaderError {e} {'='*60} Total de cartões: {len(cards4)}")

        try:
                text_header5 = SegyTextHeader(cards5)

        except SegyTextHeaderError as e:
                print(f"SegyTextHeaderError {e} {'='*60} Total de cartões: {len(cards5)}")

        print(text_header1, f'Qtde. cartões {len(text_header1.cards)}')
        print(text_header1.card(1))
        print(text_header1.card(2))
        print(text_header1.card(3))
        print("="*80)
        print(text_header2, f'Qtde. cartões {len(text_header2.cards)}')
        print("=" * 80)
        print(text_header3, f'Qtde. cartões {len(text_header3.cards)}')
        print("=" * 80)

        assert isinstance(text_header1, SegyTextHeader)
        assert isinstance(text_header2, SegyTextHeader)
        assert isinstance(text_header3, SegyTextHeader)
        assert len(text_header1.cards) == 40
        assert len(text_header2.cards) == 40
        assert len(text_header3.cards) == 40
