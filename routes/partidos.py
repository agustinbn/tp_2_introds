from flask import Blueprint, request
from db import (
    buscar_partido,
    buscar_usuario,
    crear_prediccion,
    existe_prediccion
)

partidos_bp = Blueprint("partidos", __name__)


@partidos_bp.route("/", methods=["GET"])
def get_partidos():
    return "Hello, World!"


@partidos_bp.route("/", methods=["POST"])
def create_partido():
    return "Hello, World!"


@partidos_bp.route("/<int:id>", methods=["GET"])
def get_partido(id):
    return "Hello, World!"


@partidos_bp.route("/<int:id>", methods=["PUT"])
def update_partido(id):
    return "Hello, World!"


@partidos_bp.route("/<int:id>", methods=["PATCH"])
def patch_partido(id):
    return "Hello, World!"


@partidos_bp.route("/<int:id>", methods=["DELETE"])
def delete_partido(id):
    return "Hello, World!"


@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def update_resultado(id):
    return "Hello, World!"



predicciones_bp = Blueprint("predicciones", __name__)

# esto es un scaffold, ya que aun no tengo los datos para plantear bien la estructura del problema

@predicciones_bp.route("/partidos/<int:partido_id>/prediccion", methods=["POST"])
def create_prediccion(partido_id):
 data = request.get_json()
 #    json para los usuarios y goles 
 usuario_id = data.get("usuario_id")
 goles_local = data.get("local")
 goles_visitante = data.get("visitante")
 if usuario_id is None or goles_local is None or goles_visitante is None:
    return {"error": "faltan datos"}, 400
 if goles_local < 0 or goles_visitante < 0:
    return {"error": "Los goles no pueden ser negativos"}, 400
 
 partido = buscar_partido(partido_id)
 if not partido:
    return {"error": "Partido no encontrado"}, 404
 
 partido_jugado = partido["resultado"] is not None
 if partido_jugado:
    return {"error": "Este partido ya esta jugado y no puede ser predecido"}, 400
     
 usuario = buscar_usuario(usuario_id)
 if not usuario:
    return {"error": "Usuario no encontrado"}, 404
 
 if existe_prediccion(usuario_id, partido_id):
    return {"error": "Ya existe una prediccion para este partido"}, 409
 
 crear_prediccion(usuario_id, partido_id, goles_local, goles_visitante)
 return {"mensaje": "prediccion creada"}, 201