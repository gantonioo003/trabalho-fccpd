from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 101, "user_id": 1, "produto": "Notebook", "valor": 4500.0},
    {"id": 102, "user_id": 2, "produto": "Teclado Mecânico", "valor": 450.0},
    {"id": 103, "user_id": 1, "produto": "Headset", "valor": 350.0},
    {"id": 104, "user_id": 3, "produto": "Monitor", "valor": 1200.0},
]

@app.route("/")
def index():
    return "Microsserviço de Pedidos", 200

@app.route("/orders")
def get_orders():
    return jsonify(ORDERS), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)