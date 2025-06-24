import sys
from PyQt6.QtWidgets import QApplication
from src.ui.window_login import WindowLogin
from src.ui.main_window import MainWindow

def iniciar_app():
    app = QApplication(sys.argv)
    
    def mostrar_MainWindow(usuario):
        ventana = MainWindow(usuario)
        ventana.show()
        app.exec()
        
    login = WindowLogin(on_login_exitoso = mostrar_MainWindow)
    login.show()
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    iniciar_app()
