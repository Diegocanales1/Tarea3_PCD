# FastAPI y Base de Datos

Este proyecto es una API RESTful desarrollada con **FastAPI** que gestiona información de usuarios.  
La información se persiste en una base de datos **SQLite** usando **SQLAlchemy** como ORM.

---

## 🛠️ Requisitos e Instalación

Para ejecutar el proyecto, necesitas tener **Python** instalado.  
Se recomienda usar **uv** para la gestión de dependencias.

### Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/Tarea3_PCD.git
cd Tarea3_PCD
```

### Configura el ambiente virtual y las dependencias

```
uv init
uv add fastapi --extra standard
uv add sqlalchemy
uv add pydantic
uv add python-dotenv
```

### Configura tu API Key:

Crea un archivo .env en la raíz del proyecto.
Este archivo debe contener tu clave de API para la seguridad de los endpoints.

```
API_KEY="<TU_VALOR_AQUI>"
```
---

### Como ejecutar la API

Una vez que tengas las dependencias instaladas y el archivo .env configurado, puedes iniciar la aplicación usando uv:

```
uv run fastapi dev main.py
```
La API se ejecutará en:
👉 http://127.0.0.1:8000

Puedes acceder a la documentación interactiva de la API en:
👉 http://127.0.0.1:8000/docs

---

### 📌 Endpoints

La API expone los siguientes endpoints bajo el prefijo /api/v1 protegidos con la cabecera X-API-Key.

---

#### 1. Crear usuario

- Endpoint: POST /api/v1/users/

- Descripción: Crea un nuevo usuario.

- Headers: X-API-Key: <TU_VALOR_AQUI>

- Cuerpo de la solicitud (JSON):

```json
   {
     "user_name": "name",
     "user_id": 123,
     "user_email": "email@example.com",
     "age": 30,
     "recommendations": ["a", "b", "c"],
     "ZIP": "44100"
   }
```

Respuesta (Éxito): 201 Created
Respuesta (Error): 409 Conflict si el email ya existe.

#### Obtener usuario por ID

- Endpoint: GET /api/v1/users/{user_id}

- Descripción: Recupera los datos de un usuario por su ID.

- Headers: X-API-Key: <TU_VALOR_AQUI>

Respuesta (Éxito): 200 OK
Respuesta (Error): 404 Not Found si el usuario no existe.

#### 3. Actualizar usuario

- Endpoint: PUT /api/v1/users/{user_id}

- Descripción: Actualiza la información de un usuario existente.

- Headers: X-API-Key: <TU_VALOR_AQUI>

Cuerpo de la solicitud (JSON):

```json
{
  "user_email": "nuevo.email@example.com",
  "age": 35
}
```

Respuesta (Éxito): 200 OK
Respuesta (Error):
- 404 Not Found si el usuario no existe.
- 409 Conflict si el nuevo email ya está registrado.

#### 4. Eliminar usuario

- Endpoint: DELETE /api/v1/users/{user_id}

- Descripción: Elimina un usuario de la base de datos.

- Headers: X-API-Key: <TU_VALOR_AQUI>

Respuesta (Éxito): 200 OK con un mensaje de confirmación.
Respuesta (Error): 404 Not Found si el usuario no existe.