from dotenv import load_dotenv
import os
import sqlite3

load_dotenv("/home/santiago/Projects/web/ToDo/.env")

db_path = os.getenv("DATABASE")


def getUsers():
  """Obtione los usuarios registrados.

  Returns:
      [{email, password}]: lista con diccionarios que contienen el id, email y la contasena de cada usuario.
  """
  with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT id, email, password AS hashed_password FROM user")
  return res.fetchall()


def addUser(email: str, password: str):
  """Registra a un nuevo usuario.

  Args:
      email (str): Correo electronico del nuevo usuario.
      password (str): Contrasena hasehada del usuario.

  Returns:
      {}: Diccionario con los resultados.
  """
  with sqlite3.connect(db_path) as conn:
    res = conn.execute("SELECT email FROM user WHERE email = ?", (email,))
  if res.fetchone() is not None:
    return {"response": "Error", "error": "Email ya registrado"}

  try:
    with sqlite3.connect(db_path) as conn:
      conn.execute(
        "INSERT INTO user (email, password) VALUES (?, ?)",
        (email, password)
      )
    conn.commit()
    return {"response": "Ok", "user": {"email": email, "password": password}}
  except sqlite3.Error as e:
    return {"response": "Error", "error": e}


def deleteUser(email: str):
  """Elimina a un usuario registrado.

  Args:
      email (str): Correo electronico del usuario que se quiere eliminar.

  Returns:
      {}: Diccionario con informacion de la consulta.
  """
  with sqlite3.connect(db_path) as conn:
    res = conn.execute("SELECT email FROM user WHERE email = ?", (email,))
  if res.fetchone() is None:
    return {"response": "Error", "error": "Email no registrado"}

  try:
    with sqlite3.connect(db_path) as conn:
      conn.execute("DELETE FROM user WHERE email = ?", (email,))
    conn.commit()
    return {"response": "Ok"}
  except sqlite3.Error as e:
    return {"response": "Error", "error": e}

# Notas
def addNote(user: int, content: str):
  """Anade una nueva nota.

  Args:
      user (int): Id del duenio.
      content (str): Contenido de la nota.

  Returns:
      dict: Respuesta de la db.
  """
  try:
    with sqlite3.connect(db_path) as conn:
      conn.execute(
          "INSERT INTO note (user_id, content) VALUES (?, ?)",
          (user, content)
        )
    conn.commit()
    return {"response": "Ok", "note": {"content": content, "active": False}}
  except sqlite3.Error as e:
    return {"response": "Error", "error": e}
  
def getNotes(user: int):
  with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    res = conn.execute(
      "SELECT id, content, active FROM note WHERE user_id = ?",
      (user,)
    )
  return res.fetchall()

def toggleNote(note: int, active: bool):
  try:
    with sqlite3.connect(db_path) as conn:
      conn.execute(
        "UPDATE note SET active = ? WHERE id = ?",
        [active, note]
      )
    conn.commit()
    return {"response": "Ok"}
  except sqlite3.Error as e:
    return {"response": "Error", "error": e}
  
def clearNotes(user: int):
  try:
    with sqlite3.connect(db_path) as conn:
      conn.execute(
        "DELETE FROM note WHERE active = 1 AND user_id = ?",
        (user,)
      )
    conn.commit()
    return {"response": "Ok"}
  except sqlite3.Error as e:
    return {"response": "Error", "error": e}
