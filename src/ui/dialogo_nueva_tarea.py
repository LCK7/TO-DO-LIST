from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QDateEdit, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDate
from datetime import date


class DialogoNuevaTarea(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🆕 Nueva Tarea")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Campo descripción
        label_desc = QLabel("📝 Descripción:")
        self.descripcion_edit = QLineEdit()
        layout.addWidget(label_desc)
        layout.addWidget(self.descripcion_edit)

        # Campo categoría
        label_cat = QLabel("🗂️ Categoría (opcional):")
        self.categoria_edit = QLineEdit()
        layout.addWidget(label_cat)
        layout.addWidget(self.categoria_edit)

        # Campo fecha límite
        label_fecha = QLabel("📅 Fecha límite:")
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDate(QDate.currentDate())
        layout.addWidget(label_fecha)
        layout.addWidget(self.fecha_edit)

        # Botones
        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_guardar.clicked.connect(self.validar)
        self.btn_cancelar.clicked.connect(self.reject)
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)
        self.setLayout(layout)

        # Estilo visual
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
            QLineEdit, QDateEdit {
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
        categoria = self.categoria_edit.text().strip()
        fecha = self.fecha_edit.date().toPyDate()

        return descripcion, fecha.isoformat(), categoria
