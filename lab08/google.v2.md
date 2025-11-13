### **Guía de Laboratorio 08 (Avanzado): Migrando AndesHarvest a la Nube y Optimizando para Análisis**

#### **Marco Conceptual**

Aprovisionar una base de datos en la nube es solo el primer paso. Un desafío mucho más común y complejo en el mundo real es la **migración**: mover una base de datos existente desde un entorno local (On-Premise) a la nube. Este proceso implica no solo la creación de la infraestructura, sino también la exportación de datos, su transferencia y su importación en el nuevo sistema. Además, las plataformas en la nube ofrecen una gran cantidad de opciones de configuración que un ingeniero debe entender para optimizar la instancia según la carga de trabajo, ya sea transaccional (OLTP) o analítica (OLAP).

#### **Caso de Estudio Avanzado**

"AndesHarvest Export" ha tenido éxito con su base de datos de trazabilidad (la que diseñaste en la Semana 5) que ha estado corriendo en un servidor local en su oficina (On-Premise). El sistema ha crecido y ahora contiene miles de registros. Sin embargo, el servidor local está mostrando sus límites:
1.  **Problemas de Rendimiento:** Durante el día (alta carga de inserciones de datos de cosecha), los reportes de análisis que ejecuta la gerencia se vuelven extremadamente lentos.
2.  **Riesgo de Disponibilidad:** El servidor no tiene redundancia. Si falla, toda la operación de trazabilidad se detiene.

La Gerencia ha decidido migrar a Google Cloud SQL para ganar escalabilidad y alta disponibilidad. Tu misión como Ingeniero de Datos es **liderar este proyecto de migración**.

#### **Objetivos del Desafío**

1.  Aprovisionar una instancia de Cloud SQL optimizada con una **réplica de lectura (read replica)** para separar las cargas de trabajo.
2.  Realizar una **migración de datos** exportando un esquema y datos desde un entorno local (simulado) e importándolos a la nube.
3.  Comprender y configurar la **Alta Disponibilidad (High Availability)** para proteger la base de datos contra fallos.
4.  Conectar DBeaver a la instancia principal (para escritura) y a la réplica de lectura (para análisis) y verificar que la replicación funciona.

#### **Herramientas y Prerrequisitos**
*   Una cuenta de Google Cloud Platform (GCP) con facturación habilitada.
*   DBeaver instalado.
*   Un contenedor Docker de PostgreSQL corriendo localmente (simulará el servidor "On-Premise").
*   El script `esquema_andesharvest.sql` que creaste en el laboratorio de la Semana 5.



### **Procedimiento Detallado Paso a Paso**

#### **Fase 1: Simulación del Entorno On-Premise y Exportación de Datos (~45 min)**

Primero, simularemos la base de datos local de AndesHarvest que necesitamos migrar.

1.  **Levanta un Contenedor Docker Local:**
    *   Abre una terminal y ejecuta el siguiente comando para crear tu servidor "On-Premise".
    ```bash
    docker run --name andesharvest-onprem -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d postgres
    ```
    > **Explicación Detallada:** Estamos usando el puerto `5433` en nuestra máquina para no entrar en conflicto con otras instancias de PostgreSQL que puedas tener.

2.  **Conecta DBeaver a tu Servidor Local:**
    *   Crea una nueva conexión en DBeaver a PostgreSQL.
    *   **Host:** `localhost`
    *   **Port:** `5433`
    *   **Username/Password:** `postgres` / `mysecretpassword`
    *   Nombra a esta conexión **"AndesHarvest (On-Premise)"**.

3.  **Crea y Puebla la Base de Datos Local:**
    *   Abre un editor SQL para esta conexión.
    *   Ejecuta el script `esquema_andesharvest.sql` de la Semana 5 para crear las tablas (`Empleados`, `Parcelas`, etc.).
    *   Ahora, inserta algunos datos de ejemplo ejecutando el siguiente script:
    ```sql
    INSERT INTO Empleados VALUES ('E-045', 'Ana', 'Solis', '2023-01-15');
    INSERT INTO Parcelas VALUES ('P-07B', 'Ventana', 5.2, '2020-05-10');
    INSERT INTO Registros_Cosecha (id_empleado, id_parcela, kilos_cosechados, fecha_hora_cosecha) VALUES ('E-045', 'P-07B', 25.5, '2024-06-15 10:00:00');
    ```

4.  **Exporta los Datos (Backup):**
    *   En DBeaver, haz clic derecho sobre la base de datos `postgres` de tu conexión "On-Premise".
    *   Selecciona **"Herramientas" -> "Backup"**.
    *   **Explicación Detallada:** Esta acción utiliza la utilidad `pg_dump` de PostgreSQL para crear un archivo `.sql` que contiene tanto la estructura de tus tablas (`CREATE TABLE`) como los datos (`INSERT`). Es el método estándar para realizar backups y migraciones.
    *   En el asistente de backup, asegúrate de que el formato sea **"Plain"**. Elige una ubicación en tu computadora para guardar el archivo y nómbralo `backup_andesharvest.sql`.
    *   Haz clic en "Iniciar". Ahora tienes un archivo que representa el estado completo de tu base de datos local.
    > ![Placeholder para Imagen 5.1: Captura de pantalla del asistente de backup en DBeaver, mostrando la selección de formato "Plain".]

#### **Fase 2: Aprovisionamiento de una Instancia Cloud SQL Optimizada (~60 min)**

Ahora crearemos la infraestructura en la nube, pero esta vez, con una configuración avanzada.

1.  **Crea una Instancia de Cloud SQL:**
    *   Sigue los pasos del laboratorio anterior para crear una nueva instancia de PostgreSQL en GCP.
    *   **ID de instancia:** `andesharvest-cloud-db`
    *   **Contraseña:** Genera y guarda una contraseña segura.
    *   **Configuración predefinida:** Elige **"Producción"**.
    *   **Explicación Detallada:** Al elegir "Producción" en lugar de "Desarrollo", GCP nos sugiere una configuración inicial más robusta. Vamos a personalizarla.

2.  **Habilita la Alta Disponibilidad (High Availability):**
    *   En la sección "Personalizar tu instancia", expande **"Disponibilidad"**.
    *   Selecciona **"Alta disponibilidad (regional)"**.
    *   **Explicación Detallada:** Esta es una de las ventajas más grandes de la nube. Al habilitar esto, Cloud SQL crea y mantiene automáticamente una instancia de **"failover"** en una zona diferente dentro de la misma región. Si la instancia principal falla por cualquier motivo (ej. un problema de hardware en el datacenter de Google), el sistema basculará automáticamente a la instancia de failover en cuestión de minutos, con una pérdida de datos mínima o nula. Esto resuelve el problema de disponibilidad de AndesHarvest.
    > ![Placeholder para Imagen 5.2: Captura de pantalla de la configuración de Cloud SQL, mostrando la opción "Alta disponibilidad" seleccionada.]

3.  **Crea la Instancia y Configura la Red:**
    *   Termina de crear la instancia. Mientras se aprovisiona, ve a la pestaña **"Conexiones"** y añade tu dirección IP pública a las **"Redes autorizadas"**, tal como hiciste en el laboratorio anterior.

#### **Fase 3: Creación de la Réplica de Lectura (~30 min)**

Ahora resolveremos el problema de rendimiento separando las cargas de trabajo.

1.  **Crea una Réplica de Lectura:**
    *   Una vez que tu instancia principal (`andesharvest-cloud-db`) esté "Available", selecciónala en la lista de instancias.
    *   En la parte superior, haz clic en el menú **"Réplicas"** y luego en **"Crear réplica de lectura"**.
    *   Dale un ID de instancia, como `andesharvest-cloud-db-replica`.
    *   Mantén el resto de las configuraciones y haz clic en "Crear".
    *   **Explicación Detallada:** Una réplica de lectura es una copia exacta y de solo lectura de tu base de datos principal. Cloud SQL se encarga de replicar de forma asíncrona todos los cambios de la principal a la réplica. El caso de uso es claro: todas las operaciones de escritura de la aplicación (los `INSERT` de cosecha) se envían a la instancia principal, mientras que todas las consultas pesadas de análisis (los reportes del gerente) se envían a la réplica. De esta forma, las cargas de trabajo no compiten entre sí.
    > ![Placeholder para Imagen 5.3: Diagrama simple mostrando una app de escritura apuntando a la BD Principal, y un dashboard de BI apuntando a la Réplica de Lectura.]

2.  **Configura la Red para la Réplica:**
    *   La réplica es una instancia independiente. Debes repetir el proceso de añadir tu IP pública a sus **"Redes autorizadas"** para poder conectarte a ella.

#### **Fase 4: Migración de Datos y Verificación Final (~45 min)**

1.  **Conecta DBeaver a la Instancia Principal:**
    *   Obtén la **Dirección IP pública** de tu instancia principal (`andesharvest-cloud-db`).
    *   Crea una nueva conexión en DBeaver con esta IP y tus credenciales de `postgres`. Nómbrala **"AndesHarvest Cloud (Principal)"**.

2.  **Importa los Datos (Migración):**
    *   Haz clic derecho sobre la base de datos `postgres` de tu nueva conexión en la nube.
    *   Selecciona **"Herramientas" -> "Restore"** (Restaurar).
    *   En el asistente, selecciona el archivo `backup_andesharvest.sql` que creaste en la Fase 1.
    *   Haz clic en "Iniciar".
    *   **Explicación Detallada:** Esta acción utiliza la utilidad `pg_restore` para ejecutar el script de tu backup en la nueva base de datos de la nube. Esto creará las tablas e insertará los datos, completando la migración.

3.  **Conecta DBeaver a la Réplica de Lectura:**
    *   Obtén la **Dirección IP pública** de tu instancia de réplica (`andesharvest-cloud-db-replica`).
    *   Crea una **tercera conexión** en DBeaver con la IP de la réplica y las mismas credenciales. Nómbrala **"AndesHarvest Cloud (Réplica - Solo Lectura)"**.

4.  **Verificación Final:**
    *   **Prueba de Replicación:**
        *   En la conexión **Principal**, ejecuta un nuevo `INSERT`:
          ```sql
          INSERT INTO Empleados VALUES ('E-100', 'Nuevo', 'Empleado', '2024-06-16');
          ```
        *   Espera unos segundos.
        *   Ahora, en la conexión de la **Réplica**, ejecuta una consulta de lectura:
          ```sql
          SELECT * FROM Empleados WHERE id_empleado = 'E-100';
          ```
        > ¡Deberías ver al nuevo empleado! Esto demuestra que la replicación está funcionando.
    *   **Prueba de Solo Lectura:**
        *   En la conexión de la **Réplica**, intenta ejecutar un `DELETE`:
          ```sql
          DELETE FROM Empleados WHERE id_empleado = 'E-100';
          ```
        > Deberías recibir un **error** indicando que la base de datos es de solo lectura. ¡Esto confirma que la réplica está correctamente configurada para protegerla de escrituras!



### **Entregable**

1.  Una captura de pantalla de tu ventana de DBeaver que muestre:
    *   Las **tres conexiones** en el "Database Navigator": la local "On-Premise", la "Cloud (Principal)" y la "Cloud (Réplica - Solo Lectura)".
    *   En la conexión de la **Réplica**, el resultado del `SELECT` que encontró al "Nuevo Empleado".
    *   En la misma conexión de la **Réplica**, el error que recibiste al intentar ejecutar el `DELETE`.
2.  Sube esta imagen a la plataforma.



### **Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Migración de Datos (3 pts)** | No logra exportar o importar los datos. | Logra exportar el backup, pero tiene problemas significativos al importarlo en la nube. | Realiza exitosamente el ciclo completo de backup (`pg_dump`) desde el entorno local y restauración (`pg_restore`) en la instancia de Cloud SQL principal. | / 3 |
| **Configuración de Alta Disponibilidad (2 pts)** | No habilita la Alta Disponibilidad en la instancia principal. | | Habilita correctamente la opción de Alta Disponibilidad (regional) durante la creación de la instancia principal. | / 2 |
| **Configuración de Réplica de Lectura (3 pts)** | No logra crear la réplica de lectura. | Crea la réplica, pero no logra conectarse a ella por problemas de configuración de red. | Crea y configura correctamente la réplica de lectura, incluyendo sus reglas de red, y logra conectarse a ella desde DBeaver. | / 3 |
| **Verificación y Análisis (2 pts)** | No realiza las pruebas de verificación o el entregable no las demuestra. | Realiza algunas de las pruebas, pero no demuestra claramente la replicación o la naturaleza de solo lectura de la réplica. | El entregable demuestra de forma inequívoca tanto el éxito de la **replicación de datos** como el **bloqueo de escritura** en la instancia de réplica, validando toda la arquitectura. | / 2 |
| **Total**| | | | **/ 10** |
