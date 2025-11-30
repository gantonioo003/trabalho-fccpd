# 🧪 FCCPD – Trabalho de Containers, Microsserviços e Arquiteturas Distribuídas

Este repositório reúne uma sequência de 5 desafios práticos da disciplina *Fundamentos da Computação Concorrente, Paralela e Distribuída (FCCPD)*.

Cada desafio foca em um aspecto diferente de **containers**, **comunicação entre serviços**, **persistência de dados**, **microsserviços** e **API Gateway**.

> 🔎 *Importante:*  
> Cada desafio possui *seu próprio README* dentro da respectiva pasta, com:
> - explicações mais detalhadas  
> - código comentado  
> - comandos para execução  
> - observações específicas

---

## 📂 Estrutura do Repositório

```text
trabalho-fccpd/
  desafio1-network/
    README.md
    ...
  desafio2-volumes/
    README.md
    ...
  desafio3-compose/
    README.md
    ...
  desafio4-microsservicos/
    README.md
    ...
  desafio5-gateway/
    README.md
   ...
```

---

### 🧩 Desafio 1 – Containers em Rede
•	Objetivo: mostrar dois containers se comunicando via rede interna Docker.

•	Serviços:

•	server: servidor Flask simples.

•	client: container que faz requisições periódicas ao servidor com curl.

•	Conceito principal: comunicação entre containers na mesma rede usando o nome do container como hostname.


📄 Detalhes completos em: desafio1-network/README.md


---

### 🗃 Desafio 2 – Volumes e Persistência
•	Objetivo: demonstrar persistência de dados usando volumes Docker.

•	Serviço:

•	Banco PostgreSQL salvando os dados em um volume.

•	Ideia central: mesmo removendo o container do banco, os dados permanecem no volume e podem ser usados por um novo container.


📄 Detalhes completos em: desafio2-volumes/README.md

---

### 🧩 Desafio 3 – Docker Compose Orquestrando Serviços
•	Objetivo: usar Docker Compose para subir múltiplos serviços juntos.

•	Serviços:

•	web: aplicação Flask.

•	db: PostgreSQL.

•	cache: Redis.

•	Conceitos principais:

•	docker-compose.yml organizando tudo.

•	depends_on para dependências.

•	Rede interna automática entre os serviços.


📄 Detalhes completos em: desafio3-compose/README.md


---

### 🔗 Desafio 4 – Microsserviços Independentes
•	Objetivo: criar dois microsserviços independentes que se comunicam via HTTP.

•	Serviços:

•	service-a: expõe uma lista de usuários em JSON.

•	service-b: consome service-a e monta um relatório com essas informações.

•	Conceito central: microsserviços separados, cada um com seu próprio Dockerfile, se falando apenas por HTTP.


📄 Detalhes completos em: desafio4-microsservicos/README.md

---
### 🛡 Desafio 5 – Microsserviços com API Gateway

•	Objetivo: criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços.

•	Serviços:

•	service-users: fornece dados de usuários.

•	service-orders: fornece dados de pedidos.

•	gateway: único ponto de entrada, expõe /users, /orders e um endpoint combinado /report.

•	Conceito central: o cliente fala só com o gateway, que orquestra as chamadas para os microsserviços.


📄 Detalhes completos em: desafio5-gateway/README.md

---

### ✅ Pré-requisitos gerais

Para executar os desafios é recomendado ter:
	
•	Docker instalado

•	Docker Compose (ou docker compose integrado ao Docker Desktop)

•	PowerShell, Terminal ou outro shell para rodar os comandos


Cada README específico explica os comandos necessários para subir e testar cada cenário.


---

### ✍ Autor
**•	Nome: Gabriel Antônio**

**•	E-mail: gantonioo102003@gmail.com**

