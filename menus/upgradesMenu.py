from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

class UpgradesMenu(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.isUpgradeSelected = False

        layout = QVBoxLayout()
        label = QLabel("Congratulations! You've defended enough against the waves for this objective. Get an upgrade and start at a new map!")
        label.setAlignment(Qt.AlignCenter)

        upgrade1_button = QPushButton("Upgrade 1")
        upgrade1_button.clicked.connect(self.Upgrade1Clicked)

        upgrade2_button = QPushButton("Upgrade 2")
        upgrade2_button.clicked.connect(self.Upgrade2Clicked)

        layout.addWidget(label)
        layout.addWidget(upgrade1_button)
        layout.addWidget(upgrade2_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Override keyPressEvent to prevent spacebar from triggering button clicks"""
        if event.key() == Qt.Key_Space:
            event.ignore()
        else:
            super().keyPressEvent(event)

    def Upgrade1Clicked(self) -> None:
        self.isUpgradeSelected = True
        self.close()

    def Upgrade2Clicked(self) -> None:
        self.isUpgradeSelected = True
        self.close()

    def getIsUpgradeSelected(self) -> bool:
        return self.isUpgradeSelected