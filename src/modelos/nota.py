from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.modelos.base import Base

class Nota(Base):
    __tablename__ = 'notas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)  # Text para contenidos más largos
    estado_favorito = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notas")
    
    def __repr__(self):
        return f"<Nota(id={self.id}, titulo='{self.titulo}', favorito={self.estado_favorito})>"
    
    def alternar_favorito(self):
        """Alterna el estado de favorito"""
        self.estado_favorito = not self.estado_favorito