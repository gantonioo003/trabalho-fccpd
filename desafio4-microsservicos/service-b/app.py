import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# URL do serviço A
SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:5000")

@app.route("/")
def index():
    return "Microsserviço B - Relatórios de usuários", 200

@app.route("/report")
def report():
    try:
        response = requests.get(f"{SERVICE_A_URL}/users", timeout=5)
        response.raise_for_status()
        users = response.json()
    except Exception as e:
        return jsonify({"erro": f"Falha ao chamar serviço A: {str(e)}"}), 500

    relatorio = [
        f"Usuário {u['nome']} ativo desde {u['ativo_desde']}."
        for u in users
    ]

    return jsonify({
        "origem": SERVICE_A_URL,
        "total_usuarios": len(users),
        "relatorio": relatorio
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)