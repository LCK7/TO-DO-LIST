from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from src.gestores.gestor_nota import GestorNotas
from src.ui.dialogo_nueva_nota import DialogoNuevaNota

class VentanaNotas(QWidget):
    """
    Ventana para la gestión de notas personales del usuario.

    Permite a los usuarios visualizar, crear, editar, marcar como favorito y eliminar notas.
    """
    def __init__(self, usuario, volver_a_main):
        """
        Inicializa la VentanaNotas.

        Args:
            usuario: Objeto de usuario actualmente logueado.
            volver_a_main: Función de callback para regresar a la ventana principal.
        """
        super().__init__()
        self.usuario = usuario
        self.volver_a_main = volver_a_main
        self.setWindowTitle("🗒️ Mis Notas")
        self.setMinimumSize(500, 500)

        self.gestor = GestorNotas()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.lista = QListWidget()
        self.lista.itemDoubleClicked.connect(self.editar_nota)
        layout.addWidget(self.lista)

        botones = QHBoxLayout()
        btn_nueva = QPushButton("➕ Nueva Nota")
        btn_volver = QPushButton("↩️ Volver")
        btn_nueva.clicked.connect(self.crear_nota)
        btn_volver.clicked.connect(self.volver)
        botones.addWidget(btn_nueva)
        botones.addWidget(btn_volver)

        layout.addLayout(botones)
        self.setLayout(layout)
        self.cargar_notas()

        # 🧑‍🎨 Estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2d3748;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 8px;
            }
            QListWidgetItem {
                padding: 10px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
                background-color: #3182ce;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2b6cb0;
            }
        """)

    def cargar_notas(self):
        """
        Carga y muestra todas las notas del usuario actual en la QListWidget.

        Las notas se ordenan de modo que las favoritas aparezcan primero.
        Cada elemento de la lista almacena el objeto 'Nota' completo en su UserRole.
        """
        self.lista.clear()
        notas = self.gestor.obtener_todas(self.usuario.id)
        # Ordenar para que las notas favoritas aparezcan primero
        notas.sort(key=lambda n: not n.estadoFavorito)
        for nota in notas:
            texto = f"⭐ {nota.titulo}" if nota.estadoFavorito else nota.titulo
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, nota)
            self.lista.addItem(item)
        # 

    def crear_nota(self):
        """
        Abre un diálogo para crear una nueva nota.

        Si el usuario guarda la nota en el diálogo, se agrega la nota
        a través del gestor y se recarga la lista de notas.
        """
        dialogo = DialogoNuevaNota()
        if dialogo.exec(): # Muestra el diálogo de forma modal
            titulo, contenido = dialogo.get_data()
            self.gestor.agregar_nota(titulo, contenido, self.usuario.id)
            self.cargar_notas()

    def editar_nota(self, item):
        """
        Edita la nota seleccionada al hacer doble clic.

        Abre un diálogo de edición con los datos de la nota existente.
        Si la nota se guarda en el diálogo, se actualiza a través del gestor
        y se recarga la lista. Si se cancela la edición, se muestran
        opciones adicionales para la nota (favorito/eliminar).

        Args:
            item: El QListWidgetItem que fue doble-clicado, conteniendo el objeto Nota.
        """
        nota = item.data(Qt.ItemDataRole.UserRole)
        dialogo = DialogoNuevaNota(nota) # Pasa la nota existente para edición
        if dialogo.exec():
            nuevo_titulo, nuevo_contenido = dialogo.get_data()
            self.gestor.editar_nota(nota.id, nuevo_titulo, nuevo_contenido)
            self.cargar_notas()
        else:
            # Si el usuario cierra el diálogo sin guardar (cancela la edición),
            # se le presentan opciones adicionales (eliminar/marcar favorito).
            self.opciones_nota(nota)

    def opciones_nota(self, nota):
        """
        Muestra un cuadro de diálogo con opciones para una nota específica.

        Permite al usuario marcar/desmarcar una nota como favorita o eliminarla.

        Args:
            nota: El objeto Nota sobre el cual se desean realizar acciones.
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Acciones de la Nota")
        msg.setText(f"📄 Nota: {nota.titulo}")
        
        # Botones personalizados
        btn_fav_text = "⭐ Marcar Favorito" if not nota.estadoFavorito else "🌟 Desmarcar Favorito"
        btn_fav = msg.addButton(btn_fav_text, QMessageBox.ButtonRole.ActionRole)
        btn_eliminar = msg.addButton("🗑️ Eliminar", QMessageBox.ButtonRole.DestructiveRole)
        msg.addButton("❌ Cancelar", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec() # Muestra el cuadro de diálogo y espera la interacción del usuario

        if msg.clickedButton() == btn_fav:
            self.gestor.cambiar_estado_favorito(nota.id)
            self.cargar_notas()
        elif msg.clickedButton() == btn_eliminar:
            confirm = QMessageBox.question(self, 
                                           "Confirmar Eliminación", 
                                           "¿Estás seguro de que quieres eliminar esta nota? Esta acción es irreversible.", 
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.gestor.eliminar_nota(nota.id)
                self.cargar_notas()

    def volver(self):
        """
        Cierra la ventana actual y llama a la función de callback para regresar a la ventana principal.
        """
        self.close()
        self.volver_a_main()
    
    def closeEvent(self, event: QCloseEvent): # type: ignore
        """
        Maneja el evento de cierre de la ventana.

        Al intentar cerrar la ventana directamente, pregunta al usuario si desea
        regresar al menú principal o cerrar la aplicación.

        Args:
            event: El evento de cierre (QCloseEvent).
        """
        respuesta = QMessageBox.question(
            self,
            "Salir de Notas",
            "¿Deseas regresar al menú principal?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            event.ignore() # Ignora el cierre directo
            self.hide() # Oculta la ventana
            self.volver_a_main() # Llama al callback para volver
        else:
            event.accept() # Permite que la ventana se cierre (y por ende, la aplicación si no hay otras ventanas)