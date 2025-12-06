# Usa una imagen base de Python estable basada en Debian Bullseye (versión 11).
FROM python:3.9-slim-bullseye

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /usr/app/dbt_project

# Instala git y build-essential.
# build-essential es crucial para compilar dependencias de Python que tienen componentes C/C++.
# Limpia el caché de apt para reducir el tamaño de la imagen.
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && whereis git # <-- Este comando ayudará a depurar si git no se encuentra en el PATH

# Copia el archivo requirements.txt al directorio de trabajo del contenedor.
COPY requirements.txt .

# Instala los paquetes de Python listados en requirements.txt.
# --no-cache-dir: Evita almacenar en caché los paquetes descargados.
# -r requirements.txt: Instala los paquetes desde el archivo.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio 'dbt/' de tu máquina local
# al directorio de trabajo '/usr/app/dbt_project' dentro del contenedor.
COPY dbt/ .

# Expone el puerto 8080 si planeas usar dbt docs serve.
EXPOSE 8080

# Comando por defecto al iniciar el contenedor.
CMD ["bash"]
