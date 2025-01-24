import json
from model.user import User

from fastapi import HTTPException
from utils.utils import pwd_context
from utils.db_connections import create_db_connection

class UserRepository:
    
    def __init__(self) -> None:
        self.db = create_db_connection()

    # Funciones necesarias: 
    # 1-Tareas asignadas al usuario
    
    def get_user_db(self, name: str):
        return self.db.query(User).filter(User.nombre_y_apellidos == name).first()
    
    
    def obtener_rol(self, name: str):
        user = self.db.query(User).filter(User.nombre_y_apellidos == name).first()
        if user:
            id_actual = user.id_usuario
            roleA = self.db.query(Administrador).filter(Administrador.id_usuario == id_actual).first()
            roleB = self.db.query(Profesional).filter(Profesional.id_usuario == id_actual).first()
            roleC = self.db.query(Paciente).filter(Paciente.id_usuario == id_actual).first()
            if roleA != None:
                return 'admin'
            elif roleB!= None:
                return 'profesional'
            elif roleC != None:
                return 'paciente'
        else:
            return None
        return None
    
    
    def cita_user(self, descripcion: str, fecha: str, hora: str, id_paciente: str, id_profesional: str):
        hora_ajustada = hora + ':00'
        
        try:
            db_sesion = Sesion(
                numero_sesion='1',
                fecha=fecha, 
                hora=hora_ajustada, 
                asistencia='PC', 
                observaciones=True, 
                id_usuario_profesional=id_profesional, 
                id_usuario_paciente=id_paciente
            )
            self.db.add(db_sesion)
            self.db.commit()
            self.db.refresh(db_sesion)
            return {'resultado': 'todo ok'}
        except Exception as e:
            self.db.rollback()
            print(f"Error2342342: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    def get_cita(self, id: str):
        
        try:
            sesion = self.db.query(Sesion).filter(Sesion.id_usuario_paciente == id).first()
            return {'fecha': sesion.fecha, 'hora':sesion.hora, 'asistencia': sesion.asistencia}
        except Exception as e:
            self.db.rollback()
            print(f"Error2342342: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    