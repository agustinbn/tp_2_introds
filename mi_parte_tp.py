from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# "Base de datos" en memoria
partidos = []
ultimo_id = 0

# =========================
# POST /partidos
# =========================
@app.route('/partidos', methods=['POST'])
def crear_partido():
    global ultimo_id

    data = request.get_json()

    # Validar body
    required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    if not data or not all(campo in data for campo in required):
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Faltan campos obligatorios",
                "level": "error"
            }]
        }), 400

    # Validar equipos distintos
    if data["equipo_local"] == data["equipo_visitante"]:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Los equipos no pueden ser iguales",
                "level": "error"
            }]
        }), 400

    # Validar fecha
    try:
        datetime.fromisoformat(data["fecha"])
    except:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Fecha inválida (usar YYYY-MM-DD)",
                "level": "error"
            }]
        }), 400

    # Validar fase
    fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]

    if data["fase"] not in fases_validas:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Fase inválida",
                "level": "error"
            }]
        }), 400

    # Crear partido
    ultimo_id += 1

    nuevo = {
        "id": ultimo_id,
        "equipo_local": data["equipo_local"],
        "equipo_visitante": data["equipo_visitante"],
        "fecha": data["fecha"],
        "fase": data["fase"]
    }

    partidos.append(nuevo)

    return jsonify(nuevo), 201


# =========================
# DELETE /partidos/{id}
# =========================
@app.route('/partidos/<int:id>', methods=['DELETE'])
def eliminar_partido(id):
    global partidos

    for p in partidos:
        if p["id"] == id:
            partidos = [x for x in partidos if x["id"] != id]
            return '', 204

    return jsonify({
        "errors": [{
            "code": "404",
            "message": "Partido no encontrado",
            "level": "error"
        }]
    }), 404


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)