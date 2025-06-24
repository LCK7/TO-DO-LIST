class Categoria:
    """
    """
    def __init__(self,id,nombre,usuario_id):
        """
        """
        self.id = id
        self.nombre = nombre
        self.usuario_id = usuario_id
    def __str__(self):
        """
        """
        return f"#{self.id} - {self.nombre}"