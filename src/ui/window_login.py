from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from src.gestores.gestor_usuarios import GestorUsuarios
from src.ui.window_register import WindowRegister
from src.ui.main_window import MainWindow


class WindowLogin(QWidget):
    def __init__(self, on_login_exitoso):
        super().__init__()
        self.setWindowTitle("Login | TO-DO List")
        self.setMinimumSize(350, 450)
        self.on_login_exitoso = on_login_exitoso
        self.gestor = GestorUsuarios()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial;
                font-size: 14px;
                color: #222; /* Texto más oscuro para mayor contraste */
            }
            QLabel#titulo1 {
                
                font-size: 22px;
                font-weight: bold;
                color: #333;
                margin-bottom: 25px;
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
            QPushButton#login {
                background-color: #0078D7;
                color: white;
            }
            QPushButton#login:hover {
                background-color: #005a9e;
                font-weight: bold;
            }
            QPushButton#register {
                background-color: #e0e0e0;
                color: #222;
            }
            QPushButton#register:hover {
                background-color: #c0c0c0;
                font-weight: bold;
            }
            QPushButton#salir {
                background-color: #ff4d4d;
                color: white;
            }
            QPushButton#salir:hover {
                background-color: #cc0000;
                font-weight: bold;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo1 = QLabel("TO-DO-LIST")
        titulo1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titulo = QLabel("INICIA SESIÓN")
        titulo1.setObjectName("titulo1")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingresa tu usuario")

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Ingresa tu contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setObjectName("login")
        self.boton_login.clicked.connect(self.intentar_login)

        self.boton_register = QPushButton("¿No tienes cuenta? Regístrate")
        self.boton_register.setObjectName("register")
        self.boton_register.clicked.connect(self.abrir_registro)

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setObjectName("salir")
        self.boton_salir.clicked.connect(QApplication.quit)

        layout.addWidget(titulo1)
        layout.addSpacing(10)
        layout.addWidget(titulo)
        layout.addSpacing(10)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contraseña_input)
        layout.addSpacing(10)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.boton_register)
        layout.addSpacing(10)
        layout.addWidget(self.boton_salir)

        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        self.setLayout(layout)

    def intentar_login(self):
        usuario = self.usuario_input.text()
        contraseña = self.contraseña_input.text()

        usuario_obj = self.gestor.verificar_login(usuario, contraseña)

        if usuario_obj:
            self.hide()

            def volver_al_login():
                self.show()

            from src.ui.main_window import MainWindow
            self.ventana_principal = MainWindow(usuario_obj, volver_a_login=volver_al_login)
            self.ventana_principal.show()

    def abrir_registro(self):
        self.hide()

        def volver():
            self.show()

        self.ventana_registro = WindowRegister(volver_a_login=volver)
        self.ventana_registro.show()
    