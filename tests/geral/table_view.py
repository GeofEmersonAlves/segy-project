import sys
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication, QTableView


# 1. Criar o Modelo de Dados
class TabelaModelo(QAbstractTableModel):
    def __init__(self, dados, cabecalho):
        super().__init__()
        self.dados = dados
        self.cabecalho = cabecalho

    def rowCount(self, parent=None):
        return len(self.dados)

    def columnCount(self, parent=None):
        return len(self.cabecalho)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.dados[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.cabecalho[section]
        return None


# 2. Executar a Aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Dados e colunas da tabela
    cabecalhos = ["Nome", "Idade", "Cidade"]
    matriz_dados = [
        ["Ana", 28, "São Paulo"],
        ["Bruno", 34, "Rio de Janeiro"],
        ["Carla", 22, "Curitiba"]
    ]

    # Instanciar o modelo e a visão
    modelo = TabelaModelo(matriz_dados, cabecalhos)
    tabela = QTableView()
    tabela.setModel(modelo)

    # Ajustar visualização (opcional)
    tabela.resize(400, 200)
    tabela.setWindowTitle("Exemplo QTableView - PySide6")
    tabela.show()

    sys.exit(app.exec())
