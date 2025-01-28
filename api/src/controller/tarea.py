from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta

from src.dto.token import Token
from src.dto.user import User
from src.dto.tarea import Tarea
from src.service.user_service import UserService
from src.service.tareas_service import TareaService

from src.utils.utils import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


router = APIRouter(prefix="/admin", tags=["Admin"])

servicio_usuario = UserService()
servicio_tarea = TareaService()
@router.post("/token", response_model=Token)
async def login_for_access_token(usuario_recibido: User):
    user = servicio_usuario.get_user(name=usuario_recibido.Name)
    rol = servicio_usuario.get_role(name=usuario_recibido.Name)
    if not user or not verify_password(usuario_recibido.Password, user.Password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Name}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "role":rol, "id":str(user.id_usuario)} 


@router.post("/crear_tarea")
async def crear_tarea(nueva_tarea: Tarea):
    try:
        return servicio_tarea.crear_tarea(nueva_tarea)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ocurrio el siguiente error: {str(e)}"})


@router.get("/leer_tarea")
async def leer_tarea(id_tarea: str):
    try:
        return servicio_tarea.leer_tarea(id_tarea)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ocurrio el siguiente error: {str(e)}"})
    
    
@router.get("/listar_tareas")   # tener en cuenta el tipo de usuario para que se vean unas tareas u otras
async def listar_tareas(id_usuario: str):
    try:
        return servicio_tarea.listar_tareas(id_usuario)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ocurrio el siguiente error: {str(e)}"})
    

@router.put("/actualizar_tarea")
async def actualizar_tarea(id_tarea: str, tareaModificada: Tarea):
    try:
        return servicio_tarea.actualizar_tarea(id_tarea, tareaModificada)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ocurrio el siguiente error: {str(e)}"})
    

@router.delete("/eliminar_tarea")
async def eliminar_tarea(id_tarea: str):
    try:
        return servicio_tarea.eliminar_tarea(id_tarea)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Ocurrio el siguiente error: {str(e)}"})
    
