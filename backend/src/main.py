from fastapi import FastAPI
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import jwt
from pwdlib import PasswordHash

# Configuración básica (usa variables de entorno en producción)
SECRET_KEY = "tu_clave_secreta_super_segura_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

app = FastAPI()

# Configuración de CORS imprescindible para que React se comunique con FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend React
    allow_credentials=True,                   # REQUISITO para poder enviar/recibir cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

password_hash = PasswordHash.recommended()

# Base de datos simulada (solo para demostración)
fake_users_db = {
    "usuario@test.com": {
        "email": "usuario@test.com",
        "hashed_password": password_hash.hash("mipassword123")
    }
}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Utilidades de Tokens ---
def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Endpoints ---

@app.post("/api/auth/login")
def login(login_data: LoginRequest, response: Response):
    user = fake_users_db.get(login_data.email)
    if not user or not password_hash.verify(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )
    
    # Generamos ambos tokens
    access_token = create_token(
        {"sub": user["email"]}, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": user["email"]}, 
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
    # Intentamos leer la cookie segura automáticamente
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No hay refresh token")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        # Generamos un nuevo Access Token fresco
        new_access_token = create_token(
            {"sub": email}, 
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": new_access_token}
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expirado o corrupto")


@app.post("/api/auth/logout")
def logout(response: Response):
    # Para cerrar sesión simplemente borramos la cookie
    response.delete_cookie("refresh_token")
    return {"detail": "Sesión cerrada con éxito"}

# Endpoint Protegido de ejemplo
@app.get("/api/dashboard")
def get_dashboard_data(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"data": f"Bienvenido, {payload['sub']}. Estos son datos super privados."}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
