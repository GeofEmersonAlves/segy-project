from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget, QVBoxLayout
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

texto_longo = QPlainTextEdit()
texto_longo.setPlainText("Este é um texto longo...\nCom várias linhas.")
# Para apenas leitura:
# texto_longo.setReadOnly(True)

layout.addWidget(texto_longo)
window.setLayout(layout)
window.show()
sys.exit(app.exec())
