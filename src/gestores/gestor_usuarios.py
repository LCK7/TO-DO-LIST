import sqlite3
import hashlib
from src.modelos.usuario import Usuario

class GestorUsuarios:
    """
    Clase que gestiona las operaciones relacionadas con los usuarios,
    como el registro, autenticación y creación de la tabla de usuarios.
    """

    def __init__(self, nombre_bd="tareas.db"):
        """
        Inicializa la conexión a la base de datos y activa las claves foráneas.

        Parámetros:
        - nombre_bd (str): Nombre del archivo de la base de datos SQLite.
        """
        self.conexion = sqlite3.connect(nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()

    def crear_tabla(self):
        """
        Crea la tabla 'usuarios' si no existe en la base de datos.

        La tabla contiene:
        - id: Clave primaria autoincremental.
        - nombre_usuario: Nombre único del usuario.
        - contraseña: Contraseña encriptada del usuario.
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

    def encriptar_contraseña(self, contraseña):
        """
        Encripta la contraseña utilizando el algoritmo SHA-256.

        Parámetros:
        - contraseña (str): Contraseña en texto plano.

        Retorna:
        - str: Contraseña encriptada en formato hexadecimal.
        """
        return hashlib.sha256(contraseña.encode()).hexdigest()

    def registrar_usuario(self, nombre_usuario, contraseña):
        """
        Registra un nuevo usuario en la base de datos.

        Parámetros:
        - nombre_usuario (str): Nombre del usuario.
        - contraseña (str): Contraseña en texto plano.

        Retorna:
        - bool: True si se registró correctamente, False si el usuario ya existe.
        """
        contraseña_segura = self.encriptar_contraseña(contraseña)
        try:
            self.conexion.execute(
                "INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (?, ?);",
                (nombre_usuario, contraseña_segura)
            )
            self.conexion.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verificar_login(self, nombre_usuario, contraseña):
        """
        Verifica las credenciales del usuario para iniciar sesión.

        Parámetros:
        - nombre_usuario (str): Nombre del usuario.
        - contraseña (str): Contraseña en texto plano.

        Retorna:
        - Usuario: Objeto Usuario si las credenciales son correctas.
        - None: Si no coinciden usuario y contraseña.
        """
        contraseña_segura = self.encriptar_contraseña(contraseña)
        cursor = self.conexion.execute(
            "SELECT id, nombre_usuario, contraseña FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?",
            (nombre_usuario, contraseña_segura)
        )
        f = cursor.fetchone()
        if f:
            return Usuario(id=f[0], nombre_usuario=f[1], contraseña=f[2])
        else:
            return None
    def cerrar_conexion(self):
        self.conexion.close()

