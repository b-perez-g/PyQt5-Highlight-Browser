from PyQt5.QtWidgets import QApplication, QMainWindow
from customWebengineView import CustomWebEngineView
from PyQt5.QtCore import QUrl
import os

class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación que contiene el navegador web personalizado.
    """
    def __init__(self):
        """
        Inicializa la ventana principal y el navegador web personalizado.
        """
        super().__init__()
        self.setWindowTitle("Custom Browser with Drawing")
        self.showMaximized()
        self.browser = CustomWebEngineView()
        file_path = os.path.abspath("example-page.html")
        self.browser.setUrl(QUrl.fromLocalFile(file_path))
        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    """
    Ejecuta la aplicación y muestra la ventana principal.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()