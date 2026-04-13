from flask import Blueprint, jsonify, request, url_for
from exceptions import BadRequestError, NotFoundError,Errores
import db

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
    data = request.json
    equipo_local = data.get("equipo_local")
    equipo_visitante = data.get("equipo_visitante")
    fase = data.get("fase")
    fecha = data.get("fecha")
    resultado = data.get("resultado")

    db.crear_partido(equipo_local, equipo_visitante, fase, fecha)

    return ("Partido agregado correctamente", 201)


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
