from PyQt6.QtWidgets import QDialog, QLineEdit, QDateEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout,QMessageBox
from PyQt6.QtCore import QDate
from datetime import date

class DialogoNuevaTarea(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nueva Tarea")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # 📝 Campo descripción
        layout.addWidget(QLabel("Descripción:"))
        self.descripcion_edit = QLineEdit()
        layout.addWidget(self.descripcion_edit)

        # 📅 Campo fecha límite
        layout.addWidget(QLabel("Fecha límite:"))
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_edit)

        # Botones
        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)
        self.setLayout(layout)

    def get_data(self):
        descripcion = self.descripcion_edit.text()
        fecha = self.fecha_edit.date().toPyDate()

        # ❌ Validar que la fecha no sea anterior a hoy
        if fecha < date.today():
            QMessageBox.warning(self, "Fecha inválida", "No puedes seleccionar una fecha pasada.")
            return '', ''  # Devuelve valores vacíos para que no lo guarde

        return descripcion, fecha.isoformat()
