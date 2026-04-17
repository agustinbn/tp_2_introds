from flask import Blueprint, jsonify, request

from db import (
    actualizar_usuario,
    buscar_usuario,
    crear_usuario,
    eliminar_usuario,
    obtener_usuarios,
)

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    usuarios = obtener_usuarios()

    if not usuarios:
        return jsonify([]), 204

    for usuario in usuarios:
        usuario.pop("email")

    return jsonify(usuarios), 200


@usuarios_bp.route("/", methods=["POST"])
def create_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if nombre is None or email is None:
        return "Nombre y email son requeridos", 400

    crear_usuario(nombre, email)
    return "", 201


@usuarios_bp.route("/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = buscar_usuario(id)

    if not usuario:
        return jsonify({}), 404

    return jsonify(usuario), 200


@usuarios_bp.route("/<int:id>", methods=["PUT"])
def update_usuario(id):
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if nombre is None or email is None:
        return "Nombre y email son requeridos", 400

    usuario = buscar_usuario(id)

    if not usuario:
        return jsonify({}), 404

    actualizar_usuario(id, nombre, email)
    return jsonify(usuario), 200


@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    usuario = buscar_usuario(id)

    if id is None:
        return jsonify({}), 400

    if not usuario:
        return jsonify({}), 404

    eliminar_usuario(id)
    return "Hello, World!"
