from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QDateEdit, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import QDate
from datetime import date
from src.gestores.gestor_categoria import GestorCategoria  # Usa el gestor correcto


class DialogoNuevaTarea(QDialog):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("🆕 Nueva Tarea")
        self.setMinimumWidth(350)

        self.usuario_id = usuario_id
        self.gestor_categoria = GestorCategoria()  # 👈 Cambiado

        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        label_desc = QLabel("📝 Descripción:")
        self.descripcion_edit = QLineEdit()
        layout.addWidget(label_desc)
        layout.addWidget(self.descripcion_edit)

        label_cat = QLabel("🗂️ Categoría:")
        self.combo_categoria = QComboBox()
        self.combo_categoria.setEditable(True)
        self.combo_categoria.addItem("SIN CATEGORÍA", userData=None)

        categorias = self.gestor_categoria.obtener_todas(self.usuario_id)
        for categoria in categorias:
            self.combo_categoria.addItem(categoria.nombre, userData=categoria.id)

        layout.addWidget(label_cat)
        layout.addWidget(self.combo_categoria)

        label_fecha = QLabel("📅 Fecha límite:")
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDate(QDate.currentDate())
        layout.addWidget(label_fecha)
        layout.addWidget(self.fecha_edit)

        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setObjectName("btn_cancelar")

        self.btn_guardar.clicked.connect(self.validar)
        self.btn_cancelar.clicked.connect(self.reject)

        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)

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
        descripcion = self.descripcion_edit.text().strip()
        fecha = self.fecha_edit.date().toPyDate()

        if not descripcion:
            QMessageBox.warning(self, "Campo vacío", "La descripción no puede estar vacía.")
            return

        if fecha < date.today():
            QMessageBox.warning(self, "Fecha inválida", "No puedes seleccionar una fecha pasada.")
            return

        self.accept()

    def get_data(self):
        descripcion = self.descripcion_edit.text().strip()
        fecha = self.fecha_edit.date().toPyDate() 

        texto_categoria = self.combo_categoria.currentText().strip()
        categoria_id = self.combo_categoria.currentData()

        if texto_categoria.upper() == "SIN CATEGORÍA" or not texto_categoria:
            return descripcion, fecha.isoformat(), None
        elif categoria_id is None:
            return descripcion, fecha.isoformat(), texto_categoria  # Nueva categoría
        else:
            return descripcion, fecha.isoformat(), categoria_id
