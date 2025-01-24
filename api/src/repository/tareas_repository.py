from sqlalchemy.orm import Session
from model.user import User
from datetime import datetime

from utils.utils import pwd_context
from utils.db_connections import create_db_connection

class SurveyRepository:
    
    def __init__(self) -> None:
        self.db = create_db_connection()

    # Funciones necesarias: 
    # Crear tarea 
    # Leer tarea
    # Modificar tarea
    # Eliminar tarea 
    # Listar tareas para usuario determinado
    def create_survey_in_db(self, nombre: str, id_usuario: int):
        encuestas = api.list_surveys()
        for i in encuestas:
            if i[1] == nombre:
                id_formulario_version = i[0]
                break
        db_formulario = Formulario(id_formulario=id_formulario_version, nombre=nombre, id_usuario=id_usuario)
        self.db.add(db_formulario)
        self.db.commit()
        self.db.refresh(db_formulario)

        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")

        db_Vformulario = VersionFormulario(id_formulario=id_formulario_version, id_version_formulario=id_formulario_version, fecha=formatted_date)
        self.db.add(db_Vformulario)
        self.db.commit()
        self.db.refresh(db_Vformulario)
        return db_formulario
    

    def eliminar_encuesta(self, id: str):
        try:
            db_formado = self.db.query(Formado).filter(Formado.id_formulario == id).first()
            db_Vformulario = self.db.query(VersionFormulario).filter(VersionFormulario.id_formulario == id).first()
            db_formulario = self.db.query(Formulario).filter(Formulario.id_formulario == id).first()
            
            if db_formado:
                self.db.delete(db_formado)
                self.db.commit()

            if db_Vformulario:
                self.db.delete(db_Vformulario)
                self.db.commit()

            self.db.delete(db_formulario)
            self.db.commit()

            api.delete_survey(id)

            return {"mensaje": "Formulario eliminado correctamente"}

        except Exception as e:
            print(f"Error al eliminar la encuesta: {e}")
            return {"error": str(e)}

        

    