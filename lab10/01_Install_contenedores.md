### **Guía : Instalación en Linux (Ubuntu)**

En Linux, la instalación se realiza a través de la línea de comandos. Docker Compose se instala como un plugin del motor de Docker.

**Parte A: Instalar Docker Engine**

**Paso 1: Actualizar el Sistema**
Abre una terminal y actualiza la lista de paquetes de tu sistema.
```bash
sudo apt update
```

**Paso 2: Instalar Paquetes de Prerrequisitos**
Instala los paquetes necesarios para permitir que `apt` use repositorios a través de HTTPS.
```bash
sudo apt install ca-certificates curl gnupg
```

**Paso 3: Agregar la Clave GPG Oficial de Docker**
Esto asegura que los paquetes que descargues sean auténticos.
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg


**Paso 4: Configurar el Repositorio de Docker**
Agrega el repositorio oficial de Docker a tus fuentes de `apt`.
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Paso 5: Instalar Docker Engine y el Plugin de Compose**
Actualiza de nuevo la lista de paquetes e instala la última versión de Docker y sus componentes.
```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

**Parte B: Pasos Posteriores a la Instalación (¡Muy Importante!)**

**Paso 1: Administrar Docker como un Usuario no Root**
Por defecto, necesitas usar `sudo` para ejecutar comandos de Docker. Para evitar esto, agrega tu usuario al grupo `docker`.```bash
sudo usermod -aG docker $USER```
**Importante:** Después de ejecutar este comando, debes **cerrar sesión y volver a iniciarla** (o reiniciar el sistema) para que los cambios surtan efecto.

**Paso 2: Verificar la Instalación**
Abre una nueva terminal (después de haber vuelto a iniciar sesión) y verifica que todo funciona correctamente sin `sudo`.

*   Verificar la versión de Docker:
    ```bash
    docker --version
    ```
*   Verificar la versión de Docker Compose:
    ```bash
    docker compose version
    ```
*   Ejecutar un contenedor de prueba:
    ```bash
    docker run hello-world
    ```

