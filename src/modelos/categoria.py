class Categoria:
    """
    Representa una categoría a la que pueden pertenecer tareas.

    Atributos:
    - id (int): Identificador único de la categoría.
    - nombre (str): Nombre de la categoría.
    - usuario_id (int): ID del usuario propietario de la categoría.
    """

    def __init__(self, id, nombre, usuario_id):
        """
        Inicializa una nueva instancia de la clase Categoria.

        Parámetros:
        - id (int): Identificador de la categoría.
        - nombre (str): Nombre de la categoría.
        - usuario_id (int): ID del usuario al que pertenece la categoría.
        """
        self.id = id
        self.nombre = nombre
        self.usuario_id = usuario_id

    def __str__(self):
        """
        Devuelve una representación en cadena de la categoría.

        Retorna:
        - str: Cadena con el formato '#ID - nombre'.
        """
        return f"#{self.id} - {self.nombre}"
