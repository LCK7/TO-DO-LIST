from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QInputDialog,QHBoxLayout,QMenu
from PyQt6.QtCore import Qt, QPoint,QSize
from PyQt6.QtGui import QCloseEvent,QIcon
from src.gestores.gestor_tareas import GestorTareas
from src.ui.dialogo_nueva_tarea import DialogoNuevaTarea



class VentanaTareas(QWidget):
    """
    Ventana principal para la gestión de tareas del usuario.

    Permite a los usuarios visualizar, agregar, editar, eliminar y cambiar el estado
    (completada/pendiente) de sus tareas. Ofrece un menú contextual para acciones rápidas.
    """
    def __init__(self,usuario,volver_a_main):
        """
        Inicializa la VentanaTareas.

        Args:
            usuario: Objeto del usuario actual logueado.
            volver_a_main: Función de callback para regresar a la ventana principal (menú).
        """
        super().__init__()
        self.usuario = usuario
        self.volver_a_main = volver_a_main
        self.setWindowTitle("Tus Tareas")
        self.setMinimumSize(400,500)
        
        self.gestor = GestorTareas()
        self.init_ui()
        self.cargar_tareas()
        
    def init_ui(self):
        """
        Configura la interfaz de usuario de la ventana de tareas.

        Establece el diseño, los widgets (título, lista de tareas, botones)
        y los estilos CSS. Configura el manejo de eventos para la lista de tareas.
        """
        layout = QVBoxLayout()
        layout.setSpacing(15)

        titulo = QLabel(f"Tareas de {self.usuario.nombre_usuario}")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.lista_tareas = QListWidget()
        # Habilita el menú contextual personalizado
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
        """
        Carga todas las tareas del usuario actual y las muestra en la QListWidget.

        Limpia la lista existente y agrega cada tarea como un QListWidgetItem personalizado.
        """
        self.lista_tareas.clear()
        self.tareas = self.gestor.obtener_todas(self.usuario.id)
        for tarea in self.tareas:
            self.agregar_item_tarea(tarea)
        
    def agregar_item_tarea(self, tarea):
        """
        Crea y añade un widget personalizado para representar una tarea en la QListWidget.

        Cada tarea se muestra con su descripción, categoría, fecha límite y estado,
        e incluye un botón para eliminar.

        Args:
            tarea: Objeto de la tarea a añadir (instancia de Tarea).
        """
        widget_tarea = QWidget()
        widget_tarea.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 12px;
        """)
        layout_h = QHBoxLayout()
        layout_h.setContentsMargins(5, 5, 5, 5)
        layout_h.setSpacing(20)

        layout_v = QVBoxLayout()
        layout_v.setSpacing(5)

        label_desc = QLabel(f"📝 {tarea.descripcion}")
        label_desc.setStyleSheet("font-size: 15px; font-weight: bold; color: #1a202c;margin: 3px")
        
        label_cat = QLabel(f"🗂️ Categoria: {tarea.categoria}")
        label_cat.setStyleSheet("font-size: 15px; font-weight: bold; color: #1a202c;margin: 3px")

        label_fecha = QLabel(f"📅 Límite: {tarea.fecha_limite if tarea.fecha_limite else 'Sin límite'}")
        label_fecha.setStyleSheet("font-size: 13px; color: #4a5568;margin: 3px;")

        label_estado = QLabel("✅ Completada" if tarea.estado else "❌ Pendiente")
        label_estado.setStyleSheet(f"font-size: 13px; color: {'#38a169' if tarea.estado else '#e53e3e'};margin: 3px;")

        layout_v.addWidget(label_desc)
        layout_v.addWidget(label_cat)
        layout_v.addWidget(label_fecha)
        layout_v.addWidget(label_estado)

        boton_eliminar = QPushButton()
        boton_eliminar.setIcon(QIcon("src/assets/slash.svg"))
        boton_eliminar.setIconSize(QSize(25,25))
        boton_eliminar.setFixedSize(40,45)
        boton_eliminar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        # Conecta el botón de eliminar a la función con el ID de la tarea
        boton_eliminar.clicked.connect(lambda _, tid=tarea.id: self.eliminar_tarea_confirmada(tid))
        
        layout_h.addLayout(layout_v)
        layout_h.addStretch() # Empuja el botón de eliminar al final
        layout_h.addWidget(boton_eliminar)

        widget_tarea.setLayout(layout_h)

        item = QListWidgetItem()
        item.setSizeHint(widget_tarea.sizeHint()) # Asegura que el item tenga el tamaño correcto
        self.lista_tareas.addItem(item)
        self.lista_tareas.setItemWidget(item, widget_tarea)
        
    def agregar_tarea(self):
        """
        Abre un diálogo para que el usuario cree una nueva tarea.

        Si el usuario confirma la creación, valida la descripción,
        crea la categoría si es necesario y agrega la tarea a través del gestor.
        Luego, recarga la lista de tareas. Muestra advertencias si la descripción está vacía.
        """
        dialogo = DialogoNuevaTarea(self.usuario.id)
        if dialogo.exec(): # Muestra el diálogo de forma modal
            descripcion, fecha_limite, nombre_categoria = dialogo.get_data()

            # Ajusta la fecha límite a None si está vacía
            if fecha_limite == '':
                fecha_limite = None

            if descripcion.strip():
                # Crea la categoría si no existe y obtiene su ID
                categoria_id = self.gestor.crear_categoria_si_no_existe(nombre_categoria,self.usuario.id)

                self.gestor.agregar_tarea(descripcion, self.usuario.id, fecha_limite, categoria_id)
                self.cargar_tareas() # Recarga las tareas para mostrar la nueva
            else:
                QMessageBox.warning(self, "Ups", "La descripción no puede estar vacía.")


    def eliminar_tarea_confirmada(self, id_tarea):
        """
        Pide confirmación al usuario antes de eliminar una tarea.

        Si el usuario confirma, elimina la tarea a través del gestor y recarga la lista.

        Args:
            id_tarea: El ID de la tarea a eliminar.
        """
        confirm = QMessageBox.question(self, "Eliminar Tarea", "¿Seguro que deseas eliminar esta tarea?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.gestor.eliminar_tarea(id_tarea)
            self.cargar_tareas() # Recarga las tareas después de la eliminación
    
    def editar_tarea(self, item):
        """
        Abre un diálogo para editar la tarea seleccionada (al hacer doble clic).

        Obtiene los datos de la tarea seleccionada, abre el diálogo de edición
        con esos datos y, si se guardan los cambios, actualiza la tarea
        a través del gestor y recarga la lista.

        Args:
            item: El QListWidgetItem que fue doble-clicado, del cual se extrae la tarea.
        """
        # Encuentra la tarea correspondiente al item seleccionado
        index = self.lista_tareas.row(item)
        tarea = self.tareas[index]

        # Importa aquí para evitar import circular si lo tienes, o al principio del archivo
        from src.ui.dialogo_editar_tarea import DialogoEditarTarea

        # Abre el diálogo de edición con la tarea actual
        dialogo = DialogoEditarTarea(tarea, self.usuario.id)

        if dialogo.exec(): # Muestra el diálogo de forma modal
            nueva_desc, nueva_fecha, categoria_info = dialogo.get_data()

            # Determina el ID de la categoría: si es un string (nueva categoría), la crea.
            # Si ya es un int (ID de categoría existente), lo usa directamente.
            if isinstance(categoria_info, str):
                categoria_id = self.gestor.crear_categoria_si_no_existe(categoria_info, self.usuario.id)
            else:
                categoria_id = categoria_info  # Puede ser None o un ID existente

            self.gestor.editar_tarea(tarea.id, nueva_desc, nueva_fecha, categoria_id)
            self.cargar_tareas() # Recarga las tareas para mostrar los cambios


    def mostrar_menu_contextual(self, pos: QPoint):
        """
        Muestra un menú contextual al hacer clic derecho sobre un elemento de la lista de tareas.

        El menú ofrece opciones para eliminar la tarea o cambiar su estado (completada/pendiente).

        Args:
            pos: La posición del clic del ratón dentro del QListWidget.
        """
        item = self.lista_tareas.itemAt(pos)
        if not item: # Si no se hizo clic en un item, no mostrar menú
            return

        # Obtiene la tarea asociada al item clicado
        index = self.lista_tareas.row(item)
        tarea = self.tareas[index]

        menu = QMenu(self)

        # Acciones del menú
        accion_eliminar = menu.addAction("🗑️ Eliminar tarea")
        accion_estado = menu.addAction("✅ Marcar como Completada" if not tarea.estado else "❌ Marcar como Pendiente")

        # Muestra el menú en la posición global del cursor y espera la selección del usuario
        accion = menu.exec(self.lista_tareas.mapToGlobal(pos))

        # Ejecuta la acción seleccionada
        if accion == accion_eliminar:
            self.eliminar_tarea_confirmada(tarea.id)
        elif accion == accion_estado:
            self.gestor.cambiar_estado(tarea.id, not tarea.estado) # Invierte el estado actual
            self.cargar_tareas() # Recarga para reflejar el cambio de estado
            
    def volver(self):
        """
        Oculta la ventana actual de tareas y llama a la función de callback
        para volver a la ventana principal de la aplicación.
        """
        self.hide()
        self.volver_a_main()
        
    def closeEvent(self, event:QCloseEvent): # type: ignore
        """
        Maneja el evento de cierre de la ventana de tareas.

        Pregunta al usuario si desea regresar al menú principal antes de cerrar la ventana.
        Si la respuesta es 'Sí', oculta la ventana y llama a la función de callback.
        Si es 'No', permite que la ventana se cierre.

        Args:
            event: El evento de cierre (QCloseEvent).
        """
        respuesta = QMessageBox.question(
            self,
            "Salir de Tareas",
            "¿Deseas regresar al menú principal?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            event.ignore() # Ignora el cierre inmediato
            self.hide() # Oculta la ventana
            self.volver_a_main() # Llama al callback para volver al menú
        else:
            event.accept() # Permite que la ventana se cierre (finalizando la aplicación si es la última)