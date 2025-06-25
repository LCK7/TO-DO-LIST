import sqlite3
from src.modelos.tareas import Tarea

class GestorTareas:
    """
    """
    def __init__(self,nombre_bd="tareas.db"):
        """
        """
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(self.nombre_bd)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self.crear_tabla()
    
    def crear_tabla(self):
        """
        """
        consulta = """
        CREATE TABLE IF NOT EXISTS tareas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            estado INTEGER NOT NULL DEFAULT 0,
            usuario_id INTEGER NOT NULL,
            fecha_limite TEXT,
            categoria_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );
        """
        
        self.conexion.execute(consulta)
        self.conexion.commit()
        
    def agregar_tarea(self,descripcion,usuario_id,fecha_limite,categoria_id):
        """
        """
        consulta = """
        INSERT INTO TAREAS(descripcion,usuario_id,fecha_limite,categoria_id)
        VALUES (?,?,?,?);
        """
        self.conexion.execute(consulta,(descripcion,usuario_id,fecha_limite,categoria_id,))
        self.conexion.commit()

    def obtener_categoria_id_por_nombre(self, nombre_categoria):
        consulta = "SELECT id FROM categorias WHERE nombre = ?;"
        cursor = self.conexion.execute(consulta, (nombre_categoria,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    def crear_categoria_si_no_existe(self, nombre_categoria, usuario_id):
        if not nombre_categoria:
            return None  # No crees una categoría sin nombre

        consulta_buscar = "SELECT id FROM categorias WHERE nombre = ? AND usuario_id = ?;"
        cursor = self.conexion.execute(consulta_buscar, (nombre_categoria, usuario_id))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]  # Ya existe, devuelve su ID

        consulta_insertar = "INSERT INTO categorias(nombre, usuario_id) VALUES (?, ?);"
        self.conexion.execute(consulta_insertar, (nombre_categoria, usuario_id))
        self.conexion.commit()

        cursor = self.conexion.execute(consulta_buscar, (nombre_categoria, usuario_id))
        return cursor.fetchone()[0]

    def obtener_todas(self, usuario_id):
        consulta = """
        SELECT t.id, t.descripcion, t.estado, t.fecha_limite, t.categoria_id, COALESCE(c.nombre, 'Sin categoría')
        FROM tareas t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE t.usuario_id = ?;
        """
        cursor = self.conexion.execute(consulta, (usuario_id,))
        tareas = []
        for fila in cursor:
            tarea = Tarea(
                id=fila[0],
                descripcion=fila[1],
                estado=bool(fila[2]),
                fecha_limite=fila[3],
                categoria_id=fila[4],
                usuario_id=usuario_id,
                categoria=fila[5]
            )
            tareas.append(tarea)
        return tareas
    
    def obtener_tareas_categoria(self,usuario_id,categoria_id):
        consulta = """
        SELECT id,descripcion,estado,fecha_limite
        FROM tareas
        WHERE usuario_id = ? AND categoria_id = ?;
        """
        cursor = self.conexion.execute(consulta,(usuario_id,categoria_id))
        return [Tarea(id=f[0], descripcion=f[1], estado=bool(f[2]), fecha_limite=f[3]) for f in cursor]
    
    def editar_tarea(self,id_tarea,nueva_descripcion,nueva_fecha, nueva_categoria):
        """
        """
        consulta = "UPDATE tareas SET descripcion = ?,fecha_limite = ?, categoria_id = ?  WHERE id = ?;"
        self.conexion.execute(consulta,(nueva_descripcion,nueva_fecha,nueva_categoria,id_tarea))
        self.conexion.commit()
        
    def cambiar_estado(self, id_tarea, nuevo_estado: bool):
        """
        """
        consulta = "UPDATE tareas SET estado = ? WHERE id = ?;"
        self.conexion.execute(consulta, (int(nuevo_estado), id_tarea))
        self.conexion.commit()
    
    def eliminar_categoria(self):
        item = self.lista_categorias.currentItem()
        if item:
            categoria = item.data(Qt.ItemDataRole.UserRole)
            tareas = self.gestor_tareas.obtener_por_categoria(categoria.id)  # <- Debes implementar esto
            if tareas:
                QMessageBox.warning(self, "Advertencia", "No se puede eliminar esta categoría porque tiene tareas asociadas.")
                return

            confirmacion = QMessageBox.question(self, "Confirmar eliminación",
                f"¿Estás seguro de eliminar la categoría '{categoria.nombre}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmacion == QMessageBox.StandardButton.Yes:
                self.gestor.eliminar_categoria(categoria.id)
                self.cargar_categorias()

    
    def cerrar_conexion(self):
        """
        """
        self.conexion.close()