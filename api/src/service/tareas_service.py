from repository.tareas_repository import TareasRepository
from dto.tarea import Tarea

class TareaService:
  def __init__(self):
    self.tareas_repository = TareasRepository() 

  def crear_tarea(nueva_tarea: Tarea):
    try:
      return self.tareas_repository.crear_tarea(nueva_tarea)
    except Exception as e:
      raise RuntimeError(f"Ha habido un error en el servicio de tareas{str(e)}")
        

  def leer_tarea(id_tarea: str):
    try:  
      return self.tareas_repository.leer_tarea(id_tarea)
    except Exception as e:
      raise RuntimeError(f"Ha habido un error en el servicio de tareas{str(e)}")  
          

  def listar_tareas(id_usuario: str):
    try:  
      return self.tareas_repository.listar_tareas(id_usuario)
    except Exception as e:
      raise RuntimeError(f"Ha habido un error en el servicio de tareas{str(e)}")  
          

  def actualizar_tarea(id_tarea: str, tareaModificada: Tarea):
    try:  
      return self.tareas_repository.actualizar_tarea(id_tarea, tareaModificada)
    except Exception as e:
      raise RuntimeError(f"Ha habido un error en el servicio de tareas{str(e)}")  
          

  def eliminar_tarea(id_tarea: str):
    try:  
      return self.tareas_repository.eliminar_tarea(id_tarea)
    except Exception as e:
      raise RuntimeError(f"Ha habido un error en el servicio de tareas{str(e)}")  
          