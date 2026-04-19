import json
from datetime import datetime

from flask import Blueprint, jsonify, request, url_for

from db import (
    actualizar_partido,
    actualizar_resultado,
    buscar_partido,
    buscar_usuario,
    contar_partido,
    crear_partido,
    crear_prediccion,
    eliminar_partido,
    existe_prediccion,
    obtener_partidos,
)
from exceptions import BadRequestError, ConflictError, Errores, NotFoundError

partidos_bp = Blueprint("partidos", __name__)


@partidos_bp.route("/", methods=["GET"])
def get_partidos():
    offset = request.args.get("_offset", 0, type=int)
    limit = request.args.get("_limit", 10, type=int)

    if limit <= 0 or limit > 100:
        raise BadRequestError("El límite debe ser entre 1 y 100")
    if offset < 0:
        raise BadRequestError("El offset no puede ser negativo")

    equipo = request.args.get("equipo")  # filtra local O visitante
    fecha = request.args.get("fecha")  # formato: YYYY-MM-DD
    fase = request.args.get("fase")

    try:
        total_registros = contar_partido(equipo, fase, fecha)

        if total_registros == 0:
            raise NotFoundError(
                message="No hay resultados",
                description="No se encontraron partidos que coincidan con los filtros especificados.",
            )
        partidos = obtener_partidos(limit, offset, equipo, fase, fecha)
    except Exception as e:
        if isinstance(e, (BadRequestError, NotFoundError)):
            raise e
        raise Errores("Error interno al consultar la base de datos")

    prev_url = None
    prev_url = url_for(
        "partidos.get_partidos",
        _offset=max(0, offset - limit),
        _limit=limit,
        equipo=equipo,
        fase=fase,
        fecha=fecha,
        _external=True,
    )

    next_url = None
    if offset < total_registros - limit:
        next_url = url_for(
            "partidos.get_partidos",
            _offset=offset + limit,
            _limit=limit,
            equipo=equipo,
            fase=fase,
            fecha=fecha,
            _external=True,
        )
    else:
        next_url = url_for(
            "partidos.get_partidos",
            _offset=max(0, ((total_registros - 1) // limit) * limit),
            _limit=limit,
            equipo=equipo,
            fase=fase,
            fecha=fecha,
            _external=True,
        )

    for partido in partidos:
        partido.pop("resultado")

    return jsonify(
        {
            "partidos": partidos,
            "links": {
                "_first": {
                    "href": url_for(
                        "partidos.get_partidos",
                        _offset=0,
                        _limit=limit,
                        equipo=equipo,
                        fase=fase,
                        fecha=fecha,
                        _external=True,
                    )
                },
                "_prev": {"href": prev_url},
                "_next": {"href": next_url},
                "_last": {
                    "href": url_for(
                        "partidos.get_partidos",
                        _offset=max(0, ((total_registros - 1) // limit) * limit),
                        _limit=limit,
                        equipo=equipo,
                        fase=fase,
                        fecha=fecha,
                        _external=True,
                    )
                },
            },
        }
    )


@partidos_bp.route("/", methods=["POST"])
def create_partido():
    data = request.get_json()

    required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    if not data or not all(campo in data for campo in required):
        raise BadRequestError(
            message="Faltan campos obligatorios",
            description=f"No se pudo completar la solicitud debido a la falta de uno/s de los campos requeridos que pueden ser {', '.join(required)}.",
        )

    if data["equipo_local"] == data["equipo_visitante"]:
        raise ConflictError(
            message="Los equipos no pueden ser iguales",
            description="El equipo local y el equipo visitante no pueden ser el mismo.",
        )

    try:
        fecha = datetime.fromisoformat(
            str(data["fecha"]).strip().replace("Z", "+00:00")
        ).date()
    except ValueError:
        raise BadRequestError(
            message="Fecha inválida", description="El formato de la fecha es inválido."
        )

    fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]

    if data["fase"] not in fases_validas:
        raise BadRequestError(
            message="Fase inválida", description="La fase especificada no es válida."
        )

    try:
        crear_partido(
            data["equipo_local"], data["equipo_visitante"], data["fase"], fecha
        )
    except Exception:
        raise Errores("Error interno al crear el partido")

    return "", 201


@partidos_bp.route("/<id>", methods=["GET"])
def get_partido(id):
    if not id.isdigit():
        raise BadRequestError(
            message="ID inválido",
            description="El ID del partido debe ser un número entero.",
        )

    try:
        partido = buscar_partido(id)
    except Exception:
        raise Errores("Error interno al obtener el partido")

    if partido is None:
        raise NotFoundError(
            "Partido no encontrado",
            description=f"No se encontró un partido con el ID {id}",
        )

    if partido.get("fecha"):
        partido["fecha"] = str(partido["fecha"])

    if partido.get("resultado"):
        partido["resultado"] = json.loads(partido["resultado"])

    return jsonify(partido), 200


@partidos_bp.route("/<int:id>", methods=["PUT"])
def update_partido(id):
    data = request.get_json()
    if not data:
        raise BadRequestError(
            message="Datos requeridos",
            description="No se pudo completar la solicitud debido a la falta de datos en el cuerpo de la solicitud.",
        )

    required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    if not all(campo in data for campo in required):
        raise BadRequestError(
            message="Faltan campos obligatorios",
            description=f"No se pudo completar la solicitud debido a la falta de uno/s de los campos requeridos que pueden ser {', '.join(required)}.",
        )

    if data["equipo_local"] == data["equipo_visitante"]:
        raise BadRequestError(
            message="Los equipos no pueden ser iguales",
            description="El equipo local y el equipo visitante no pueden ser el mismo.",
        )

    try:
        fecha = datetime.fromisoformat(
            str(data["fecha"]).strip().replace("Z", "+00:00")
        ).date()
    except ValueError:
        raise BadRequestError(
            message="Fecha inválida", description="El formato de la fecha es inválido."
        )

    fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
    if data["fase"] not in fases_validas:
        raise BadRequestError(
            message="Fase inválida", description="La fase especificada no es válida."
        )

    try:
        partido = buscar_partido(id)
    except Exception:
        raise Errores("Error interno al obtener el partido")

    if not partido:
        raise BadRequestError(
            "Partido no encontrado",
            description=f"No se encontró un partido con el ID {id}",
        )

    try:
        actualizar_partido(
            id, data["equipo_local"], data["equipo_visitante"], data["fase"], fecha
        )
    except Exception:
        raise Errores("Error interno al actualizar el partido")
    return "", 204


@partidos_bp.route("/<int:id>", methods=["PATCH"])
def patch_partido(id):
    partido = buscar_partido(id)
    if partido is None:
        raise NotFoundError(
            "Partido no encontrado",
            description=f"No se encontró un partido con el ID {id}",
        )

    data = request.get_json()
    if not data:
        raise BadRequestError(
            message="Datos requeridos",
            description="No se pudo completar la solicitud debido a la falta de datos en el cuerpo de la solicitud.",
        )

    # Get current values
    equipo_local = data.get("equipo_local", partido["equipo_local"])
    equipo_visitante = data.get("equipo_visitante", partido["equipo_visitante"])
    fase = data.get("fase", partido["fase"])
    fecha_str = data.get("fecha", str(partido["fecha"]))

    # Validate
    if equipo_local == equipo_visitante:
        raise BadRequestError(
            message="Los equipos no pueden ser iguales",
            description="El equipo local y el equipo visitante no pueden ser el mismo.",
        )

    try:
        fecha = datetime.fromisoformat(
            str(fecha_str).strip().replace("Z", "+00:00")
        ).date()
    except ValueError:
        raise BadRequestError(
            message="Fecha inválida", description="El formato de la fecha es inválido."
        )

    fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
    if fase not in fases_validas:
        raise BadRequestError(
            message="Fase inválida", description="La fase especificada no es válida."
        )

    try:
        actualizar_partido(id, equipo_local, equipo_visitante, fase, fecha)
    except Exception:
        raise Errores("Error interno al actualizar el partido")
    return "", 204


@partidos_bp.route("/<id>", methods=["DELETE"])
def delete_partido(id):
    if not id.isdigit():
        raise BadRequestError(
            message="ID inválido",
            description="El ID del partido debe ser un número entero.",
        )
    try:
        partido = buscar_partido(id)
    except Exception:
        raise Errores("Error interno al obtener el partido")

    if not partido:
        raise NotFoundError(
            message="Partido no encontrado",
            description=f"No se encontraron partidos con el id {id}.",
        )

    try:
        eliminar_partido(id)
    except Exception:
        raise Errores("Error interno al eliminar el partido")

    return jsonify({}), 204


@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def update_resultado(id):
    data = request.get_json()
    if not data:
        raise BadRequestError(
            message="Datos requeridos",
            description="No se pudo completar la solicitud debido a la falta de datos en el cuerpo de la solicitud.",
        )
    if "local" not in data or "visitante" not in data:
        raise BadRequestError(
            message="Faltan campos local y visitante",
            description="No se pudo completar la solicitud debido a la falta de uno/s de los campos requeridos.",
        )

    try:
        partido = buscar_partido(id)
    except Exception:
        raise Errores("Error interno al obtener el partido")
    if partido is None:
        raise NotFoundError(
            "Partido no encontrado",
            description=f"No se encontró un partido con el ID {id}",
        )

    try:
        local = int(data["local"])
        visitante = int(data["visitante"])
        if local < 0 or visitante < 0:
            raise BadRequestError(
                message="Goles inválidos",
                description="Los goles no pueden ser negativos.",
            )
    except Exception:
        raise BadRequestError(
            message="Goles inválidos",
            description="Los goles deben ser enteros no negativos.",
        )

    resultado = {"local": local, "visitante": visitante}

    try:
        actualizar_resultado(id, resultado)
    except Exception:
        raise Errores("Error interno al actualizar el resultado")

    return "", 204


@partidos_bp.route("/<int:partido_id>/prediccion", methods=["POST"])
def create_prediccion(partido_id):
    data = request.get_json()
    usuario_id = data.get("id_usuario")
    goles_local = data.get("local")
    goles_visitante = data.get("visitante")
    if usuario_id is None or goles_local is None or goles_visitante is None:
        raise BadRequestError(
            message="Faltan campos obligatorios",
            description="No se pudo completar la solicitud debido a la falta de uno/s de los campos requeridos que pueden ser usuario_id, local y visitante.",
        )
    if goles_local < 0 or goles_visitante < 0:
        raise BadRequestError(
            message="Goles inválidos", description="Los goles no pueden ser negativos."
        )

    partido = buscar_partido(partido_id)
    if not partido:
        raise NotFoundError(
            message="Partido no encontrado",
            description=f"No se encontraron partidos con el id {partido_id}.",
        )

    partido_jugado = partido["resultado"] is not None
    if partido_jugado:
        raise ConflictError(
            message="Partido ya jugado",
            description="Este partido ya esta jugado y no puede ser predecido.",
        )

    usuario = buscar_usuario(usuario_id)
    if not usuario:
        raise NotFoundError(
            message="Usuario no encontrado",
            description=f"No se encontraron usuarios con el id {usuario_id}.",
        )

    if existe_prediccion(usuario_id, partido_id):
        raise ConflictError(
            message="Prediccion ya existe",
            description="Ya existe una prediccion para este partido.",
        )

    try:
        crear_prediccion(usuario_id, partido_id, goles_local, goles_visitante)
    except Exception:
        raise Errores("Error interno al crear la prediccion")

    return "", 201
