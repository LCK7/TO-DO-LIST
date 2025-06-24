from src.gestores.gestor_usuarios import GestorUsuarios
from src.gestores.gestor_tareas import GestorTareas
from src.gestores.gestor_categoria import GestorCategoria
from src.gestores.gestor_nota import GestorNotas

def inicializar_db():
    """
    Crea todas las tablas necesarias para la aplicación.
    """
    GestorUsuarios()
    GestorTareas()
    GestorCategoria()
    GestorNotas()