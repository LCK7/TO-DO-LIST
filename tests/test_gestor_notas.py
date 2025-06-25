import unittest
import os
import sqlite3
from src.gestores.gestor_nota import GestorNotas
from src.modelos.nota import Nota

class TestGestorNotas(unittest.TestCase):
    def setUp(self):
        self.nombre_bd = "test_notas.db"
        self.gestor = GestorNotas(self.nombre_bd)

        # Crear tabla de usuarios y agregar uno
        self.gestor.conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT, contraseña TEXT
            );
        """)
        self.gestor.conexion.execute("INSERT INTO usuarios(nombre_usuario, contraseña) VALUES ('testuser', '1234');")
        self.usuario_id = self.gestor.conexion.execute("SELECT id FROM usuarios WHERE nombre_usuario = 'testuser';").fetchone()[0]

    def tearDown(self):
        self.gestor.cerrar_conexion()
        os.remove(self.nombre_bd)

    def test_agregar_y_obtener_nota(self):
        self.gestor.agregar_nota("Título A", "Contenido A", self.usuario_id)
        notas = self.gestor.obtener_todas(self.usuario_id)
        self.assertEqual(len(notas), 1)
        self.assertEqual(notas[0].titulo, "Título A")
        self.assertEqual(notas[0].contenido, "Contenido A")
        self.assertFalse(notas[0].estadoFavorito)

    def test_cambiar_estado_favorito(self):
        self.gestor.agregar_nota("Mi Favorita", "Contenido importante", self.usuario_id)
        nota = self.gestor.obtener_todas(self.usuario_id)[0]
        self.gestor.cambiar_estado_favorito(nota.id)
        nota_fav = self.gestor.obtener_todas(self.usuario_id)[0]
        self.assertTrue(nota_fav.estadoFavorito)

    def test_editar_nota(self):
        self.gestor.agregar_nota("Nota vieja", "Contenido viejo", self.usuario_id)
        nota = self.gestor.obtener_todas(self.usuario_id)[0]
        self.gestor.editar_nota(nota.id, "Nota nueva", "Contenido nuevo")
        actualizada = self.gestor.obtener_todas(self.usuario_id)[0]
        self.assertEqual(actualizada.titulo, "Nota nueva")
        self.assertEqual(actualizada.contenido, "Contenido nuevo")

    def test_eliminar_nota(self):
        self.gestor.agregar_nota("Temporal", "Para borrar", self.usuario_id)
        nota = self.gestor.obtener_todas(self.usuario_id)[0]
        self.gestor.eliminar_nota(nota.id)
        notas = self.gestor.obtener_todas(self.usuario_id)
        self.assertEqual(len(notas), 0)

if __name__ == "__main__":
    unittest.main()
