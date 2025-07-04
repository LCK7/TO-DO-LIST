import pytest
from datetime import datetime, timedelta
from src.gestores.gestor_tareas import GestorTareas
from src.gestores.gestor_categoria import GestorCategoria
from src.modelos.usuario import Usuario
from src.modelos.tareas import Tarea
from src.modelos.categoria import Categoria

class TestGestorTareas:
    """Tests para GestorTareas con SQLAlchemy."""

    @pytest.fixture
    def usuario(self, session):
        """Crea un usuario de prueba."""
        usuario = Usuario(nombre_usuario="testuser", contraseña="encriptada")
        session.add(usuario)
        session.commit()
        return usuario

    @pytest.fixture
    def categoria(self, session, usuario):
        """Crea una categoría de prueba."""
        categoria = Categoria(nombre="Trabajo", usuario_id=usuario.id)
        session.add(categoria)
        session.commit()
        return categoria

    def test_agregar_y_obtener_tarea(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        tarea = gestor.agregar_tarea(
            descripcion="Aprender PyQt",
            usuario_id=usuario.id,
            fecha_limite=fecha_limite,
            categoria_id=categoria.id
        )
        
        assert tarea.id is not None
        assert tarea.descripcion == "Aprender PyQt"
        assert tarea.usuario_id == usuario.id
        assert tarea.categoria_id == categoria.id
        assert tarea.estado is False
        
        # Verificar que se puede obtener la tarea
        tareas = gestor.obtener_todas(usuario.id)
        assert len(tareas) == 1
        assert tareas[0].descripcion == "Aprender PyQt"

    def test_obtener_pendientes(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear una tarea pendiente
        tarea1 = gestor.agregar_tarea("Tarea pendiente", usuario.id, fecha_limite, categoria.id)
        
        # Crear una tarea completada
        tarea2 = gestor.agregar_tarea("Tarea completada", usuario.id, fecha_limite, categoria.id)
        gestor.marcar_completada(tarea2.id)
        
        # Verificar que solo se obtiene la tarea pendiente
        tareas_pendientes = gestor.obtener_pendientes(usuario.id)
        assert len(tareas_pendientes) == 1
        assert tareas_pendientes[0].descripcion == "Tarea pendiente"
        assert tareas_pendientes[0].estado is False

    def test_obtener_completadas(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear una tarea pendiente
        tarea1 = gestor.agregar_tarea("Tarea pendiente", usuario.id, fecha_limite, categoria.id)
        
        # Crear una tarea completada
        tarea2 = gestor.agregar_tarea("Tarea completada", usuario.id, fecha_limite, categoria.id)
        gestor.marcar_completada(tarea2.id)
        
        # Verificar que solo se obtiene la tarea completada
        tareas_completadas = gestor.obtener_completadas(usuario.id)
        assert len(tareas_completadas) == 1
        assert tareas_completadas[0].descripcion == "Tarea completada"
        assert tareas_completadas[0].estado is True
        assert tareas_completadas[0].fecha_completado is not None

    def test_obtener_por_categoria(self, session, usuario):
        gestor = GestorTareas(session)
        gestor_categoria = GestorCategoria(session)
        
        # Crear dos categorías
        categoria1 = Categoria(nombre="Trabajo", usuario_id=usuario.id)
        categoria2 = Categoria(nombre="Personal", usuario_id=usuario.id)
        session.add_all([categoria1, categoria2])
        session.commit()
        
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear tareas en diferentes categorías
        tarea1 = gestor.agregar_tarea("Tarea trabajo", usuario.id, fecha_limite, categoria1.id)
        tarea2 = gestor.agregar_tarea("Tarea personal", usuario.id, fecha_limite, categoria2.id)
        
        # Verificar que se filtran correctamente por categoría
        tareas_trabajo = gestor.obtener_por_categoria(usuario.id, categoria1.id)
        assert len(tareas_trabajo) == 1
        assert tareas_trabajo[0].descripcion == "Tarea trabajo"
        
        tareas_personal = gestor.obtener_por_categoria(usuario.id, categoria2.id)
        assert len(tareas_personal) == 1
        assert tareas_personal[0].descripcion == "Tarea personal"

    def test_editar_tarea(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite_original = datetime.now().date() + timedelta(days=7)
        fecha_limite_nueva = datetime.now().date() + timedelta(days=14)
        
        # Crear una tarea
        tarea = gestor.agregar_tarea("Tarea original", usuario.id, fecha_limite_original, categoria.id)
        
        # Crear otra categoría
        nueva_categoria = Categoria(nombre="Universidad", usuario_id=usuario.id)
        session.add(nueva_categoria)
        session.commit()
        
        # Editar la tarea
        resultado = gestor.editar_tarea(
            tarea.id,
            "Tarea editada",
            fecha_limite_nueva,
            nueva_categoria.id
        )
        
        assert resultado is True
        
        # Verificar que la tarea se actualizó correctamente
        tarea_actualizada = gestor.obtener_todas(usuario.id)[0]
        assert tarea_actualizada.descripcion == "Tarea editada"
        assert tarea_actualizada.fecha_limite == fecha_limite_nueva
        assert tarea_actualizada.categoria_id == nueva_categoria.id

    def test_cambiar_estado(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear una tarea
        tarea = gestor.agregar_tarea("Tarea de prueba", usuario.id, fecha_limite, categoria.id)
        assert tarea.estado is False
        
        # Cambiar a completada
        resultado = gestor.cambiar_estado(tarea.id, True)
        assert resultado is True
        
        tarea_actualizada = gestor.obtener_todas(usuario.id)[0]
        assert tarea_actualizada.estado is True
        assert tarea_actualizada.fecha_completado is not None
        
        # Cambiar a pendiente
        resultado = gestor.cambiar_estado(tarea.id, False)
        assert resultado is True
        
        tarea_actualizada = gestor.obtener_todas(usuario.id)[0]
        assert tarea_actualizada.estado is False
        assert tarea_actualizada.fecha_completado is None

    def test_eliminar_tarea(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear una tarea
        tarea = gestor.agregar_tarea("Tarea para eliminar", usuario.id, fecha_limite, categoria.id)
        
        # Verificar que existe
        tareas = gestor.obtener_todas(usuario.id)
        assert len(tareas) == 1
        
        # Eliminar la tarea
        resultado = gestor.eliminar_tarea(tarea.id)
        assert resultado is True
        
        # Verificar que ya no existe
        tareas = gestor.obtener_todas(usuario.id)
        assert len(tareas) == 0

    def test_obtener_estadisticas(self, session, usuario, categoria):
        gestor = GestorTareas(session)
        fecha_limite = datetime.now().date() + timedelta(days=7)
        
        # Crear tres tareas: 2 pendientes, 1 completada
        tarea1 = gestor.agregar_tarea("Tarea 1", usuario.id, fecha_limite, categoria.id)
        tarea2 = gestor.agregar_tarea("Tarea 2", usuario.id, fecha_limite, categoria.id)
        tarea3 = gestor.agregar_tarea("Tarea 3", usuario.id, fecha_limite, categoria.id)
        
        gestor.marcar_completada(tarea1.id)
        
        # Verificar estadísticas
        estadisticas = gestor.obtener_estadisticas(usuario.id)
        assert estadisticas['total'] == 3
        assert estadisticas['completadas'] == 1
        assert estadisticas['pendientes'] == 2
        assert estadisticas['porcentaje_completado'] == 33.3  # 1/3 = 33.3%
