from repository.survey_repository import SurveyRepository


class encuestaService:
  def __init__(self):
    self.survey_repository = SurveyRepository()
    
  # Las funciones necesarias son las mismas que en tareas_repository
  def crear_encuesta(self, nombre_encuesta: str, idioma: str):
    try:
      return api.add_survey(nombre_encuesta, idioma)
    except Exception as e:
      raise RuntimeError(f"EncuestaServices: algo fue mal en create_encuesta: {str(e)}")


  def listar_encuestas(self):
    try:
      surveys = api.list_surveys()
      cont = 0
      datos = {}
      for sid, survey_title in surveys:
          datos[f"{sid}"] = survey_title
          cont += 1
      return datos
    except Exception as e:
      raise RuntimeError(f"EncuestaServices: algo fue mal en listar_encuestas: {str(e)}")
    

  def eliminar_encuesta(self, id: str):
    try:
      return self.survey_repository.eliminar_encuesta(id=id)
    except Exception as e:
      raise RuntimeError(f"EncuestaServices: algo fue mal en eliminar_encuesta: {str(e)}")
  
