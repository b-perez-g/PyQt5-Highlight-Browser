from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from drawSqareWidget import DrawSquareWidget

class CustomWebEngineView(QWebEngineView):
    """
    Vista personalizada del motor de renderizado web que permite integrar el widget de dibujo
    y controlar el zoom y la interacción del ratón.
    """
    def __init__(self):
        """
        Inicializa la vista del navegador y el widget de dibujo.
        """
        super().__init__()
        self.setHtml("<body></body>")
        self.setGeometry(0, 0, 800, 600)
        self.selection_widget = DrawSquareWidget(self)
        self.selection_widget.setGeometry(self.geometry())
        self.selection_widget.show()
        self.zoom_factor = 1.0
        self.selection_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.ignoreZoom = True

    def load(self, url):
        """
        Carga una URL y actualiza el widget de selección.
        """
        self.selection_widget.rect = None
        self.selection_widget.update()
        super().load(url)
        self.selection_widget.raise_()

    def setUrl(self, url):
        """
        Establece una URL para cargar en el navegador.
        """
        super().setUrl(url)
        self.selection_widget.raise_()

    def resizeEvent(self, event):
        """
        Ajusta la geometría del widget de selección al redimensionar la ventana.
        """
        self.selection_widget.setGeometry(self.geometry())
        super().resizeEvent(event)

    def contextMenuEvent(self, event):
        """
        Activa el widget de selección para permitir dibujar o eliminar rectángulos.
        """
        self.selection_widget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        event.accept()

    def wheelEvent(self, event):
        """
        Controla el zoom usando la rueda del ratón cuando se presiona la tecla Ctrl.
        """
        if QApplication.keyboardModifiers() == Qt.ControlModifier and not self.ignoreZoom:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            elif delta < 0:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        """
        Realiza un acercamiento (zoom in) en la vista del navegador.
        """
        self.zoom_factor *= 1.1
        self.set_zoom(self.zoom_factor)

    def zoom_out(self):
        """
        Realiza un alejamiento (zoom out) en la vista del navegador.
        """
        self.zoom_factor *= 0.9
        self.set_zoom(self.zoom_factor)

    def set_zoom(self, factor):
        """
        Establece el nivel de zoom del navegador.
        """
        self.setZoomFactor(factor)

    def reset_zoom(self):
        """
        Restablece el zoom al valor predeterminado (1.0).
        """
        self.zoom_factor = 1.0
        self.set_zoom(self.zoom_factor)

    def mousePressEvent(self, event):
        """
        Desactiva el widget de selección al hacer clic izquierdo en la vista del navegador.
        """
        if event.button() == Qt.LeftButton:
            self.selection_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Activa el widget de selección al soltar el botón izquierdo del ratón.
        """
        if event.button() == Qt.LeftButton:
            self.selection_widget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        return super().mouseReleaseEvent(event)
