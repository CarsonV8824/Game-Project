from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.isLoadedGame = False

        layout = QVBoxLayout()
        label = QLabel("Welcome to the Tower Defense Game!")

        start_new_game_button = QPushButton("New Game")
        start_new_game_button.clicked.connect(self.NewClicked)

        load_new_game_button = QPushButton("Load Game")
        load_new_game_button.clicked.connect(self.LoadedClicked)

        layout.addWidget(label)
        layout.addWidget(start_new_game_button)
        layout.addWidget(load_new_game_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def LoadedClicked(self) -> None:
        self.isLoadedGame = True
        self.close()

    def NewClicked(self) -> None:
        self.isLoadedGame = False
        self.close()

    def getIsLoadedGame(self) -> bool:
        return self.isLoadedGame