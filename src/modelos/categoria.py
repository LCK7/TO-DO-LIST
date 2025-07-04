from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.modelos.base import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="categorias")
    tareas = relationship("Tarea", back_populates="categoria")
    
    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"