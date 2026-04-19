from flask import Blueprint, jsonify, request, url_for

from db import obtener_ranking
from exceptions import BadRequestError, Errores

ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/", methods=["GET"])
def get_ranking():
    offset = request.args.get("_offset", 0, type=int)
    limit = request.args.get("_limit", 10, type=int)

    if limit <= 0 or limit > 100:
        raise BadRequestError("El límite debe ser entre 1 y 100")
    if offset < 0:
        raise BadRequestError("El offset no puede ser negativo")

    try:
        ranking = obtener_ranking(limit, offset)
    except Exception:
        raise Errores("Error interno al consultar la base de datos")

    if not ranking:
        return jsonify([]), 204

    total_registros = len(ranking)

    prev_url = None
    prev_url = url_for(
        "ranking.get_ranking",
        _offset=max(0, offset - limit),
        _limit=limit,
        _external=True,
    )

    next_url = None
    if offset < total_registros - limit:
        next_url = url_for(
            "ranking.get_ranking",
            _offset=offset + limit,
            _limit=limit,
            _external=True,
        )
    else:
        next_url = url_for(
            "ranking.get_ranking",
            _offset=max(0, ((total_registros - 1) // limit) * limit),
            _limit=limit,
            _external=True,
        )

    return jsonify(
        {
            "ranking": ranking,
            "links": {
                "_first": {
                    "href": url_for(
                        "ranking.get_ranking", _offset=0, _limit=limit, _external=True
                    )
                },
                "_prev": {"href": prev_url},
                "_next": {"href": next_url},
                "_last": {
                    "href": url_for(
                        "ranking.get_ranking",
                        _offset=max(0, ((total_registros - 1) // limit) * limit),
                        _limit=limit,
                        _external=True,
                    )
                },
            },
        }
    )
