from pathlib import Path
import numpy as np
from segy_viewer.domain.headers import SegyTraceHeader, SegyBinaryHeader, SegyTextHeader
from segy_viewer.domain.traces import SeismicTrace
from segy_viewer.domain.datasets import SeismicDataset, SeismicSwath3D, SeismicVolume3D
from segy_viewer.infrastructure.segy import SegyFile,SegyioReader
import csv

path_segy_file = Path("H:/") / "ENTREGA - ANP" / "SÍSMICA" / "0328-SW0001.sgy"
path_br = Path("E:/") / "BGP" / "04 - MEDICAO 4 - SW17-SW01" / "01 - REMESSA 4" / "01-DADOS" / "0328-SW16_BRV06.sgy"
path_anp = Path("C:/") / "Users" / "Emerson" / "Documents" / "MBA" / "Projetos" / "SEGY_File" / "R0254_RIO_UATUMA_3D.3D.POST-STM.1.sgy"

dataset1 = SeismicSwath3D(name = "0328-3D-TAMBAQUI", swath_number = 1)
seyFile1 = SegyFile(path_segy_file, dataset=dataset1)

dataset2 = SeismicSwath3D(name = "0328-3D-CAMPO-DE-PILAR", swath_number = 16)
seyFile2 = SegyFile(path_segy_file, dataset = dataset2)

dataset3 =  SeismicVolume3D("R0254_RIO_UATUMA_3D.3D.POST-STM.1")
seyFile3 = SegyFile(path_anp, dataset = dataset3)

#Um segy sem um dataset associado
segyFile4 = SegyFile(path_segy_file)

print(seyFile1.is_open)
print(seyFile2.is_open)
print(seyFile3.is_open)

seyFile1.open()
print(seyFile1.is_open)
print(type(seyFile1.dataset))
print(seyFile1.dataset.describe())
print(str(seyFile1.text_header))
trace_count = seyFile1.trace_count
print(trace_count)

indices = np.linspace(0, trace_count - 1, int(trace_count * 0.001), dtype=int)
print(f'Total de traços a serem analisados: {len(indices)}')
print('-'*80)
# for traco in seyFile1.reader.iter_traces():
#     print(traco)

readerSegy1:SegyioReader = seyFile1.reader

print(indices)
for index in indices:
    traco = readerSegy1.read_trace(index)
    print(traco.header)
    print(len(traco.samples))

matrix_traco = readerSegy1.read_samples_matrix(0, 100)
print(matrix_traco.shape)
# with open("Tracos.csv", "w", newline="", encoding="utf-8") as f:
#     escritor = csv.writer(f)
#     escritor.writerows(matrix_traco)

seyFile1.close()