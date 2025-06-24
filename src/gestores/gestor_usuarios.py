import sqlite3
import hashlib
from src.modelos.usuario import Usuario

class GestorUsuarios:
    """
    """
    def __init__(self,nombre_bd = "tareas.db"):
        """
        """
        self.conexion = sqlite3.connect(nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
        
    def crear_tabla(self):
        """
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS usuarios(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre_usuario TEXT NOT NULL UNIQUE,
          contraseña TEXT NOT NULL  
        );
        """
        self.conexion.execute(consulta)
        self.conexion.commit()
        
    def encriptar_contraseña(self,contraseña):
        """
        """
        return hashlib.sha256(contraseña.encode()).hexdigest()
    
    def registrar_usuario(self,nombre_usuario,contraseña):
        """
        """
        contraseña_segura = self.encriptar_contraseña(contraseña)
        try:
            self.conexion.execute(
                "INSERT INTO usuarios (nombre_usuario,contraseña) VALUES (?,?);",
                (nombre_usuario,contraseña_segura)
            )
            self.conexion.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def verificar_login(self,nombre_usuario,contraseña):
        """
        """
        contraseña_segura = self.encriptar_contraseña(contraseña)
        cursor = self.conexion.execute(
            "SELECT id, nombre_usuario,contraseña FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?",
            (nombre_usuario,contraseña_segura)
        )
        f = cursor.fetchone()
        if f:
            return Usuario(id=f[0],nombre_usuario=f[1],contraseña=f[2])
        else:
            return None