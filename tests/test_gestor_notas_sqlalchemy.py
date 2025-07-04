import pytest
from src.gestores.gestor_nota import GestorNotas
from src.modelos.usuario import Usuario
from src.modelos.nota import Nota

class TestGestorNotasSQLAlchemy:
    """Tests para GestorNotas con SQLAlchemy."""

    @pytest.fixture
    def usuario(self, session):
        """Crea un usuario de prueba."""
        usuario = Usuario(nombre_usuario="testuser", contraseña="encriptada")
        session.add(usuario)
        session.commit()
        return usuario

    def test_agregar_y_obtener_nota(self, session, usuario):
        gestor = GestorNotas(session)
        
        # Agregar una nota
        gestor.agregar_nota("Título A", "Contenido A", usuario.id)
        
        # Verificar que se puede obtener
        notas = gestor.obtener_todas(usuario.id)
        assert len(notas) == 1
        assert notas[0].titulo == "Título A"
        assert notas[0].contenido == "Contenido A"
        assert not notas[0].estado_favorito

    def test_cambiar_estado_favorito(self, session, usuario):
        gestor = GestorNotas(session)
        
        # Agregar una nota
        gestor.agregar_nota("Mi Favorita", "Contenido importante", usuario.id)
        
        # Obtener la nota y cambiar estado favorito
        nota = gestor.obtener_todas(usuario.id)[0]
        gestor.cambiar_estado_favorito(nota.id)
        
        # Verificar que cambió el estado
        nota_actualizada = gestor.obtener_todas(usuario.id)[0]
        assert nota_actualizada.estado_favorito

    def test_editar_nota(self, session, usuario):
        gestor = GestorNotas(session)
        
        # Agregar una nota
        gestor.agregar_nota("Nota vieja", "Contenido viejo", usuario.id)
        
        # Editar la nota
        nota = gestor.obtener_todas(usuario.id)[0]
        gestor.editar_nota(nota.id, "Nota nueva", "Contenido nuevo")
        
        # Verificar cambios
        actualizada = gestor.obtener_todas(usuario.id)[0]
        assert actualizada.titulo == "Nota nueva"
        assert actualizada.contenido == "Contenido nuevo"

    def test_eliminar_nota(self, session, usuario):
        gestor = GestorNotas(session)
        
        # Agregar una nota
        gestor.agregar_nota("Temporal", "Para borrar", usuario.id)
        
        # Eliminar la nota
        nota = gestor.obtener_todas(usuario.id)[0]
        gestor.eliminar_nota(nota.id)
        
        # Verificar que se eliminó
        notas = gestor.obtener_todas(usuario.id)
        assert len(notas) == 0

    def test_obtener_favoritas(self, session, usuario):
        gestor = GestorNotas(session)
        
        # Agregar varias notas
        gestor.agregar_nota("Nota 1", "Contenido 1", usuario.id)
        gestor.agregar_nota("Favorita 1", "Contenido favorito 1", usuario.id)
        gestor.agregar_nota("Favorita 2", "Contenido favorito 2", usuario.id)
        
        # Marcar algunas como favoritas
        notas = gestor.obtener_todas(usuario.id)
        for nota in notas:
            if "Favorita" in nota.titulo:
                gestor.cambiar_estado_favorito(nota.id)
        
        # Obtener solo favoritas
        favoritas = [nota for nota in gestor.obtener_todas(usuario.id) if nota.estado_favorito]
        assert len(favoritas) == 2
        titulos = [nota.titulo for nota in favoritas]
        assert "Favorita 1" in titulos
        assert "Favorita 2" in titulos
