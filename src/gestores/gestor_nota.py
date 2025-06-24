import sqlite3
from src.modelos.nota import Nota

class GestorNotas:
    """
    """
    def __init__(self,nombre_bd="tareas.db"):
        """
        """
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()

    def crear_tabla(self):
        """
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS notas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            estado_favorito INTEGER NOT NULL DEFAULT 0
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """
        self.conexion.execute(consulta)
        self.conexion.commit()
        
    def agregar_nota(self,titulo,contenido,usuario_id):
        """
        """
        consulta = "INSERT INTO notas(titulo,contenido,usuario_id) VALUES(?,?,?);"
        self.conexion.execute(consulta,(titulo,contenido,usuario_id))
        self.conexion.commit()
    
    def obtener_todas(self,usuario_id):
        """
        """
        consulta = "SELECT id, titulo,contenido FROM notas WHERE usuario_id = ?;"
        cursor = self.conexion.execute(consulta,(usuario_id,))
        return [Nota(id=f[0], titulo=f[1], contenido=f[2], estadoFavorito=f[3]) for f in cursor]

    def cambiar_estado_favorito(self,id_nota):
        """
        """
        consulta = "UPDATE notas SET estado_favorito = 1 WHERE id = ?"
        self.conexion.execute(consulta,(id_nota,))
        self.conexion.commit()
    
    def editar_nota(self, id_nota, nuevo_titulo, nuevo_contenido):
        """
        """
        consulta = "UPDATE notas SET titulo = ?,contenido = ? WHERE id = ?;"
        self.conexion.execute(consulta,(nuevo_titulo,nuevo_contenido,id_nota))
        self.conexion.commit()
            
    def eliminar_nota(self,id_nota):
        """
        """
        consulta = "DELETE FROM notas WHERE id = ?;"
        self.conexion.execute(consulta,(id_nota,))
        self.conexion.commit()
        
    def cerrar_conexion(self):
        """
        """
        self.conexion.close()
    