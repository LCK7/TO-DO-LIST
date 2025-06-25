from src.gestores.gestor_usuarios import GestorUsuarios
from src.gestores.gestor_tareas import GestorTareas
from src.gestores.gestor_categoria import GestorCategoria
from src.gestores.gestor_nota import GestorNotas

def inicializar_db():
    """
    Inicializa la base de datos de la aplicación creando todas las tablas necesarias.

    Esta función instancia los gestores de usuarios, tareas, categorías y notas, lo cual
    desencadena la creación automática de las tablas correspondientes en la base de datos
    si no existen aún.

    Es recomendable ejecutar esta función al iniciar la aplicación por primera vez
    o al reiniciar la base de datos para asegurarse de que todas las estructuras estén disponibles.
    """
    GestorUsuarios()
    GestorTareas()
    GestorCategoria()
    GestorNotas()