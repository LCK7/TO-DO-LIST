class Usuario:
    """
    Representa a un usuario del sistema.

    Atributos:
    - id (int): Identificador único del usuario.
    - nombre_usuario (str): Nombre de usuario (debe ser único).
    - contraseña (str): Contraseña del usuario (almacenada de forma segura).
    """

    def __init__(self, id, nombre_usuario, contraseña):
        """
        Inicializa una nueva instancia de la clase Usuario.

        Parámetros:
        - id (int): ID único del usuario.
        - nombre_usuario (str): Nombre del usuario.
        - contraseña (str): Contraseña encriptada del usuario.
        """
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
