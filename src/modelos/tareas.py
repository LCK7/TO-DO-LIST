class Tarea:
    """
    Representa una tarea de un usuario, con opción a marcar estado,
    agregar fecha límite y asignarla a una categoría.

    Atributos:
    - id (int): Identificador único de la tarea.
    - descripcion (str): Descripción de la tarea.
    - estado (bool): Estado de la tarea (True = completada, False = pendiente).
    - fecha_limite (str | None): Fecha límite de la tarea (opcional).
    - categoria_id (int | None): ID de la categoría asociada (opcional).
    - usuario_id (int | None): ID del usuario dueño de la tarea (opcional).
    - categoria (str): Nombre de la categoría (por defecto "Sin Categoría").
    """

    def __init__(
        self,
        id: int,
        descripcion: str,
        estado: bool = False,
        fecha_limite=None,
        categoria_id=None,
        usuario_id=None,
        categoria: str = "Sin Categoría"
    ):
        """
        Inicializa una nueva instancia de la clase Tarea.

        Parámetros:
        - id (int): ID de la tarea.
        - descripcion (str): Descripción de la tarea.
        - estado (bool): Estado de la tarea (por defecto False).
        - fecha_limite (str | None): Fecha límite de la tarea.
        - categoria_id (int | None): ID de la categoría asociada.
        - usuario_id (int | None): ID del usuario propietario.
        - categoria (str): Nombre de la categoría.
        """
        self.id = id
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_limite = fecha_limite
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id
        self.categoria = categoria

    def definir_estado(self):
        """
        Marca la tarea como completada (estado = True).
        """
        self.estado = True

    def __str__(self):
        """
        Devuelve una representación en texto de la tarea.

        Retorna:
        - str: Cadena con el ID, descripción, estado y fecha límite si está definida.
        """
        estado = "Tarea Completada" if self.estado else "Pendiente"
        fecha = f" | Fecha límite: {self.fecha_limite}" if self.fecha_limite else ""
        return f"Tarea #{self.id}: {self.descripcion} - {estado}{fecha}"
