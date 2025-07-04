import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Asegurar que la BD esté en la raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "tareas.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(f"Base de datos ubicada en: {DB_PATH}")