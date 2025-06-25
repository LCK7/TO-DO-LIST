from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from src.gestores.gestor_nota import GestorNotas
from src.ui.dialogo_nueva_nota import DialogoNuevaNota

class VentanaNotas(QWidget):
    def __init__(self, usuario, volver_a_main):
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
        self.lista.clear()
        notas = self.gestor.obtener_todas(self.usuario.id)
        notas.sort(key=lambda n: not n.estadoFavorito)
        for nota in notas:
            texto = f"⭐ {nota.titulo}" if nota.estadoFavorito else nota.titulo
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, nota)
            self.lista.addItem(item)

    def crear_nota(self):
        dialogo = DialogoNuevaNota()
        if dialogo.exec():
            titulo, contenido = dialogo.get_data()
            self.gestor.agregar_nota(titulo, contenido, self.usuario.id)
            self.cargar_notas()

    def editar_nota(self, item):
        nota = item.data(Qt.ItemDataRole.UserRole)
        dialogo = DialogoNuevaNota(nota)
        if dialogo.exec():
            nuevo_titulo, nuevo_contenido = dialogo.get_data()
            self.gestor.editar_nota(nota.id, nuevo_titulo, nuevo_contenido)
            self.cargar_notas()
        else:
            self.opciones_nota(nota)

    def opciones_nota(self, nota):
        msg = QMessageBox(self)
        msg.setWindowTitle("Acciones")
        msg.setText(f"📄 {nota.titulo}")
        btn_fav = msg.addButton("⭐ Marcar Favorito", QMessageBox.ButtonRole.ActionRole)
        btn_eliminar = msg.addButton("🗑️ Eliminar", QMessageBox.ButtonRole.DestructiveRole)
        msg.addButton("❌ Cancelar", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        if msg.clickedButton() == btn_fav:
            self.gestor.cambiar_estado_favorito(nota.id)
            self.cargar_notas()
        elif msg.clickedButton() == btn_eliminar:
            confirm = QMessageBox.question(self, "Eliminar", "¿Estás seguro?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.gestor.eliminar_nota(nota.id)
                self.cargar_notas()

    def volver(self):
        self.close()
        self.volver_a_main()
    
    def closeEvent(self, event:QCloseEvent): # type: ignore
        respuesta = QMessageBox.question(
            self,
            "Salir de tareas",
            "¿Deseas regresar al menú principal?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            event.ignore()
            self.hide()
            self.volver_a_main()
        else:
            self.close()
