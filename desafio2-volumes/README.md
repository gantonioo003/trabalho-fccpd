# 🗃️ Desafio 2 – Volumes e Persistência (FCCPD)

Este desafio demonstra como usar **volumes Docker** para garantir **persistência de dados** mesmo após a remoção de containers.  
Usamos um banco PostgreSQL em um container e armazenamos seus dados em um volume Docker.

---

## 🎯 Objetivo

- Criar um container com um banco de dados (PostgreSQL).
- Usar um **volume Docker** para armazenar os dados fora do container.
- Mostrar que, ao remover o container e criar outro usando o mesmo volume, os dados permanecem.
- (Opcional) Permitir que outro processo/cliente acesse esses dados.

---

## 🧱 Estrutura de Pastas

```text
desafio2-volumes/
  db/
    init.sql
  README.md
````

---
### 🗄️ Arquivo de Inicialização (``init.sql``)
**Arquivo:** `` db/init.sql``

``` text
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

INSERT INTO usuarios (nome) VALUES
('Ana'),
('Bruno'),
('Carlos');
```
Esse script é executado automaticamente na primeira inicialização do banco.

---

### 📦 Criando o Volume
```
docker volume create fccpd_db_data
````
Esse volume será usado para armazenar os arquivos de dados do PostgreSQL, de forma persistente.

---

### 🐳 Subindo o Container com PostgreSQL

Comando executado dentro de ``desafio2-volumes``:

```code
docker run -d --name pg-desafio2 \
  -e POSTGRES_PASSWORD=senha \
  -e POSTGRES_DB=desafio2db \
  -v fccpd_db_data:/var/lib/postgresql/data \
  -v ${PWD}/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
  -p 5432:5432 postgres:15
  ````

Explicação dos principais parâmetros:

- ```POSTGRES_PASSWORD=senha``` → senha do usuário postgres.
- ```POSTGRES_DB=desafio2db``` → banco criado automaticamente.
- ```-v fccpd_db_data:/var/lib/postgresql/data```→ volume onde os dados são persistidos.
- ```-v .../init.sql:/docker-entrypoint-initdb.d/init.sql``` → script SQL executado na primeira inicialização.
- ```-p 5432:5432``` → expõe a porta do banco para acesso externo (opcional).

### 🔎 Verificando os Dados (1ª Execução)
Entrar no container:

```
docker exec -it pg-desafio2 psql -U postgres -d desafio2db
```
Dentro do psql, executar:

```
SELECT * FROM usuarios;
```
Saída esperada:

```
 id |  nome
----+--------
  1 | Ana
  2 | Bruno
  3 | Carlos
(3 rows)
```
Sair do psql:

```
\q
```

---
### 💀 Removendo o Container
Agora, removemos o container, mas não o volume:

```
docker rm -f pg-desafio2
```
O volume fccpd_db_data continua existindo:

```
docker volume ls
```
---
### ♻️ Recriando o Container Usando o Mesmo Volume
Criamos um NOVO container PostgreSQL, apontando para o MESMO volume:

```
docker run -d --name pg-desafio2 \
  -e POSTGRES_PASSWORD=senha \
  -e POSTGRES_DB=desafio2db \
  -v fccpd_db_data:/var/lib/postgresql/data \
  -p 5432:5432 postgres:15
  ```
Note que aqui não montamos mais o ```init.sql``` — pois o banco já existe no volume.

### 🔁 Verificando os Dados (2ª Execução)
Novamente:

```
docker exec -it pg-desafio2 psql -U postgres -d desafio2db
```
E rodamos:

```
SELECT * FROM usuarios;
```
Se os dados ainda estiverem lá, a persistência foi comprovada.

---

### 🧠 Conceitos Importantes (FCCPD)
✔ Containers são efêmeros (podem ser descartados).
✔ Volumes Docker armazenam dados de forma persistente.
✔ O ciclo de vida do container é diferente do ciclo de vida dos dados.
✔ Persistência é fundamental em sistemas distribuídos que armazenam estado (bancos de dados).

---

### 🧹 Limpeza (Opcional)
```
docker rm -f pg-desafio2
docker volume rm fccpd_db_data
```

---
### ✅ Conclusão
Neste desafio, mostramos que é possível remover e recriar containers sem perder os dados, desde que eles estejam armazenados em um volume Docker.
Esse conceito é essencial para arquiteturas modernas em que containers sobem e descem o tempo todo, mas os dados precisam permanecer consistentes e duráveis.


