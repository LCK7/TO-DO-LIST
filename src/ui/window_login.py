from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QPushButton,QLabel,QMessageBox
from src.gestores.gestor_usuarios import GestorUsuarios
from src.ui.window_register import  WindowRegister


class WindowLogin(QWidget):
    def __init__(self,on_login_exitoso):
        super().__init__()
        self.setWindowTitle("Login_TodoList")
        self.on_login_exitoso = on_login_exitoso
        self.gestor = GestorUsuarios()
        
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingresa tu Usuario")
        
        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Ingresa tu contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.clicked.connect(self.intentar_login)
        
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.clicked.connect(self.intentar_login)
        
        self.boton_register = QPushButton("¿No tienes cuenta? Registrate")
        self.boton_register.clicked.connect(self.abrir_registro)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("INICIA SESIÓN"))
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contraseña_input)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.boton_register)
        layout.addWidget(self.boton_salir)
        
        
        self.setLayout(layout)
        
    def intentar_login(self):
        usuario = self.usuario_input.text()
        contraseña = self.contraseña_input.text()
        
        usuario_obj = self.gestor.verificar_login(usuario,contraseña)
        
        if usuario_obj:
            self.on_login_exitoso(usuario_obj)
            self.close()
        else:
            QMessageBox.warning(self,"Error","Usuario o Contraseña incorrectos.")
    def abrir_registro(self):
        self.hide()
        
        def volver():
            self.show()
        
        self.ventana_registro = WindowRegister(volver_a_login=volver)
        self.ventana_registro.show()