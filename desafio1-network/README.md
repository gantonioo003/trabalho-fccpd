### 📦 Desafio 1 – Comunicação entre Containers em Rede (FCCPD)

Este desafio demonstra o funcionamento básico de comunicação entre containers Docker utilizando redes internas.
O objetivo é mostrar como dois serviços isolados podem se comunicar pelo nome do container, sem depender de IP fixo, usando o DNS interno do Docker.

🎯 Objetivo

Criar dois containers:

server → servidor Flask respondendo em http://server:5000

client → container que chama o servidor periodicamente usando curl

Ambos devem estar na mesma rede Docker chamada fccpd_net.

### 🧱 Estrutura de Pastas
desafio1-network/
  server/
    app.py
    Dockerfile
  client/
    entrypoint.sh
    Dockerfile
  README.md

### 🖥️ Arquitetura do Sistema
            Rede Docker: fccpd_net
┌───────────────────────────────────────────┐
│                                           │
│   +----------------------+                │
│   |       server         |                │
│   |  Flask (porta 5000)  |                │
│   +----------------------+                │
│                 ▲                          │
│                 │ HTTP                     │
│                 ▼                          │
│   +----------------------+                │
│   |       client         |                │
│   |  loop com curl       |                │
│   +----------------------+                │
│                                           │
└───────────────────────────────────────────┘


A rede interna criada: fccpd_net

O client acessa o servidor através do hostname: http://server:5000

### 🐍 Código do Servidor (Flask)

Arquivo: server/app.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from server (desafio1-network)!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

🐳 Dockerfile do Servidor

Arquivo: server/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

### 📄 Script do Cliente

Arquivo: client/entrypoint.sh

#!/bin/sh

echo "Iniciando client... Vou ficar chamando http://server:5000 a cada 3 segundos."
while true; do
  echo "-----"
  date
  curl -s http://server:5000 || echo "Erro ao conectar no server"
  sleep 3
done

### 🐳 Dockerfile do Cliente

Arquivo: client/Dockerfile

FROM alpine:3.19

RUN apk add --no-cache curl

WORKDIR /app

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]

### 🚀 Como Executar o Projeto
1️⃣ Criar a rede Docker
docker network create fccpd_net

2️⃣ Construir as imagens
docker build -t fccpd-desafio1-server ./server
docker build -t fccpd-desafio1-client ./client

3️⃣ Subir o servidor (Flask)
docker run -d --name server --network fccpd_net -p 5000:5000 fccpd-desafio1-server


Testar no navegador:

http://localhost:5000


Ou no PowerShell:

curl http://localhost:5000

4️⃣ Subir o cliente
docker run -it --name client --network fccpd_net fccpd-desafio1-client

Saída esperada:
-----
Sat Nov 30 05:12:00 UTC 2025
Hello from server (desafio1-network)!
-----
Sat Nov 30 05:12:03 UTC 2025
Hello from server (desafio1-network)!

### 🧠 Conceitos Importantes (FCCPD)

✔ Containers isolam processos
✔ Docker usa DNS interno para resolver nomes de containers
✔ Cada container tem seu próprio filesystem e rede virtual
✔ Comunicação é feita via TCP/IP (HTTP)
✔ O cliente usa curl para enviar requisições repetidas
✔ A rede customizada fccpd_net simula um ambiente distribuído simples
✔ Comunicação usando hostname → server

### 🧹 Comandos Úteis (Limpeza)
docker rm -f client server
docker network rm fccpd_net

### ✅ Conclusão

Este desafio mostra como containers podem atuar como processos distribuídos, cada um com seu próprio ambiente isolado, comunicando-se via rede virtual.
Essa base será fundamental para os próximos desafios (Volumes, Docker Compose, Microsserviços e API Gateway), onde construiremos um sistema distribuído completo e modular.
