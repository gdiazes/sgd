### **Guía de Laboratorio 07: Desafío de Optimización - El Reporte Lento de AndesHarvest**

#### ** Marco Conceptual**

La eficiencia de una base de datos no depende solo de la potencia del hardware, sino fundamentalmente de su **estrategia de acceso a los datos**. En tablas con millones de filas, una consulta mal optimizada puede tardar minutos u horas, mientras que la misma consulta, bien optimizada con un índice, puede ejecutarse en milisegundos. En este laboratorio, actuarás como un **Ingeniero de Rendimiento de Datos (Database Performance Engineer)**. Tu misión es diagnosticar una consulta lenta utilizando la herramienta `EXPLAIN ANALYZE`, implementar la solución (un índice) y medir el impacto dramático de tu optimización.

#### ** Caso de Estudio**

"AndesHarvest Export" ha estado operando exitosamente por más de un año y su tabla `Registros_Cosecha` ahora contiene **más de 2 millones de registros**. El Gerente de RRHH necesita urgentemente un reporte para calcular las bonificaciones de fin de año. Su petición es simple: **"Necesito ver todos los registros de cosecha de la empleada Ana Solis (ID 'E-045') para auditar su producción"**.

El equipo de desarrollo ha ejecutado la consulta `SELECT * FROM Registros_Cosecha WHERE id_empleado = 'E-045';` pero la aplicación se congela y la consulta nunca parece terminar. Te han llamado a ti, el experto, para solucionar el problema.

#### ** Objetivos del Laboratorio**

1.  Trabajar con un volumen de datos significativo para simular un escenario de rendimiento realista.
2.  Utilizar `EXPLAIN ANALYZE` para diagnosticar el plan de ejecución de una consulta lenta e identificar un **Escaneo Secuencial (Seq Scan)**.
3.  Implementar un **índice (B-Tree)** en la columna apropiada para optimizar la consulta.
4.  Volver a ejecutar `EXPLAIN ANALYZE` para verificar que la consulta ahora utiliza un **Escaneo de Índice (Index Scan)**.
5.  Cuantificar y comunicar la mejora en el rendimiento (en términos de tiempo de ejecución) lograda por la optimización.

#### ** Herramientas y Entorno**
*   PostgreSQL y DBeaver.



### **Procedimiento del Desafío**

#### **Fase 1: Preparación del Escenario de Gran Volumen (~45 min)**

Vamos a crear una tabla grande. Este proceso puede tardar unos minutos. ¡Ten paciencia!

1.  Abre DBeaver, conéctate a tu base de datos y abre un nuevo Editor de SQL.
2.  Ejecuta el siguiente script para crear la tabla `Registros_Cosecha` y poblarla con aproximadamente **2 millones de filas**.

    ```sql
    -- ===== INICIO DEL ESCENARIO: TABLA DE GRAN VOLUMEN =====

    DROP TABLE IF EXISTS Registros_Cosecha;

    CREATE TABLE Registros_Cosecha (
        id_registro SERIAL PRIMARY KEY,
        id_empleado VARCHAR(10) NOT NULL,
        id_parcela VARCHAR(10) NOT NULL,
        kilos_cosechados NUMERIC(5,2) NOT NULL,
        fecha_hora_cosecha TIMESTAMP NOT NULL
    );

    -- Insertamos 2 millones de filas de datos sintéticos.
    -- Esta consulta puede tardar entre 1 y 5 minutos en ejecutarse.
    INSERT INTO Registros_Cosecha (id_empleado, id_parcela, kilos_cosechados, fecha_hora_cosecha)
    SELECT
        'E-' || LPAD((n % 1000)::text, 3, '0'), -- Genera IDs de empleado de E-000 a E-999
        'P-' || LPAD(((n % 100) + 1)::text, 2, '0'), -- Genera IDs de parcela de P-01 a P-100
        ROUND((RANDOM() * 30 + 5)::numeric, 2), -- Kilos entre 5 y 35
        NOW() - (n || ' minutes')::interval -- Fechas hacia el pasado
    FROM generate_series(1, 2000000) AS n;

    -- ===== FIN DEL ESCENARIO =====
    ```
3.  **Verificación:** Una vez que el `INSERT` termine, ejecuta una consulta de conteo para confirmar el tamaño de la tabla.
    ```sql
    SELECT COUNT(*) FROM Registros_Cosecha; -- Debería devolver 2,000,000
    ```


#### **Fase 2: Diagnóstico de la Consulta Lenta (~45 min)**

Ahora, vamos a experimentar el problema del Gerente de RRHH.

1.  **Ejecuta el Diagnóstico:** Usa `EXPLAIN ANALYZE` para ejecutar la consulta problemática y ver su plan de ejecución y tiempos reales.

    ```sql
    -- Diagnóstico de la consulta original
    EXPLAIN ANALYZE SELECT * FROM Registros_Cosecha WHERE id_empleado = 'E-045';
    ```

2.  **Analiza el Resultado:**
    *   Observa la salida en DBeaver. En la pestaña "Explain Plan", verás el plan visual, pero también es crucial ver la salida de texto.
    *   **Identifica el `Seq Scan`:** La primera línea del plan probablemente dirá `Parallel Seq Scan on registros_cosecha` o `Seq Scan on registros_cosecha`. Esto te confirma que la base de datos está leyendo la tabla completa.
    *   **Anota el Tiempo de Ejecución:** Busca la línea `Execution Time: ... ms` al final de la salida. Anota este número. Debería ser de varios cientos o incluso miles de milisegundos (dependiendo de tu máquina).
    *   **Anota el Costo:** Observa el valor de `cost=...` en la primera línea. Anota el segundo número (el costo total estimado).

    > **Tu Misión:** Copia y pega la salida completa de texto de este `EXPLAIN ANALYZE` en un archivo de texto. Esta es tu "Evidencia del Problema".


#### **Fase 3: Implementación de la Solución de Optimización (~45 min)**

Basado en tu diagnóstico, la solución es crear un índice en la columna que se usa para filtrar.

1.  **Crea el Índice:** Escribe y ejecuta el comando para crear un índice en la columna `id_empleado`.

    ```sql
    -- Implementación de la solución
    CREATE INDEX idx_registros_cosecha_id_empleado ON Registros_Cosecha (id_empleado);
    ```
    > Esta operación también puede tardar uno o dos minutos, ya que la base de datos debe leer los 2 millones de valores de `id_empleado` para construir el índice.

2.  **Vuelve a Ejecutar el Diagnóstico:** Ahora que el índice existe, ejecuta exactamente el mismo comando `EXPLAIN ANALYZE` de la Fase 2.

    ```sql
    -- Verificación de la optimización
    EXPLAIN ANALYZE SELECT * FROM Registros_Cosecha WHERE id_empleado = 'E-045';
    ```

3.  **Analiza el Nuevo Resultado:**
    *   **Identifica el `Index Scan`:** Observa la nueva salida. El plan ahora debería usar un `Bitmap Heap Scan` y un `Bitmap Index Scan` sobre `idx_registros_cosecha_id_empleado`. ¡Esto confirma que el optimizador está usando tu índice!
    *   **Compara el Tiempo de Ejecución:** Busca la nueva línea `Execution Time: ... ms`. Compara este número con el que anotaste antes. La diferencia debería ser dramática (a menudo 10x a 100x más rápido).
    *   **Compara el Costo:** Observa el nuevo valor de `cost=...`. Debería ser significativamente más bajo que el costo del `Seq Scan`.

    > **Tu Misión:** Copia y pega la salida completa de texto de este segundo `EXPLAIN ANALYZE` en tu archivo de texto. Esta es tu "Evidencia de la Solución".


### **Entregable**

Un único archivo de texto (`reporte_optimizacion.txt`) que contenga:
1.  **Sección 1: Diagnóstico del Problema**
    *   Un título ("Diagnóstico del Problema").
    *   La salida completa del primer `EXPLAIN ANALYZE` (con el `Seq Scan`).
    *   Una línea que resuma: `Tiempo de Ejecución sin Índice: [Tu tiempo aquí] ms`.
2.  **Sección 2: Implementación de la Solución**
    *   Un título ("Implementación de la Solución").
    *   El comando `CREATE INDEX` que ejecutaste.
3.  **Sección 3: Verificación de la Mejora**
    *   Un título ("Verificación de la Mejora").
    *   La salida completa del segundo `EXPLAIN ANALYZE` (con el `Index Scan`).
    *   Una línea que resuma: `Tiempo de Ejecución con Índice: [Tu tiempo aquí] ms`.
4.  **Sección 4: Conclusión**
    *   Un título ("Conclusión").
    *   Un breve párrafo (2-3 líneas) donde calcules y comuniques la mejora. Ejemplo: "La implementación del índice en la columna `id_empleado` redujo el tiempo de ejecución de la consulta de XXXX ms a YY ms, logrando una mejora en el rendimiento de aproximadamente **[Calcula el factor de mejora aquí] veces**."

---

### ** Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Diagnóstico del Problema (3 pts)** | No ejecuta `EXPLAIN ANALYZE` o no incluye la salida en el reporte. | Ejecuta el comando, pero en su reporte no identifica correctamente el `Seq Scan` ni anota el tiempo de ejecución. | Ejecuta `EXPLAIN ANALYZE`, incluye la salida completa en el reporte e identifica correctamente que el problema es un `Seq Scan`, anotando el tiempo. | / 3 |
| **Implementación de la Solución (3 pts)** | No logra crear el índice o lo crea en una columna incorrecta. | Crea el índice correctamente, pero no incluye el comando `CREATE INDEX` en su reporte como evidencia. | El reporte incluye la sentencia `CREATE INDEX` correcta y ejecutada sobre la columna `id_empleado`. | / 3 |
| **Verificación de la Mejora (3 pts)** | No vuelve a ejecutar el diagnóstico o no incluye la nueva salida en el reporte. | Vuelve a ejecutar `EXPLAIN ANALYZE`, pero no logra identificar el cambio a `Index Scan` o no compara los tiempos. | Ejecuta el segundo `EXPLAIN ANALYZE`, incluye la salida completa y demuestra que el plan ahora usa un `Index Scan`, anotando el nuevo tiempo. | / 3 |
| **Análisis y Comunicación (1 pto)** | | El reporte está incompleto y no presenta una conclusión clara sobre la mejora. | El reporte está completo, bien estructurado y la sección de **Conclusión** comunica de forma clara y cuantitativa la magnitud de la mejora en el rendimiento. | / 1 |
| **Total**| | | | **/ 10** |
