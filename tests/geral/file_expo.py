import sys
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QApplication, QFileSystemModel, QMainWindow, QTreeView


class FileBrowser(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle('Explorador de Arquivos - PySide6')
    self.resize(800, 500)

    # 1. Configurar o Modelo de Arquivos
    self.model = QFileSystemModel()
    self.model.setRootPath(QDir.rootPath())  # Define a raiz do sistema

    # 2. Configurar a Visão em Árvore
    self.tree = QTreeView()
    self.tree.setModel(self.model)

    # Opcional: Definir um caminho inicial específico (ex: pasta do usuário)
    # self.tree.setRootIndex(self.model.index(QDir.homePath()))

    # Ajustar colunas (Nome, Tamanho, Tipo, Data de Modificação)
    self.tree.setColumnWidth(0, 300)

    # Definir o widget central da janela
    self.setCentralWidget(self.tree)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  browser = FileBrowser()
  browser.show()
  sys.exit(app.exec())
