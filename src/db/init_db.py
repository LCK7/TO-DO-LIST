from src.modelos.base import Base
from src.db.conexion import engine, DB_PATH
import os
# Importar todos los modelos para que SQLAlchemy los registre
import src.modelos.usuario
import src.modelos.tareas
import src.modelos.categoria
import src.modelos.nota

def inicializar_db():
    """
    Inicializa la base de datos creando todas las tablas necesarias.
    """
    if not os.path.exists(DB_PATH):
        print(f"Creando nueva base de datos en: {DB_PATH}")
    
    Base.metadata.create_all(engine)
    print("Base de datos inicializada correctamente")