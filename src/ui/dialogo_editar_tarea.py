from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDate
from datetime import datetime
from src.gestores.gestor_categoria import GestorCategoria


class DialogoEditarTarea(QDialog):
    def __init__(self, tarea, usuario_id):
        super().__init__()
        self.setWindowTitle("✏️ Editar Tarea")
        self.setMinimumWidth(350)

        self.tarea = tarea
        self.usuario_id = usuario_id
        self.gestor_cat = GestorCategoria()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Descripción
        layout.addWidget(QLabel("📝 Nueva descripción:"))
        self.input_desc = QLineEdit(tarea.descripcion)
        layout.addWidget(self.input_desc)

        # Fecha límite
        layout.addWidget(QLabel("📅 Nueva fecha límite:"))
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        if tarea.fecha_limite:
            fecha_dt = datetime.strptime(tarea.fecha_limite, "%Y-%m-%d")
            self.input_fecha.setDate(QDate(fecha_dt.year, fecha_dt.month, fecha_dt.day))
        else:
            self.input_fecha.setDate(QDate.currentDate())
        layout.addWidget(self.input_fecha)

        # Categoría
        layout.addWidget(QLabel("🗂️ Categoría:"))
        self.combo_categoria = QComboBox()
        self.combo_categoria.setEditable(True)
        self.combo_categoria.addItem("SIN CATEGORÍA", userData=None)

        self.categorias = self.gestor_cat.obtener_todas(usuario_id)
        for cat in self.categorias:
            self.combo_categoria.addItem(cat.nombre, userData=cat.id)

        # Seleccionar actual
        for i in range(self.combo_categoria.count()):
            if self.combo_categoria.itemData(i) == tarea.categoria_id:
                self.combo_categoria.setCurrentIndex(i)
                break

        layout.addWidget(self.combo_categoria)

        # Botones
        botones = QHBoxLayout()
        btn_guardar = QPushButton("💾 Guardar")
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_guardar.clicked.connect(self.validar)
        btn_cancelar.clicked.connect(self.reject)
        botones.addWidget(btn_guardar)
        botones.addWidget(btn_cancelar)

        layout.addLayout(botones)
        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #f7fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2d3748;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
                color: #1a1a1a;
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #cbd5e0;
                background-color: white;
                color: #1a1a1a;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
                border: none;
                background-color: #3182ce;
                color: white;
            }
            QPushButton:hover {
                background-color: #2b6cb0;
            }
            QPushButton#btn_cancelar {
                background-color: #718096;
            }
            QPushButton#btn_cancelar:hover {
                background-color: #4a5568;
            }
        """)

    def validar(self):
        if not self.input_desc.text().strip():
            QMessageBox.warning(self, "Error", "La descripción no puede estar vacía.")
            return
        self.accept()

    def get_data(self):
        desc = self.input_desc.text().strip()
        fecha = self.input_fecha.date().toPyDate().isoformat()
        texto_categoria = self.combo_categoria.currentText().strip()
        cat_id = self.combo_categoria.currentData()

        if not texto_categoria or texto_categoria.upper() == "SIN CATEGORÍA":
            return desc, fecha, None
        elif cat_id is None:
            return desc, fecha, texto_categoria 
        else:
            return desc, fecha, cat_id
