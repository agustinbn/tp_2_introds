from datetime import datetime

from flask import Blueprint, jsonify, request

from db import (
    buscar_partido,
    buscar_usuario,
    crear_partido,
    crear_prediccion,
    eliminar_partido,
    existe_prediccion,
)

partidos_bp = Blueprint("partidos", __name__)


@partidos_bp.route("/", methods=["GET"])
def get_partidos():
    return "Hello, World!"


@partidos_bp.route("/", methods=["POST"])
def create_partido():
    data = request.get_json()

    required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    if not data or not all(campo in data for campo in required):
        return jsonify(
            {
                "errors": [
                    {
                        "code": "400",
                        "message": "Faltan campos obligatorios",
                        "level": "error",
                    }
                ]
            }
        ), 400

    if data["equipo_local"] == data["equipo_visitante"]:
        return jsonify(
            {
                "errors": [
                    {
                        "code": "400",
                        "message": "Los equipos no pueden ser iguales",
                        "level": "error",
                    }
                ]
            }
        ), 400

    try:
        fecha = datetime.fromisoformat(
            str(data["fecha"]).strip().replace("Z", "+00:00")
        ).date()
    except ValueError:
        return jsonify(
            {
                "errors": [
                    {
                        "code": "400",
                        "message": "Fecha inválida",
                        "level": "error",
                    }
                ]
            }
        ), 400

    fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]

    if data["fase"] not in fases_validas:
        return jsonify(
            {"errors": [{"code": "400", "message": "Fase inválida", "level": "error"}]}
        ), 400

    crear_partido(data["equipo_local"], data["equipo_visitante"], data["fase"], fecha)

    return jsonify(data), 201


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
    partido = buscar_partido(id)

    if not partido:
        return jsonify(
            {
                "errors": [
                    {
                        "code": "404",
                        "message": "Partido no encontrado",
                        "level": "error",
                    }
                ]
            }
        ), 404

    eliminar_partido(id)

    return jsonify({}), 204


@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def update_resultado(id):
    return "Hello, World!"


predicciones_bp = Blueprint("predicciones", __name__)


@predicciones_bp.route("/partidos/<int:partido_id>/prediccion", methods=["POST"])
def create_prediccion(partido_id):
    data = request.get_json()
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
