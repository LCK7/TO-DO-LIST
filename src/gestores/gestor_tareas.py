from src.modelos.tareas import Tarea
from src.modelos.categoria import Categoria
from sqlalchemy.sql import func
from datetime import datetime

class GestorTareas:
    def __init__(self, session):
        self.session = session

    def agregar_tarea(self, descripcion, usuario_id, fecha_limite, categoria_id):
        nueva_tarea = Tarea(
            descripcion=descripcion,
            usuario_id=usuario_id,
            fecha_limite=fecha_limite,
            categoria_id=categoria_id,
            estado=False
        )
        self.session.add(nueva_tarea)
        self.session.commit()
        return nueva_tarea

    def obtener_todas(self, usuario_id):
        return self.session.query(Tarea).filter_by(usuario_id=usuario_id).order_by(Tarea.fecha_creacion.desc()).all()

    def obtener_pendientes(self, usuario_id):
        """Obtiene solo las tareas pendientes"""
        return self.session.query(Tarea).filter_by(usuario_id=usuario_id, estado=False).order_by(Tarea.fecha_limite.asc()).all()

    def obtener_completadas(self, usuario_id):
        """Obtiene solo las tareas completadas"""
        return self.session.query(Tarea).filter_by(usuario_id=usuario_id, estado=True).order_by(Tarea.fecha_completado.desc()).all()

    def obtener_por_categoria(self, usuario_id, categoria_id):
        """Obtiene tareas filtradas por categoría"""
        return self.session.query(Tarea).filter_by(usuario_id=usuario_id, categoria_id=categoria_id).all()

    def editar_tarea(self, id_tarea, nueva_descripcion, nueva_fecha, nueva_categoria):
        tarea = self.session.query(Tarea).filter_by(id=id_tarea).first()
        if tarea:
            tarea.descripcion = nueva_descripcion
            tarea.fecha_limite = nueva_fecha
            tarea.categoria_id = nueva_categoria
            self.session.commit()
            return True
        return False

    def cambiar_estado(self, id_tarea, nuevo_estado: bool):
        tarea = self.session.query(Tarea).filter_by(id=id_tarea).first()
        if tarea:
            if nuevo_estado:
                tarea.marcar_completada()
                tarea.fecha_completado = datetime.now()  # Usar datetime actual
            else:
                tarea.marcar_pendiente()
            self.session.commit()
            return True
        return False

    def marcar_completada(self, id_tarea):
        """Marca específicamente una tarea como completada"""
        return self.cambiar_estado(id_tarea, True)

    def marcar_pendiente(self, id_tarea):
        """Marca específicamente una tarea como pendiente"""
        return self.cambiar_estado(id_tarea, False)

    def eliminar_tarea(self, id_tarea):
        tarea = self.session.query(Tarea).filter_by(id=id_tarea).first()
        if tarea:
            self.session.delete(tarea)
            self.session.commit()
            return True
        return False

    def obtener_estadisticas(self, usuario_id):
        """Obtiene estadísticas de las tareas del usuario"""
        total = self.session.query(Tarea).filter_by(usuario_id=usuario_id).count()
        completadas = self.session.query(Tarea).filter_by(usuario_id=usuario_id, estado=True).count()
        pendientes = total - completadas
        
        return {
            'total': total,
            'completadas': completadas,
            'pendientes': pendientes,
            'porcentaje_completado': round((completadas / total * 100) if total > 0 else 0, 1)
        }

    def cerrar_conexion(self):
        self.session.close()