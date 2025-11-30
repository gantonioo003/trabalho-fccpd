# 🛡 Desafio 5 – Microsserviços com API Gateway (FCCPD)

Este desafio demonstra uma arquitetura simples de *API Gateway* centralizando o acesso a dois microsserviços distintos:

- **Microsserviço 1 (service-users)** → fornece dados de usuários.
- **Microsserviço 2 (service-orders)** → fornece dados de pedidos.
- **Gateway (gateway)** → ponto único de entrada, expõe /users, /orders e um endpoint combinado /report.

Toda a arquitetura roda em containers utilizando *Docker Compose*.

---

## 🎯 Objetivo

- Criar dois microsserviços independentes:
  - service-users: API de usuários.
  - service-orders: API de pedidos.
- Criar um *API Gateway* que:
  - exponha os endpoints:
    - GET /users
    - GET /orders
- GET /report (opcional, combinação dos dois)
  - consuma os dois microsserviços via HTTP.
- Subir tudo via docker-compose, com rede interna e integração correta.

---

## 🧱 Estrutura de Pastas

```text
desafio5-gateway/
  docker-compose.yml
  gateway/
    app.py
    requirements.txt
    Dockerfile
  service-users/
    app.py
    requirements.txt
    Dockerfile
  service-orders/
    app.py
    requirements.txt
    Dockerfile
  README.md

```

---
### 🖥 Arquitetura

```

                        Rede interna do Docker Compose
 ┌──────────────────────────────────────────────────────────────────────┐
 │                                                                      │
 │   +------------------------+          +-------------------------+    │
 │   |   service-users        |          |    service-orders       |    │
 │   |  /users                |          |   /orders               |    │
 │   +------------------------+          +-------------------------+    │
 │             ▲                                  ▲                    │
 │             │                                  │                    │
 │             └──────────────┬───────────────┬──┘                    │
 │                            │               │                        │
 │                      +-----------+         │                        │
 │                      |  gateway  |         │                        │
 │                      | /users    |─────────┘                        │
 │                      | /orders   |                                  │
 │                      | /report   |                                  │
 │                      +-----------+                                  │
 │                            ▲                                       │
 │                            │  porta 8080 (exposta no host)         │
 └────────────────────────────┴───────────────────────────────────────┘
```

O Gateway é o ponto único de entrada para o cliente externo.

---

### ⚙ Arquivo docker-compose.yml
```
version: "3.9"

services:
  service-users:
    build: ./service-users
    container_name: svc-users
    ports:
      - "5003:5000"

  service-orders:
    build: ./service-orders
    container_name: svc-orders
    ports:
      - "5004:5000"

  gateway:
    build: ./gateway
    container_name: api-gateway
    depends_on:
      - service-users
      - service-orders
    environment:
      USERS_SERVICE_URL: http://service-users:5000
      ORDERS_SERVICE_URL: http://service-orders:5000
    ports:
- "8080:8080"

```

	•	O Compose cria automaticamente uma rede interna entre os serviços.
	•	O gateway conversa com:
	•	service-users via http://service-users:5000
	•	service-orders via http://service-orders:5000
	•	Apenas o gateway precisa ser acessado de fora (porta 8080).

---

### 🚀 Como Executar

Na pasta desafio5-gateway:
```
docker compose up --build
```







---
#🔎 Testando a Arquitetura

⿡ Testar o Gateway
	•	GET /
```
http://localhost:8080/
```


•	GET /users
```
http://localhost:8080/users
```

→ retorna a lista de usuários vinda do service-users.

•	GET /orders
```
http://localhost:8080/orders
```

→ retorna a lista de pedidos vinda do service-orders.

•	GET /report (opcional, agregado)
```
http://localhost:8080/report
```

→ retorna um JSON combinando usuários e seus pedidos.


Exemplo de resposta em /report:

```
{
  "total_usuarios": 3,
  "relatorio": [
    {
      "usuario": "Ana",
      "email": "ana@example.com",
      "total_pedidos": 2,
      "pedidos": [
        {"id": 101, "user_id": 1, "produto": "Notebook", "valor": 4500.0},
        {"id": 103, "user_id": 1, "produto": "Headset", "valor": 350.0}
      ]
    },
    {
      "usuario": "Bruno",
      "email": "bruno@example.com",
      "total_pedidos": 1,
      "pedidos": [
        {"id": 102, "user_id": 2, "produto": "Teclado Mecânico", "valor": 450.0}
      ]
    },
    {
      "usuario": "Carla",
      "email": "carla@example.com",
      "total_pedidos": 1,
      "pedidos": [
        {"id": 104, "user_id": 3, "produto": "Monitor", "valor": 1200.0}
      ]
    }
  ]
}
```


---


### ⿢ Testar os Microsserviços Diretamente (opcional)
	•	service-users:
	•	http://localhost:5003/
	•	http://localhost:5003/users
	•	service-orders:
	•	http://localhost:5004/
	•	http://localhost:5004/orders

---

### 🧠 Conceitos Importantes (FCCPD)

✔ Arquitetura de API Gateway como ponto único de entrada.

✔ Dois microsserviços independentes, cada um no seu container.

✔ Integração via HTTP com nomes de serviço (DNS interno do Docker).

✔ Uso de docker-compose para orquestrar múltiplos serviços.

✔ Separação clara entre:

	•	serviços de dados (users/orders)
	
	•	camada de gateway/orquestração.

___

### 🧹 Encerrando os Serviços
```
docker compose down
```

---

### ✅ Conclusão

Este desafio mostra uma arquitetura distribuída simples com API Gateway centralizando o acesso a múltiplos microsserviços.
A partir desse padrão, é possível evoluir para autenticação, versionamento de APIs, rate limiting, observabilidade e outras funcionalidades típicas de gateways em sistemas reais.

