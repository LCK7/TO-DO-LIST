import sqlite3
from src.modelos.categoria import Categoria

class GestorCategoria:
    def __init__(self,nombre_db = "tareas.db"):
        """
        """
        self.conexion = sqlite3.connect(nombre_db)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
    
    def crear_tabla(self):
        """
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
        """
        self.conexion.execute("INSERT INTO categorias(nombre,usuario_id) VALUES (?,?);",(nombre,usuario_id))
        self.conexion.commit()
    
    def obtener_todas(self, usuario_id):
        """
        """
        cursor = self.conexion.execute("SELECT id, nombre, usuario_id FROM categorias WHERE usuario_id = ?;", (usuario_id,))
        return [Categoria(*fila) for fila in cursor]

    def eliminar_categoria(self, id_categoria):
        """
        """
        self.conexion.execute("DELETE FROM categorias WHERE id = ?;", (id_categoria,))
        self.conexion.commit()

    def actualizar_categoria(self, id_categoria, nuevo_nombre):
        """
        """
        self.conexion.execute("UPDATE categorias SET nombre = ? WHERE id = ?;", (nuevo_nombre, id_categoria))
        self.conexion.commit()
        
    def cerrar_conexion(self):
        """
        """
        self.conexion.close()
    