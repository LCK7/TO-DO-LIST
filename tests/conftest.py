import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración para ignorar los tests obsoletos
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "obsolete: mark test as obsolete, will be ignored"
    )

def pytest_collection_modifyitems(items):
    # Ignorar los tests marcados como obsoletos
    # y los archivos de test que no tienen "_sqlalchemy" en su nombre
    # (excepto el test_e2e_flujo_usuario.py que sí queremos ejecutar)
    for item in items:
        if "test_gestor_" in item.nodeid and "_sqlalchemy" not in item.nodeid:
            item.add_marker(pytest.mark.skip(reason="Obsolete test"))

# Asegurarse de que el directorio de la aplicación esté en sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelos.base import Base
import src.modelos.usuario
import src.modelos.tareas
import src.modelos.categoria
import src.modelos.nota

@pytest.fixture(scope="function")
def engine():
    """Crea un motor de base de datos en memoria para las pruebas."""
    return create_engine("sqlite:///:memory:", echo=False)

@pytest.fixture(scope="function")
def tables(engine):
    """Crea todas las tablas en la base de datos en memoria."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(engine, tables):
    """Crea una nueva sesión para interactuar con la base de datos."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
