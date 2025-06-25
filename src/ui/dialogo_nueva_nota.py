from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QMessageBox

class DialogoNuevaNota(QDialog):
    """
    Diálogo para crear o editar una nota.

    Permite ingresar un título y contenido. Se puede reutilizar tanto para nuevas notas como para editar existentes.
    """

    def __init__(self, nota=None):
        """
        Inicializa el diálogo con campos de entrada para título y contenido.

        Parámetros:
        - nota (Nota | None): Nota existente a editar. Si es None, se asume que se está creando una nueva.
        """
        super().__init__()
        self.setWindowTitle("📝 Crear Nota" if nota is None else "✏️ Editar Nota")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        label_titulo = QLabel("📌 Título:")
        self.input_titulo = QLineEdit()
        layout.addWidget(label_titulo)
        layout.addWidget(self.input_titulo)

        label_contenido = QLabel("📝 Contenido:")
        self.input_contenido = QTextEdit()
        layout.addWidget(label_contenido)
        layout.addWidget(self.input_contenido)

        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("💾 Guardar")
        btn_cancelar = QPushButton("🗂️ Acciones")
        btn_guardar.clicked.connect(self.validar)
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        if nota:
            self.input_titulo.setText(nota.titulo)
            self.input_contenido.setPlainText(nota.contenido)

        self.setStyleSheet("""
            QDialog {
                background-color: #f7fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2d3748;
            }
            QLabel {
                font-weight: bold;
                color: #1a202c;
                margin-bottom: 5px;
            }
            QLineEdit, QTextEdit {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #cbd5e0;
                background-color: #fff;
                color: #2d3748;
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

    def validar(self):
        """
        Verifica que el campo de título no esté vacío.

        Si está vacío, se muestra un mensaje de advertencia. 
        Si no, se cierra el diálogo con aceptación.
        """
        if not self.input_titulo.text().strip():
            QMessageBox.warning(self, "Error", "El título no puede estar vacío.")
            return
        self.accept()

    def get_data(self):
        """
        Obtiene los datos ingresados por el usuario.

        Retorna:
        - tuple: (titulo (str), contenido (str)) de la nota.
        """
        return self.input_titulo.text().strip(), self.input_contenido.toPlainText().strip()
