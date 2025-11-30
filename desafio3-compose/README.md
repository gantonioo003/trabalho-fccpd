# 🧩 Desafio 3 – Docker Compose Orquestrando Serviços (FCCPD)

Este desafio demonstra como usar *Docker Compose* para orquestrar múltiplos serviços dependentes em um ambiente distribuído simples.  
Aqui utilizamos três serviços:

- *web* → aplicação Flask
- *db* → banco de dados PostgreSQL
- *cache* → Redis para cache/contador

---

## 🎯 Objetivo

- Subir múltiplos serviços com *um único comando* usando Docker Compose.
- Configurar dependências entre serviços com depends_on.
- Usar uma *rede interna automática* criada pelo Compose.
- Configurar serviços via *variáveis de ambiente* no docker-compose.yml.
- Demonstrar comunicação entre web → db e web → cache.

---

## 🧱 Estrutura de Pastas

```text
desafio3-compose/
  docker-compose.yml
  web/
    app.py
    requirements.txt
    Dockerfile
  README.md
  ```

---

### 🐳 Arquitetura

               (rede interna Docker)
    ┌───────────────────────────────────────┐
    │                                       │
    │   +----------+       +-----------+    │
    │   |   db     |       |  cache    |    │
    │   | Postgres |       |  Redis    |    │
    │   +----------+       +-----------+    │
    │          ▲                 ▲          │
    │          │                 │          │
    │          └───────┬─────────┘          │
    │                  │                    │
    │             +----------+              │
    │             |   web    |              │
    │             |  Flask   |              │
    │             +----------+              │
    │                  ▲                    │
    │                  │ porta 8080         │
    └──────────────────┴────────────────────┘
                       |
                       ▼
                http://localhost:8080


---

### ⚙ Arquivo docker-compose.yml

```text
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: db-desafio3
    environment:
      POSTGRES_PASSWORD: senha
      POSTGRES_DB: desafio3db
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    container_name: cache-desafio3

  web:
    build: ./web
    container_name: web-desafio3
    depends_on:
      - db
      - cache
    ports:
      - "8080:8080"
    environment:
      DB_HOST: db
      DB_PORT: "5432"
      DB_NAME: desafio3db
      DB_USER: postgres
      DB_PASSWORD: senha
      REDIS_HOST: cache
      REDIS_PORT: "6379"
volumes:
  db_data:
```


---

### 🐍 Aplicação Web (web/app.py)

A aplicação Flask expõe três endpoints:
	•	/ → teste básico
	•	/db → grava e lê dados no PostgreSQL
	•	/cache → incrementa contador no Redis

(código completo igual ao app.py do projeto)

---

### 🚀 Como Executar

Na pasta desafio3-compose:
```code
docker compose up --build
```
Acessar no navegador:
	•	http://localhost:8080/ → verifica se o serviço web está no ar
	•	http://localhost:8080/db → testa comunicação com o PostgreSQL
	•	http://localhost:8080/cache → testa comunicação com o Redis

---

### 🧠 Conceitos Importantes (FCCPD)

✔ Orquestração de múltiplos serviços com Docker Compose
✔ Rede interna automática entre containers
✔ Comunicação entre serviços via nome (db, cache, web)
✔ Uso de depends_on para expressar dependências
✔ Configuração de serviços com variáveis de ambiente
✔ Arquitetura típica de microsserviços (web + db + cache)

---

### 🧹 Encerrando os serviços
```code
docker compose down
```

Para também remover o volume de dados:
```code
docker compose down -v
```

---

### ✅ Conclusão

Este desafio mostra como é possível orquestrar múltiplos serviços interdependentes utilizando o Docker Compose, simulando uma arquitetura típica de sistemas distribuídos modernos com aplicação, banco de dados e cache.
