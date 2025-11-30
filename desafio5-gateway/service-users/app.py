from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "nome": "Ana", "email": "ana@example.com"},
    {"id": 2, "nome": "Bruno", "email": "bruno@example.com"},
    {"id": 3, "nome": "Carla", "email": "carla@example.com"},
]

@app.route("/")
def index():
    return "Microsserviço de Usuários", 200

@app.route("/users")
def get_users():
    return jsonify(USERS), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)