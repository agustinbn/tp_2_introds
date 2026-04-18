from flask import Blueprint, jsonify, request

from db import get_db

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route("/", methods=["GET"])
def get_ranking():

    try:
        limit = request.args.get("limit", default=10, type=int)
        offset = request.args.get("offset", default=0, type=int)
    except ValueError:
        return jsonify({"error": "limit y offset deben ser números enteros"}), 400

    query = """
    SELECT
        u.id AS id_usuario,
        u.nombre,
        SUM(
            CASE 
                -- 3 PUNTOS: Acierto Exacto
                WHEN pr.local = JSON_EXTRACT(pa.resultado, '$.local') 
                 AND pr.visitante = JSON_EXTRACT(pa.resultado, '$.visitante') THEN 3
                
                -- 1 PUNTO: Acierto Tendencia (Ganador o Empate)
                WHEN SIGN(pr.local - pr.visitante) = SIGN(JSON_EXTRACT(pa.resultado, '$.local') - JSON_EXTRACT(pa.resultado, '$.visitante')) THEN 1
                
                ELSE 0 
            END
        ) AS puntos
    FROM usuarios u
    JOIN predicciones pr ON u.id = pr.id_usuario
    JOIN partidos pa ON pr.id_partido = pa.id
    WHERE pa.resultado IS NOT NULL
    GROUP BY u.id
    ORDER BY puntos DESC
    LIMIT %s OFFSET %s
    """
    
    try:
        conn= get_db()

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (limit, offset))
        ranking = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(ranking), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

