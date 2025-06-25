import sqlite3
from src.modelos.tareas import Tarea

class GestorTareas:
    """
    Clase responsable de gestionar las tareas en la base de datos.

    Permite realizar operaciones como crear la tabla de tareas, agregar, editar,
    eliminar y listar tareas, así como gestionar su estado y asociarlas con categorías.
    """
    def __init__(self,nombre_bd="tareas.db"):
        """
        Inicializa la conexión a la base de datos y activa las claves foráneas.

        Parámetros:
        - nombre_bd (str): Nombre del archivo de base de datos SQLite.
        """
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(self.nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
    
    def crear_tabla(self):
        """
        Crea la tabla 'tareas' en la base de datos si no existe.

        La tabla contiene:
        - id: clave primaria.
        - descripcion: texto que describe la tarea.
        - estado: 0 (pendiente) o 1 (completada).
        - usuario_id: clave foránea hacia la tabla usuarios.
        - fecha_limite: fecha límite opcional.
        - categoria_id: clave foránea hacia la tabla categorías.
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS tareas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            estado INTEGER NOT NULL DEFAULT 0,
            usuario_id INTEGER NOT NULL,
            fecha_limite TEXT,
            categoria_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );
        """
        
        self.conexion.execute(consulta)
        self.conexion.commit()
        
    def agregar_tarea(self,descripcion,usuario_id,fecha_limite,categoria_id):
        """
        Agrega una nueva tarea a la base de datos.

        Parámetros:
        - descripcion (str): Descripción de la tarea.
        - usuario_id (int): ID del usuario que la crea.
        - fecha_limite (str): Fecha límite de la tarea (formato texto).
        - categoria_id (int): ID de la categoría asociada.
        """
        consulta = """
        INSERT INTO TAREAS(descripcion,usuario_id,fecha_limite,categoria_id)
        VALUES (?,?,?,?);
        """
        self.conexion.execute(consulta,(descripcion,usuario_id,fecha_limite,categoria_id,))
        self.conexion.commit()

    def obtener_categoria_id_por_nombre(self, nombre_categoria):
        """
        Obtiene el ID de una categoría según su nombre.

        Parámetros:
        - nombre_categoria (str): Nombre de la categoría.

        Retorna:
        - ID de la categoría (int) o None si no se encuentra.
        """
        consulta = "SELECT id FROM categorias WHERE nombre = ?;"
        cursor = self.conexion.execute(consulta, (nombre_categoria,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    def crear_categoria_si_no_existe(self, nombre_categoria, usuario_id):
        """
        Crea una categoría si no existe previamente para el usuario dado.

        Parámetros:
        - nombre_categoria (str): Nombre de la categoría.
        - usuario_id (int): ID del usuario.

        Retorna:
        - ID de la categoría existente o recién creada.
        """
        if not nombre_categoria:
            return None  # No crees una categoría sin nombre

        consulta_buscar = "SELECT id FROM categorias WHERE nombre = ? AND usuario_id = ?;"
        cursor = self.conexion.execute(consulta_buscar, (nombre_categoria, usuario_id))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]  # Ya existe, devuelve su ID

        consulta_insertar = "INSERT INTO categorias(nombre, usuario_id) VALUES (?, ?);"
        self.conexion.execute(consulta_insertar, (nombre_categoria, usuario_id))
        self.conexion.commit()

        cursor = self.conexion.execute(consulta_buscar, (nombre_categoria, usuario_id))
        return cursor.fetchone()[0]

    def obtener_todas(self, usuario_id):
        """
        Obtiene todas las tareas asociadas a un usuario, incluyendo el nombre de su categoría.

        Parámetros:
        - usuario_id (int): ID del usuario.

        Retorna:
        - Lista de objetos Tarea.
        """
        consulta = """
        SELECT t.id, t.descripcion, t.estado, t.fecha_limite, t.categoria_id, COALESCE(c.nombre, 'Sin categoría')
        FROM tareas t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE t.usuario_id = ?;
        """
        cursor = self.conexion.execute(consulta, (usuario_id,))
        tareas = []
        for fila in cursor:
            tarea = Tarea(
                id=fila[0],
                descripcion=fila[1],
                estado=bool(fila[2]),
                fecha_limite=fila[3],
                categoria_id=fila[4],
                usuario_id=usuario_id,
                categoria=fila[5]
            )
            tareas.append(tarea)
        return tareas
    
    def obtener_tareas_categoria(self,usuario_id,categoria_id):
        """
        Devuelve todas las tareas de un usuario que pertenecen a una categoría específica.

        Parámetros:
        - usuario_id (int): ID del usuario.
        - categoria_id (int): ID de la categoría.

        Retorna:
        - Lista de objetos Tarea.
        """
        consulta = """
        SELECT id,descripcion,estado,fecha_limite
        FROM tareas
        WHERE usuario_id = ? AND categoria_id = ?;
        """
        cursor = self.conexion.execute(consulta,(usuario_id,categoria_id))
        return [Tarea(id=f[0], descripcion=f[1], estado=bool(f[2]), fecha_limite=f[3]) for f in cursor]
    
    def editar_tarea(self,id_tarea,nueva_descripcion,nueva_fecha, nueva_categoria):
        """
        Edita los datos de una tarea existente.

        Parámetros:
        - id_tarea (int): ID de la tarea.
        - nueva_descripcion (str): Nueva descripción.
        - nueva_fecha (str): Nueva fecha límite.
        - nueva_categoria (int): Nuevo ID de categoría.
        """
        consulta = "UPDATE tareas SET descripcion = ?,fecha_limite = ?, categoria_id = ?  WHERE id = ?;"
        self.conexion.execute(consulta,(nueva_descripcion,nueva_fecha,nueva_categoria,id_tarea))
        self.conexion.commit()
        
    def cambiar_estado(self, id_tarea, nuevo_estado: bool):
        """
        Cambia el estado de una tarea (completada o no).

        Parámetros:
        - id_tarea (int): ID de la tarea.
        - nuevo_estado (bool): True si se completa, False si no.
        """
        consulta = "UPDATE tareas SET estado = ? WHERE id = ?;"
        self.conexion.execute(consulta, (int(nuevo_estado), id_tarea))
        self.conexion.commit()
    
    def eliminar_tarea(self,id_tarea):
        """
        Elimina una tarea de la base de datos.

        Parámetros:
        - id_tarea (int): ID de la tarea a eliminar.
        """
        consulta="DELETE FROM tareas WHERE id = ?;"
        self.conexion.execute(consulta,(id_tarea,))
        self.conexion.commit()
    
    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.conexion.close()