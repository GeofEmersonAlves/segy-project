import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Tabs PySide6")
        self.resize(500, 400)

        # 1. Criar o QTabWidget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Adicionar abas de teste
        for i in range(1, 4):
            aba = QWidget()
            layout = QVBoxLayout(aba)
            layout.addWidget(QLabel(f"Conteúdo da Aba {i}", styleSheet="color: #ffffff; font-size: 16px;"))
            self.tabs.addTab(aba, f"Aba {i}")

        # 2. Aplicar o CSS / QSS
        self.aplicar_estilo()

    def aplicar_estilo(self):
        css = """
        /* Estilo do painel/conteúdo interno das abas */
        QTabWidget::pane {
            border: 2px solid #2d2d2d;
            background-color: #222222;
            top: -2px; /* Remove a fresta entre a aba e o conteúdo */
            border-radius: 4px;
        }

        /* Alinhamento da barra de abas */
        QTabBar {
            qproperty-drawBase: 0; /* Remove a linha nativa do sistema abaixo das abas */
            left: 5px; /* Margem esquerda inicial */
        }

        /* Estilo padrão de todas as abas (Não selecionadas) */
        QTabBar::tab {
            background-color: #333333;
            color: #b1b1b1;
            border: 1px solid #2d2d2d;
            border-bottom: none;
            padding: 8px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-size: 13px;
            font-weight: bold;
        }

        /* Estado Hover (Passar o mouse por cima) */
        QTabBar::tab:hover {
            background-color: #444444;
            color: #ffffff;
        }

        /* Estado Selecionado (Aba ativa) */
        QTabBar::tab:selected {
            background-color: #222222;
            color: #3b82f6; /* Azul moderno */
            border: 2px solid #2d2d2d;
            border-bottom-color: #222222; /* Mescla a aba com o fundo do painel */
        }
        """
        self.setStyleSheet(css)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
