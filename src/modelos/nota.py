
class Nota:
    
    def __init__(self,id:int,titulo:str,contenido:str,estadoFavorito:bool=False,usuario_id=None):
        """
        """
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.estadoFavorito = estadoFavorito
        self.usuario_id = usuario_id
        
    def estado_favorito(self):
        """
        """
        self.estadoFavorito = True
        
    def __str__(self):
        """
        """
        return f"{self.titulo}\n{self.contenido}"
    
    