
class Tarea:
    """
    Representa una tarea asociada a un usuario.
    """
    def __init__(self, id:int,descripcion:str,estado:bool =False,fecha_limite=None,categoria_id=None,usuario_id=None):
        """
        
        """
        self.id = id
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_limite = fecha_limite
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id
        
    def definir_estado(self):
        """
        """
        self.estado = True
        
    def __str__(self):
        """
        """
        estado = "Tarea Completada" if self.estado else "Pendiente"
        fecha = f" | Fecha límite: {self.fecha_limite}" if self.fecha_limite else ""
        return f"Tarea #{self.id}: {self.descripcion} - {estado}{fecha}"