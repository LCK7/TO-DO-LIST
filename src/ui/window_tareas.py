from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QInputDialog,QHBoxLayout,QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QCloseEvent
from src.gestores.gestor_tareas import GestorTareas
from src.ui.dialogo_nueva_tarea import DialogoNuevaTarea


class VentanaTareas(QWidget):
    def __init__(self,usuario,volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.volver_a_main = volver_a_main
        self.setWindowTitle("Tus Tareas")
        self.setMinimumSize(400,500)
        
        self.gestor = GestorTareas()
        self.init_ui()
        self.cargar_tareas()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        titulo = QLabel(f"Tareas de {self.usuario.nombre_usuario}")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.lista_tareas = QListWidget()
        self.lista_tareas.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.lista_tareas.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.lista_tareas.itemDoubleClicked.connect(self.editar_tarea)
        layout.addWidget(self.lista_tareas)

        # Botón Agregar
        self.boton_agregar = QPushButton("➕ Agregar tarea")
        self.boton_agregar.clicked.connect(self.agregar_tarea)
        layout.addWidget(self.boton_agregar)

        # Botón Volver
        self.btn_volver = QPushButton("⬅️ Volver al Inicio")
        self.btn_volver.setObjectName("btn_volver")
        self.btn_volver.clicked.connect(self.volver)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #1a202c;
                font-size: 14px;
            }
            
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
                color: #2d3748;
                font-weight: bold;
            }

            QListWidget {
                background-color: #ffffff;
                border: 1px solid #cbd5e0;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton {
                background-color: #3182ce;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 14px;
                margin-top: 10px;
            }

            QPushButton:hover {
                background-color: #2b6cb0;
                font-weight: bold;
            }

            QPushButton#btn_volver {
                background-color: #4a5568;
            }

            QPushButton#btn_volver:hover {
                background-color: #2d3748;
            }
        """)
    
    def cargar_tareas(self):
        self.lista_tareas.clear()
        self.tareas = self.gestor.obtener_todas(self.usuario.id)
        for tarea in self.tareas:
            self.agregar_item_tarea(tarea)
        
    def agregar_item_tarea(self, tarea):
        widget_tarea = QWidget()
        layout_h = QHBoxLayout()
        layout_h.setContentsMargins(10, 5, 10, 5)

        label_desc = QLabel(f"📝 {tarea.descripcion}")
        label_fecha = QLabel(f"📅 Límite: {tarea.fecha_limite if tarea.fecha_limite else 'Sin límite'}")
        label_estado = QLabel(f"{'✅ Completada' if tarea.estado else '❌ Pendiente'}")

        layout_v = QVBoxLayout()
        layout_v.addWidget(label_desc)
        layout_v.addWidget(label_fecha)
        layout_v.addWidget(label_estado)

        layout_h.addLayout(layout_v)

        boton_eliminar = QPushButton("🗑️")
        boton_eliminar.setFixedSize(30, 30)
        boton_eliminar.setStyleSheet("background-color: black; color: white; border-radius: 5px;")
        boton_eliminar.clicked.connect(lambda _, tid=tarea.id: self.eliminar_tarea_confirmada(tid))

        layout_h.addStretch()
        layout_h.addWidget(boton_eliminar)

        widget_tarea.setLayout(layout_h)

        item = QListWidgetItem()
        item.setSizeHint(widget_tarea.sizeHint())
        self.lista_tareas.addItem(item)
        self.lista_tareas.setItemWidget(item, widget_tarea)
        
        
    def agregar_tarea(self):
        
        dialogo = DialogoNuevaTarea()
        if dialogo.exec():
            descripcion, fecha_limite, categoria = dialogo.get_data()
            
            if fecha_limite == '':
                fecha_limite = None
            
            if descripcion.strip():
                self.gestor.agregar_tarea(descripcion, self.usuario.id, fecha_limite, categoria)
                self.cargar_tareas()
            else:
                QMessageBox.warning(self, "Ups", "La descripción no puede estar vacía.")

    def eliminar_tarea_confirmada(self, id_tarea):
        confirm = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar esta tarea?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.gestor.eliminar_tarea(id_tarea)
            self.cargar_tareas()
    
    def editar_tarea(self, item):
        index = self.lista_tareas.row(item)
        tarea = self.tareas[index]

        opciones = QMessageBox.question(self, "Tarea",
            f"¿Marcar como {'Pendiente' if tarea.estado else 'Completada'}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)

        if opciones == QMessageBox.StandardButton.Yes:
            self.gestor.cambiar_estado(tarea.id, not tarea.estado)
            self.cargar_tareas()
        elif opciones == QMessageBox.StandardButton.No:
            self.eliminar_tarea_confirmada(tarea.id)
        
    def mostrar_menu_contextual(self, pos: QPoint):
        """
        """
        item = self.lista_tareas.itemAt(pos)
        if not item:
            return

        index = self.lista_tareas.row(item)
        tarea = self.tareas[index]

        menu = QMenu(self)

        accion_editar = menu.addAction("✏️ Editar tarea")
        accion_eliminar = menu.addAction("🗑️ Eliminar tarea")
        accion_estado = menu.addAction("✅ Marcar como Completada" if not tarea.estado else "❌ Marcar como Pendiente")

        accion = menu.exec(self.lista_tareas.mapToGlobal(pos))

        if accion == accion_editar:
            self.editar_descripcion(tarea)
        elif accion == accion_eliminar:
            self.eliminar_tarea_confirmada(tarea.id)
        elif accion == accion_estado:
            self.gestor.cambiar_estado(tarea.id, not tarea.estado)
            self.cargar_tareas()
            
    def editar_descripcion(self, tarea):
        """
        """
        texto, ok = QInputDialog.getText(self, "Editar tarea", "Nueva descripción:", text=tarea.descripcion)
        if ok and texto.strip():
            self.gestor.editar_tarea(tarea.id, texto.strip())
            self.cargar_tareas()
        elif ok:
            QMessageBox.warning(self, "Advertencia", "La descripción no puede estar vacía.")
    
    def volver(self):
        self.hide()
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
            event.ignore() 