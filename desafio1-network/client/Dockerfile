FROM alpine:3.19

# Instalar curl
RUN apk add --no-cache curl

WORKDIR /app

COPY entrypoint.sh .

# Garantir que o script é executável dentro do container
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
