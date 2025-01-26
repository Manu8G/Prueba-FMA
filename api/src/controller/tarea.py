from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta

from dto.token import Token
from dto.user import User
from dto.tarea import Tarea
from service.user_service import UserService
from utils.utils import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(prefix="/admin", tags=["Admin"])
ususu = UserService()

@router.post("/token", response_model=Token)
async def login_for_access_token(usuario: User):
    user = ususu.get_user(name=usuario.name)
    rol = ususu.obtener_rol(name=usuario.name)
    if not user or not verify_password(usuario.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre_y_apellidos}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "role":rol, "id":str(user.id_usuario)} 


@router.post("/crear_tarea")
async def crear_tarea(user: nuevoUsuario):
    try:
        ususu.crear_usuario(nombre_y_apellidos=user.name, password=user.password, role=user.role)
        return {"message": "User created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something goes wrong: {str(e)}"})


@router.get("/leer_tarea")
async def leer_tarea():
    try:
        return survey.listar_encuestas()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something goes wrong: {str(e)}"})
    
    
@router.get("/listar_tareas")   # tener en cuenta el tipo de usuario para que se vean unas tareas u otras
async def listar_tareas():
    try:
        return survey.listar_encuestas()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something goes wrong: {str(e)}"})
    

@router.put("/actualizar_tarea")
async def actualizar_tarea(caso: Caso):
    try:
        return flujo.asignar_flujo(caso.id_flujo, caso.id_usuario)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something goes wrong: {str(e)}"})
    

@router.delete("/eliminar_tarea")
async def eliminar_tarea(id: IdModel):
    try:
        survey.eliminar_encuesta(id=id.Id)
        return {"message": "User created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something goes wrong: {str(e)}"})
    
