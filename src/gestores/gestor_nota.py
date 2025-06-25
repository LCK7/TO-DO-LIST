import sqlite3
from src.modelos.nota import Nota

class GestorNotas:
    """
    Clase que gestiona las operaciones CRUD relacionadas con notas de usuario.

    Esta clase permite crear la tabla de notas, agregar nuevas notas, obtener todas
    las notas de un usuario, editar y eliminar notas, así como marcar una nota como favorita.
    """

    def __init__(self,nombre_bd="tareas.db"):
        """
        Inicializa la conexión a la base de datos y crea la tabla de notas si no existe.

        Parámetros:
        - nombre_bd (str): Nombre del archivo de la base de datos SQLite.
        """
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()

    def crear_tabla(self):
        """
        Crea la tabla 'notas' en la base de datos si aún no existe.

        La tabla incluye los campos:
        - id: clave primaria autoincremental.
        - titulo: título de la nota.
        - contenido: contenido de la nota.
        - estado_favorito: indica si la nota está marcada como favorita (1) o no (0).
        - usuario_id: clave foránea que vincula la nota a un usuario.
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS notas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            estado_favorito INTEGER NOT NULL DEFAULT 0,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """
        self.conexion.execute(consulta)
        self.conexion.commit()
        
    def agregar_nota(self,titulo,contenido,usuario_id):
        """
        Agrega una nueva nota a la base de datos para un usuario específico.

        Parámetros:
        - titulo (str): Título de la nota.
        - contenido (str): Cuerpo de la nota.
        - usuario_id (int): ID del usuario dueño de la nota.
        """
        consulta = "INSERT INTO notas(titulo,contenido,usuario_id) VALUES(?,?,?);"
        self.conexion.execute(consulta,(titulo,contenido,usuario_id))
        self.conexion.commit()
    
    def obtener_todas(self,usuario_id):
        """
        Obtiene todas las notas pertenecientes a un usuario.

        Parámetros:
        - usuario_id (int): ID del usuario.

        Retorna:
        - Lista de objetos Nota.
        """
        consulta = "SELECT id, titulo,contenido,estado_favorito FROM notas WHERE usuario_id = ?;"
        cursor = self.conexion.execute(consulta,(usuario_id,))
        return [Nota(id=f[0], titulo=f[1], contenido=f[2], estadoFavorito=f[3]) for f in cursor]

    def cambiar_estado_favorito(self,id_nota):
        """
        Marca una nota como favorita (estado_favorito = 1).

        Parámetros:
        - id_nota (int): ID de la nota a actualizar.
        """
        consulta = "UPDATE notas SET estado_favorito = 1 WHERE id = ?"
        self.conexion.execute(consulta,(id_nota,))
        self.conexion.commit()
    
    def editar_nota(self, id_nota, nuevo_titulo, nuevo_contenido):
        """
        Edita el título y el contenido de una nota existente.

        Parámetros:
        - id_nota (int): ID de la nota a editar.
        - nuevo_titulo (str): Nuevo título para la nota.
        - nuevo_contenido (str): Nuevo contenido para la nota.
        """
        consulta = "UPDATE notas SET titulo = ?,contenido = ? WHERE id = ?;"
        self.conexion.execute(consulta,(nuevo_titulo,nuevo_contenido,id_nota))
        self.conexion.commit()
            
    def eliminar_nota(self,id_nota):
        """
        Elimina una nota de la base de datos.

        Parámetros:
        - id_nota (int): ID de la nota que se desea eliminar.
        """
        consulta = "DELETE FROM notas WHERE id = ?;"
        self.conexion.execute(consulta,(id_nota,))
        self.conexion.commit()
        
    def cerrar_conexion(self):
        """
        Cierra la conexión activa con la base de datos.
        """
        self.conexion.close()
    