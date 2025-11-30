import os
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

# Configurações vindas de variáveis de ambiente (definidas no docker-compose.yml)
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "desafio3db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "senha")

REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Conexões globais (preguiçosas)
_db_conn = None
_redis_client = None


def get_db_connection():
    global _db_conn
    if _db_conn is None or _db_conn.closed != 0:
        _db_conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
    return _db_conn


def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return _redis_client


@app.route("/")
def index():
    return "Web service do Desafio 3 está no ar!", 200


@app.route("/db")
def db_example():
    conn = get_db_connection()
    cur = conn.cursor()

    # Cria tabela se não existir
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS visitas (
            id SERIAL PRIMARY KEY,
            mensagem TEXT NOT NULL
        );
        """
    )

    # Insere nova visita
    cur.execute(
        "INSERT INTO visitas (mensagem) VALUES (%s);",
        ("Visita registrada pelo serviço web.",),
    )

    # Conta quantas visitas existem
    cur.execute("SELECT COUNT(*) FROM visitas;")
    total, = cur.fetchone()

    conn.commit()
    cur.close()

    return jsonify({"mensagem": "Registro salvo no banco!", "total_visitas": total})


@app.route("/cache")
def cache_example():
    client = get_redis_client()
    # Incrementa um contador no Redis
    total = client.incr("contador_cache")
    return jsonify({"mensagem": "Contador no Redis incrementado!", "valor": int(total)})


if __name__ == "__main__":
    # Porta 8080 para combinar com o mapeamento do docker-compose
    app.run(host="0.0.0.0", port=8080)
