from flask import Blueprint, request


predicciones_bp = Blueprint("predicciones", __name__)


# esto es un scaffold, ya que aun no tengo los datos para plantear bien la estructura del problema

@predicciones_bp.route("/partidos/<int:partido_id>/prediccion", methods=["POST"])
def create_prediccion(partido_id):
 data = request.get_json()
 # usamos el json para los usuarios y goles 
 usuario_id = data.get("usuario_id")
 goles_local = data.get("goles_local")
 goles_visitante = data.get("goles_visitante")
 if not usuario_id or goles_local is None or goles_visitante is None:
    return {"error": "faltan datos"}, 400

 partido = buscar_partido(partido_id)
 if not partido:
    return 404, error

 else :  
     if partido_ya_jugado(partido):
        return error, "Este partido ya esta jugado y no puede ser predecido"
     else:
        usuario = buscar_usuario(usuario_id)
        if not usuario:
          return error
        if existe_prediccion(usuario_id, partido_id):
          return error
        else:
          
            prediccion = crear_prediccion(usuario_id, partido_id, goles_local, goles_visitante)
            return prediccion


   
     