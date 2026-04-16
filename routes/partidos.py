from datetime import datetime

from flask import Blueprint, jsonify, request

from db import buscar_partido, crear_partido, eliminar_partido

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
