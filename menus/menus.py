import os
from PySide6.QtWidgets import QApplication
from menus.mainWindow import MainWindow

def show_menu():
    """Show the Qt menu in a separate function"""
    stylesheet_path = os.path.join("assets", "stylesheet.css")
    with open(stylesheet_path, "r") as f:
        stylesheet = f.read()
    app = QApplication.instance() or QApplication()
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.setWindowTitle("Tower Defense Game")

    window.show()
    
    result = app.exec()
    loadedGame = window.getIsLoadedGame() if result == 0 else None
    
    # Properly shut down Qt
    try:
        app.quit()
    except:
        pass
    
    return loadedGame