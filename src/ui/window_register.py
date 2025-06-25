from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from src.gestores.gestor_usuarios import GestorUsuarios


class WindowRegister(QWidget):
    def __init__(self, volver_a_login):
        super().__init__()
        self.setWindowTitle("Registro de Usuario | TO-DO List")
        self.setFixedSize(350, 450)
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
        self.contraseña_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setObjectName("registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)

        self.btn_volver = QPushButton("Volver al login")
        self.btn_volver.setObjectName("volver")
        self.btn_volver.clicked.connect(self.volver)

        layout.addWidget(titulo)
        layout.addSpacing(10)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contraseña_input)
        layout.addWidget(self.btn_registrar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

    def registrar_usuario(self):
        usuario = self.usuario_input.text()
        contraseña = self.contraseña_input.text()

        if usuario and contraseña:
            if self.gestor.registrar_usuario(usuario, contraseña):
                QMessageBox.information(self, "Éxito", "¡Usuario registrado con éxito!")
                self.volver()
            else:
                QMessageBox.warning(self, "Error", "Ese usuario ya existe")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor llena todos los campos")

    def volver(self):
        self.close()
        self.volver_a_login()