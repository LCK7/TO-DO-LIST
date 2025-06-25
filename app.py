import sys
from PyQt6.QtWidgets import QApplication
from src.ui.window_login import WindowLogin
from src.ui.main_window import MainWindow
from src.db.init_db import inicializar_db

def iniciar_app():
    """
    Inicializa y ejecuta la aplicación principal TO-DO List.

    Esta función se encarga de:
    1. Inicializar la base de datos.
    2. Crear la instancia de la aplicación QApplication.
    3. Configurar la ventana de login como punto de entrada.
    4. Definir un callback para mostrar la ventana principal una vez el login sea exitoso.
    5. Iniciar el bucle de eventos de la aplicación.
    """
    inicializar_db() # Asegura que la base de datos esté lista
    app = QApplication(sys.argv) # Crea la instancia de la aplicación PyQt

    def mostrar_MainWindow(usuario):
        """
        Callback que se ejecuta cuando el login es exitoso.

        Oculta la ventana de login (si aún está visible) y muestra la ventana principal de la aplicación,
        pasando el objeto de usuario logueado.

        Args:
            usuario: El objeto de usuario que ha iniciado sesión exitosamente.
        """
        # Se asocia la MainWindow a la aplicación para evitar que sea recolectada por el garbage collector
        app.main_window = MainWindow(usuario) # type: ignore 
        app.main_window.show() # type: ignore # Muestra la ventana principal

    # Crea la ventana de login y le pasa el callback para cuando el login sea exitoso
    login = WindowLogin(on_login_exitoso = mostrar_MainWindow)
    login.show() # Muestra la ventana de login

    # Inicia el bucle de eventos de la aplicación, manteniendo la ventana abierta hasta que se cierre
    sys.exit(app.exec())

if __name__ == "__main__":
    # Asegura que iniciar_app() se ejecute solo cuando el script es el programa principal
    iniciar_app()