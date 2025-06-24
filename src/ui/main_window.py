from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton,QHBoxLayout
from PyQt6.QtGui import QFont
from src.ui.window_tareas import VentanaTareas

class MainWindow(QWidget):
    def __init__(self,usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"TO-DO-LIST de {usuario.nombre_usuario}")
        self.setMinimumSize(500,400)
        
        self.init_ui()
        
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        label = QLabel(f"Hola, {self.usuario.nombre_usuario}")
        label.setObjectName("titulo")
        saludo = QLabel("¿Qué quieres gestionar el día de hoy?")
        saludo.setObjectName("subtitulo")
        label.setFont(QFont("Arial",16,QFont.Weight.Bold))
        saludo.setFont(QFont("Arial",16,QFont.Weight.Bold))
        layout.addWidget(label)
        layout.addWidget(saludo)
        
        layout_botones=QHBoxLayout()
        
        self.btn_tareas = QPushButton("TAREAS")
        self.btn_tareas.setObjectName("tareas")
        self.btn_tareas.setFixedHeight(40)
        self.btn_tareas.clicked.connect(self.abrir_tareas)
            
        self.btn_notas = QPushButton("NOTAS")
        self.btn_notas.setObjectName("tareas")
        self.btn_notas.setFixedHeight(40)
        self.btn_notas.clicked.connect(self.abrir_notas)
        
        self.btn_calendario = QPushButton("CALENDARIO")
        self.btn_calendario.setObjectName("tareas")
        self.btn_calendario.setFixedHeight(40)
        self.btn_calendario.clicked.connect(self.abrir_calendario)
        
        layout_botones.addWidget(self.btn_tareas)
        layout_botones.addWidget(self.btn_notas)
        layout_botones.addWidget(self.btn_calendario)
        
        layout.addLayout(layout_botones)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #222;
            }
            QLabel {
                color: #333;
            }
            QLabel#titulo {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #222;
            }
            QLabel#subtitulo {
                font-size: 16px;
                margin-bottom: 20px;
                color: #555;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 10px;
                background-color: #e0e0e0;
                color: #222;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
                font-weight: bold;
                transform: scale(1.03);
            }
            QPushButton:disabled {
                background-color: #aaa;
                color: #666;
            }
            QPushButton#tareas {
                background-color: #0078D7;
                color: white;
            }
            QPushButton#tareas:hover {
                background-color: #005a9e;
            }
        """)
        
        self.setLayout(layout)
        
    def abrir_tareas(self):
        print("Ocultando ventana principal...")
        self.hide()

        def volver():
            self.show()
            self.btn_tareas.setEnabled(True)

        self.btn_tareas.setEnabled(False)
        self.ventana_tareas = VentanaTareas(self.usuario, volver_a_main=volver)
        self.ventana_tareas.show()

    def abrir_notas(self):
        print("Esto abrira window_notas")

    def abrir_calendario(self):
        print("Esto abrira window_calendario")