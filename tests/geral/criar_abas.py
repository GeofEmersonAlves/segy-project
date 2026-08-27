import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, \
    QLineEdit


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplo de Abas com PySide6")
        self.resize(400, 300)

        # Criar o widget de abas principal
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Criar e popular a Aba 1
        self.aba1 = QWidget()
        self.criar_aba1()
        self.tabs.addTab(self.aba1, "Aba 1 (Texto)")

        # Criar e popular a Aba 2
        self.aba2 = QWidget()
        self.criar_aba2()
        self.tabs.addTab(self.aba2, "Aba 2 (Ação)")

    def criar_aba1(self):
        layout = QVBoxLayout()
        label = QLabel("Este é o conteúdo da primeira aba.")
        botao = QPushButton("Clique na Aba 1")

        layout.addWidget(label)
        layout.addWidget(botao)
        self.aba1.setLayout(layout)

    def criar_aba2(self):
        layout = QVBoxLayout()
        label = QLabel("Digite algo na segunda aba:")
        campo_texto = QLineEdit()
        botao = QPushButton("Enviar")

        layout.addWidget(label)
        layout.addWidget(campo_texto)
        layout.addWidget(botao)
        self.aba2.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
