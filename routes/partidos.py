from datetime import datetime

from flask import Blueprint, jsonify, request, url_for

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
    offset = request.args.get('_offset', 0, type=int)
    limit = request.args.get('_limit', 10, type=int)

    if limit <= 0 or limit > 100:
        raise BadRequestError("El límite debe ser entre 1 y 100")
    if offset < 0:
        raise BadRequestError("El offset no puede ser negativo")

    equipo = request.args.get('equipo', None, type=str)
    fase = request.args.get('fase', None, type=str)
    fecha = request.args.get('fecha', None, type=str)

    try:
        total_registros = db.contar_partido(equipo, fase, fecha)

        if total_registros == 0:
            raise NotFoundError(
                message="No hay resultados",
                description=f"No se encontraron partidos para el equipo '{equipo}' en la fase '{fase}'."
            )
        partidos = db.obtener_partidos(limit, offset, equipo, fase, fecha)
    except Exception as e:
        if isinstance(e, (BadRequestError, NotFoundError)):
            raise e
        raise Errores("Error interno al consultar la base de datos", status_code=500)

    total_paginas = (total_registros + limit - 1) // limit

    prev_url = None
    prev_url = url_for('partidos.get_partidos', _offset=max(0, offset - limit), _limit=limit,equipo=equipo, fase=fase, fecha=fecha, _external=True)

    next_url = None
    if offset < total_registros - limit:
        next_url = url_for('partidos.get_partidos', _offset=offset + limit, _limit=limit,equipo=equipo, fase=fase, fecha=fecha, _external=True)
    else:
        next_url = url_for('partidos.get_partidos', _offset=max(0, ((total_registros - 1) // limit) * limit), _limit=limit,equipo=equipo, fase=fase, fecha=fecha, _external=True)

    return jsonify({
        "partidos": partidos,
        "links": {
            "_first": {
                "href":url_for('partidos.get_partidos', _offset=0, _limit=limit,equipo=equipo, fase=fase, fecha=fecha, _external=True)
            },
            "_prev": {
                "href":prev_url
            },
            "_next": {
                "href":next_url
            },
            "_last": {
                "href":url_for('partidos.get_partidos', _offset= max(0, ((total_registros - 1) // limit) * limit), _limit=limit,equipo=equipo, fase=fase, fecha=fecha, _external=True)
            }
        }
    })


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
