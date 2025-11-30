# 🔗 Desafio 4 – Microsserviços Independentes (FCCPD)

Este desafio demonstra como criar *dois microsserviços independentes*, cada um com seu próprio Dockerfile, rodando em containers distintos e se comunicando via HTTP.  
É uma simulação simples de uma arquitetura real de microsserviços, em que cada serviço cumpre um papel específico e se comunica apenas por API.

---

## 🎯 Objetivo

- Criar *Microsserviço A*: fornece uma lista de usuários em JSON.  
- Criar *Microsserviço B*: consome o serviço A via HTTP e gera um relatório textual.  
- Cada serviço deve rodar em seu *próprio container*.  
- A comunicação deve ocorrer *somente via HTTP*, usando o hostname do serviço.  
- Utilizar Docker Compose para orquestrar ambos.

---
## 🧱 Estrutura de Pastas

```text
desafio4-microsservicos/
  docker-compose.yml
  service-a/
    app.py
    requirements.txt
    Dockerfile
  service-b/
    app.py
    requirements.txt
    Dockerfile
  README.md
  ```


---
### 🖥 Arquitetura do Sistema
```
                       Rede interna do Docker Compose
 ┌──────────────────────────────────────────────────────────────────────┐
 │                                                                      │
 │   +--------------------+        HTTP        +---------------------+   │
 │   |   Microsserviço A  | <----------------- |   Microsserviço B   |   │
 │   |   /users (JSON)    | -----------------> |   /report (API)     |   │
 │   +--------------------+                    +---------------------+   │
 │        Porta interna: 5000                      Porta interna: 5000   │
 │        Porta externa: 5001                      Porta externa: 5002   │
 │                                                                      │
 └──────────────────────────────────────────────────────────────────────┘

- Microsserviço A fornece os dados.
- Microsserviço B consome os dados e gera um relatório consolidado.
- Comunicação via HTTP em http://service-a:5000/users.

```

---
### 🧩 Microsserviço A — Lista de Usuários (service-a)

**📄 service-a/app.py**
```
from flask import Flask, jsonify

app = Flask(_name_)

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

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)

```

---

**🐳 service-a/Dockerfile**
```
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

```

---

### 🧩 Microsserviço B — Consome A e Gera Relatório (service-b)
**📄 service-b/app.py**

```

import os
import requests
from flask import Flask, jsonify

app = Flask(_name_)

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:5000")

@app.route("/")
def index():
    return "Microsserviço B - Relatórios de usuários", 200

@app.route("/report")
def report():
    try:
        response = requests.get(f"{SERVICE_A_URL}/users", timeout=5)
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
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)

```

---

**🐳 service-b/Dockerfile**

```

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]


```

---
### 🐳 Arquivo docker-compose.yml
```
version: "3.9"

services:
  service-a:
    build: ./service-a
    container_name: ms-service-a
    ports:
      - "5001:5000"

  service-b:
    build: ./service-b
    container_name: ms-service-b
    depends_on:
      - service-a
    environment:
      SERVICE_A_URL: http://service-a:5000
    ports:
      - "5002:5000"

```

	•	Rede interna automática criada pelo Compose.
	•	service-b acessa service-a pelo hostname service-a.
	•	Cada serviço exposto em uma porta externa diferente.

---

### 🚀 Como Executar o Projeto

Na pasta desafio4-microsservicos/:
```
docker compose up --build
```

**✔ Testar Microsserviço A**
	•	http://localhost:5001/
	•	http://localhost:5001/users

**✔ Testar Microsserviço B (que consome A)**
	•	http://localhost:5002/
	•	http://localhost:5002/report

Exemplo de resposta do B:
```

{
  "origem": "http://service-a:5000",
  "total_usuarios": 3,
  "relatorio": [
    "Usuário Ana ativo desde 2023-01-10.",
    "Usuário Bruno ativo desde 2022-06-05.",
    "Usuário Carla ativo desde 2024-03-20."
  ]
}
```

---

### 🧠 Conceitos Importantes (FCCPD)

✔ Microsserviços independentes (cada um com seu container)
 
✔ Comunicação entre serviços via HTTP

✔ Dockerfiles separados e isolamento real

✔ DNS interno do Docker: service-a como hostname

✔ depends_on garante ordem básica de subida

✔ Arquitetura desacoplada baseada em APIs

---

### 🧹 Encerrando os serviços

```
docker compose down
```

---

### ✅ Conclusão

Este desafio mostrou como criar dois microsserviços independentes e isolados, cada um com seu container Docker, comunicando-se apenas via HTTP.
Esse é o modelo fundamental de arquiteturas modernas baseadas em microsserviços, onde cada serviço tem sua responsabilidade e se comunica apenas por APIs bem definidas.

---
