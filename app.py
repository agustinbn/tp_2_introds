from flask import Flask, jsonify
from routes.partidos import partidos_bp
from routes.usuarios import usuarios_bp
from routes.ranking import ranking_bp
from exceptions import Errores, BadRequestError, NotFoundError

app = Flask(__name__)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(ranking_bp, url_prefix="/ranking")


@app.route("/")
def index():
    return "Hello, World!"

@app.errorhandler(Errores)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)
