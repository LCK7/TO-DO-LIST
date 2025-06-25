import sqlite3
from src.modelos.categoria import Categoria
from src.modelos.tareas import Tarea


class GestorCategoria:
    """
    Clase encargada de gestionar las operaciones relacionadas con las categorías
    dentro de la base de datos de tareas.

    Métodos disponibles:
        - crear_tabla(): Crea la tabla de categorías si no existe.
        - agregar_categoria(nombre, usuario_id): Inserta una nueva categoría.
        - obtener_todas(usuario_id): Devuelve todas las categorías de un usuario.
        - obtener_por_categoria(categoria_id): Devuelve todas las tareas de una categoría.
        - eliminar_categoria(id_categoria): Elimina una categoría por su ID.
        - actualizar_categoria(id_categoria, nuevo_nombre): Cambia el nombre de una categoría.
        - cerrar_conexion(): Cierra la conexión a la base de datos.
    """
    def __init__(self,nombre_db = "tareas.db"):
        """
        Inicializa la conexión a la base de datos y activa las claves foráneas.

        Parámetros:
        - nombre_db (str): Nombre del archivo de la base de datos SQLite. Por defecto es "tareas.db".
        """
        self.conexion = sqlite3.connect(nombre_db)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
    
    def crear_tabla(self):
        """
        Crea la tabla 'categorias' en la base de datos si no existe.

        La tabla contiene:
        - id (INTEGER): Clave primaria autoincremental.
        - nombre (TEXT): Nombre de la categoría.
        - usuario_id (INTEGER): Clave foránea relacionada con la tabla usuarios.
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS categorias(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """
        self.conexion.execute(consulta)
        self.conexion.commit()
    
    def agregar_categoria(self,nombre, usuario_id):
        """
        Inserta una nueva categoría asociada a un usuario.

        Parámetros:
        - nombre (str): Nombre de la nueva categoría.
        - usuario_id (int): ID del usuario al que pertenece la categoría.
        """
        self.conexion.execute("INSERT INTO categorias(nombre,usuario_id) VALUES (?,?);",(nombre,usuario_id))
        self.conexion.commit()
    
    def obtener_todas(self, usuario_id):
        """
        Obtiene todas las categorías asociadas a un usuario específico.

        Parámetros:
        - usuario_id (int): ID del usuario.

        Retorna:
        - Lista de objetos Categoria.
        """
        cursor = self.conexion.execute("SELECT id, nombre, usuario_id FROM categorias WHERE usuario_id = ?;", (usuario_id,))
        return [Categoria(*fila) for fila in cursor]

    def obtener_por_categoria(self, categoria_id):
        """
        Obtiene todas las tareas asociadas a una categoría específica.

        Parámetros:
        - categoria_id (int): ID de la categoría.

        Retorna:
        - Lista de objetos Tarea.
        """
        cursor = self.conexion.execute(
            "SELECT * FROM tareas WHERE categoria_id = ?;",
            (categoria_id,)
        )
        return [Tarea(*fila) for fila in cursor]

    def eliminar_categoria(self, id_categoria):
        """
        Elimina una categoría de la base de datos según su ID.

        Parámetros:
        - id_categoria (int): ID de la categoría a eliminar.
        """
        self.conexion.execute("DELETE FROM categorias WHERE id = ?;", (id_categoria,))
        self.conexion.commit()

    def actualizar_categoria(self, id_categoria, nuevo_nombre):
        """
        Actualiza el nombre de una categoría existente.

        Parámetros:
        - id_categoria (int): ID de la categoría.
        - nuevo_nombre (str): Nuevo nombre para la categoría.
        """
        self.conexion.execute("UPDATE categorias SET nombre = ? WHERE id = ?;", (nuevo_nombre, id_categoria))
        self.conexion.commit()
        
    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.conexion.close()
    