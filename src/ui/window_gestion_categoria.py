from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QLabel, QLineEdit, QMessageBox, QInputDialog,
    QDialog, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class VentanaGestionCategoria(QWidget):
    """
    Ventana para gestionar las categorías del usuario.
    """

    def __init__(self, usuario, gestor_categoria, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.gestor = gestor_categoria
        self.volver_a_main = volver_a_main
        self.setWindowTitle(f"🏷️ Categorías de {usuario.nombre_usuario}")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.aplicar_estilos()
        self.cargar_categorias()

    def init_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        
        # Header solo con botón volver (izquierda)
        header_layout = QHBoxLayout()
        self.btn_volver = QPushButton("← Volver al Menú")
        self.btn_volver.setObjectName("btn_volver")
        self.btn_volver.clicked.connect(self.volver)
        header_layout.addWidget(self.btn_volver)
        header_layout.addStretch()
        layout_principal.addLayout(header_layout)

        # Título centrado
        titulo = QLabel("🏷️ Gestión de Categorías")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Botón agregar
        seccion_agregar = QHBoxLayout()
        self.btn_agregar = QPushButton("+ Agregar Nueva Categoría")
        self.btn_agregar.setObjectName("btn_agregar")
        self.btn_agregar.clicked.connect(self.agregar_categoria)
        seccion_agregar.addWidget(self.btn_agregar)
        seccion_agregar.addStretch()
        layout_principal.addLayout(seccion_agregar)
        
        # Lista de categorías
        self.lista_categorias = QListWidget()
        self.lista_categorias.setObjectName("lista_categorias")
        self.lista_categorias.itemDoubleClicked.connect(self.editar_categoria_seleccionada)
        layout_principal.addWidget(self.lista_categorias)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_eliminar.setObjectName("btn_eliminar")
        self.btn_editar.clicked.connect(self.editar_categoria_seleccionada)
        self.btn_eliminar.clicked.connect(self.eliminar_categoria)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_eliminar)
        layout_principal.addLayout(botones_layout)
        self.setLayout(layout_principal)

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #333;
            }
            QLabel#titulo_principal {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QPushButton#btn_volver {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_volver:hover {
                background-color: #5a6268;
            }
            QPushButton#btn_agregar {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btn_agregar:hover {
                background-color: #138496;
            }
            QListWidget#lista_categorias {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
            }
            QListWidget#lista_categorias::item {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                margin: 6px;
                font-weight: 500;
            }
            QListWidget#lista_categorias::item:selected {
                background-color: #17a2b8;
                color: white;
            }
            QListWidget#lista_categorias::item:hover {
                background-color: #e9ecef;
            }
            QPushButton#btn_editar {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_editar:hover {
                background-color: #e0a800;
            }
            QPushButton#btn_eliminar {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_eliminar:hover {
                background-color: #c82333;
            }
        """)

    def cargar_categorias(self):
        self.lista_categorias.clear()
        categorias = self.gestor.obtener_todas(self.usuario.id)
        for categoria in categorias:
            item = QListWidgetItem(f"🏷️ {categoria.nombre}")
            item.setData(Qt.ItemDataRole.UserRole, categoria.id)
            self.lista_categorias.addItem(item)

    def agregar_categoria(self):
        dialog = DialogCategoria(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_nombre()
            if nombre:
                self.gestor.agregar_categoria(nombre, self.usuario.id)
                self.cargar_categorias()

    def editar_categoria_seleccionada(self):
        item_actual = self.lista_categorias.currentItem()
        if item_actual:
            id_categoria = item_actual.data(Qt.ItemDataRole.UserRole)
            categorias = self.gestor.obtener_todas(self.usuario.id)
            categoria_actual = next((c for c in categorias if c.id == id_categoria), None)
            if categoria_actual:
                dialog = DialogCategoria(self, categoria_actual.nombre)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    nuevo_nombre = dialog.get_nombre()
                    if nuevo_nombre:
                        self.gestor.actualizar_categoria(id_categoria, nuevo_nombre)
                        self.cargar_categorias()

    def eliminar_categoria(self):
        item_actual = self.lista_categorias.currentItem()
        if item_actual:
            respuesta = QMessageBox.question(
                self, "Eliminar Categoría", 
                "¿Estás seguro de que deseas eliminar esta categoría?\n"
                "Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                id_categoria = item_actual.data(Qt.ItemDataRole.UserRole)
                self.gestor.eliminar_categoria(id_categoria)
                self.cargar_categorias()

    def volver(self):
        self.close()
        self.volver_a_main()

class DialogCategoria(QDialog):
    def __init__(self, parent, nombre=""):
        super().__init__(parent)
        self.setWindowTitle("Categoría")
        self.setMinimumSize(300, 150)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.input_nombre = QLineEdit(nombre)
        self.input_nombre.setPlaceholderText("Nombre de la categoría")
        form_layout.addRow("Nombre:", self.input_nombre)
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(botones)
        self.setLayout(layout)
        # Aplicar estilos
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #17a2b8;
            }
        """)
   
    def get_nombre(self):
        return self.input_nombre.text().strip()