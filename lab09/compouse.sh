# Usar la versión 3.8 o superior para mejor compatibilidad
version: '3.8'

services:
  db:
    image: postgres:15 # Es buena práctica fijar una versión mayor específica
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: example
      POSTGRES_DB: mi_base_de_datos # Opcional: crea esta base de datos al iniciar
    volumes:
      # Este volumen persistirá los datos de tu base de datos
      - db_data:/var/lib/postgresql/data
    ports:
      # Expone el puerto 5432 del contenedor al puerto 5432 de tu máquina
      # Formato: <puerto_en_tu_maquina>:<puerto_en_el_contenedor>
      - "5432:5432"
    # Límite de memoria compartida recomendado para postgres
    shm_size: 128mb

# Define el volumen nombrado para la persistencia de datos
volumes:
  db_data:
