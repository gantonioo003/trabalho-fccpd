from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "nome": "Ana", "ativo_desde": "2023-01-10"},
    {"id": 2, "nome": "Bruno", "ativo_desde": "2022-06-05"},
    {"id": 3, "nome": "Carla", "ativo_desde": "2024-03-20"},
]


@app.route("/users")
def get_users():
    return jsonify(USERS), 200


@app.route("/")
def index():
    return "Microsserviço A - Lista de usuários", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)