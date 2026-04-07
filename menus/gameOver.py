from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from menus.mainWindow import MainWindow

import matplotlib.pyplot as plt
import seaborn as sns

class GameOverScreen(QMainWindow):
    def __init__(self, score, screen_width, screen_height):
        super().__init__()
        self.setWindowTitle("Game Over")
        self.score = score
        self.init_ui()
        self.isMainMenu = False
        
        # Set window size to match pygame screen dimensions
        self.resize(screen_width, screen_height)

    def init_ui(self):
        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Create a label to display the score
        self.score_label = QLabel(f"Your Score: {self.score}")
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        # Create a button to return to the main menu
        self.menu_button = QPushButton("Return to Main Menu")
        self.menu_button.clicked.connect(self.return_to_menu)
        layout.addWidget(self.menu_button)
        
        # Set the layout and central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def return_to_menu(self):
        self.isMainMenu = True
        self.close()

    def getIsMainMenu(self):
        return self.isMainMenu