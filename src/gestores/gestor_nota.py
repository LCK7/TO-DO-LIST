from src.modelos.nota import Nota

class GestorNotas:
    def __init__(self, session):
        self.session = session

    def agregar_nota(self, titulo, contenido, usuario_id):
        nueva_nota = Nota(titulo=titulo, contenido=contenido, usuario_id=usuario_id)
        self.session.add(nueva_nota)
        self.session.commit()

    def obtener_todas(self, usuario_id):
        return self.session.query(Nota).filter_by(usuario_id=usuario_id).all()

    def cambiar_estado_favorito(self, id_nota):
        nota = self.session.query(Nota).filter_by(id=id_nota).first()
        if nota:
            nota.estado_favorito = not nota.estado_favorito
            self.session.commit()

    def editar_nota(self, id_nota, nuevo_titulo, nuevo_contenido):
        nota = self.session.query(Nota).filter_by(id=id_nota).first()
        if nota:
            nota.titulo = nuevo_titulo
            nota.contenido = nuevo_contenido
            self.session.commit()

    def eliminar_nota(self, id_nota):
        nota = self.session.query(Nota).filter_by(id=id_nota).first()
        if nota:
            self.session.delete(nota)
            self.session.commit()

    def cerrar_conexion(self):
        self.session.close()