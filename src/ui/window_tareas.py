from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QLabel, QLineEdit, QMessageBox, QInputDialog, QDateEdit,
    QDialog, QFormLayout, QDialogButtonBox, QComboBox, QCheckBox, QTabWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from datetime import datetime, date

class VentanaTareas(QWidget):
    """
    Ventana para gestionar las tareas del usuario con filtro de categoría y sin estadísticas.
    """

    def __init__(self, usuario, gestor_tareas, gestor_categoria, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.gestor = gestor_tareas
        self.gestor_categoria = gestor_categoria
        self.volver_a_main = volver_a_main
        self.setWindowTitle(f"📋 Tareas de {usuario.nombre_usuario}")
        self.setMinimumSize(1000, 800)
        self.init_ui()
        self.aplicar_estilos()
        self.cargar_categorias_filtro()
        self.cargar_tareas()

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
        titulo = QLabel("📋 Gestión de Tareas")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Filtro de categoría
        filtro_layout = QHBoxLayout()
        lbl_filtro = QLabel("Filtrar por categoría:")
        self.combo_filtro_categoria = QComboBox()
        self.combo_filtro_categoria.setObjectName("combo_filtro_categoria")
        self.combo_filtro_categoria.currentIndexChanged.connect(self.cargar_tareas)
        filtro_layout.addWidget(lbl_filtro)
        filtro_layout.addWidget(self.combo_filtro_categoria)
        filtro_layout.addStretch()
        layout_principal.addLayout(filtro_layout)
        
        # Botones de acción principales
        botones_principales = QHBoxLayout()
        self.btn_agregar = QPushButton("+ Agregar Nueva Tarea")
        self.btn_agregar.setObjectName("btn_agregar")
        self.btn_agregar.clicked.connect(self.agregar_tarea)
        
        self.btn_refresh = QPushButton("🔄 Actualizar")
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.clicked.connect(self.cargar_tareas)
        
        botones_principales.addWidget(self.btn_agregar)
        botones_principales.addStretch()
        botones_principales.addWidget(self.btn_refresh)
        layout_principal.addLayout(botones_principales)
        
        # Tabs para diferentes vistas
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs_tareas")
        
        # Tab 1: Todas las tareas
        self.tab_todas = QWidget()
        self.crear_tab_todas()
        self.tabs.addTab(self.tab_todas, "📋 Todas")
        self.tab_todas.setObjectName("tab_todas")
        
        # Tab 2: Pendientes
        self.tab_pendientes = QWidget()
        self.crear_tab_pendientes()
        self.tabs.addTab(self.tab_pendientes, "⏳ Pendientes")
        self.tab_pendientes.setObjectName("tab_pendientes")
        
        # Tab 3: Completadas
        self.tab_completadas = QWidget()
        self.crear_tab_completadas()
        self.tabs.addTab(self.tab_completadas, "✅ Completadas")
        self.tab_completadas.setObjectName("tab_completadas")
        
        layout_principal.addWidget(self.tabs)
        self.setLayout(layout_principal)

    def cargar_categorias_filtro(self):
        self.combo_filtro_categoria.clear()
        self.combo_filtro_categoria.addItem("Todas", None)
        categorias = self.gestor_categoria.obtener_todas(self.usuario.id)
        for categoria in categorias:
            self.combo_filtro_categoria.addItem(categoria.nombre, categoria.id)

    def crear_tab_todas(self):
        layout = QVBoxLayout()
        self.lista_todas = QListWidget()
        self.lista_todas.setObjectName("lista_tareas")
        self.lista_todas.itemDoubleClicked.connect(self.editar_tarea_seleccionada)
        layout.addWidget(self.lista_todas)
        botones_layout = QHBoxLayout()
        self.btn_completar = QPushButton("✅ Completar/Pendiente")
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_completar.setObjectName("btn_completar")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_eliminar.setObjectName("btn_eliminar")
        self.btn_completar.clicked.connect(self.cambiar_estado_tarea)
        self.btn_editar.clicked.connect(self.editar_tarea_seleccionada)
        self.btn_eliminar.clicked.connect(self.eliminar_tarea)
        botones_layout.addWidget(self.btn_completar)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_eliminar)
        layout.addLayout(botones_layout)
        self.tab_todas.setLayout(layout)

    def crear_tab_pendientes(self):
        layout = QVBoxLayout()
        self.lista_pendientes = QListWidget()
        self.lista_pendientes.setObjectName("lista_tareas")
        layout.addWidget(self.lista_pendientes)
        btn_completar_pendiente = QPushButton("✅ Marcar como Completada")
        btn_completar_pendiente.setObjectName("btn_completar")
        btn_completar_pendiente.clicked.connect(lambda: self.marcar_completada_desde_tab())
        layout.addWidget(btn_completar_pendiente)
        self.tab_pendientes.setLayout(layout)

    def crear_tab_completadas(self):
        layout = QVBoxLayout()
        self.lista_completadas = QListWidget()
        self.lista_completadas.setObjectName("lista_tareas")
        layout.addWidget(self.lista_completadas)
        btn_pendiente = QPushButton("⏳ Marcar como Pendiente")
        btn_pendiente.setObjectName("btn_editar")
        btn_pendiente.clicked.connect(lambda: self.marcar_pendiente_desde_tab())
        layout.addWidget(btn_pendiente)
        self.tab_completadas.setLayout(layout)

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
            QTabWidget#tabs_tareas::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
            QTabWidget#tabs_tareas::tab-bar {
                alignment: center;
            }
            QTabWidget#tabs_tareas QTabBar::tab {
                background-color: #e9ecef;
                color: #222;
                border: 1px solid #dee2e6;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabWidget#tabs_tareas QTabBar::tab:selected {
                background-color: #ffffff;
                color: #222;
                border-bottom-color: #ffffff;
            }
            QComboBox#combo_filtro_categoria {
                background-color: #e9ecef;
                color: #222;
                border: 1.5px solid #bbb;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 15px;
                min-width: 180px;
                font-weight: bold;
            }
            QComboBox#combo_filtro_categoria QAbstractItemView {
                background: #fff;
                color: #222;
                selection-background-color: #007bff;
                selection-color: #fff;
            }
            QComboBox#combo_filtro_categoria:focus {
                border: 2px solid #007bff;
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
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btn_agregar:hover {
                background-color: #0056b3;
            }
            QPushButton#btn_refresh {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_refresh:hover {
                background-color: #138496;
            }
            QListWidget#lista_tareas {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget#lista_tareas::item {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }
            QListWidget#lista_tareas::item:selected {
                background-color: #007bff;
                color: #fff;
            }
            QListWidget#lista_tareas::item:selected:hover {
                background-color: #66b3ff;
                color: #222;
            }
            QListWidget#lista_tareas::item:hover {
                background-color: #e9ecef;
            }
            QPushButton#btn_completar {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#btn_completar:hover {
                background-color: #218838;
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

    def cargar_tareas(self):
        # Filtrar por categoría si corresponde
        categoria_id = self.combo_filtro_categoria.currentData()
        if categoria_id:
            tareas_todas = self.gestor.obtener_por_categoria(self.usuario.id, categoria_id)
            tareas_pendientes = [t for t in tareas_todas if not t.estado]
            tareas_completadas = [t for t in tareas_todas if t.estado]
        else:
            tareas_todas = self.gestor.obtener_todas(self.usuario.id)
            tareas_pendientes = self.gestor.obtener_pendientes(self.usuario.id)
            tareas_completadas = self.gestor.obtener_completadas(self.usuario.id)

        # Tab todas
        self.lista_todas.clear()
        for tarea in tareas_todas:
            self.agregar_tarea_a_lista(self.lista_todas, tarea)
        # Tab pendientes
        self.lista_pendientes.clear()
        for tarea in tareas_pendientes:
            self.agregar_tarea_a_lista(self.lista_pendientes, tarea, mostrar_urgencia=True)
        # Tab completadas
        self.lista_completadas.clear()
        for tarea in tareas_completadas:
            self.agregar_tarea_a_lista(self.lista_completadas, tarea, mostrar_fecha_completado=True)

    def agregar_tarea_a_lista(self, lista, tarea, mostrar_urgencia=False, mostrar_fecha_completado=False):
        estado_icon = "✅" if tarea.estado else "⏳"
        fecha_info = ""
        if mostrar_fecha_completado and tarea.fecha_completado:
            fecha_info = f" - Completada: {tarea.fecha_completado.strftime('%d/%m/%Y %H:%M')}"
        elif tarea.fecha_limite:
            fecha_info = f" - Vence: {tarea.fecha_limite.strftime('%d/%m/%Y')}"
            if mostrar_urgencia and not tarea.estado:
                dias_restantes = (tarea.fecha_limite - date.today()).days
                if dias_restantes < 0:
                    fecha_info += " ⚠️ VENCIDA"
                elif dias_restantes == 0:
                    fecha_info += " 🔥 HOY"
                elif dias_restantes <= 3:
                    fecha_info += f" ⚡ {dias_restantes} días"
        categoria_info = ""
        if tarea.categoria:
            categoria_info = f" [{tarea.categoria.nombre}]"
        texto = f"{estado_icon} {tarea.descripcion}{categoria_info}{fecha_info}"
        item = QListWidgetItem(texto)
        item.setData(Qt.ItemDataRole.UserRole, tarea.id)
        if mostrar_urgencia and not tarea.estado and tarea.fecha_limite:
            dias_restantes = (tarea.fecha_limite - date.today()).days
            if dias_restantes < 0:
                item.setBackground(QColor("#ffebee"))
            elif dias_restantes <= 1:
                item.setBackground(QColor("#fff3e0"))
        lista.addItem(item)

    def agregar_tarea(self):
        categorias = self.gestor_categoria.obtener_todas(self.usuario.id)
        dialog = DialogTarea(self, categorias=categorias)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            descripcion, fecha_limite, categoria_id = dialog.get_datos()
            self.gestor.agregar_tarea(descripcion, self.usuario.id, fecha_limite, categoria_id)
            self.cargar_tareas()
            self.cargar_categorias_filtro()

    def editar_tarea_seleccionada(self):
        lista_actual = self.obtener_lista_actual()
        item_actual = lista_actual.currentItem()
        if item_actual:
            id_tarea = item_actual.data(Qt.ItemDataRole.UserRole)
            tareas = self.gestor.obtener_todas(self.usuario.id)
            tarea_actual = next((t for t in tareas if t.id == id_tarea), None)
            if tarea_actual:
                categorias = self.gestor_categoria.obtener_todas(self.usuario.id)
                dialog = DialogTarea(
                    self, 
                    tarea_actual.descripcion, 
                    tarea_actual.fecha_limite, 
                    tarea_actual.categoria_id,
                    categorias
                )
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    descripcion, fecha_limite, categoria_id = dialog.get_datos()
                    self.gestor.editar_tarea(id_tarea, descripcion, fecha_limite, categoria_id)
                    self.cargar_tareas()

    def cambiar_estado_tarea(self):
        item_actual = self.lista_todas.currentItem()
        if item_actual:
            id_tarea = item_actual.data(Qt.ItemDataRole.UserRole)
            tareas = self.gestor.obtener_todas(self.usuario.id)
            tarea_actual = next((t for t in tareas if t.id == id_tarea), None)
            if tarea_actual:
                nuevo_estado = not tarea_actual.estado
                self.gestor.cambiar_estado(id_tarea, nuevo_estado)
                self.cargar_tareas()

    def marcar_completada_desde_tab(self):
        item_actual = self.lista_pendientes.currentItem()
        if item_actual:
            id_tarea = item_actual.data(Qt.ItemDataRole.UserRole)
            self.gestor.marcar_completada(id_tarea)
            self.cargar_tareas()

    def marcar_pendiente_desde_tab(self):
        item_actual = self.lista_completadas.currentItem()
        if item_actual:
            id_tarea = item_actual.data(Qt.ItemDataRole.UserRole)
            self.gestor.marcar_pendiente(id_tarea)
            self.cargar_tareas()

    def eliminar_tarea(self):
        lista_actual = self.obtener_lista_actual()
        item_actual = lista_actual.currentItem()
        if item_actual:
            respuesta = QMessageBox.question(
                self, "Eliminar Tarea", 
                "¿Estás seguro de que deseas eliminar esta tarea?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                id_tarea = item_actual.data(Qt.ItemDataRole.UserRole)
                self.gestor.eliminar_tarea(id_tarea)
                self.cargar_tareas()
                self.cargar_categorias_filtro()

    def obtener_lista_actual(self):
        tab_actual = self.tabs.currentIndex()
        if tab_actual == 0:
            return self.lista_todas
        elif tab_actual == 1:
            return self.lista_pendientes
        else:
            return self.lista_completadas

    def volver(self):
        self.close()
        self.volver_a_main()


class DialogTarea(QDialog):
    def __init__(self, parent, descripcion="", fecha_limite=None, categoria_id=None, categorias=None):
        super().__init__(parent)
        self.setWindowTitle("Tarea")
        self.setMinimumSize(500, 300)
        self.categorias = categorias or []
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.input_descripcion = QLineEdit(descripcion)
        self.input_descripcion.setPlaceholderText("Describe tu tarea...")
        self.input_fecha = QDateEdit()
        self.input_fecha.setDate(QDate.currentDate() if not fecha_limite else QDate.fromString(str(fecha_limite), "yyyy-MM-dd"))
        self.input_fecha.setCalendarPopup(True)
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem("Sin categoría", None)
        for categoria in self.categorias:
            self.combo_categoria.addItem(categoria.nombre, categoria.id)
        if categoria_id:
            for i in range(self.combo_categoria.count()):
                if self.combo_categoria.itemData(i) == categoria_id:
                    self.combo_categoria.setCurrentIndex(i)
                    break
        form_layout.addRow("Descripción:", self.input_descripcion)
        form_layout.addRow("Fecha límite:", self.input_fecha)
        form_layout.addRow("Categoría:", self.combo_categoria)
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(botones)
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #007bff;
            }
        """)
    
    def get_datos(self):
        return (
            self.input_descripcion.text(), 
            self.input_fecha.date().toPyDate(),
            self.combo_categoria.currentData()
        )