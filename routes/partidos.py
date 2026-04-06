from flask import Blueprint

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
