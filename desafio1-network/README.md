# 📦 Desafio 1 – Comunicação entre Containers em Rede (FCCPD)

  

Este desafio demonstra o funcionamento básico de comunicação entre containers Docker utilizando **redes internas**.

Ele mostra como dois serviços isolados podem se comunicar **pelo nome do container**, usando o **DNS interno do Docker**, sem depender de IP fixo.

  

---

  

## 🎯 Objetivo

  

Criar **dois containers**:

  

-  **server** → servidor Flask respondendo em `http://server:5000`

-  **client** → container que chama o servidor periodicamente usando `curl`

  

Ambos devem estar conectados à rede Docker chamada **`fccpd_net`**.

  

---

  

## 🧱 Estrutura de Pastas

  

```text

desafio1-network/

server/

app.py

Dockerfile

client/

entrypoint.sh

Dockerfile

README.md

```

## 🖥️ Arquitetura do Sistema

```text

Rede Docker: fccpd_net

┌───────────────────────────────────────────────┐

│ │

│ +----------------------+ │

│ | server | │

│ | Flask (porta 5000) | │

│ +----------------------+ │

│ ▲ │

│ │ HTTP (curl) │

│ ▼ │

│ +----------------------+ │

│ | client | │

│ | loop chamando server | │

│ +----------------------+ │

│ │

└───────────────────────────────────────────────┘

```

-  **Rede interna criada: fccpd_net**

  

-  **O client acessa o servidor via hostname: http://server:5000**
---

  

### 🐍 Código do Servidor (Flask)

  

-  **Arquivo:**  ```server/app.py```

  

```text

from flask import Flask

  

app = Flask(__name__)

  

@app.route("/")

def index():

return "Hello from server (desafio1-network)!", 200

  

if __name__ == "__main__":

app.run(host="0.0.0.0", port=5000)


```

---

  

### 🐳 Dockerfile do Servidor

-  **Arquivo:**  ```server/Dockerfile```

  

```code

FROM python:3.11-slim

  

WORKDIR /app

  

RUN pip install flask

  

COPY app.py .

  

EXPOSE 5000

  

CMD ["python", "app.py"]

```

----

  

### 📄 Script do Cliente

  

-  **Arquivo:**  ```client/entrypoint.sh```

```code

#!/bin/sh

  

echo "Iniciando client... Chamando http://server:5000 a cada 3 segundos."

  

while true; do

echo "-----"

date

curl -s http://server:5000 || echo "Erro ao conectar ao server"

sleep 3

done

```

---

  

### 🐳 Dockerfile do Cliente

  

-  **Arquivo:**  ```client/Dockerfile```

  

```code

FROM alpine:3.19

  

RUN apk add --no-cache curl

  

WORKDIR /app

  

COPY entrypoint.sh .

  

RUN chmod +x entrypoint.sh

  

CMD ["./entrypoint.sh"]

```
---

  

### 🚀 Como Executar o Projeto
---

### 1️⃣ Criar a rede Docker

```text

docker network create fccpd_net

```
---

### 2️⃣ Construir as imagens

```text

docker build -t fccpd-desafio1-server ./server

docker build -t fccpd-desafio1-client ./client

```
---

### 3️⃣ Subir o servidor (Flask)

```text

docker run -d --name server --network fccpd_net -p 5000:5000 fccpd-desafio1-server

```
---

Testar no navegador:

```text

http://localhost:5000

```

Ou:

```text

curl http://localhost:5000

```
---

### 4️⃣ Subir o cliente

```text

docker run -it --name client --network fccpd_net fccpd-desafio1-client

```
---

### Saída esperada

```text

-----

Sat Nov 30 05:12:00 UTC 2025

Hello from server (desafio1-network)!

-----

Sat Nov 30 05:12:03 UTC 2025

Hello from server (desafio1-network)!

```

---

  

### 🧠 Conceitos Importantes (FCCPD)

✔ Containers isolam processos

✔ Docker usa DNS interno para resolver nomes de containers

✔ Cada container tem filesystem e rede própria

✔ Comunicação ocorre via TCP/IP (HTTP)

✔ O cliente simula um processo distribuído consumindo outro serviço

✔ A rede fccpd_net simula um cluster mínimo

✔ Comunicação usando hostname → server

---

  

### 🧹 Comandos Úteis (Limpeza)

```text

docker rm -f client server

docker network rm fccpd_net

```

---

### ✅ Conclusão

Este desafio demonstra como containers podem atuar como processos distribuídos, comunicando-se por uma rede virtual interna.

Essa base será utilizada nos próximos desafios (Volumes, Docker Compose, Microsserviços e API Gateway), formando um sistema distribuído completo e modular.