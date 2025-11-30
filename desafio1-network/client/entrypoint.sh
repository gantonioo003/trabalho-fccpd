#!/bin/sh

echo "Iniciando client... chamando http://server:5000 a cada 3 segundos."

while true; do
  echo "-----"
  date
  curl -s http://server:5000 || echo "Erro ao conectar no server"
  sleep 3
done
