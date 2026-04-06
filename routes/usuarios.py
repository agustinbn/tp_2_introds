from flask import Blueprint

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    return "Hello, World!"


@usuarios_bp.route("/", methods=["POST"])
def create_usuario():
    return "Hello, World!"


@usuarios_bp.route("/<int:id>", methods=["GET"])
def get_usuario(id):
    return "Hello, World!"


@usuarios_bp.route("/<int:id>", methods=["PUT"])
def update_usuario(id):
    return "Hello, World!"


@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    return "Hello, World!"
