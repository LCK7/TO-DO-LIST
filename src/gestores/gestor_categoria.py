from src.modelos.categoria import Categoria

class GestorCategoria:
    """
    Clase encargada de gestionar las operaciones relacionadas con las categorías usando SQLAlchemy.
    """
    def __init__(self, session):
        """
        Recibe una sesión SQLAlchemy para operar sobre la base de datos.
        """
        self.session = session

    def agregar_categoria(self, nombre, usuario_id):
        nueva_categoria = Categoria(nombre=nombre, usuario_id=usuario_id)
        self.session.add(nueva_categoria)
        self.session.commit()

    def obtener_todas(self, usuario_id):
        categorias = self.session.query(Categoria).filter_by(usuario_id=usuario_id).all()
        return categorias

    def eliminar_categoria(self, id_categoria):
        categoria = self.session.query(Categoria).filter_by(id=id_categoria).first()
        if categoria:
            self.session.delete(categoria)
            self.session.commit()

    def actualizar_categoria(self, id_categoria, nuevo_nombre):
        categoria = self.session.query(Categoria).filter_by(id=id_categoria).first()
        if categoria:
            categoria.nombre = nuevo_nombre
            self.session.commit()

    def cerrar_conexion(self):
        self.session.close()