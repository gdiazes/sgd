### **Guía de Laboratorio 11: Implementando un Pipeline de Datos Confiable con `dbt`**

#### **Marco Conceptual**

La calidad de datos en un entorno ágil no se puede garantizar con limpiezas manuales. Se requiere un enfoque de "Datos como Código", donde las transformaciones y, crucialmente, las pruebas de calidad, se definen en código, se versionan y se ejecutan automáticamente. `dbt` (Data Build Tool) es la herramienta estándar de la industria para implementar esta filosofía. En este laboratorio, actuarás como el primer Ingeniero Analítico de "FrutiFresh". Tu misión es construir un pipeline de datos básico pero robusto que transforme los datos crudos de ventas y clientes y, lo más importante, que implemente pruebas automatizadas para garantizar su confiabilidad continua.

#### **Caso de Estudio**

"FrutiFresh" está creciendo, y sus dashboards en Looker Studio dependen de datos crudos que a menudo tienen problemas de calidad. La CEO quiere un pipeline de datos más confiable. Te ha pedido que uses `dbt` para crear un "área de staging" en la base de datos. Esta área contendrá versiones limpias y estandarizadas de las tablas de clientes y ventas. Además, te ha exigido que el pipeline incluya **pruebas automáticas** que fallen y alerten al equipo si los datos de origen no cumplen con las reglas de negocio básicas.

#### **Objetivos del Laboratorio**

1.  Inicializar un proyecto `dbt` y conectarlo a una base de datos PostgreSQL.
2.  Crear **modelos** `dbt` (usando sentencias `SELECT`) para limpiar y estandarizar datos de origen.
3.  Definir y ejecutar **pruebas de datos genéricas** (`unique`, `not_null`, `accepted_values`) para validar la calidad de las tablas.
4.  Generar y explorar la **documentación automática** del proyecto `dbt`.

#### **Herramientas y Prerrequisitos**
*   Docker Desktop con `docker-compose`.
*   Un editor de texto (como VS Code).
*   Un navegador web.


### **Procedimiento Detallado**

#### **Fase 1: Preparación del Entorno (~45 min)**

Vamos a usar `docker-compose` para levantar nuestra base de datos y un contenedor con `dbt` y todas sus dependencias.

1.  **Crea la Estructura de tu Proyecto:**
    *   **Acción:** En tu computadora, crea una nueva carpeta llamada `lab11-dbt`.
    *   Dentro de `lab11-dbt`, crea dos archivos vacíos: `docker-compose.yml` y `dbt_project.yml`.
    *   Crea una subcarpeta llamada `models`.

2.  **Configura `docker-compose.yml`:**
    *   **Acción:** Pega el siguiente código en tu archivo `docker-compose.yml`.

    ```yaml
    version: '3.8'
    services:
      postgres_db:
        image: postgres:15.15-trixie
        container_name: dbt-postgres
        environment:
          - POSTGRES_USER=dbt_user
          - POSTGRES_PASSWORD=dbt_password
          - POSTGRES_DB=dbt_db
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data

      dbt:
        image: ghcr.io/dbt-labs/dbt-postgres:1.5.0
        container_name: dbt-container
        volumes:
          - .:/usr/app
        command: ["--version"] # Comando inicial solo para verificar que funciona
        depends_on:
          - postgres_db

    volumes:
      postgres_data:
    ```
    *   **Explicación:** Este archivo crea dos servicios: una base de datos PostgreSQL y un contenedor con `dbt-postgres` (que incluye `dbt` y los drivers para conectar a Postgres). El `volumes: - .:/usr/app` es clave: mapea nuestra carpeta de proyecto `lab11-dbt` al directorio de trabajo dentro del contenedor `dbt`.

3.  **Configura `dbt_project.yml`:**
    *   **Acción:** Pega el siguiente código en tu archivo `dbt_project.yml`.

    ```yaml
    name: 'frutifresh_analytics'
    version: '1.0.0'
    config-version: 2

    profile: 'frutifresh'

    model-paths: ["models"]
    test-paths: ["tests"]

    target-path: "target"
    clean-targets:
      - "target"
      - "dbt_packages"
    ```
    *   **Explicación:** Este es el archivo principal de configuración de un proyecto `dbt`. Le dice a `dbt` el nombre del proyecto y dónde encontrar los modelos y las pruebas.

4.  **Levanta el Entorno:**
    *   **Acción:** Abre una terminal en la carpeta `lab11-dbt` y ejecuta:
        ```bash
        docker-compose up -d
        ```

5.  **Carga los Datos Crudos:**
    *   **Acción:** Conecta DBeaver a la base de datos (`localhost:5432`, db: `dbt_db`, user: `dbt_user`, pass: `dbt_password`).
    *   **Acción:** En un editor SQL, ejecuta el siguiente script para simular las tablas de datos crudos ("raw data") que `dbt` transformará.
    ```sql
    CREATE TABLE raw_customers (
        id_cliente INT,
        nombre VARCHAR(50),
        status_cliente VARCHAR(20)
    );

    CREATE TABLE raw_sales (
        id_transaccion INT,
        id_cliente INT,
        monto NUMERIC(10, 2)
    );

    INSERT INTO raw_customers VALUES
    (1, 'Ana Solis', 'activo'),
    (2, 'Carlos Rojas', 'inactivo'),
    (3, 'David Luna', 'potencial'),
    (4, 'Laura Paz', 'activo'),
    (4, 'Laura de Paz', 'pendiente'); -- Problema: ID duplicado y status inválido

    INSERT INTO raw_sales VALUES
    (101, 1, 12.50),
    (102, 2, 5.00),
    (103, 1, 15.00),
    (104, 4, 20.00),
    (105, 5, 10.00); -- Problema: Venta para un cliente que no existe
    ```


#### **Fase 2: Construcción de Modelos de Staging con `dbt` (~75 min)**

Nuestra misión es crear versiones limpias de estas tablas.

1.  **Crea tu Primer Modelo: `stg_customers.sql`**
    *   **Acción:** Dentro de la carpeta `models`, crea un archivo llamado `stg_customers.sql`.
    *   **Acción:** Pega la siguiente consulta `SELECT`.
    ```sql
    -- models/stg_customers.sql

    SELECT
        id_cliente,
        nombre,
        status_cliente
    FROM
        {{ source('public', 'raw_customers') }} -- ¡Esto es Jinja! Es una referencia a la tabla de origen.
    ```

2.  **Crea tu Segundo Modelo: `stg_sales.sql`**
    *   **Acción:** Dentro de la carpeta `models`, crea un archivo llamado `stg_sales.sql`.
    *   **Acción:** Pega la siguiente consulta.
    ```sql
    -- models/stg_sales.sql

    SELECT
        id_transaccion,
        id_cliente,
        monto
    FROM
        {{ source('public', 'raw_sales') }}
    ```

3.  **Configura las Fuentes y las Pruebas:**
    *   **Acción:** Dentro de la carpeta `models`, crea un nuevo archivo llamado `schema.yml`.
    *   **Acción:** Pega el siguiente contenido YAML. ¡La indentación es crucial!
    ```yaml
    version: 2

    sources:
      - name: public
        schema: public
        tables:
          - name: raw_customers
          - name: raw_sales

    models:
      - name: stg_customers
        description: "Tabla limpia y estandarizada de clientes de FrutiFresh."
        columns:
          - name: id_cliente
            description: "El identificador único para un cliente."
            tests:
              - unique
              - not_null
          - name: status_cliente
            description: "El estado actual del cliente en el programa de lealtad."
            tests:
              - accepted_values:
                  values: ['activo', 'inactivo', 'potencial']

      - name: stg_sales
        description: "Tabla limpia de transacciones de ventas."
        columns:
          - name: id_transaccion
            tests:
              - unique
              - not_null
          - name: id_cliente
            tests:
              - not_null
              - relationships:
                  to: ref('stg_customers')
                  field: id_cliente
    ```
    *   **Explicación Detallada:**
        *   `sources:`: Le dice a `dbt` dónde encontrar las tablas de origen.
        *   `models:`: Aquí definimos nuestras expectativas (pruebas) para los modelos de staging.
        *   `unique`, `not_null`: Pruebas genéricas que verifican unicidad y no nulidad.
        *   `accepted_values`: Verifica que una columna solo contenga valores de una lista específica.
        *   `relationships`: ¡Muy potente! Verifica la **integridad referencial**. Esta prueba asegura que cada `id_cliente` en `stg_sales` exista en la tabla `stg_customers`.


#### **Fase 3: Ejecución y Validación (~60 min)**

Ahora, usaremos `dbt` desde la línea de comandos para ejecutar nuestro pipeline.

1.  **Ejecuta los Modelos:**
    *   **Acción:** En tu terminal (dentro de la carpeta `lab11-dbt`), ejecuta el siguiente comando.
    ```bash
    docker-compose run --rm dbt dbt run --profiles-dir .
    ```
    *   **Explicación:** Este comando le dice a `docker-compose` que ejecute un comando (`dbt run`) dentro del servicio `dbt`. El `dbt run` encontrará tus archivos `.sql` y los ejecutará, creando vistas o tablas en tu base de datos.
    *   **Verificación:** En DBeaver, actualiza tu esquema. Deberías ver dos nuevas vistas: `stg_customers` y `stg_sales`.

2.  **¡Ejecuta las Pruebas!**
    *   **Acción:** Ahora, vamos a validar la calidad de nuestros datos de origen contra las reglas que definimos en `schema.yml`.
    ```bash
    docker-compose run --rm dbt dbt test --profiles-dir .
    ```
    *   **¡Observa el Resultado!** `dbt` ejecutará todas las pruebas. Verás que algunas pasan (`PASS`), pero varias **fallan (`FAIL`)** en rojo.
    *   **Análisis del Fracaso:** La salida te dirá exactamente por qué fallaron las pruebas:
        *   `unique` en `stg_customers.id_cliente` fallará porque hay un ID duplicado (4).
        *   `accepted_values` en `stg_customers.status_cliente` fallará por el valor 'pendiente'.
        *   `relationships` en `stg_sales.id_cliente` fallará porque la venta con `id_cliente = 5` no tiene un cliente correspondiente.

3.  **Genera la Documentación:**
    *   **Acción:** `dbt` puede generar un sitio web completo con toda la documentación de tu proyecto y el linaje de datos.
    ```bash
    docker-compose run --rm dbt dbt docs generate --profiles-dir .
    ```
    *   Este comando crea los archivos del sitio web dentro de la carpeta `target`. (Explorarlo localmente es más avanzado, pero este paso demuestra la capacidad).


### **Entregable**

1.  Toma una captura de pantalla completa de tu ventana de terminal después de ejecutar el comando `dbt test`.
2.  La captura debe mostrar claramente:
    *   El comando `dbt test` que ejecutaste.
    *   La lista de pruebas que se ejecutaron.
    *   Los resultados `PASS` en verde y, lo más importante, los resultados `FAIL` en rojo, con el resumen de por qué fallaron.
3.  Sube esta imagen a la plataforma del curso. El objetivo de este laboratorio no es "arreglar" los datos, sino **demostrar que has construido un sistema de pruebas automáticas que detecta exitosamente los problemas de calidad**.


### **Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Configuración del Entorno `dbt` (3 pts)** | No logra configurar los archivos `yml` o el `docker-compose up` falla. | El entorno se levanta, pero con errores en la configuración que impiden la correcta ejecución de `dbt`. | Configura correctamente el proyecto `dbt` y el entorno `docker-compose`, y logra una conexión exitosa entre `dbt` y la base de datos. | / 3 |
| **Creación de Modelos y Fuentes (3 pts)** | No crea los archivos de modelo `.sql` o el `schema.yml`. | Crea los archivos, pero con errores de sintaxis en el `schema.yml` o en las referencias `source()` de los modelos. | Define correctamente los modelos de staging y configura el archivo `schema.yml` para declarar las fuentes y los modelos de forma válida. | / 3 |
| **Implementación y Ejecución de Pruebas (4 pts)** | No logra ejecutar el comando `dbt test` o este falla por errores de configuración. | Ejecuta `dbt test`, pero las pruebas definidas en el `schema.yml` son incompletas o no cubren todos los tipos de pruebas solicitadas (unique, not_null, accepted_values, relationships). | Define un conjunto completo de pruebas en `schema.yml` y el entregable demuestra la ejecución exitosa de `dbt test`, mostrando claramente tanto las pruebas que pasan como las que fallan, validando la detección de todos los problemas de calidad. | / 4 |
| **Total**| | | | **/ 10** |
