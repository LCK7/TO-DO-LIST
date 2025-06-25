class Nota:
    """
    Representa una nota escrita por un usuario, que puede marcarse como favorita.

    Atributos:
    - id (int): Identificador único de la nota.
    - titulo (str): Título de la nota.
    - contenido (str): Texto o contenido de la nota.
    - estadoFavorito (bool): Indicador de si la nota está marcada como favorita.
    - usuario_id (int | None): ID del usuario al que pertenece la nota.
    """

    def __init__(self, id: int, titulo: str, contenido: str, estadoFavorito: bool = False, usuario_id=None):
        """
        Inicializa una nueva instancia de la clase Nota.

        Parámetros:
        - id (int): ID único de la nota.
        - titulo (str): Título de la nota.
        - contenido (str): Cuerpo del texto de la nota.
        - estadoFavorito (bool): Estado de favorito (por defecto False).
        - usuario_id (int | None): ID del usuario propietario (opcional).
        """
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.estadoFavorito = estadoFavorito
        self.usuario_id = usuario_id

    def estado_favorito(self):
        """
        Marca la nota como favorita estableciendo `estadoFavorito` a True.
        """
        self.estadoFavorito = True

    def __str__(self):
        """
        Devuelve una representación en texto de la nota.

        Retorna:
        - str: Cadena compuesta por el título y el contenido.
        """
        return f"{self.titulo}\n{self.contenido}"

    
    