from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox,
    QInputDialog
)
from PyQt6.QtCore import Qt
from src.gestores.gestor_categoria import GestorCategoria
from src.gestores.gestor_tareas import GestorTareas

class VentanaGestionCategoria(QWidget):
    def __init__(self, usuario, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.volver_a_main = volver_a_main
        self.gestor = GestorCategoria()
        self.gestor_tareas = GestorTareas()

        self.setWindowTitle("🏷️ Gestión de Categorías")
        self.setMinimumSize(400, 500)

        self.init_ui()
        self.mostrar_categorias()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("🏷️ Categorías")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)

        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("Nombre de nueva categoría")
        layout.addWidget(self.input_categoria)

        btn_agregar = QPushButton("➕ Agregar Categoría")
        btn_agregar.clicked.connect(self.agregar_categoria)
        layout.addWidget(btn_agregar)

        self.lista_categorias = QListWidget()
        layout.addWidget(self.lista_categorias)

        # Botones Editar y Eliminar
        botones_edicion = QHBoxLayout()
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_eliminar = QPushButton("🗑️ Eliminar")

        self.btn_editar.clicked.connect(self.editar_categoria)
        self.btn_eliminar.clicked.connect(self.eliminar_categoria)

        botones_edicion.addWidget(self.btn_editar)
        botones_edicion.addWidget(self.btn_eliminar)
        layout.addLayout(botones_edicion)

        # Volver
        btn_volver = QPushButton("⬅ Volver")
        btn_volver.clicked.connect(self.volver)
        layout.addWidget(btn_volver)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', sans-serif;
            }
            
            QLabel {
                font-size: 18px;
                color: black;
            }
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #cbd5e0;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1e40af;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #cbd5e0;
                border-radius: 6px;
                font-size: 14px;
                padding: 4px;
                color: #1a202c; 
            }
        """)

        self.setLayout(layout)

    def mostrar_categorias(self):
        self.lista_categorias.clear()
        categorias = self.gestor.obtener_todas(self.usuario.id)
        for cat in categorias:
            item = QListWidgetItem(f"{cat.nombre}")
            item.setData(Qt.ItemDataRole.UserRole, cat.id)
            self.lista_categorias.addItem(item)

    def agregar_categoria(self):
        nombre = self.input_categoria.text().strip()
        if nombre:
            self.gestor.agregar_categoria(nombre, self.usuario.id)
            self.input_categoria.clear()
            self.mostrar_categorias()
        else:
            QMessageBox.warning(self, "Error", "El nombre de la categoría no puede estar vacío.")

    def eliminar_categoria(self):
        item = self.lista_categorias.currentItem()
        if item:
            id_categoria = item.data(Qt.ItemDataRole.UserRole)

            # Validar si hay tareas asociadas
            tareas_asociadas = self.gestor_tareas.obtener_tareas_categoria(self.usuario.id, id_categoria)
            if tareas_asociadas:
                QMessageBox.warning(
                    self,
                    "⚠️ No se puede eliminar",
                    "Esta categoría tiene tareas asociadas. Elimínalas o cambia su categoría antes."
                )
                return

            confirmacion = QMessageBox.question(
                self,
                "¿Eliminar categoría?",
                "¿Estás seguro de eliminar esta categoría?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmacion == QMessageBox.StandardButton.Yes:
                self.gestor.eliminar_categoria(id_categoria)
                self.mostrar_categorias()
        else:
            QMessageBox.warning(self, "Selecciona una categoría", "Por favor, selecciona una categoría para eliminar.")

    def editar_categoria(self):
        item = self.lista_categorias.currentItem()
        if item:
            id_categoria = item.data(Qt.ItemDataRole.UserRole)
            nuevo_nombre, ok = QInputDialog.getText(self, "Editar Categoría", "Nuevo nombre:", text=item.text())
            if ok and nuevo_nombre.strip():
                self.gestor.actualizar_categoria(id_categoria, nuevo_nombre.strip())
                self.mostrar_categorias()
        else:
            QMessageBox.warning(self, "Selecciona una categoría", "Selecciona una categoría para editar.")

    def volver(self):
        self.close()
        self.volver_a_main()
