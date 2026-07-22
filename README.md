# ToDo

Aplicación web de lista de tareas (To-Do) con autenticación JWT, backend en Python y frontend en React.

## Stack

- **Backend:** Python 3.14+, FastAPI, Uvicorn, SQLite3, PyJWT, PwdLib (Argon2)
- **Frontend:** React 19, Vite 8, React Router 7, Axios, Oxlint
- **Base de datos:** SQLite con migraciones vía C++ (SQLiteCpp, CMake)
- **Scripts:** C++17, CMake, dotenv-cpp

## Estructura

```
backend/         API REST (FastAPI)
  src/
    main.py      Punto de entrada y rutas
    libraries/
      db.py      Operaciones con SQLite
database/
  migrations/    Migraciones SQL secuenciales
  sqlite.db      Base de datos
frontend/        SPA con React + Vite
  src/
    api/         Cliente Axios
    modules/     Componentes reutilizables
    pages/       Login, Register, Main
    style/       Hojas de estilo
scripts/         Migrador C++ (CMake)
```

## Requisitos

- Python >= 3.14
- Node.js >= 22
- CMake >= 3.20
- Compilador con soporte C++17

## Instalación

```bash
# Backend
uv sync

# Frontend
cd frontend && npm install

# Migraciones (C++)
cmake -S scripts -B scripts/build
cmake --build scripts/build
./scripts/build/migration
```

## Variables de entorno

Copiar `.env.example` a `.env` y configurar:

| Variable | Descripción |
|---|---|
| `DATABASE` | Ruta a la base de datos SQLite |
| `MIGRATIONS` | Ruta a la carpeta de migraciones |
| `SECRET_KEY` | Clave secreta para JWT |
| `ALGORITHM` | Algoritmo JWT (HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | TTL del access token |
| `REFRESH_TOKEN_EXPIRE_DAYS` | TTL del refresh token |

## Ejecución

```bash
# Backend (desde backend/)
uv run uvicorn src.main:app --reload

# Frontend (desde frontend/)
npm run dev
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/register` | Registro de usuario |
| POST | `/api/auth/login` | Inicio de sesión |
| POST | `/api/auth/refresh` | Renovar access token |
| POST | `/api/auth/logout` | Cerrar sesión |
| GET | `/api/me` | Obtener email del usuario |
| POST | `/api/note/add` | Agregar nota |
| GET | `/api/note/get` | Obtener notas |
| POST | `/api/note/toggle` | Marcar/desmarcar nota |
| DELETE | `/api/note/clear` | Limpiar notas completadas |

## Licencia

GNU General Public License v3.0
