from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel

class PauseMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.quit = False
        self.ToMenu = False

        layout = QVBoxLayout()
        label = QLabel("Game Paused")

        resume_button = QPushButton("Resume")
        resume_button.clicked.connect(self.ResumeClicked)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.QuitClicked)

        menu_button = QPushButton("Main Menu")
        menu_button.clicked.connect(self.toMenu)

        layout.addWidget(label)
        layout.addWidget(resume_button)
        layout.addWidget(quit_button)
        layout.addWidget(menu_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def ResumeClicked(self) -> None:
        self.close()

    def QuitClicked(self) -> None:
        self.quit = True
        self.close()

    def toMenu(self) -> None:
        self.ToMenu = True
        self.quit = True
        self.close()

    def getQuit(self) -> bool:
        return self.quit
    
    def getToMenu(self) -> bool:
        return self.ToMenu