import unittest
import os
import sqlite3
from src.gestores.gestor_usuarios import GestorUsuarios
from src.modelos.usuario import Usuario

class TestGestorUsuarios(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test. Usa una base de datos temporal."""
        self.nombre_bd = "test_usuarios.db"
        self.gestor = GestorUsuarios(self.nombre_bd)

    def tearDown(self):
        """Se ejecuta después de cada test. Borra la base de datos temporal."""
        self.gestor.conexion.close()
        os.remove(self.nombre_bd)

    def test_registro_usuario_nuevo(self):
        resultado = self.gestor.registrar_usuario("testuser", "1234")
        self.assertTrue(resultado)

    def test_registro_usuario_duplicado(self):
        self.gestor.registrar_usuario("testuser", "1234")
        resultado = self.gestor.registrar_usuario("testuser", "5678")
        self.assertFalse(resultado)

    def test_verificar_login_exitoso(self):
        self.gestor.registrar_usuario("loginuser", "mypassword")
        usuario = self.gestor.verificar_login("loginuser", "mypassword")
        self.assertIsNotNone(usuario)
        self.assertIsInstance(usuario, Usuario)
        print("Usuario devuelto:", usuario)
        print("Tipo:", type(usuario))
        if usuario:
            print("Nombre de usuario:", usuario.nombre_usuario)
        self.assertEqual(usuario.nombre_usuario, "loginuser") # type: ignore


    def test_verificar_login_fallido(self):
        self.gestor.registrar_usuario("wronguser", "password123")
        usuario = self.gestor.verificar_login("wronguser", "wrongpassword")
        self.assertIsNone(usuario)

    def test_contraseña_encriptada(self):
        texto_plano = "segura123"
        encriptada = self.gestor.encriptar_contraseña(texto_plano)
        self.assertNotEqual(texto_plano, encriptada)
        self.assertEqual(len(encriptada), 64)  # SHA-256 da 64 caracteres hexadecimales

if __name__ == '__main__':
    unittest.main()
