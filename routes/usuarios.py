from flask import Blueprint, jsonify, request, url_for

from db import (
    actualizar_usuario,
    buscar_usuario,
    crear_usuario,
    eliminar_usuario,
    obtener_usuarios,
)
from exceptions import BadRequestError, Errores, NotFoundError

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    offset = request.args.get("_offset", 0, type=int)
    limit = request.args.get("_limit", 10, type=int)

    if limit <= 0 or limit > 100:
        raise BadRequestError("El límite debe ser entre 1 y 100")
    if offset < 0:
        raise BadRequestError("El offset no puede ser negativo")

    try:
        usuarios = obtener_usuarios()
    except Exception:
        raise Errores("Error interno al consultar la base de datos")

    total_registros = len(usuarios)

    if not usuarios:
        return jsonify([]), 204

    for usuario in usuarios:
        usuario.pop("email")

    prev_url = None
    prev_url = url_for(
        "usuarios.get_usuarios",
        _offset=max(0, offset - limit),
        _limit=limit,
        _external=True,
    )

    next_url = None
    if offset < total_registros - limit:
        next_url = url_for(
            "usuarios.get_usuarios",
            _offset=offset + limit,
            _limit=limit,
            _external=True,
        )
    else:
        next_url = url_for(
            "usuarios.get_usuarios",
            _offset=max(0, ((total_registros - 1) // limit) * limit),
            _limit=limit,
            _external=True,
        )

    return jsonify(
        {
            "usuarios": usuarios,
            "links": {
                "_first": {
                    "href": url_for(
                        "usuarios.get_usuarios", _offset=0, _limit=limit, _external=True
                    )
                },
                "_prev": {"href": prev_url},
                "_next": {"href": next_url},
                "_last": {
                    "href": url_for(
                        "usuarios.get_usuarios",
                        _offset=max(0, ((total_registros - 1) // limit) * limit),
                        _limit=limit,
                        _external=True,
                    )
                },
            },
        }
    ), 200


@usuarios_bp.route("/", methods=["POST"])
def create_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if nombre is None or email is None:
        raise BadRequestError("Nombre y email son requeridos")

    try:
        crear_usuario(nombre, email)
    except Exception:
        raise Errores("Error interno al crear el usuario")

    return "", 201


@usuarios_bp.route("/<int:id>", methods=["GET"])
def get_usuario(id):
    try:
        usuario = buscar_usuario(id)
    except Exception:
        raise Errores("Error interno al obtener el usuario")

    if not usuario:
        raise NotFoundError(
            "Usuario no encontrado",
            description=f"No se encontró un usuario con el ID {id}",
        )

    return jsonify(usuario), 201


@usuarios_bp.route("/<int:id>", methods=["PUT"])
def update_usuario(id):
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if nombre is None or email is None:
        raise BadRequestError("Nombre y email son requeridos")

    try:
        usuario = buscar_usuario(id)
    except Exception:
        raise Errores("Error interno al obtener el usuario")

    if not usuario:
        raise NotFoundError(
            "Usuario no encontrado",
            description=f"No se encontró un usuario con el ID {id}",
        )

    try:
        actualizar_usuario(id, nombre, email)
    except Exception:
        raise Errores("Error interno al actualizar el usuario")
    return jsonify(usuario), 204


@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    if id is None:
        raise BadRequestError("ID es requerido")

    try:
        usuario = buscar_usuario(id)
    except Exception:
        raise Errores("Error interno al obtener el usuario")

    if not usuario:
        raise NotFoundError(
            "Usuario no encontrado",
            description=f"No se encontró un usuario con el ID {id}",
        )

    try:
        eliminar_usuario(id)
    except Exception:
        raise Errores("Error interno al eliminar el usuario")
    return "", 204
