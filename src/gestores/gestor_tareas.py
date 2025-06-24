import sqlite3
from src.modelos.tareas import Tarea

class GestorTareas:
    """
    """
    def __init__(self,nombre_bd="tareas.db"):
        """
        """
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(self.nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
    
    def crear_tabla(self):
        """
        """
        consulta = """
        CREATE TABLE IF NOT EXIST tareas(
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
        """
        consulta = """
        INSERT INTO TAREAS(descripcion,usuario_id,fecha_limite,categoria_id)
        VALUES (?,?,?,?);
        """
        self.conexion.execute(consulta,(descripcion,usuario_id,fecha_limite,categoria_id))
        self.conexion.commit()

    def obtener_todas(self,usuario_id):
        """
        """
        consulta = "SELECT id, descripcion, estado,fecha_limite FROM tareas WHERE id_usuario = ?;"
        cursor = self.conexion.execute(consulta,(usuario_id,))
        tareas = []
        for fila in cursor:
            tarea = Tarea(id=fila[0], descripcion=fila[1], estado=bool(fila[2]))
            tareas.append(tarea)
        return tareas
    
    def obtener_tareas_categoria(self,usuario_id,categoria_id):
        consulta = """
        SELECT id,description,estado,fecha_limite
        FROM tareas
        WHERE usuario_id = ? AND categoria_id = ?;
        """
        cursor = self.conexion.execute(consulta,(usuario_id,categoria_id))
        return [Tarea(id=f[0], descripcion=f[1], estado=bool(f[2]), fecha_limite=f[3]) for f in cursor]
    
    def editar_tarea(self,id_tarea,nueva_descripcion):
        """
        """
        consulta = "UDPATE tareas SET descripcion = ? WHERE id = ?;"
        self.conexion.execute(consulta,(nueva_descripcion,id_tarea))
        self.conexion.commit()
        
    def cambiar_estado(self,id_tarea):
        """
        """
        consulta = "UPDATE tareas SET estado = 1 WHERE id = ?;"
        self.conexion.execute(consulta,(id_tarea,))
        self.conexion.commit()
    
    def eliminar_tarea(self,id_tarea):
        """
        """
        consulta="DELETE FROM tareas WHERE id = ?;"
        self.conexion.execute(consulta,(id_tarea))
        self.conexion.commit()
    
    def cerrar_conexion(self):
        """
        """
        self.conexion.close()