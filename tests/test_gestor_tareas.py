import unittest
import os
import sqlite3
from src.gestores.gestor_tareas import GestorTareas
from src.modelos.tareas import Tarea

class TestGestorTareas(unittest.TestCase):
    def setUp(self):
        self.nombre_bd = "test_tareas.db"
        self.gestor = GestorTareas(self.nombre_bd)
        self.gestor.conexion.execute("CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY, nombre_usuario TEXT, contraseña TEXT);")
        self.gestor.conexion.execute("CREATE TABLE IF NOT EXISTS categorias(id INTEGER PRIMARY KEY, nombre TEXT, usuario_id INTEGER);")
        self.gestor.conexion.execute("INSERT INTO usuarios(nombre_usuario, contraseña) VALUES ('testuser', '1234');")
        self.usuario_id = self.gestor.conexion.execute("SELECT id FROM usuarios WHERE nombre_usuario = 'testuser';").fetchone()[0]
        self.categoria_id = self.gestor.crear_categoria_si_no_existe("Trabajo", self.usuario_id)

    def tearDown(self):
        self.gestor.cerrar_conexion()
        os.remove(self.nombre_bd)

    def test_agregar_y_listar_tarea(self):
        self.gestor.agregar_tarea("Aprender PyQt", self.usuario_id, "2025-07-01", self.categoria_id)
        tareas = self.gestor.obtener_todas(self.usuario_id)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0].descripcion, "Aprender PyQt")
        self.assertEqual(tareas[0].categoria, "Trabajo")

    def test_editar_tarea(self):
        self.gestor.agregar_tarea("Tarea antigua", self.usuario_id, "2025-07-01", self.categoria_id)
        tarea = self.gestor.obtener_todas(self.usuario_id)[0]
        nueva_categoria_id = self.gestor.crear_categoria_si_no_existe("Universidad", self.usuario_id)
        self.gestor.editar_tarea(tarea.id, "Tarea actualizada", "2025-08-01", nueva_categoria_id)
        tarea_editada = self.gestor.obtener_todas(self.usuario_id)[0]
        self.assertEqual(tarea_editada.descripcion, "Tarea actualizada")
        self.assertEqual(tarea_editada.fecha_limite, "2025-08-01")
        self.assertEqual(tarea_editada.categoria, "Universidad")

    def test_cambiar_estado(self):
        self.gestor.agregar_tarea("Completar diseño", self.usuario_id, "2025-07-15", self.categoria_id)
        tarea = self.gestor.obtener_todas(self.usuario_id)[0]
        self.assertFalse(tarea.estado)
        self.gestor.cambiar_estado(tarea.id, True)
        tarea_actualizada = self.gestor.obtener_todas(self.usuario_id)[0]
        self.assertTrue(tarea_actualizada.estado)

    def test_eliminar_tarea(self):
        self.gestor.agregar_tarea("Eliminarme", self.usuario_id, "2025-07-20", self.categoria_id)
        tarea = self.gestor.obtener_todas(self.usuario_id)[0]
        self.gestor.eliminar_tarea(tarea.id)
        tareas_restantes = self.gestor.obtener_todas(self.usuario_id)
        self.assertEqual(len(tareas_restantes), 0)

if __name__ == "__main__":
    unittest.main()
