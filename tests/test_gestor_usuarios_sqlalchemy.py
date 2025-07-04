import pytest
from src.gestores.gestor_usuarios import GestorUsuarios
from src.modelos.usuario import Usuario

class TestGestorUsuarios:
    """Tests para GestorUsuarios con SQLAlchemy."""

    def test_registro_usuario_nuevo(self, session):
        gestor = GestorUsuarios(session)
        resultado = gestor.registrar_usuario("testuser", "1234")
        usuario = session.query(Usuario).filter_by(nombre_usuario="testuser").first()
        
        assert resultado is True
        assert usuario is not None
        assert usuario.nombre_usuario == "testuser"

    def test_registro_usuario_duplicado(self, session):
        gestor = GestorUsuarios(session)
        # Primero registramos un usuario
        gestor.registrar_usuario("testuser", "1234")
        # Intentamos registrar otro con el mismo nombre
        resultado = gestor.registrar_usuario("testuser", "5678")
        
        assert resultado is False

    def test_verificar_login_exitoso(self, session):
        gestor = GestorUsuarios(session)
        # Registrar un usuario
        gestor.registrar_usuario("loginuser", "mypassword")
        # Intentar iniciar sesión
        usuario = gestor.verificar_login("loginuser", "mypassword")
        
        assert usuario is not None
        assert isinstance(usuario, Usuario)
        assert usuario.nombre_usuario == "loginuser"

    def test_verificar_login_fallido(self, session):
        gestor = GestorUsuarios(session)
        # Registrar un usuario
        gestor.registrar_usuario("wronguser", "password123")
        # Intentar iniciar sesión con contraseña incorrecta
        usuario = gestor.verificar_login("wronguser", "wrongpassword")
        
        assert usuario is None

    def test_contraseña_encriptada(self, session):
        gestor = GestorUsuarios(session)
        texto_plano = "segura123"
        encriptada = gestor.encriptar_contraseña(texto_plano)
        
        assert texto_plano != encriptada
        assert len(encriptada) == 64  # SHA-256 da 64 caracteres hexadecimales
        
        # Verificar que diferentes encriptaciones de la misma contraseña dan el mismo resultado
        encriptada2 = gestor.encriptar_contraseña(texto_plano)
        assert encriptada == encriptada2
