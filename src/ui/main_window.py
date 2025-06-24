from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton

class MainWindow(QWidget):
    def __init__(self,usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"TO-DO-LIST de {usuario.nombre_usuario}")
        
        layout = QVBoxLayout()
        label = QLabel(f"Hola, {usuario.nombre_usuario}")
        layout.addWidget(label)
        
        self.setLayout(layout)