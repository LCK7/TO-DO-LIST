import pytest
from src.gestores.gestor_categoria import GestorCategoria
from src.modelos.usuario import Usuario
from src.modelos.categoria import Categoria

class TestGestorCategoria:
    """Tests para GestorCategoria con SQLAlchemy."""

    @pytest.fixture
    def usuario(self, session):
        """Crea un usuario de prueba."""
        usuario = Usuario(nombre_usuario="testuser", contraseña="encriptada")
        session.add(usuario)
        session.commit()
        return usuario

    def test_agregar_y_obtener_categoria(self, session, usuario):
        gestor = GestorCategoria(session)
        
        # Agregar una categoría
        gestor.agregar_categoria("Trabajo", usuario.id)
        
        # Verificar que se puede obtener
        categorias = gestor.obtener_todas(usuario.id)
        assert len(categorias) == 1
        assert categorias[0].nombre == "Trabajo"
        assert categorias[0].usuario_id == usuario.id

    def test_obtener_todas_categorias(self, session, usuario):
        gestor = GestorCategoria(session)
        
        # Agregar varias categorías
        gestor.agregar_categoria("Trabajo", usuario.id)
        gestor.agregar_categoria("Personal", usuario.id)
        gestor.agregar_categoria("Estudios", usuario.id)
        
        # Crear otro usuario con sus propias categorías
        otro_usuario = Usuario(nombre_usuario="otro_user", contraseña="encriptada")
        session.add(otro_usuario)
        session.commit()
        
        gestor.agregar_categoria("Viajes", otro_usuario.id)
        
        # Verificar que obtener_todas solo devuelve las categorías del usuario
        categorias_usuario1 = gestor.obtener_todas(usuario.id)
        assert len(categorias_usuario1) == 3
        nombres = [cat.nombre for cat in categorias_usuario1]
        assert "Trabajo" in nombres
        assert "Personal" in nombres
        assert "Estudios" in nombres
        
        categorias_usuario2 = gestor.obtener_todas(otro_usuario.id)
        assert len(categorias_usuario2) == 1
        assert categorias_usuario2[0].nombre == "Viajes"

    def test_eliminar_categoria(self, session, usuario):
        gestor = GestorCategoria(session)
        
        # Agregar categorías
        gestor.agregar_categoria("Para eliminar", usuario.id)
        gestor.agregar_categoria("Para mantener", usuario.id)
        
        # Obtener la categoría a eliminar
        categorias = gestor.obtener_todas(usuario.id)
        categoria_eliminar = next(cat for cat in categorias if cat.nombre == "Para eliminar")
        
        # Eliminar la categoría
        gestor.eliminar_categoria(categoria_eliminar.id)
        
        # Verificar que se eliminó correctamente
        categorias_actualizadas = gestor.obtener_todas(usuario.id)
        assert len(categorias_actualizadas) == 1
        assert categorias_actualizadas[0].nombre == "Para mantener"

    def test_actualizar_categoria(self, session, usuario):
        gestor = GestorCategoria(session)
        
        # Agregar una categoría
        gestor.agregar_categoria("Nombre antiguo", usuario.id)
        
        # Obtener la categoría a actualizar
        categoria = gestor.obtener_todas(usuario.id)[0]
        
        # Actualizar la categoría
        gestor.actualizar_categoria(categoria.id, "Nombre nuevo")
        
        # Verificar que se actualizó correctamente
        categorias_actualizadas = gestor.obtener_todas(usuario.id)
        assert len(categorias_actualizadas) == 1
        assert categorias_actualizadas[0].nombre == "Nombre nuevo"
