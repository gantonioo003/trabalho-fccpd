import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://service-users:5000")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://service-orders:5000")

@app.route("/")
def index():
    return "API Gateway - ponto único de entrada", 200

@app.route("/users")
def gateway_users():
    try:
        resp = requests.get(f"{USERS_SERVICE_URL}/users", timeout=5)
        resp.raise_for_status()
        users = resp.json()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"erro": f"Falha ao acessar serviço de usuários: {str(e)}"}), 502

@app.route("/orders")
def gateway_orders():
    try:
        resp = requests.get(f"{ORDERS_SERVICE_URL}/orders", timeout=5)
        resp.raise_for_status()
        orders = resp.json()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"erro": f"Falha ao acessar serviço de pedidos: {str(e)}"}), 502

@app.route("/report")
def gateway_report():
    """
    Endpoint opcional que combina usuários e pedidos:
    retorna, por usuário, seus pedidos.
    """
    try:
        users_resp = requests.get(f"{USERS_SERVICE_URL}/users", timeout=5)
        users_resp.raise_for_status()
        users = users_resp.json()

        orders_resp = requests.get(f"{ORDERS_SERVICE_URL}/orders", timeout=5)
        orders_resp.raise_for_status()
        orders = orders_resp.json()
    except Exception as e:
        return jsonify({"erro": f"Falha ao acessar microsserviços: {str(e)}"}), 502

    # Indexar pedidos por user_id
    pedidos_por_usuario = {}
    for order in orders:
        uid = order["user_id"]
        pedidos_por_usuario.setdefault(uid, []).append(order)

    relatorio = []
    for user in users:
        uid = user["id"]
        user_orders = pedidos_por_usuario.get(uid, [])
        relatorio.append({
            "usuario": user["nome"],
            "email": user["email"],
            "total_pedidos": len(user_orders),
            "pedidos": user_orders,
        })

    return jsonify({"total_usuarios": len(users), "relatorio": relatorio}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
