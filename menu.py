from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide App")
        
        # Add a central widget (like a button)
        button = QPushButton("Click Me!")
        self.setCentralWidget(button)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()