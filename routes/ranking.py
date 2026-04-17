from flask import Blueprint

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route("/", methods=["GET"])
def get_ranking():
    return "Hello, World!" 