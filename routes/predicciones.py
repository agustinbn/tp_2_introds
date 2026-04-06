from flask import Blueprint

predicciones_bp = Blueprint("predicciones", __name__)

@predicciones_bp.route("/", methods=["POST"])
def create_prediccion():
    return "Hello, World!"