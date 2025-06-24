import sys
from PyQt6.QtWidgets import QApplication
from src.ui.window_login import WindowLogin
from src.ui.main_window import MainWindow
from src.db.init_db import inicializar_db

def iniciar_app():
    """
    """
    inicializar_db()
    app = QApplication(sys.argv)

    def mostrar_MainWindow(usuario):
        """
        """
        app.main_window = MainWindow(usuario) # type: ignore
        app.main_window.show() # type: ignore

    login = WindowLogin(on_login_exitoso = mostrar_MainWindow)
    login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_app()
