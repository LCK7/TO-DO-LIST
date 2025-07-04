from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QCalendarWidget, QHBoxLayout,
    QDialog, QListWidget, QListWidgetItem, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QLocale
from PyQt6.QtGui import QFont, QTextCharFormat, QColor
from datetime import datetime, date, timedelta
import locale

class VentanaCalendario(QWidget):
    """
    Ventana del calendario con funcionalidad de tareas integrada.
    """

    def __init__(self, usuario, gestor_tareas, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.gestor_tareas = gestor_tareas
        self.volver_a_main = volver_a_main
        self.tareas = []
        self.setWindowTitle(f"📅 Calendario de {usuario.nombre_usuario}")
        self.setMinimumSize(950, 850)  # Tamaño fijo más grande
        self.setMaximumSize(950, 850)  # Evita redimensionado
        
        # Configurar idioma español
        self.configurar_idioma_espanol()
        
        self.init_ui()
        self.aplicar_estilos()
        self.cargar_tareas_y_configurar_calendario()

    def configurar_idioma_espanol(self):
        """Configura el calendario en español"""
        try:
            # Intentar configurar locale en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
            except:
                try:
                    locale.setlocale(locale.LC_TIME, 'es_ES')
                except:
                    pass  # Si no funciona, usar inglés por defecto

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
        titulo = QLabel("📅 Calendario de Tareas")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Información de ayuda
        info_superior = QLabel("🔵 = Tareas pendientes | 🔴 = Vencidas | 🟡 = Hoy | Haz clic para ver detalles")
        info_superior.setObjectName("info_ayuda")
        info_superior.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(info_superior)
        
        # Calendario con tamaño fijo
        self.calendario = QCalendarWidget()
        self.calendario.setObjectName("calendario_principal")
        self.calendario.clicked.connect(self.fecha_seleccionada)
        self.calendario.setFixedHeight(400)  # Altura fija
        
        # Configurar calendario en español
        locale_es = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
        self.calendario.setLocale(locale_es)
        
        layout_principal.addWidget(self.calendario)
        
        # Información de tareas con altura fija
        self.info_tareas = QLabel("Selecciona una fecha para ver las tareas de ese día")
        self.info_tareas.setObjectName("info_tareas")
        self.info_tareas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_tareas.setWordWrap(True)
        self.info_tareas.setFixedHeight(120)  # Altura fija para evitar redimensionado
        layout_principal.addWidget(self.info_tareas)
        
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
            QLabel#info_ayuda {
                font-size: 14px;
                color: #495057;
                font-weight: 500;
                padding: 8px;
                background-color: #e9ecef;
                border-radius: 6px;
                margin: 5px;
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
            QCalendarWidget#calendario_principal {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                font-size: 14px;
                selection-background-color: #007bff;
            }
            QCalendarWidget QToolButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                min-width: 80px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #0056b3;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #007bff;
                color: white;
                border-radius: 6px;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 13px;
                background-color: white;
                selection-background-color: #007bff;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView::item:selected {
                background-color: #007bff;
                color: white;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #e9ecef;
                color: #495057;
                padding: 4px;
                font-weight: bold;
                border: 1px solid #dee2e6;
            }
            QLabel#info_tareas {
                font-size: 14px;
                color: #495057;
                padding: 15px;
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                min-height: 100px;
                max-height: 120px;
            }
        """)

    def cargar_tareas_y_configurar_calendario(self):
        """Carga las tareas y configura el rango del calendario"""
        self.tareas = self.gestor_tareas.obtener_todas(self.usuario.id)
        
        # Configurar rango de fechas basado en tareas
        if self.tareas:
            fechas_tareas = [t.fecha_limite for t in self.tareas if t.fecha_limite]
            if fechas_tareas:
                fecha_min = min(fechas_tareas)
                fecha_max = max(fechas_tareas)
                
                # Expandir el rango un poco
                fecha_min = fecha_min - timedelta(days=30)
                fecha_max = fecha_max + timedelta(days=30)
                
                self.calendario.setMinimumDate(QDate(fecha_min))
                self.calendario.setMaximumDate(QDate(fecha_max))
            else:
                # Si no hay fechas límite, usar rango actual
                hoy = date.today()
                self.calendario.setMinimumDate(QDate(hoy.year - 1, 1, 1))
                self.calendario.setMaximumDate(QDate(hoy.year + 1, 12, 31))
        else:
            # Si no hay tareas, usar rango actual
            hoy = date.today()
            self.calendario.setMinimumDate(QDate(hoy.year - 1, 1, 1))
            self.calendario.setMaximumDate(QDate(hoy.year + 1, 12, 31))
        
        # Marcar días con tareas pendientes
        self.marcar_dias_con_tareas()

    def marcar_dias_con_tareas(self):
        """Marca los días que tienen tareas pendientes"""
        formato_pendiente = QTextCharFormat()
        formato_pendiente.setBackground(QColor("#66b3ff"))
        formato_pendiente.setForeground(QColor("white"))
        formato_pendiente.setFontWeight(QFont.Weight.Bold)
        
        formato_vencida = QTextCharFormat()
        formato_vencida.setBackground(QColor("#dc3545"))
        formato_vencida.setForeground(QColor("white"))
        formato_vencida.setFontWeight(QFont.Weight.Bold)
        
        formato_hoy = QTextCharFormat()
        formato_hoy.setBackground(QColor("#ffc107"))
        formato_hoy.setForeground(QColor("#212529"))
        formato_hoy.setFontWeight(QFont.Weight.Bold)
        
        hoy = date.today()
        
        for tarea in self.tareas:
            if tarea.fecha_limite and not tarea.estado:  # Solo tareas pendientes
                fecha_qdate = QDate(tarea.fecha_limite)
                
                if tarea.fecha_limite < hoy:
                    # Tarea vencida
                    self.calendario.setDateTextFormat(fecha_qdate, formato_vencida)
                elif tarea.fecha_limite == hoy:
                    # Tarea para hoy
                    self.calendario.setDateTextFormat(fecha_qdate, formato_hoy)
                else:
                    # Tarea pendiente
                    self.calendario.setDateTextFormat(fecha_qdate, formato_pendiente)

    def fecha_seleccionada(self, fecha_qdate):
        """Maneja la selección de una fecha en el calendario"""
        fecha_python = fecha_qdate.toPyDate()
        tareas_del_dia = [t for t in self.tareas if t.fecha_limite == fecha_python]
        
        if tareas_del_dia:
            # Mostrar modal con las tareas del día
            self.mostrar_modal_tareas(fecha_python, tareas_del_dia)
        else:
            # Actualizar info inferior
            fecha_str = self.formatear_fecha_espanol(fecha_python)
            self.info_tareas.setText(f"📅 {fecha_str}\n\nNo hay tareas programadas para este día.")

    def formatear_fecha_espanol(self, fecha):
        """Formatea la fecha en español"""
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        
        dias_semana = [
            "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
        ]
        
        dia_semana = dias_semana[fecha.weekday()]
        dia = fecha.day
        mes = meses[fecha.month - 1]
        año = fecha.year
        
        return f"{dia_semana}, {dia} de {mes} de {año}"

    def mostrar_modal_tareas(self, fecha, tareas_del_dia):
        """Muestra un modal con las tareas del día seleccionado"""
        dialog = DialogTareasDelDia(self, fecha, tareas_del_dia)
        dialog.exec()
        
        # Actualizar info inferior con fecha en español
        fecha_str = self.formatear_fecha_espanol(fecha)
        pendientes = len([t for t in tareas_del_dia if not t.estado])
        completadas = len([t for t in tareas_del_dia if t.estado])
        
        if pendientes > 0:
            self.info_tareas.setText(
                f"📅 {fecha_str}\n\n"
                f"📋 {len(tareas_del_dia)} tarea(s) total(es)\n"
                f"⏳ {pendientes} pendiente(s) | ✅ {completadas} completada(s)\n\n"
                f"Haz clic nuevamente para ver detalles."
            )
        else:
            self.info_tareas.setText(
                f"📅 {fecha_str}\n\n"
                f"✅ Todas las tareas completadas ({completadas})\n\n"
                f"¡Excelente trabajo!"
            )

    def volver(self):
        self.close()
        self.volver_a_main()


class DialogTareasDelDia(QDialog):
    """Modal que muestra las tareas de un día específico"""
    
    def __init__(self, parent, fecha, tareas):
        super().__init__(parent)
        self.fecha = fecha
        self.tareas = tareas
        self.setWindowTitle(f"Tareas del {fecha.strftime('%d/%m/%Y')}")
        self.setMinimumSize(500, 400)
        self.init_ui()
        self.aplicar_estilos()

    def formatear_fecha_espanol(self, fecha):
        """Formatea la fecha en español para el modal"""
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        
        dia = fecha.day
        mes = meses[fecha.month - 1]
        año = fecha.year
        
        return f"{dia} de {mes} de {año}"

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título con fecha en español
        fecha_str = self.formatear_fecha_espanol(self.fecha)
        titulo = QLabel(f"📅 Tareas del {fecha_str}")
        titulo.setObjectName("titulo_modal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Estadísticas
        pendientes = len([t for t in self.tareas if not t.estado])
        completadas = len([t for t in self.tareas if t.estado])
        
        stats = QLabel(f"📊 Total: {len(self.tareas)} | ⏳ Pendientes: {pendientes} | ✅ Completadas: {completadas}")
        stats.setObjectName("stats_modal")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats)
        
        # Lista de tareas
        self.lista_tareas = QListWidget()
        self.lista_tareas.setObjectName("lista_modal")
        
        for tarea in self.tareas:
            estado_icon = "✅" if tarea.estado else "⏳"
            categoria_info = f" [{tarea.categoria.nombre}]" if tarea.categoria else ""
            
            # Verificar urgencia
            urgencia = ""
            if not tarea.estado:
                hoy = date.today()
                if tarea.fecha_limite < hoy:
                    urgencia = " ⚠️ VENCIDA"
                elif tarea.fecha_limite == hoy:
                    urgencia = " 🔥 HOY"
            
            texto = f"{estado_icon} {tarea.descripcion}{categoria_info}{urgencia}"
            item = QListWidgetItem(texto)
            
            # Colorear según estado
            if not tarea.estado and tarea.fecha_limite < date.today():
                item.setBackground(QColor("#ffebee"))  # Rojo claro para vencidas
            elif not tarea.estado and tarea.fecha_limite == date.today():
                item.setBackground(QColor("#fff3e0"))  # Naranja claro para hoy
            elif tarea.estado:
                item.setBackground(QColor("#e8f5e8"))  # Verde claro para completadas
            
            self.lista_tareas.addItem(item)
        
        layout.addWidget(self.lista_tareas)
        
        # Botón cerrar
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)
        
        self.setLayout(layout)

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#titulo_modal {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QLabel#stats_modal {
                font-size: 14px;
                color: #495057;
                background-color: #e9ecef;
                padding: 8px;
                border-radius: 6px;
                font-weight: 500;
            }
            QListWidget#lista_modal {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget#lista_modal::item {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 10px;
                margin: 3px;
            }
            QListWidget#lista_modal::item:hover {
                background-color: #e9ecef;
            }
        """)