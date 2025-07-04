import sys
from PyQt6.QtWidgets import QApplication
from src.ui.window_login import WindowLogin
from src.db.init_db import inicializar_db
from src.db.conexion import SessionLocal
from src.gestores.gestor_usuarios import GestorUsuarios
from src.gestores.gestor_nota import GestorNotas
from src.gestores.gestor_tareas import GestorTareas
from src.gestores.gestor_categoria import GestorCategoria

def iniciar_app():
    inicializar_db()
    session = SessionLocal()
    gestor_usuarios = GestorUsuarios(session)
    gestor_notas = GestorNotas(session)
    gestor_tareas = GestorTareas(session)
    gestor_categoria = GestorCategoria(session)

    app = QApplication(sys.argv)

    def mostrar_MainWindow(usuario):
        from src.ui.main_window import MainWindow
        app.main_window = MainWindow(
            usuario,
            gestor_notas,
            gestor_tareas,
            gestor_categoria,
            volver_a_login=login.show  # <-- Esto es importante
        )
        app.main_window.show()

    login = WindowLogin(gestor_usuarios, on_login_exitoso=mostrar_MainWindow)
    login.show()
    sys.exit(app.exec())
    session.close()

if __name__ == "__main__":
    iniciar_app()