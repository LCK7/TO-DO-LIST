from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.ui.window_tareas import VentanaTareas
from src.ui.window_notas import VentanaNotas
from src.ui.window_calendario import VentanaCalendario
from src.ui.window_gestion_categoria import VentanaGestionCategoria


class MainWindow(QWidget):
    """
    Ventana principal de la aplicación TO-DO-LIST.

    Permite al usuario acceder a tareas, notas, calendario, gestión de categorías
    y cerrar sesión.
    """

    def __init__(self, usuario, volver_a_login):
        """
        Inicializa la ventana principal con el usuario actual.

        Args:
            usuario: Instancia del usuario autenticado.
            volver_a_login: Función para regresar al login al cerrar sesión.
        """
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"TO-DO-LIST de {usuario.nombre_usuario}")
        self.setMinimumSize(700, 500)
        self.volver_a_login = volver_a_login
        self.init_ui()

    def init_ui(self):
        """
        Configura y construye la interfaz gráfica de la ventana principal.
        """
        fila_administracion = QHBoxLayout()
        fila_administracion.addStretch()
        btn_gestion_categorias = QPushButton("🏷️ GESTION CATEGORÍA")
        btn_gestion_categorias.setObjectName("categorias")
        btn_gestion_categorias.setFixedSize(250, 40)

        btn_gestion_categorias.clicked.connect(self.abrir_gestion_categorias)
        fila_administracion.addWidget(btn_gestion_categorias)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(fila_administracion)
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

        self.btn_cerrar_sesion = QPushButton("🚪 Cerrar sesión")
        self.btn_cerrar_sesion.setFixedSize(150, 40)
        self.btn_cerrar_sesion.setObjectName("cerrar")
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)

        layout.addSpacing(20)

        botones_centrados.addWidget(self.btn_tareas)
        botones_centrados.addWidget(self.btn_notas)
        botones_centrados.addWidget(self.btn_calendario)

        layout.addLayout(botones_centrados)
        layout.addStretch()

        fila_cerrar = QHBoxLayout()
        fila_cerrar.addStretch()
        fila_cerrar.addWidget(self.btn_cerrar_sesion)

        layout.addLayout(fila_cerrar)

        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QPushButton#categorias {
                background-color: #f59e0b;
                color: white;
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
            QPushButton#cerrar {
                background-color: #ef4444;
                color: white;
            }
            QPushButton#cerrar:hover {
                background-color: #dc2626;
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
        """
        Oculta la ventana principal y muestra la ventana de gestión de tareas.
        """
        print("Ocultando ventana principal...")
        self.hide()

        def volver():
            self.show()
            self.btn_tareas.setEnabled(True)

        self.btn_tareas.setEnabled(False)
        self.ventana_tareas = VentanaTareas(self.usuario, volver_a_main=volver)
        self.ventana_tareas.show()

    def abrir_notas(self):
        """
        Oculta la ventana principal y muestra la ventana de notas.
        """
        print("Ocultando ventana principal (Notas)...")
        self.hide()

        def volver():
            self.show()
            self.btn_notas.setEnabled(True)

        self.btn_notas.setEnabled(False)
        self.ventana_notas = VentanaNotas(self.usuario, volver_a_main=volver)
        self.ventana_notas.show()

    def abrir_calendario(self):
        """
        Oculta la ventana principal y abre la ventana de calendario.
        """
        self.hide()

        def volver():
            self.ventana_calendario.close()
            self.show()

        self.ventana_calendario = VentanaCalendario(self.usuario, volver_a_main=volver)
        self.ventana_calendario.show()

    def abrir_gestion_categorias(self):
        """
        Oculta la ventana principal y muestra la gestión de categorías.
        """
        self.hide()

        def volver():
            self.ventana_gestion_categorias.close()
            self.show()

        self.ventana_gestion_categorias = VentanaGestionCategoria(self.usuario, volver)
        self.ventana_gestion_categorias.show()

    def cerrar_sesion(self):
        """
        Pregunta al usuario si desea cerrar sesión y, si confirma, vuelve al login.
        """
        confirmacion = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Estás seguro que deseas cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            self.close()
            self.volver_a_login()
