from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from src.gestores.gestor_usuarios import GestorUsuarios

class WindowRegister(QWidget):
    def __init__(self, volver_a_login):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setFixedSize(300, 400)
        self.gestor = GestorUsuarios()
        self.volver_a_login = volver_a_login

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Nombre de usuario")

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)

        self.btn_volver = QPushButton("Volver al login")
        self.btn_volver.clicked.connect(self.volver)

        layout.addWidget(QLabel("Registro de Usuario"))
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
