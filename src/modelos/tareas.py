from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.modelos.base import Base

class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    estado = Column(Boolean, default=False)
    fecha_limite = Column(Date, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_completado = Column(DateTime, nullable=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="tareas")
    categoria = relationship("Categoria", back_populates="tareas")
    
    def __repr__(self):
        return f"<Tarea(id={self.id}, descripcion='{self.descripcion}', estado={self.estado})>"
    
    def marcar_completada(self):
        """Marca la tarea como completada y registra la fecha"""
        self.estado = True
        self.fecha_completado = func.now()
    
    def marcar_pendiente(self):
        """Marca la tarea como pendiente"""
        self.estado = False
        self.fecha_completado = None