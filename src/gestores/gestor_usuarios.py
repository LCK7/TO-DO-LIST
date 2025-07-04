import hashlib
from src.modelos.usuario import Usuario

class GestorUsuarios:
    def __init__(self, session):
        self.session = session

    def encriptar_contraseña(self, contraseña):
        return hashlib.sha256(contraseña.encode()).hexdigest()

    def registrar_usuario(self, nombre_usuario, contraseña):
        contraseña_segura = self.encriptar_contraseña(contraseña)
        if self.session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            return False
        nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contraseña=contraseña_segura)
        self.session.add(nuevo_usuario)
        self.session.commit()
        return True

    def verificar_login(self, nombre_usuario, contraseña):
        contraseña_segura = self.encriptar_contraseña(contraseña)
        usuario = self.session.query(Usuario).filter_by(
            nombre_usuario=nombre_usuario,
            contraseña=contraseña_segura
        ).first()
        return usuario

    def cerrar_conexion(self):
        self.session.close()