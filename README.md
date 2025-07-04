# ✅ TO-DO-LIST

Aplicación de escritorio desarrollada en **Python** con **PyQt6**, que permite a los usuarios **crear y gestionar tareas, notas, categorías y calendario** de forma organizada y personalizada mediante una cuenta de acceso individual.

---

## 📌 Características principales

- 🔐 **Login por usuario:** Cada usuario tiene su cuenta y ve únicamente sus tareas.
- ✅ **Gestión de tareas:** Agregar, editar, eliminar, completar y categorizar tareas.
- 🗂️ **Gestión de categorías:** Crea tus propias categorías personalizadas.
- 🗒️ **Notas personales:** Crea, edita, borra y marca notas como favoritas.
- 📅 **Calendario integrado:** Visualiza tus tareas con fecha límite en vista calendario.
- 🎨 **Interfaz amigable y responsiva** con diseño intuitivo usando PyQt6.
- 🗄️ **Persistencia con SQLAlchemy** compatible con SQLite y otros motores SQL.
- 🔐 **Contraseñas encriptadas** usando SHA-256.
- 🧪 **Pruebas unitarias y E2E** con más del 94% de cobertura.

---

## 🧠 Modelo de datos

### 📦 Clases modelo (SQLAlchemy ORM)

| Clase     | Atributos destacados | Relaciones |
|-----------|----------------------|------------|
| `Usuario` | `id`, `nombre_usuario`, `contraseña` (encriptada), `fecha_creacion` | `tareas`, `categorias`, `notas` |
| `Tarea`   | `id`, `descripcion`, `estado`, `fecha_limite`, `fecha_creacion`, `fecha_completado` | `usuario`, `categoria` |
| `Nota`    | `id`, `titulo`, `contenido`, `estado_favorito`, `fecha_creacion`, `fecha_modificacion` | `usuario` |
| `Categoria` | `id`, `nombre`, `usuario_id`, `fecha_creacion` | `usuario`, `tareas` |

Las clases utilizan SQLAlchemy ORM para definir:
- Esquema de tablas y columnas
- Relaciones entre entidades (one-to-many, many-to-one)
- Comportamiento en cascada para operaciones de eliminación
- Métodos de utilidad para operaciones comunes

Este diseño orientado a objetos facilita el mantenimiento del código y permite una evolución más flexible del modelo de datos.

---

## Documento

[Visita el documento](https://docs.google.com/document/d/1h_WIGW-LbQVDuDdO5rqCobXio_KOkSiNV3eRZhvRemk/edit?usp=sharing)

```

---

## 🧰 Estructura del proyecto

```

TO-DO-LIST/
│
├── app.py                         # Punto de entrada de la app
├── src/
│   ├── modelos/                   # Clases: Usuario, Tarea, Nota, Categoria
│   ├── gestores/                  # Gestores: Usuarios, Tareas, Categorías, Notas
│   ├── db/
│   │   └── init\_db.py             # Inicializador de base de datos
│   └── ui/                        # Interfaz: Ventanas (login, main, tareas, etc.)
├── tests/                         # Tests unitarios y E2E
│   ├── conftest.py                # Configuración para tests con pytest
│   ├── test_gestor_*.py           # Tests unitarios para gestores
│   └── test_e2e_*.py              # Tests end-to-end
├── run_tests_with_coverage.bat    # Script para ejecutar tests con coverage (Windows)
├── run_tests_with_coverage.sh     # Script para ejecutar tests con coverage (Linux/Mac)
└── README.md

```

---

## 🗃️ Base de datos

El proyecto utiliza **SQLAlchemy ORM** como capa de abstracción para la base de datos, lo que permite:

- Soporte para múltiples motores de bases de datos (SQLite, MySQL, PostgreSQL)
- Configuración por defecto con **SQLite3** para desarrollo y pruebas
- Mapeo objeto-relacional completo con modelos declarativos
- Gestión automática de sesiones y transacciones

### Estructura de la base de datos

- `usuarios`: Almacena información de usuario (nombre único, contraseña encriptada)
- `tareas`: Vinculadas a `usuarios` y opcionalmente a `categorias`, con fechas de creación/vencimiento
- `categorias`: Organizan las tareas por tipo, relacionadas con `usuarios`
- `notas`: Sistema de notas personales vinculadas a `usuarios`, con soporte para marcar favoritos

Todas las **relaciones están definidas explícitamente** en los modelos, manteniendo integridad referencial y permitiendo operaciones en cascada cuando es necesario.

---

## 🔑 Seguridad

- Las contraseñas se encriptan con `SHA-256` al momento del registro.
- No se almacenan contraseñas en texto plano.

---

## 🛠 Instalación de dependencias

Este proyecto requiere [Python 3.10+](https://www.python.org/downloads/) y las siguientes bibliotecas principales:

- **PyQt6**: Para la interfaz gráfica
- **SQLAlchemy**: Para la persistencia y ORM
- **pytest**: Para ejecutar las pruebas unitarias y E2E

Puedes instalar todas las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

> ⚠️ Asegúrate de estar en el entorno virtual correcto antes de ejecutar el comando.

Para configurar un entorno de desarrollo completo:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas (opcional)
pytest
```

---

### 📌 Verificar la versión de PyQt6

Para comprobar qué versión de PyQt6 tienes instalada, ejecuta el siguiente comando en tu terminal:

```bash
pip show PyQt6
```

También puedes verificarlo desde Python con:

```python
import PyQt6
print(PyQt6.__version__)
```

---
### 📌 Ejecutar

```bash
python app.py
```

---

## 🛠️ Arquitectura y componentes principales

La aplicación sigue un patrón de arquitectura en capas, separando claramente modelos, lógica de negocio e interfaz de usuario.

### 🧩 Modelos (src/modelos/)

| Modelo            | Descripción                                           |
| ----------------- | ----------------------------------------------------- |
| `Usuario`         | Entidad central con relaciones a tareas, notas y categorías |
| `Tarea`           | Incluye estado, fechas, relaciones con usuario y categoría |
| `Nota`            | Almacena contenido con formato, estados y metadatos |
| `Categoria`       | Sistema de clasificación para organizar tareas |
| `Base`            | Clase base declarativa para SQLAlchemy |

### 🔧 Gestores (src/gestores/)

| Gestor            | Funcionalidades clave                                |
| ----------------- | ---------------------------------------------------- |
| `GestorUsuarios`  | Registro, autenticación, encriptación de contraseñas |
| `GestorTareas`    | CRUD tareas, cambio estado, filtrado, estadísticas   |
| `GestorNotas`     | CRUD notas, gestión de favoritos                     |
| `GestorCategoria` | CRUD categorías, asociación con tareas y usuarios    |

### 🖼️ Interfaz de Usuario (src/ui/)

| Componente        | Descripción                                          |
| ----------------- | ---------------------------------------------------- |
| `MainWindow`      | Centro de navegación principal con estructura de tabs |
| `WindowLogin`     | Control de acceso y registro de usuarios             |
| `WindowTareas`    | Vista principal de gestión de tareas con filtros     |
| `WindowNotas`     | Editor y organizador de notas personales             |
| `WindowCalendario`| Visualización de tareas en formato calendario        |
| `WindowGestionCategoria` | Administración de categorías personalizadas   |

### 🗄️ Capa de Datos (src/db/)

| Componente        | Funcionalidad                                        |
| ----------------- | ---------------------------------------------------- |
| `conexion.py`     | Configuración de SQLAlchemy y gestión de sesiones    |
| `init_db.py`      | Inicialización y migración de esquemas               |

---

## 🚀 Futuras mejoras

* 📱 **Versión móvil**: Desarrollo de cliente móvil con Kivy, Flutter o React Native
* 🌐 **Sincronización en la nube**: Implementación de backend REST o GraphQL para sincronización
* 🌐 **Soporte para MySQL/PostgreSQL**: Aprovechando la abstracción de SQLAlchemy
* 🔔 **Sistema de notificaciones**: Recordatorios para tareas próximas a vencer
* 📊 **Dashboard de productividad**: Métricas y estadísticas avanzadas
* 🎨 **Temas personalizables**: Soporte para modo oscuro y temas custom
* 🔌 **Sistema de plugins**: Arquitectura extensible para funcionalidades adicionales

---

## 👨‍💻 Desarrollado por

| Nombre completo                   | Rol               |
|-----------------------------------|-------------------|
| Landa Rojas Alexander Nelson      | Desarrollador     |
| Arce Curi Rodrigo Vladimir        | Desarrollador     |
| Gamarra Curi Gianmarco            | Desarrollador     |
| Gutierrez Taipe Luis Alberto      | Desarrollador     |
| Salvador Rivera Bruce Joshua      | Desarrollador     |
| Tucto Ubaldo Ricardo David        | Desarrollador     |

---

## 🧪 Ejemplo visual

![preview](src/assets/preview.jpg) <!-- Si algún día tienes una imagen -->

---

## 🧪 Testing y Control de Calidad

El proyecto implementa una completa suite de pruebas automatizadas para garantizar la calidad del código y la estabilidad de la aplicación.

### 📋 Tipos de pruebas

#### Tests unitarios
- Cobertura del **94%** del código base
- Prueba aislada de cada gestor y sus métodos
- Validación de todos los flujos y casos extremos
- Automatización completa mediante pytest

| Módulo            | Cobertura | Características probadas |
|-------------------|-----------|--------------------------|
| GestorUsuarios    | 95%       | Registro, autenticación, seguridad |
| GestorTareas      | 91%       | CRUD, filtros, estados, estadísticas |
| GestorNotas       | 96%       | CRUD, marcado de favoritos |
| GestorCategoria   | 96%       | CRUD, relaciones |

#### Tests End-to-End (E2E)
Simulación completa de flujos de usuario que prueban la integración entre todos los componentes:

1. **Registro e inicio de sesión**
2. **Gestión de categorías personalizadas**
3. **Creación y organización de tareas**
4. **Completado y filtrado de tareas**
5. **Sistema de notas y favoritos**
6. **Consulta de estadísticas y reportes**

### 📊 Cobertura y ejecución

Para ejecutar las pruebas y generar informes de cobertura detallados:

**En Windows:**
```powershell
.\run_tests_with_coverage.bat
```

**En Linux/Mac:**
```bash
chmod +x run_tests_with_coverage.sh
./run_tests_with_coverage.sh
```

El informe de cobertura HTML estará disponible en `./htmlcov/index.html`, proporcionando detalles línea por línea de todo el código probado.

