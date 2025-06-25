from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem,QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from datetime import datetime, timedelta
from src.gestores.gestor_tareas import GestorTareas

class VentanaCalendario(QWidget):
    def __init__(self, usuario, volver_a_main):
        super().__init__()
        self.usuario = usuario
        self.volver_a_main = volver_a_main
        self.gestor = GestorTareas()
        self.setWindowTitle("📅 Calendario Semanal de Tareas")
        self.setMinimumSize(800, 600)

        self.fecha_actual = datetime.today()

        self.init_ui()
        self.mostrar_tareas()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("📆 Tareas Pendientes por Semana")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e3a8a;")
        layout.addWidget(titulo)

        self.semana_label = QLabel()
        self.semana_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.semana_label.setStyleSheet("font-size: 16px; color: #555;")
        layout.addWidget(self.semana_label)

        botones_nav = QHBoxLayout()
        btn_anterior = QPushButton("⬅ Semana anterior")
        btn_siguiente = QPushButton("Semana siguiente ➡")
        btn_anterior.clicked.connect(self.semana_anterior)
        btn_siguiente.clicked.connect(self.semana_siguiente)
        botones_nav.addWidget(btn_anterior)
        botones_nav.addWidget(btn_siguiente)
        layout.addLayout(botones_nav)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Descripción"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch) # type: ignore
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # type: ignore
        self.tabla.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.tabla)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.clicked.connect(self.volver)
        layout.addWidget(btn_volver)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
                color: #2d3748;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #1e40af;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #e2e8f0;
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

    def mostrar_tareas(self):
        inicio_semana = self.fecha_actual - timedelta(days=self.fecha_actual.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        self.semana_label.setText(
            f"🗓️ Semana: {inicio_semana.strftime('%d/%m/%Y')} - {fin_semana.strftime('%d/%m/%Y')}"
        )

        tareas = self.gestor.obtener_todas(self.usuario.id)
        tareas_semana = [
            t for t in tareas
            if t.fecha_limite
            and inicio_semana.date() <= datetime.strptime(t.fecha_limite, "%Y-%m-%d").date() <= fin_semana.date()
            and not t.estado
        ]

        self.tabla.clearContents()
        self.tabla.setRowCount(len(tareas_semana)) 

        for i, tarea in enumerate(tareas_semana):
            fecha = tarea.fecha_limite or "Sin fecha"
            descripcion = tarea.descripcion or "Sin descripción"
            categoria = getattr(tarea, 'categoria', "Sin categoría")

            fecha_item = QTableWidgetItem(fecha)
            descripcion_item = QTableWidgetItem(descripcion)
            categoria_item = QTableWidgetItem(categoria)

            for item in (fecha_item, descripcion_item, categoria_item):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setForeground(Qt.GlobalColor.black)

            color_fondo = Qt.GlobalColor.white

            for item in (fecha_item, descripcion_item, categoria_item):
                item.setBackground(color_fondo)

            self.tabla.setItem(i,0,fecha_item)
            self.tabla.setItem(i,1,descripcion_item)
            self.tabla.setItem(i,2,categoria_item)

    def semana_anterior(self):
        self.fecha_actual -= timedelta(days=7)
        self.mostrar_tareas()

    def semana_siguiente(self):
        self.fecha_actual += timedelta(days=7)
        self.mostrar_tareas()

    def volver(self):
        self.close()
        self.volver_a_main()
    