from bson import ObjectId

from utils.db_connections import db
from service.user_service import UserService
from dto.tarea import Tarea

servicio_usuario = UserService()

class TareasRepository:
    
    def __init__(self) -> None:
        None
    
    def crear_tarea(nueva_tarea: Tarea):
        dic_tarea = nueva_tarea.model_dump(by_alias=True)  # Convertir a dict con alias (_id -> id)
        return db.tareas.insert_one(dic_tarea)
        

    def leer_tarea(id_tarea: str):
        if not ObjectId.is_valid(id_tarea):
            return {"message": "El tipo de dato recibido es erroneo"}
        
        tarea_buscada = db.tareas.find_one({"_id": ObjectId(id_tarea)})
        
        if tarea_buscada:
            return tarea_buscada  
        else:
            return {"message": "Tarea no encontrada, algo ha ido muy mal"}
        

    def listar_tareas(id_usuario: str):
        tipo_user = servicio_usuario.get_role(id_usuario)
        if tipo_user == 'user':
            filtro = {
                "_id": id_usuario
            }
            
            tareas =  db.tareas.find(filtro) 
            return tareas
        
        elif tipo_user == 'admin':
            tareas =  db.tareas.find()  
            '''
            Se podrian haber creado filtros para que mostrase solo las tareas propias y las de los usuarios user, 
            excluyendo asi las tareas de otros admin pero al no aparecer en el documento no se ha implementado,
            se deja un ejemplo de como seria el filtro aplicado:
            filtro = {
                "$or": [
                    {"_id": id_usuario},     
                    {"Role": "user"}           
                ]
            }
            '''
            return tareas
            


    def actualizar_tarea(id_tarea: str, tareaModificada: Tarea):
        datosModificados = {k: v for k, v in tareaModificada.model_dump(by_alias=True).items() if v is not None}
        '''
        model_dump  -> paso a dic
        items       -> Devuelve una lista de pares
        '''
        result =  db.tareas.update_one(
            {"_id": ObjectId(id_tarea)},
            {"$set": datosModificados}
        )
        if result.modified_count == 1:
            actualizacionTarea =  db.tareas.find_one({"_id": ObjectId(id_tarea)})
            return actualizacionTarea
       

    def eliminar_tarea(id_tarea: str):
        result =  db.tareas.delete_one({"_id": ObjectId(id_tarea)})
        if result.deleted_count == 1:
            return {"message": "Tarea eliminada correctamente"}
    