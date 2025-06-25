from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from src.gestores.gestor_usuarios import GestorUsuarios


class WindowRegister(QWidget):
    """
    Ventana de registro de nuevos usuarios para la aplicación TO-DO List.

    Permite a los usuarios crear una nueva cuenta proporcionando un nombre de usuario
    y una contraseña.
    """
    def __init__(self, volver_a_login):
        """
        Inicializa la ventana de registro.

        Args:
            volver_a_login: Función de callback para regresar a la ventana de login
                            después de un registro exitoso o al presionar el botón "Volver".
        """
        super().__init__()
        self.setWindowTitle("Registro de Usuario | TO-DO List")
        self.setFixedSize(350, 450) # Fija el tamaño de la ventana
        self.gestor = GestorUsuarios()
        self.volver_a_login = volver_a_login

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial;
                font-size: 14px;
                color: #222;
            }
            QLabel#titulo {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                margin-bottom: 25px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #bbb;
                border-radius: 8px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 8px;
            }
            QPushButton#registrar {
                background-color: #0078D7;
                color: white;
            }
            QPushButton#registrar:hover {
                background-color: #005a9e;
                font-weight: bold;
            }
            QPushButton#volver {
                background-color: #e0e0e0;
                color: #222;
            }
            QPushButton#volver:hover {
                background-color: #c0c0c0;
                font-weight: bold;
            }
        """)

        self.init_ui()

    def init_ui(self):
        """
        Configura la interfaz de usuario de la ventana de registro.

        Incluye campos para el nombre de usuario y la contraseña,
        y botones para registrarse y volver al login.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        titulo = QLabel("REGISTRO DE USUARIO")
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titulo.setObjectName("titulo")

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Nombre de usuario")

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.EchoMode.Password) # Oculta la contraseña

        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setObjectName("registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)

        self.btn_volver = QPushButton("Volver al login")
        self.btn_volver.setObjectName("volver")
        self.btn_volver.clicked.connect(self.volver)

        layout.addWidget(titulo)
        layout.addSpacing(10) # Espacio después del título
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contraseña_input)
        layout.addWidget(self.btn_registrar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

    def registrar_usuario(self):
        """
        Intenta registrar un nuevo usuario con los datos proporcionados.

        Valida que los campos no estén vacíos y utiliza el gestor de usuarios
        para intentar el registro. Muestra mensajes de éxito o error
        mediante QMessageBox. Si el registro es exitoso, regresa a la ventana de login.
        """
        usuario = self.usuario_input.text().strip() # Elimina espacios en blanco
        contraseña = self.contraseña_input.text().strip()

        if usuario and contraseña:
            if self.gestor.registrar_usuario(usuario, contraseña):
                QMessageBox.information(self, "Éxito", "¡Usuario registrado con éxito! Ahora puedes iniciar sesión.")
                self.volver() # Regresa al login después del registro exitoso
            else:
                QMessageBox.warning(self, "Error de Registro", "Ese nombre de usuario ya existe. Por favor, elige otro.")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, ingresa un nombre de usuario y una contraseña.")

    def volver(self):
        """
        Cierra la ventana actual de registro y llama a la función de callback
        para volver a mostrar la ventana de login.
        """
        self.close()
        self.volver_a_login()