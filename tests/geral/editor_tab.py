import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QVBoxLayout, QPlainTextEdit, QStatusBar
)


class EditorTab(QWidget):
    """Widget de aba contendo um QPlainTextEdit e uma QStatusBar própria."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal da aba
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margens extras se preferir

        # Widget de texto
        self.text_edit = QPlainTextEdit()
        layout.addWidget(self.text_edit)

        # Barra de status própria da aba
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Pronto")
        layout.addWidget(self.status_bar)

        # Conecta sinal para atualizar a barra de status ao digitar
        self.text_edit.cursorPositionChanged.connect(self.atualizar_posicao)

    def atualizar_posicao(self):
        """Atualiza a barra de status com a linha e coluna atuais."""
        cursor = self.text_edit.textCursor()
        linha = cursor.blockNumber() + 1
        coluna = cursor.columnNumber() + 1
        self.status_bar.showMessage(f"Linha: {linha} | Coluna: {coluna}")


class MainWindow(QMainWindow):
    """Janela principal contendo o QTabWidget."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor com Abas e StatusBars Próprias")
        self.resize(800, 600)

        # Gerenciador de abas central
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Adiciona abas de exemplo
        self.adicionar_nova_aba("Documento 1")
        self.adicionar_nova_aba("Documento 2")

    def adicionar_nova_aba(self, titulo):
        nova_aba = EditorTab()
        self.tab_widget.addTab(nova_aba, titulo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
