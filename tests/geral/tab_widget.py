from PySide6 .QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QLineEdit

app = QApplication([])

janela = QWidget()
layout = QVBoxLayout(janela)

# Cria o QTabWidget e duas abas
tabs = QTabWidget()
aba1 = QWidget()
aba2 = QWidget()

# Adiciona campos de texto em cada aba
campo1 = QLineEdit(aba1)  # Campo 1 na aba 1
campo2 = QLineEdit(aba1)  # Campo 2 na aba 1
campo3 = QLineEdit(aba2)  # Campo 3 na aba 2

# Organiza o layout da aba 1
v1 = QVBoxLayout(aba1)
v1.addWidget(campo1)
v1.addWidget(campo2)

# Organiza o layout da aba 2
v2 = QVBoxLayout(aba2)
v2.addWidget(campo3)

tabs.addTab(aba1, "Aba 1")
tabs.addTab(aba2, "Aba 2")

layout.addWidget(tabs)

# Define a ordem do Tab: campo1 -> campo2 -> campo3
QWidget.setTabOrder(campo1, campo2)
QWidget.setTabOrder(campo2, campo3)

janela.show()
app.exec_()

#
# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
#
# app = QApplication(sys.argv)
# window = QMainWindow()
# tabs = QTabWidget()
#
# tab1 = QWidget()
# tab2 = QWidget()
#
# tabs.addTab(tab1, "First Tab")
# tabs.addTab(tab2, "Second Tab")
#
# window.setCentralWidget(tabs)
# window.show()
# sys.exit(app.exec())
