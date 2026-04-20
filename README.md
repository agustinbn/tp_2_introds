# TP N°2 - Introducción al Desarrollo de Software

API REST para gestionar un prode (torneo de predicciones de fútbol). Permite administrar partidos, usuarios, predicciones y un ranking.

## Tecnologías

- **Python** con **Flask** (servidor web)
- **MySQL** (base de datos)

## Requisitos previos

- Python 3.x instalado
- MySQL instalado y corriendo
- Una base de datos llamada `prode` creada en MySQL

## Instalación

**1. Clonar el repositorio**
```bash
git clone https://github.com/agustinbn/tp_2_introds.git
cd tp_2_introds
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Configurar la base de datos**

Asegurarse de tener MySQL corriendo con usuario `root` y contraseña `root`, y una base de datos llamada `prode`. Luego ejecutar:
```bash
python3 init_db.py
```

**4. Correr el servidor**
```bash
flask run
```

El servidor queda disponible en `http://localhost:5000`.

---

## Endpoints disponibles

### Partidos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/partidos` | Listar partidos (sin resultado) |
| POST | `/partidos` | Crear un partido |
| GET | `/partidos/{id}` | Obtener un partido por ID |
| PUT | `/partidos/{id}` | Reemplazar un partido |
| PATCH | `/partidos/{id}` | Actualizar parcialmente un partido |
| DELETE | `/partidos/{id}` | Eliminar un partido |
| PUT | `/partidos/{id}/resultado` | Cargar el resultado de un partido |
| POST | `/partidos/{id}/prediccion` | Registrar una predicción para un partido |

### Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/usuarios` | Listar usuarios |
| POST | `/usuarios` | Crear un usuario |
| GET | `/usuarios/{id}` | Obtener un usuario por ID |
| PUT | `/usuarios/{id}` | Reemplazar un usuario |
| DELETE | `/usuarios/{id}` | Eliminar un usuario |

### Ranking

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/ranking` | Ver el ranking de usuarios por puntos |

---

## Parámetros de paginación

Los endpoints de listado (`/partidos`, `/usuarios`, `/ranking`) aceptan:

- `_limit`: cuántos resultados traer por página (por defecto: 10)
- `_offset`: desde qué posición empezar

Ejemplo: `GET /partidos?_limit=5&_offset=10`

## Filtros disponibles en `/partidos`

- `equipo`: filtrar por nombre de equipo (local o visitante)
- `fecha`: filtrar por fecha (`YYYY-MM-DD`)
- `fase`: filtrar por fase del torneo (`grupos`, `dieciseisavos`, `octavos`, `cuartos`, `semis`, `final`)

---

## Estructura del proyecto

```
tp_2_introds/
├── app.py          # Punto de entrada, configuración de Flask
├── db.py           # Conexión a la base de datos
├── exceptions.py   # Manejo de errores personalizados
├── init_db.py      # Script para inicializar la base de datos
├── prode.sql       # Esquema SQL de la base de datos
├── requirements.txt
├── routes/
│   ├── partidos.py
│   ├── usuarios.py
│   └── ranking.py
└── docs/
    └── swagger.yaml  # Documentación de la API
```

## Documentación completa

La especificación completa de la API está en `docs/swagger.yaml` en formato OpenAPI 3.0. Se puede visualizar con [Swagger Editor](https://editor.swagger.io/) pegando el contenido del archivo.
