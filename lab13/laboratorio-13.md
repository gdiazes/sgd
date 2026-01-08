### **Guía de Laboratorio 13: Construyendo el Catálogo de Datos de "FrutiFresh" con `dbt`**

#### **Marco Conceptual**

La documentación en un entorno ágil no puede ser un documento estático; debe ser un artefacto vivo, generado a partir del código y versionado junto a él. `dbt` facilita esta práctica a través de los archivos `schema.yml`, que permiten a los equipos definir **metadatos de negocio** (descripciones) y **pruebas de calidad** en el mismo lugar. El comando `dbt docs generate` transforma esta información en un sitio web interactivo que actúa como un catálogo de datos y un mapa de linaje para todo el proyecto. En este laboratorio, actuarás como un Ingeniero Analítico encargado de documentar el pipeline de datos de "FrutiFresh" para hacerlo comprensible y confiable para toda la organización.

#### **Caso de Estudio**

El pipeline de datos de "FrutiFresh" que construiste en la Semana 11 está funcionando, pero es una "caja negra" para el resto del equipo. Un nuevo analista de marketing se ha unido a la empresa y está confundido sobre qué tablas usar y qué significa cada columna. La CEO (Data Owner) te ha dado una nueva tarea: **"Necesito que documentes nuestro pipeline de datos. Quiero un 'único lugar de la verdad' donde cualquiera pueda ir para entender nuestros modelos de datos, ver qué pruebas de calidad tienen y, lo más importante, visualizar cómo fluyen los datos desde el origen hasta los modelos finales. Quiero un mapa de nuestros datos."**

#### **Objetivos del Laboratorio**

1.  Enriquecer un archivo `schema.yml` existente con **descripciones** para modelos y columnas.
2.  Añadir **etiquetas (tags)** a los modelos para mejorar la organización del proyecto.
3.  Utilizar los comandos `dbt docs generate` y `dbt docs serve` para crear y visualizar el sitio de documentación del proyecto.
4.  Navegar por el sitio de documentación para encontrar información sobre un modelo y analizar su **gráfico de linaje (DAG)**.

#### **Herramientas y Prerrequisitos**
*   El proyecto `lab11-dbt` completado, con su `docker-compose.yml` y la estructura de carpetas de `dbt`.
*   Docker Desktop con `docker-compose`.
*   Un navegador web.



### **Procedimiento Detallado**

#### **Fase 1: Preparación del Entorno (~15 min)**

1.  **Abre tu Proyecto:**
    *   Navega a la carpeta de tu proyecto del Laboratorio 11 (`lab11-dbt`).
    *   **Acción:** Abre una terminal en esta carpeta.

2.  **Levanta la Base de Datos:**
    *   **Explicación:** `dbt docs generate` necesita conectarse a la base de datos para obtener metadatos técnicos (como los tipos de datos de las columnas). Por lo tanto, nuestro contenedor de PostgreSQL debe estar en ejecución.
    *   **Acción:** Ejecuta el siguiente comando para iniciar solo el servicio de la base de datos en segundo plano.
        ```bash
        sudo apt-get update
        sudo apt-get install --reinstall ca-certificates
        sudo update-ca-certificates
        sudo systemctl restart docker
        docker compose up -d postgres_db
        ```
    *   **Verificación:** Ejecuta `docker ps` para confirmar que el contenedor `dbt-postgres` está corriendo.



#### **Fase 2: Enriqueciendo los Metadatos "Como Código" (~60 min)**

Ahora, vamos a darle "contexto de negocio" a nuestro proyecto `dbt` editando el archivo `schema.yml`.

1.  **Abre el Archivo `schema.yml`:**
    *   **Acción:** Navega a la carpeta `models` dentro de tu proyecto `dbt` y abre el archivo `schema.yml` con tu editor de texto preferido (como VS Code).

2.  **Añade Descripciones a las Fuentes:**
    *   **Explicación:** Vamos a documentar de dónde vienen nuestros datos crudos.
    *   **Acción:** Modifica la sección `sources` para que se vea así. Presta mucha atención a la indentación.

    ```yaml
    sources:
      - name: public
        schema: public
        description: "Datos crudos cargados desde el sistema de punto de venta (POS)."
        tables:
          - name: raw_customers
            description: "Tabla de clientes sin procesar, tal como se registra en la app."
          - name: raw_sales
            description: "Tabla de transacciones de ventas sin procesar."
    ```

3.  **Añade Descripciones y Etiquetas a los Modelos:**
    *   **Explicación:** Ahora documentaremos nuestros modelos de staging, explicando su propósito y añadiendo etiquetas para poder seleccionarlos más fácilmente en el futuro.
    *   **Acción:** Modifica la sección `models` en tu `schema.yml`.

    ```yaml
    models:
      - name: stg_customers
        description: "Modelo de Staging: Limpia y estandariza la tabla de clientes. Cada fila representa un cliente único. Los clientes con IDs duplicados o status inválidos han sido filtrados en esta etapa (aunque la prueba los detectará en el origen)."
        tags: ['staging', 'clientes']
        columns:
          - name: id_cliente
            description: "La clave primaria (PK) del cliente."
            tests:
              - unique
              - not_null
          - name: status_cliente
            description: "El estado actual del cliente. Valores permitidos: ['activo', 'inactivo', 'potencial']."
            tests:
              - accepted_values:
                  values: ['activo', 'inactivo', 'potencial']

      - name: stg_sales
        description: "Modelo de Staging: Limpia la tabla de ventas. Filtra ventas que no tienen un cliente válido."
        tags: ['staging', 'ventas']
        columns:
          - name: id_transaccion
            description: "La clave primaria (PK) de la transacción."
            tests:
              - unique
              - not_null
          - name: id_cliente
            description: "La clave foránea (FK) que se relaciona con stg_customers.id_cliente."
            tests:
              - not_null
              - relationships:
                  to: ref('stg_customers')
                  field: id_cliente
    ```

4.  **Guarda el archivo `schema.yml`**.



#### **Fase 3: Generando y Explorando el Catálogo de Datos (~60 min)**

¡Es hora de ver la magia de `dbt`!

1.  **Genera los Artefactos de Documentación:**
    *   **Explicación:** Este comando le dice a `dbt` que lea todo tu proyecto (modelos, `schema.yml`, etc.) y que también se conecte a tu base de datos para obtener información del esquema. Luego, compila toda esta información en dos archivos clave: `manifest.json` y `catalog.json` dentro de la carpeta `target`.
    *   **Acción:** En tu terminal, ejecuta:
        ```bash
        docker compose run --rm dbt dbt docs generate --profiles-dir .
        ```
    *   **Resultado Esperado:** Verás una salida que indica que `dbt` está construyendo la documentación. Si todo va bien, terminará con un mensaje de éxito.

2.  **Lanza el Servidor Web Local:**
    *   **Explicación:** Este comando inicia un pequeño servidor web en tu computadora que lee los archivos `JSON` generados en el paso anterior y te presenta un sitio web interactivo.
    *   **Acción:** En tu terminal, ejecuta:
        ```bash
        docker compose run --rm -p 8080:8080 dbt dbt docs serve --profiles-dir .
        ```
    *   **Detalle Clave:** Hemos añadido `-p 8080:8080` para exponer el puerto del servidor de documentación a tu máquina local.
    *   **Resultado Esperado:** Tu terminal mostrará un mensaje como `Running on http://0.0.0.0:8080`. **No cierres esta terminal.**

3.  **Explora tu Catálogo de Datos:**
    *   **Acción:** Abre tu navegador web y navega a la siguiente dirección: **http://localhost:8080**
    *   **¡Felicidades!** Estás viendo el sitio de documentación de tu proyecto `dbt`.
    > ![Placeholder para Imagen 13.1: Captura de pantalla de la página de inicio del sitio de documentación de dbt.]



#### **Fase 4: Navegación Guiada y Búsqueda de Respuestas (~30 min)**

Ahora, usa el sitio de documentación para responder las preguntas del nuevo analista.

1.  **Investiga el Modelo `stg_customers`:**
    *   **Acción:** En el panel izquierdo, bajo "Models", haz clic en `stg_customers`.
    *   **Observa:**
        *   La **descripción** que escribiste para el modelo.
        *   La lista de **columnas**, con sus tipos de datos y las descripciones que añadiste.
        *   Las **pruebas** asociadas a cada columna.
        *   El **código fuente** del modelo.
    *   **Respuesta:** Ahora puedes responder fácilmente a la pregunta "¿Qué significa `status_cliente`?".

2.  **Analiza el Linaje de Datos (DAG):**
    *   **Acción:** En la parte inferior derecha de la página, haz clic en el botón verde "Lineage Graph".
    *   **Observa:** Verás un gráfico (DAG) que muestra tu pipeline. Deberías ver el nodo de la fuente `raw_customers` a la izquierda, una flecha apuntando a tu modelo `stg_customers` en el centro, y otra flecha desde `stg_customers` apuntando al nodo de la prueba de relación en `stg_sales`.
    > ![Placeholder para Imagen 13.2: Captura de pantalla del gráfico de linaje (DAG) en la documentación de dbt, mostrando las dependencias.]
    *   **Acción:** Haz clic en los nodos. Puedes ver cómo `dbt` te muestra las dependencias "upstream" (de dónde vienen los datos) y "downstream" (qué modelos se verán afectados si cambias este).
    *   **Respuesta:** Ahora puedes responder a la pregunta "¿Qué se rompe si cambio `raw_customers`?".

3.  **Cierra el Servidor:**
    *   **Acción:** Cuando termines de explorar, vuelve a la terminal donde se está ejecutando `dbt docs serve` y presiona `Ctrl + C` para detenerlo.

---

### **Entregable**

1.  Un archivo `.zip` que contenga tu **carpeta de proyecto `dbt_project` actualizada**, incluyendo el `schema.yml` enriquecido.
2.  Una **captura de pantalla (`documentacion.png`)** de tu navegador mostrando la página de detalles del modelo `stg_customers` en el sitio de documentación de `dbt`. La captura debe mostrar claramente las descripciones que añadiste para el modelo y sus columnas.

---

### **Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)**| **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Enriquecimiento de Metadatos (4 pts)** | El archivo `schema.yml` no se modifica o tiene errores graves de sintaxis YAML. | Añade algunas descripciones, pero son superficiales, incompletas o no cubren tanto las fuentes como los modelos. | Enriquece el archivo `schema.yml` con **descripciones claras y útiles** para todas las fuentes, modelos y columnas clave, y aplica `tags` correctamente. | / 4 |
| **Generación de la Documentación (3 pts)**| No logra ejecutar el comando `dbt docs generate` o este falla. | Ejecuta `dbt docs generate` con éxito, pero tiene problemas para lanzar o acceder al servidor web con `dbt docs serve`. | Ejecuta exitosamente los comandos `dbt docs generate` y `dbt docs serve`, y logra acceder al sitio de documentación local en el navegador. | / 3 |
| **Análisis del Linaje y Calidad del Entregable (3 pts)**| No logra encontrar o interpretar el gráfico de linaje. El entregable está incompleto. | Navega por la documentación, pero tiene dificultades para encontrar el gráfico de linaje o para explicar lo que representa. | El entregable está completo y la captura de pantalla demuestra que el sitio de documentación se generó correctamente. El estudiante puede explicar verbalmente cómo el gráfico de linaje responde a una pregunta de análisis de impacto. | / 3 |
| **Total**| | | | **/ 10** |
