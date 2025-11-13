### **Guía de Laboratorio 08: Desplegando "FrutiFresh Lealtad" en Google Cloud SQL**

#### **Marco Conceptual**

En los laboratorios anteriores, hemos trabajado con bases de datos locales utilizando Docker. Si bien es excelente para el desarrollo, las aplicaciones del mundo real se despliegan en la nube para aprovechar su escalabilidad, disponibilidad y gestión simplificada. En este laboratorio, darás el salto de desarrollador a ingeniero de DevOps/Cloud. Tu misión es aprovisionar una base de datos PostgreSQL de grado empresarial utilizando un servicio PaaS (Plataforma como Servicio) en Google Cloud Platform (GCP), específicamente **Cloud SQL**. Luego, te conectarás a esta base de datos remota y desplegarás el esquema que diseñaste, llevando tu trabajo del entorno local al mundo real.

#### **Caso de Estudio**

"FrutiFresh" está lista para lanzar la primera versión de su programa de lealtad. Como ingeniero de datos, se te ha encargado la tarea de configurar la infraestructura de base de datos en la nube. La CEO ha decidido usar Google Cloud Platform por su generosa capa gratuita (Free Tier) y su facilidad de uso. Debes crear una base de datos PostgreSQL, asegurarla y desplegar el esquema `frutifresh_lealtad` para que los desarrolladores de la aplicación puedan empezar a trabajar.

#### **Objetivos del Laboratorio**

1.  Crear una cuenta en Google Cloud Platform y familiarizarse con su consola.
2.  Aprovisionar (crear) una instancia de PostgreSQL utilizando el servicio gestionado **Cloud SQL**.
3.  Configurar las reglas de red (firewall) para permitir una conexión segura desde tu computadora.
4.  Conectar tu cliente de base de datos local (DBeaver) a la instancia remota en la nube.
5.  Ejecutar un script SQL para desplegar un esquema de base de datos en la instancia de Cloud SQL.

#### **Herramientas y Prerrequisitos**
*   Una cuenta de Google.
*   Una tarjeta de crédito/débito (GCP la requiere para la verificación, pero no se te cobrará nada si sigues los pasos del Free Tier).
*   El archivo `esquema_lealtad_frutifresh.sql` que creaste en el laboratorio de la Semana 5.
*   DBeaver instalado.



### **Procedimiento Paso a Paso**

#### **Fase 1: Creación y Configuración de la Cuenta de GCP (~45 min)**

1.  **Activa tu Cuenta Gratuita:**
    *   Navega a la página de la capa gratuita de Google Cloud: [cloud.google.com/free](https://cloud.google.com/free).
    *   Haz clic en **"Comenzar gratis"** e inicia sesión con tu cuenta de Google.
    *   Sigue los pasos del asistente. Deberás verificar tu identidad y proporcionar una forma de pago. **No te preocupes, no se te cobrará nada si no sales de los límites de la capa gratuita.** Recibirás 300 USD en créditos para experimentar.

2.  **Crea tu Primer Proyecto:**
    *   Una vez en la consola de Google Cloud, es posible que se te pida crear un proyecto. Si no, ve a la parte superior de la página, haz clic en el selector de proyectos y luego en **"PROYECTO NUEVO"**.
    *   **Nombre del proyecto:** `frutifresh-lealtad-lab`
    *   Haz clic en **"CREAR"**. Asegúrate de que este nuevo proyecto esté seleccionado.
    > ![Placeholder para Imagen 4.1: Captura de pantalla de la ventana de creación de proyecto en GCP.]

3.  **Habilita las APIs Necesarias:**
    *   En la barra de búsqueda de la consola, escribe **"Cloud SQL Admin API"** y selecciónala.
    *   Si no está habilitada, haz clic en el botón **"HABILITAR"**. Esto permite que tu proyecto interactúe con el servicio Cloud SQL.

#### **Fase 2: Aprovisionamiento de la Instancia de Cloud SQL (~45 min)**

Ahora, vamos a crear nuestra base de datos gestionada.

1.  **Navega a Cloud SQL:**
    *   En la barra de búsqueda de la consola, escribe **"SQL"** y selecciona el servicio **"SQL"**.

2.  **Crea una Nueva Instancia:**
    *   Haz clic en **"CREAR INSTANCIA"**.
    *   Elige el motor de base de datos: **"Elegir PostgreSQL"**.
    *   **ID de instancia:** `frutifresh-lealtad-db` (debe ser único en el proyecto).
    *   **Contraseña de postgres:** Crea una contraseña segura para el usuario administrador `postgres` y **guárdala en un lugar seguro**.
    *   **Versión de la base de datos:** Elige una versión reciente (ej. PostgreSQL 14 o superior).
    *   **Configuración predefinida:** Selecciona **"Desarrollo"**. Esto elige una máquina pequeña, adecuada para nuestro laboratorio y de bajo costo.
    *   **Región y Zona:** Elige una región cercana a tu ubicación (ej. `us-east1` o `us-central1`).
    *   Haz clic en **"CREAR INSTANCIA"**. El aprovisionamiento puede tardar entre 5 y 10 minutos.

    > ![Placeholder para Imagen 4.2: Captura de pantalla del asistente de creación de instancia de Cloud SQL con los campos rellenados.]

#### **Fase 3: Configuración de la Conectividad de Red (~45 min)**

Por defecto, tu base de datos no es accesible desde internet. Debemos abrir el "firewall" de forma segura.

1.  **Encuentra la IP Pública de tu Computadora:**
    *   Abre una nueva pestaña en tu navegador y busca "¿Cuál es mi IP?". Google te mostrará tu dirección IP pública. Cópiala.

2.  **Configura las Redes Autorizadas:**
    *   Una vez que tu instancia de Cloud SQL esté creada, haz clic en su nombre para ver los detalles.
    *   Ve a la pestaña **"Conexiones"**.
    *   En la sección "Conectividad", busca la pestaña **"Red pública"**.
    *   Haz clic en **"AÑADIR UNA RED"**.
    *   **Nombre:** `mi-ip-casa` (o un nombre descriptivo).
    *   **Red:** Pega la dirección IP que copiaste en el paso anterior y añade `/32` al final (ej. `200.100.50.25/32`). El `/32` significa que solo esa IP exacta tiene permiso.
    *   Haz clic en **"HECHO"** y luego en **"GUARDAR"** en la parte inferior de la página. La instancia se reiniciará para aplicar los cambios.

3.  **Obtén la IP Pública de la Base de Datos:**
    *   En la página de "Visión general" de tu instancia, busca el campo **"Dirección IP pública"**. Cópiala. Esta es la dirección del servidor a la que nos conectaremos.

#### **Fase 4: Conexión y Despliegue del Esquema (~60 min)**

1.  **Configura DBeaver:**
    *   Abre DBeaver y crea una nueva conexión a **PostgreSQL**.
    *   **Host:** Pega la **"Dirección IP pública"** de tu instancia de Cloud SQL.
    *   **Database:** `postgres`
    *   **Username:** `postgres`
    *   **Password:** La contraseña que creaste para la instancia.
    *   Haz clic en **"Test Connection..."**. Si configuraste la red autorizada correctamente, ¡deberías ver un mensaje de éxito!

2.  **Despliega tu Esquema:**
    *   Abre un nuevo Editor de SQL en DBeaver para tu nueva conexión en la nube.
    *   Abre tu archivo `esquema_lealtad_frutifresh.sql` de la Semana 5.
    *   Copia y pega todo el contenido del script en el editor de DBeaver.
    *   Ejecuta el script completo.

3.  **Verificación Final:**
    *   En el "Database Navigator" de DBeaver, haz clic derecho sobre tu esquema `public` y selecciona "Actualizar".
    *   Expande la sección "Tablas". Deberías ver las cuatro tablas que diseñaste (`clientes`, `transacciones_puntos`, etc.) creadas exitosamente en tu base de datos en la nube.



### **Entregable**

1.  Toma una captura de pantalla completa de tu ventana de DBeaver.
2.  La captura debe mostrar claramente:
    *   En el "Database Navigator", la conexión a la IP de Google Cloud expandida, mostrando las **cuatro tablas** del programa de lealtad.
    *   En el Editor SQL, el script `CREATE TABLE` que ejecutaste.
3.  Sube esta imagen a la plataforma del curso.

---

### **Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Aprovisionamiento de Instancia (3 pts)** | No logra crear la instancia de Cloud SQL o la crea con una configuración incorrecta. | Crea la instancia, pero tiene dificultades significativas siguiendo los pasos. | Aprovisiona exitosamente una instancia de PostgreSQL en Cloud SQL siguiendo la guía. | / 3 |
| **Configuración de Red (4 pts)** | No configura las redes autorizadas, impidiendo la conexión. | Configura la red, pero comete errores (ej. olvida el `/32`) que requieren ayuda para ser corregidos. | Configura correctamente las redes autorizadas, añadiendo su IP pública para permitir una conexión segura. Demuestra comprensión del concepto de firewall. | / 4 |
| **Conexión y Despliegue (3 pts)** | No logra conectar DBeaver a la instancia de la nube. | Logra conectar, pero no ejecuta el script SQL o el script falla por errores no resueltos. | Conecta exitosamente DBeaver a la instancia de Cloud SQL y ejecuta el script de creación de esquemas, demostrando que las tablas se crearon en la nube. | / 3 |
| **Total**| | | | **/ 10** |
