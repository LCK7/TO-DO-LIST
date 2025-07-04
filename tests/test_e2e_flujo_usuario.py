import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import os
import tempfile
import sys

# Asegurarse de que el directorio de la aplicación esté en sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelos.base import Base
from src.gestores.gestor_usuarios import GestorUsuarios
from src.gestores.gestor_tareas import GestorTareas
from src.gestores.gestor_categoria import GestorCategoria
from src.gestores.gestor_nota import GestorNotas
from src.modelos.usuario import Usuario
from src.modelos.tareas import Tarea
from src.modelos.categoria import Categoria
from src.modelos.nota import Nota

class TestEndToEnd:
    """
    Prueba de flujo completo de un usuario que:
    1. Se registra
    2. Inicia sesión
    3. Crea categorías
    4. Crea tareas en diferentes categorías
    5. Completa algunas tareas
    6. Crea notas
    7. Marca notas como favoritas
    8. Consulta estadísticas
    """
    
    @pytest.fixture
    def setup_database(self):
        """Configurar una base de datos temporal para las pruebas E2E."""
        # Crear una base de datos temporal en SQLite
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        engine = create_engine(f"sqlite:///{db_path}", echo=False)
        
        # Crear tablas
        Base.metadata.create_all(engine)
        
        # Crear sesión
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        # Cerrar y limpiar después de las pruebas
        session.close()
        os.close(db_fd)
        try:
            os.unlink(db_path)
        except PermissionError:
            # En Windows a veces no se puede eliminar inmediatamente
            print(f"Nota: No se pudo eliminar {db_path} (problema común en Windows)")
        
    def test_flujo_completo_usuario(self, setup_database):
        """Test de flujo completo de uso de la aplicación."""
        session = setup_database
        
        # Inicializar gestores
        gestor_usuarios = GestorUsuarios(session)
        gestor_tareas = GestorTareas(session)
        gestor_categoria = GestorCategoria(session)
        gestor_notas = GestorNotas(session)
        
        # 1. Registro de usuario
        resultado_registro = gestor_usuarios.registrar_usuario("usuario_test", "contraseña123")
        assert resultado_registro is True
        
        # 2. Inicio de sesión
        usuario = gestor_usuarios.verificar_login("usuario_test", "contraseña123")
        assert usuario is not None
        assert usuario.nombre_usuario == "usuario_test"
        
        # 3. Creación de categorías
        gestor_categoria.agregar_categoria("Trabajo", usuario.id)
        gestor_categoria.agregar_categoria("Personal", usuario.id)
        gestor_categoria.agregar_categoria("Estudios", usuario.id)
        
        categorias = gestor_categoria.obtener_todas(usuario.id)
        assert len(categorias) == 3
        
        # Mapear nombres a IDs para usar más adelante
        categoria_trabajo = next(cat for cat in categorias if cat.nombre == "Trabajo")
        categoria_personal = next(cat for cat in categorias if cat.nombre == "Personal")
        categoria_estudios = next(cat for cat in categorias if cat.nombre == "Estudios")
        
        # 4. Creación de tareas
        fecha_hoy = datetime.date.today()
        fecha_manana = fecha_hoy + datetime.timedelta(days=1)
        fecha_semana = fecha_hoy + datetime.timedelta(days=7)
        
        # Tareas de trabajo
        tarea_trabajo1 = gestor_tareas.agregar_tarea(
            "Enviar informe", usuario.id, fecha_manana, categoria_trabajo.id
        )
        tarea_trabajo2 = gestor_tareas.agregar_tarea(
            "Actualizar CV", usuario.id, fecha_semana, categoria_trabajo.id
        )
        
        # Tareas personales
        tarea_personal1 = gestor_tareas.agregar_tarea(
            "Comprar regalo", usuario.id, fecha_manana, categoria_personal.id
        )
        
        # Tareas de estudio
        tarea_estudio1 = gestor_tareas.agregar_tarea(
            "Estudiar SQLAlchemy", usuario.id, fecha_hoy, categoria_estudios.id
        )
        tarea_estudio2 = gestor_tareas.agregar_tarea(
            "Practicar PyQt", usuario.id, fecha_semana, categoria_estudios.id
        )
        
        # Verificar que hay 5 tareas en total
        todas_tareas = gestor_tareas.obtener_todas(usuario.id)
        assert len(todas_tareas) == 5
        
        # Verificar tareas por categoría
        tareas_trabajo = gestor_tareas.obtener_por_categoria(usuario.id, categoria_trabajo.id)
        assert len(tareas_trabajo) == 2
        
        tareas_estudios = gestor_tareas.obtener_por_categoria(usuario.id, categoria_estudios.id)
        assert len(tareas_estudios) == 2
        
        # 5. Completar algunas tareas
        gestor_tareas.marcar_completada(tarea_trabajo1.id)
        gestor_tareas.marcar_completada(tarea_estudio1.id)
        
        # Verificar tareas completadas y pendientes
        completadas = gestor_tareas.obtener_completadas(usuario.id)
        assert len(completadas) == 2
        
        pendientes = gestor_tareas.obtener_pendientes(usuario.id)
        assert len(pendientes) == 3
        
        # 6. Creación de notas
        gestor_notas.agregar_nota("Ideas de proyecto", "1. Aplicación de tareas\n2. Gestor de gastos", usuario.id)
        gestor_notas.agregar_nota("Receta", "Ingredientes:\n- Harina\n- Huevos\n- Azúcar", usuario.id)
        gestor_notas.agregar_nota("Links útiles", "- SQLAlchemy: https://www.sqlalchemy.org\n- PyQt: https://doc.qt.io", usuario.id)
        
        # Verificar notas
        notas = gestor_notas.obtener_todas(usuario.id)
        assert len(notas) == 3
        
        # 7. Marcar notas como favoritas
        nota_links = next(nota for nota in notas if nota.titulo == "Links útiles")
        gestor_notas.cambiar_estado_favorito(nota_links.id)
        
        # Verificar nota favorita
        notas_actualizadas = gestor_notas.obtener_todas(usuario.id)
        nota_favorita = next(nota for nota in notas_actualizadas if nota.titulo == "Links útiles")
        assert nota_favorita.estado_favorito is True
        
        # 8. Consultar estadísticas
        estadisticas = gestor_tareas.obtener_estadisticas(usuario.id)
        assert estadisticas['total'] == 5
        assert estadisticas['completadas'] == 2
        assert estadisticas['pendientes'] == 3
        assert estadisticas['porcentaje_completado'] == 40.0  # 2/5 = 40%
