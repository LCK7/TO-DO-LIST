from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton,QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.ui.window_tareas import VentanaTareas

class MainWindow(QWidget):
    def __init__(self,usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"TO-DO-LIST de {usuario.nombre_usuario}")
        self.setMinimumSize(700,600)
        
        self.init_ui()
        
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        label = QLabel(f"Hola, {self.usuario.nombre_usuario}")
        label.setObjectName("titulo")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        saludo = QLabel("¿Qué quieres gestionar el día de hoy?")
        saludo.setObjectName("subtitulo")
        saludo.setFont(QFont("Arial", 14))
        saludo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        layout.addWidget(label)
        layout.addWidget(saludo)
        
        botones_centrados = QHBoxLayout()
        botones_centrados.setAlignment(Qt.AlignmentFlag.AlignCenter)
        botones_centrados.setSpacing(30)
        
        self.btn_tareas = QPushButton("📝 TAREAS")
        self.btn_tareas.setObjectName("tareas")
        self.btn_tareas.setFixedSize(200, 50)
        self.btn_tareas.clicked.connect(self.abrir_tareas)

        self.btn_notas = QPushButton("🗒️ NOTAS")
        self.btn_notas.setObjectName("notas")
        self.btn_notas.setFixedSize(200, 50)
        self.btn_notas.clicked.connect(self.abrir_notas)

        self.btn_calendario = QPushButton("📅 CALENDARIO")
        self.btn_calendario.setObjectName("calendario")
        self.btn_calendario.setFixedSize(200, 50)
        self.btn_calendario.clicked.connect(self.abrir_calendario)
        
        botones_centrados.addWidget(self.btn_tareas)
        botones_centrados.addWidget(self.btn_notas)
        botones_centrados.addWidget(self.btn_calendario)
        
        layout.addLayout(botones_centrados)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QLabel#titulo {
                font-size: 26px;
                font-weight: bold;
                color: #1e3a8a;
            }
            QLabel#subtitulo {
                font-size: 18px;
                color: #555;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 12px;
                border: none;
                background-color: #e2e8f0;
                color: #1a202c;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #a0aec0;
                color: #718096;
            }
            QPushButton#tareas {
                background-color: #2563eb;
                color: white;
            }
            QPushButton#tareas:hover {
                background-color: #1d4ed8;
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