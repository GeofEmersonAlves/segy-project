import sys
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QToolButton

from segy_viewer.resources import resource_path


# 1. Criamos um botão customizado para interceptar o efeito de hover
class HoverToolButton(QToolButton):

    def __init__(self, action: QAction, parent=None):
        super().__init__(parent)
        self.setDefaultAction(action)

        # Define os tamanhos: normal e quando o mouse está em cima
        self.normal_size = QSize(32, 32)
        self.hover_size = QSize(100, 100)  # Tamanho aumentado

        # Configura o tamanho inicial do ícone do botão
        self.setIconSize(self.normal_size)

    def enterEvent(self, event):
        """Disparado quando o mouse entra no botão."""
        self.setIconSize(self.hover_size)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Disparado quando o mouse sai do botão."""
        self.setIconSize(self.normal_size)
        super().leaveEvent(event)


# 2. Janela principal do aplicativo
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Efeito Hover na Toolbar")
        self.resize(600, 400)

        # Cria a barra de ferramentas
        toolbar = QToolBar("Minha Barra de Ferramentas")
        self.addToolBar(toolbar)
        _PROCESSING_TOOL_ICON = resource_path("resources/icons/processing_tool.png")
        # Cria uma ação padrão (substitua pelo caminho do seu ícone)
        action_home = QAction(QIcon(str(_PROCESSING_TOOL_ICON)), "Início", self)

        # Em vez de adicionar a ação diretamente, criamos o nosso botão customizado
        btn_home = HoverToolButton(action_home, self)

        # Adiciona o botão customizado à toolbar
        toolbar.addWidget(btn_home)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
