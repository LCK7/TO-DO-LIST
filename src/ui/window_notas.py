from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QLabel, QLineEdit, QTextEdit, QMessageBox,
    QDialog, QFormLayout, QDialogButtonBox, QTabWidget
)
from PyQt6.QtCore import Qt

class VentanaNotas(QWidget):
    """
    Ventana para gestionar las notas del usuario con pestañas: Todas y Favoritos.
    """

    def __init__(self, usuario, gestor_notas, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.gestor = gestor_notas
        self.volver_a_main = volver_a_main
        self.setWindowTitle(f"📝 Notas de {usuario.nombre_usuario}")
        self.setMinimumSize(900, 700)
        self.init_ui()
        self.aplicar_estilos()
        self.cargar_notas()

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
        titulo = QLabel("📝 Gestión de Notas")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Sección de agregar nota
        seccion_agregar = QHBoxLayout()
        self.btn_agregar = QPushButton("+ Agregar Nueva Nota")
        self.btn_agregar.setObjectName("btn_agregar")
        self.btn_agregar.clicked.connect(self.agregar_nota)
        seccion_agregar.addWidget(self.btn_agregar)
        seccion_agregar.addStretch()
        layout_principal.addLayout(seccion_agregar)
        
        # Tabs para todas y favoritos
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs_notas")
        self.tab_todas = QWidget()
        self.tab_favoritos = QWidget()
        self.tabs.addTab(self.tab_todas, "🗒️ Todas")
        self.tabs.addTab(self.tab_favoritos, "⭐ Favoritos")
        self.tabs.currentChanged.connect(self.cargar_notas)
        layout_principal.addWidget(self.tabs)

        # Lista de notas para cada tab
        self.lista_todas = QListWidget()
        self.lista_todas.setObjectName("lista_notas")
        self.lista_todas.itemDoubleClicked.connect(self.editar_nota_seleccionada)
        self.lista_favoritos = QListWidget()
        self.lista_favoritos.setObjectName("lista_notas")
        self.lista_favoritos.itemDoubleClicked.connect(self.editar_nota_seleccionada)

        # Layout para tab todas
        layout_todas = QVBoxLayout()
        layout_todas.addWidget(self.lista_todas)
        self.tab_todas.setLayout(layout_todas)

        # Layout para tab favoritos
        layout_favoritos = QVBoxLayout()
        layout_favoritos.addWidget(self.lista_favoritos)
        self.tab_favoritos.setLayout(layout_favoritos)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_favorito = QPushButton("⭐ Favorito")
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_favorito.setObjectName("btn_favorito")
        self.btn_eliminar.setObjectName("btn_eliminar")
        self.btn_editar.clicked.connect(self.editar_nota_seleccionada)
        self.btn_favorito.clicked.connect(self.cambiar_favorito)
        self.btn_eliminar.clicked.connect(self.eliminar_nota)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_favorito)
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
            QTabWidget#tabs_notas::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
            QTabWidget#tabs_notas::tab-bar {
                alignment: center;
            }
            QTabWidget#tabs_notas QTabBar::tab {
                background-color: #e9ecef;
                color: #222;
                border: 1px solid #dee2e6;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabWidget#tabs_notas QTabBar::tab:selected {
                background-color: #ffffff;
                color: #222;
                border-bottom-color: #ffffff;
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
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btn_agregar:hover {
                background-color: #218838;
            }
            QListWidget#lista_notas {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget#lista_notas::item {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }
            QListWidget#lista_notas::item:selected {
                background-color: #007bff;
                color: #fff;
            }
            QListWidget#lista_notas::item:selected:hover {
                background-color: #66b3ff;
                color: #222;
            }
            QListWidget#lista_notas::item:hover {
                background-color: #e9ecef;
            }
            QPushButton#btn_editar {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_editar:hover {
                background-color: #e0a800;
            }
            QPushButton#btn_favorito {
                background-color: #fd7e14;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_favorito:hover {
                background-color: #e8670f;
            }
            QPushButton#btn_eliminar {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_eliminar:hover {
                background-color: #c82333;
            }
        """)

    def cargar_notas(self):
        # Determina el tab activo
        tab = self.tabs.currentIndex()
        notas = self.gestor.obtener_todas(self.usuario.id)
        if tab == 0:  # Todas
            self.lista_todas.clear()
            for nota in notas:
                self._agregar_nota_a_lista(self.lista_todas, nota)
        else:  # Favoritos
            self.lista_favoritos.clear()
            for nota in notas:
                if nota.estado_favorito:
                    self._agregar_nota_a_lista(self.lista_favoritos, nota)

    def _agregar_nota_a_lista(self, lista, nota):
        favorito_icon = "⭐" if nota.estado_favorito else ""
        contenido_preview = nota.contenido[:80] + "..." if len(nota.contenido) > 80 else nota.contenido
        texto = f"{favorito_icon} {nota.titulo}\n{contenido_preview}"
        item = QListWidgetItem(texto)
        item.setData(Qt.ItemDataRole.UserRole, nota.id)
        lista.addItem(item)

    def agregar_nota(self):
        dialog = DialogNota(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            titulo, contenido = dialog.get_datos()
            self.gestor.agregar_nota(titulo, contenido, self.usuario.id)
            self.cargar_notas()

    def editar_nota_seleccionada(self):
        lista_actual = self._obtener_lista_actual()
        item_actual = lista_actual.currentItem()
        if item_actual:
            id_nota = item_actual.data(Qt.ItemDataRole.UserRole)
            notas = self.gestor.obtener_todas(self.usuario.id)
            nota_actual = next((n for n in notas if n.id == id_nota), None)
            if nota_actual:
                dialog = DialogNota(self, nota_actual.titulo, nota_actual.contenido)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    titulo, contenido = dialog.get_datos()
                    self.gestor.editar_nota(id_nota, titulo, contenido)
                    self.cargar_notas()

    def cambiar_favorito(self):
        lista_actual = self._obtener_lista_actual()
        item_actual = lista_actual.currentItem()
        if item_actual:
            id_nota = item_actual.data(Qt.ItemDataRole.UserRole)
            self.gestor.cambiar_estado_favorito(id_nota)
            self.cargar_notas()

    def eliminar_nota(self):
        lista_actual = self._obtener_lista_actual()
        item_actual = lista_actual.currentItem()
        if item_actual:
            respuesta = QMessageBox.question(
                self, "Eliminar Nota", 
                "¿Estás seguro de que deseas eliminar esta nota?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                id_nota = item_actual.data(Qt.ItemDataRole.UserRole)
                self.gestor.eliminar_nota(id_nota)
                self.cargar_notas()

    def _obtener_lista_actual(self):
        if self.tabs.currentIndex() == 0:
            return self.lista_todas
        else:
            return self.lista_favoritos

    def volver(self):
        self.close()
        self.volver_a_main()


class DialogNota(QDialog):
    def __init__(self, parent, titulo="", contenido=""):
        super().__init__(parent)
        self.setWindowTitle("Nota")
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.input_titulo = QLineEdit(titulo)
        self.input_contenido = QTextEdit(contenido)
        form_layout.addRow("Título:", self.input_titulo)
        form_layout.addRow("Contenido:", self.input_contenido)
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(botones)
        self.setLayout(layout)
    
    def get_datos(self):
        return self.input_titulo.text(), self.input_contenido.toPlainText()