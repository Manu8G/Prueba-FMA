from bson import ObjectId

from src.utils.db_connections import db
from src.service.user_service import UserService
from src.dto.tarea import Tarea

servicio_usuario = UserService()

class TareasRepository:
    
    def __init__(self):
        None
    
    # Funcion que nos permite crear una nueva tarea
    async def crear_tarea(self, nueva_tarea: Tarea):
        dic_tarea = nueva_tarea.model_dump(by_alias=True)  # Convertir a dict con alias (_id -> id)
        result = await db.tareas.insert_one(dic_tarea)      # 
        return {"inserted_id": str(result.inserted_id)}
        
        
    # Funcion que nos permite obtener la informacion de una tarea concreta
    async def leer_tarea(self, id_tarea: str):
        if not ObjectId.is_valid(id_tarea):
            return {"message": "El tipo de dato recibido es erroneo"}
        coleccion = db["tareas"]
        tarea_buscada = await coleccion.find_one({"_id": ObjectId(id_tarea)})
        if tarea_buscada:
            tarea_buscada["_id"] = str(tarea_buscada["_id"])    # Cambiamos el tipo para que sea iterable
            return tarea_buscada
        else:
            return {"message": "Tarea no encontrada, algo ha ido muy mal"}
        
    # Funcion que nos permite listar las tareas a las que tiene acceso un usuario
    async def listar_tareas(self, id_usuario: str):
        user = await servicio_usuario.get_user_info(id_usuario)
        # print("ARCHIVO 3.9"+str(user))
        tipo_user = user["Role"]
        # print("ARCHIVO 3.99"+str(tipo_user))
        if tipo_user == 'user':
            print("ARCHIVO -0")
            tareas = self.listar_tareas_propias(id_usuario)
            print("ARCHIVO 2316"+str(tareas))
            return tareas
        
        elif tipo_user == 'admin':
            print("ARCHIVO 7")
            tareas =  db.tareas.find().to_list() 
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
            print("ARCHIVO 7")
            return tareas
    
     
    # Funcion que nos permite listar las tareas propias de un usuario
    async def listar_tareas_propias(self, id_usuario: str):
        print("ARCHIVO 6.5.4.3.2.1")
        user = await servicio_usuario.get_user_info(id_usuario)
        print("ARCHIVO 6.5.4.3.2")
        filtro = {
            "user_id": user["user_id"]
        }
        coleccion = db["tareas"]
        print("ARCHIVO 6.5.4.3"+str(coleccion))
        tareas = coleccion.find(filtro).to_list()
        print("ARCHIVO 6.5.4"+str(tareas))
        return tareas


    async def actualizar_tarea(self, id_tarea: str, tareaModificada: Tarea):
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
       

    async def eliminar_tarea(self, id_tarea: str):
        result =  db.tareas.delete_one({"_id": ObjectId(id_tarea)})
        if result.deleted_count == 1:
            return {"message": "Tarea eliminada correctamente"}
    