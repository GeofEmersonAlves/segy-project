import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolButton, QVBoxLayout, QWidget, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QToolButton Example")
        self.resize(300, 200)

        # 1. Initialize the Tool Button
        tool_button = QToolButton(self)
        tool_button.setText("Options")

        # Load a standard built-in Qt icon for demonstration
        pixmap_icon = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        tool_button.setIcon(pixmap_icon)

        # 2. Configure Appearance Style
        # Changes the button layout to show text underneath the icon
        tool_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # 3. Create and Attach a Dropdown Menu
        menu = QMenu(self)
        action_1 = QAction("Save Profile", self)
        action_2 = QAction("Load Profile", self)
        menu.addAction(action_1)
        menu.addAction(action_2)

        tool_button.setMenu(menu)

        # 4. Set Popup Behavior
        # Makes it a split button (Clicking arrow opens menu, clicking button fires default action)
        # tool_button.setPopupMode(QToolButton.popupMode.menu MenuButtonPopup)

        # 5. Connect Signal Events
        tool_button.clicked.connect(self.on_button_clicked)
        action_1.triggered.connect(lambda: print("Save Profile chosen."))
        action_2.triggered.connect(lambda: print("Load Profile chosen."))

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(tool_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_clicked(self):
        print("Main tool button body clicked!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
