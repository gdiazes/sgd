### **Guía para Instalar Ubuntu desde la Microsoft Store (con WSL)**

Este proceso se divide en dos fases principales: primero, habilitar la característica de Windows necesaria y, segundo, instalar Ubuntu desde la tienda.

#### **Fase 1: Preparar Windows para Instalar Ubuntu**

Antes de poder instalar Ubuntu desde la Microsoft Store, debes habilitar el "Subsistema de Windows para Linux" (WSL).

**Requisitos Previos:**

*   **Sistema Operativo:** Debes tener Windows 10 (versión 2004 o superior) o Windows 11.
*   **Permisos:** Necesitas tener permisos de administrador en tu equipo.

**Paso 1: Habilitar el Subsistema de Windows para Linux (WSL)**

Este es el método más sencillo y recomendado, ya que realiza toda la configuración necesaria con un solo comando.

1.  **Abrir PowerShell o Símbolo del sistema como Administrador:**
    *   Haz clic en el menú Inicio.
    *   Escribe "PowerShell" o "CMD".
    *   En el resultado, haz clic derecho sobre "Windows PowerShell" o "Símbolo del sistema" y selecciona **"Ejecutar como administrador"**.

2.  **Ejecutar el comando de instalación:**
    *   En la ventana de la terminal que se abrió, escribe el siguiente comando y presiona **Enter**:
        ```
        wsl --install
        ```

3.  **¿Qué hace este comando?**
    *   Habilita las características opcionales necesarias de WSL y la Plataforma de máquina virtual.
    *   Descarga e instala la versión más reciente del kernel de Linux.
    *   Establece WSL 2 como la versión predeterminada.
    *   Descarga e instala la distribución de Ubuntu por defecto.

4.  **Reiniciar el equipo:**
    *   Una vez que el proceso finalice, se te pedirá que reinicies tu computadora para completar la instalación. Guarda tu trabajo y reinicia.

**Método Alternativo (Manual):**

Si el comando anterior no funciona, puedes habilitar las características manualmente.

1.  Abre **PowerShell como Administrador** y ejecuta los siguientes dos comandos, uno después del otro:

    *   Para habilitar WSL:
        ```
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        ```
    *   Para habilitar la Plataforma de máquina virtual:
        ```
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        ```
2.  **Reinicia** tu computadora.
3.  **Establece WSL 2 como la versión predeterminada** (opcional pero recomendado) abriendo PowerShell como administrador después de reiniciar y ejecutando:
    ```
    wsl --set-default-version 2
    ```

#### **Fase 2: Instalar Ubuntu desde la Microsoft Store**

Después de reiniciar tu PC, la instalación de Ubuntu debería continuar automáticamente. Si no lo hace, o si usaste el método manual, sigue estos pasos.

**Paso 2: Descargar Ubuntu desde la Tienda**

1.  **Abre la Microsoft Store:**
    *   Ve al menú Inicio y escribe "Microsoft Store" para abrirla.

2.  **Busca Ubuntu:**
    *   En la barra de búsqueda de la tienda, escribe "Ubuntu". Verás varias versiones disponibles (por ejemplo, Ubuntu 22.04.3 LTS, Ubuntu 24.04 LTS). Se recomienda elegir la versión **LTS (Long-Term Support)** más reciente por su estabilidad.

3.  **Instala la aplicación:**
    *   Selecciona la versión de Ubuntu que prefieras y haz clic en el botón **"Obtener"** o **"Instalar"**. La descarga e instalación comenzarán automáticamente.

**Paso 3: Configuración Inicial de Ubuntu**

1.  **Iniciar Ubuntu por primera vez:**
    *   Una vez instalado, puedes encontrar Ubuntu en tu menú Inicio como cualquier otra aplicación. Haz clic en el ícono de Ubuntu para lanzarlo.
    *   La primera vez que se ejecute, verás un mensaje que dice "Installing, this may take a few minutes...". El sistema estará descomprimiendo los archivos necesarios y finalizando la configuración.

2.  **Crear tu cuenta de usuario de Linux:**
    *   Cuando el proceso termine, se te pedirá que crees un nombre de usuario y una contraseña.
    *   **Importante:** Este usuario es específico para el entorno de Ubuntu y no tiene relación con tu nombre de usuario y contraseña de Windows.
    *   Introduce un nombre de usuario (en minúsculas, sin espacios) y presiona **Enter**.
    *   Luego, introduce una contraseña segura y vuelve a escribirla para confirmarla. No verás los caracteres de la contraseña mientras escribes, esto es normal en las terminales de Linux.

3.  **¡Instalación completada!**
    *   Una vez que hayas creado tu usuario, verás el símbolo del sistema de la terminal de Ubuntu (por ejemplo, `nombredeusuario@nombredetuPC:~$`).
    *   ¡Felicidades! Ahora tienes una terminal de Ubuntu completamente funcional dentro de tu sistema Windows.

#### **Comandos Básicos para Empezar**

Ya puedes usar comandos de Linux. Prueba con estos para asegurarte de que todo funciona:

*   **Actualizar la lista de paquetes:**
    ```
    sudo apt update
    ```
*   **Instalar las actualizaciones disponibles:**
    ```
    sudo apt upgrade
    ```
*   **Ver el directorio actual:**
    ```
    pwd
    ```
*   **Listar los archivos:**
    ```
    ls -l
    ```
