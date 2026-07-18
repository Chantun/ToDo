from dotenv import load_dotenv
import os
from fastapi import FastAPI
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import jwt
from pwdlib import PasswordHash
import libraries.db as db

load_dotenv("/home/santiago/Projects/web/ToDo/.env")

# Configuración básica
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

app = FastAPI()

# Configuración de CORS imprescindible para que React se comunique con FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # URL de tu frontend React
    allow_credentials=True,                   # REQUISITO para poder enviar/recibir cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

password_hash = PasswordHash.recommended()

users = db.getUsers()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AddNoteRequest(BaseModel):
    content: str

class NoteRequest(BaseModel):
    id: int
    value: bool

# --- Utilidades de Tokens ---
def create_token(data: dict, expires_delta: timedelta) -> str:
    """Crea Javascripts Web Tokens (JWT).

    Args:
        data (dict): {"sub": user["email"]}
        expires_delta (timedelta): Tiempo en minutos en los que va a expirar el token.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Endpoints ---

@app.post("/api/auth/register")
def register(login_data: LoginRequest):
    """Endpoint de registro de nuevas cuentas.

    Args:
        login_data (LoginRequest): {"sub": user["email"]}

    Raises:
        HTTPException: Excepcion 409 si el correo ya esta en uso

    Returns:
        dict: Resultado proporcionado por la base de datos.
    """
    if any(u["email"] == login_data.email for u in users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya esta registrado"
        )
    
    res = db.addUser(login_data.email, password_hash.hash(login_data.password))
    if (res["user"]):
        users.append(res["user"])

    return res


@app.post("/api/auth/login")
def login(login_data: LoginRequest, response: Response):
    """Endpoint de inicio de sesion.

    Args:
        login_data (LoginRequest): {"sub": user["email"]}
        response (Response): Utilizado para poder guardar el refresh_token en una cookie.

    Raises:
        HTTPException: Excepcion 401 si el usuario no esta autorizado.

    Returns:
        dict: Diccionario con el token o con un error.
    """
    user = next(
        (u for u in users if u["email"] == login_data.email),
        None
    )
    hashed_password = user.get("hashed_password") if user else None
    if not user or not hashed_password or not password_hash.verify(login_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )
    
    # Generamos ambos tokens
    access_token = create_token(
        {
            "sub": user["email"],
            "id": user["id"]
        }, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {
            "sub": user["email"],
            "id": user["id"]
        }, 
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    # Inyectamos el Refresh Token en una Cookie HTTPOnly ultra-segura
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,            # Bloquea lectura desde JavaScript (Previene XSS)
        secure=False,             # Cambiar a True en producción (requiere HTTPS)
        samesite="lax",           # Protege contra ataques CSRF
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60 # Tiempo de vida en segundos
    )
    
    # Retornamos el Access Token en el cuerpo de la respuesta para el frontend
    return {"access_token": access_token}

@app.post("/api/auth/refresh")
def refresh(request: Request, response: Response):
    """Renueva el acces_tocken usando el refresh_token.

    Args:
        request (Request): Lee el refresh_token.
        response (Response): idk.

    Raises:
        HTTPException: 401 si no existe el refresh_token.
        HTTPException: 401 si el refresh_token no concuerda con el email.
        HTTPException: 401 si el token expiro o se corrompio.

    Returns:
        dict: Diccionaraio con el access_token
    """
    # Intentamos leer la cookie segura automáticamente
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No hay refresh token")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        # Generamos un nuevo Access Token fresco
        new_access_token = create_token(
            {
                "sub": email,
                "id": user_id
            },
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": new_access_token}
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expirado o corrupto")


@app.post("/api/auth/logout")
def logout(response: Response):
    """Endpoint de cierre de sesion.

    Args:
        response (Response): Para eliminar la cookie.

    Returns:
        dict: Resultado del cierre de sesion.
    """
    # Para cerrar sesión simplemente borramos la cookie
    response.delete_cookie("refresh_token")
    return {"detail": "Sesión cerrada con éxito"}

@app.get("/api/me")
def getMe(request: Request):
    """Retorna el email de quien lo llame.

    Args:
        request (Request): Para leer las cookies.

    Raises:
        HTTPException: 401 si el usuario logueado no esta autorizado.
        HTTPException: 401 si el token a expirado.

    Returns:
        str: El email de la persona logueada.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

###                    ###
# Endpoints de las notas #
###                    ###

@app.post("/api/note/add")
def addNote(note_data: AddNoteRequest, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    if note_data.content is '':
        raise HTTPException(status_code=422, detail="Debe ingresar contenido a la nota")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        result = db.addNote(payload['id'], note_data.content)
        return result
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@app.get("/api/note/get")
def getNote(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        result = db.getNotes(payload['id'])
        return result
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@app.post("/api/note/toggle")
def toggleNote(note: NoteRequest, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    result = db.toggleNote(note.id, note.value)
    return result

@app.delete("/api/note/clear")
def clearNotes(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        result = db.clearNotes(payload['id'])
        return result
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
