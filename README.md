# Tutorial Youtube
https://www.youtube.com/watch?v=3rAXmWvhWg8&list=PLKBxfVADNf1VBeAnACnbDVVA450s81Jpm&index=3


## DOCKER

# Detener todos los contenedores en ejecución
sudo docker stop $(sudo docker ps -q)

# Verificar contenedores detenidos
sudo docker ps -a
sudo docker ps

# Reiniciar todos los contenedores en ejecución:
sudo docker restart $(sudo docker ps -q)

# Eliminar todos los contenedores detenidos
sudo docker container prune

# Crear contenedor
sudo docker-compose up -d