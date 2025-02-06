from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QStyle

class DrawSquareWidget(QWidget):
    """
    Widget personalizado para dibujar rectángulos en la ventana principal.
    Permite dibujar y eliminar rectángulos con clic derecho del ratón.
    """
    def __init__(self, parent):
        """
        Inicializa el widget y configura su geometría y estilo.
        """
        super().__init__(parent)
        self.setGeometry(parent.geometry())
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.rect = None
        self.drawing = False
        self.rects = []
        self.setStyleSheet("background: transparent;")
        style = self.style()
        self.trash_cursor = QCursor(style.standardIcon(QStyle.SP_MessageBoxCritical).pixmap(27, 27))
        self.drawing_cursor = QCursor(Qt.CrossCursor)
        self.setCursor(self.drawing_cursor)

    def mousePressEvent(self, event):
        """
        Detecta el clic derecho del ratón y empieza a dibujar un rectángulo.
        También permite eliminar rectángulos si el clic es sobre uno existente.
        """
        if event.button() == Qt.RightButton:
            clicked_pos = event.pos()
            for rect in self.rects:
                if rect.contains(clicked_pos):
                    self.rects.remove(rect)
                    self.update()
                    return
            self.start_pos = clicked_pos
            self.rect = QRect(self.start_pos, self.start_pos).normalized()
            self.drawing = True
            self.update()
        event.accept()

    def mouseMoveEvent(self, event):
        """
        Cambia el cursor al pasar por encima de un rectángulo y actualiza el rectángulo en construcción.
        """
        hovered_pos = event.pos()
        cursor_changed = False
        for rect in self.rects:
            if rect.contains(hovered_pos):
                self.setCursor(self.trash_cursor)
                cursor_changed = True
                break
        if not cursor_changed:
            self.setCursor(self.drawing_cursor)
        if self.drawing:
            self.rect = QRect(self.start_pos, event.pos()).normalized()
            self.update()
        event.accept()

    def mouseReleaseEvent(self, event):
        """
        Finaliza el dibujo de un rectángulo cuando se suelta el botón derecho del ratón.
        """
        if event.button() == Qt.RightButton and self.rect:
            self.drawing = False
            self.rects.append(self.rect)
            self.rect = None
            self.update()
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        event.accept()
    
    def wheelEvent(self, event):
        """
        Ignora el evento de la rueda del ratón.
        """
        event.ignore()

    def paintEvent(self, event):
        """
        Dibuja los rectángulos en el widget.
        """
        painter = QPainter(self)
        for rect in self.rects:
            painter.setPen(QColor(0, 0, 255, 0))
            painter.setBrush(QColor(0, 0, 255, 50))
            painter.drawRoundedRect(rect, 10, 10)
        if self.rect:
            painter.setPen(Qt.red)
            painter.setBrush(QColor(255, 0, 0, 40))
            painter.drawRoundedRect(self.rect, 10, 10)