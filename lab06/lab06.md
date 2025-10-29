### **Guía de Laboratorio 06: Preparando los Datos para el Primer Reporte de Productividad de AndesHarvest**

#### ** Marco Conceptual**

En el mundo real, los datos rara vez llegan limpios. Antes de que se pueda realizar cualquier análisis de negocio significativo, un analista o ingeniero de datos debe realizar un proceso de **limpieza y preparación de datos** (también conocido como Data Wrangling). Este proceso implica auditar los datos para identificar problemas de calidad (perfilado), aplicar transformaciones para corregirlos y verificar que el conjunto de datos resultante sea confiable. En este laboratorio, seguirás este proceso sistemático para transformar un conjunto de datos crudos y "sucios" en un activo de información listo para el análisis.

#### ** Caso de Estudio**

El Gerente de Operaciones de AndesHarvest quiere crear el primer "Reporte de Productividad de Cosechadores". El objetivo es calcular los kilos totales cosechados por cada empleado en el último mes. Sin embargo, al intentar ejecutar un primer análisis, los resultados son absurdos: aparecen empleados sin nombre, kilos negativos y totales inflados.

Te han entregado una tabla temporal llamada `cosecha_mensual_crudo` que contiene los datos en bruto. Tu misión como Analista de Datos es **diagnosticar los problemas de calidad, escribir un script SQL para limpiar los datos y producir una tabla final, `cosecha_mensual_limpia`, que sea 100% confiable** para el análisis gerencial.

#### ** Objetivos del Laboratorio**

1.  **Perfilar** un conjunto de datos utilizando consultas de agregación SQL para identificar problemas de calidad (nulos, duplicados, inconsistencias, outliers).
2.  Escribir sentencias `UPDATE` y `DELETE` para **corregir y estandarizar** los datos.
3.  Utilizar técnicas de `GROUP BY` y `window functions` (opcional) para **identificar y eliminar duplicados**.
4.  Crear una nueva tabla limpia a partir de la tabla sucia, demostrando un proceso de transformación de datos repetible.

#### ** Herramientas y Entorno**
*   Docker, PostgreSQL y DBeaver.
*   El contenedor de base de datos debe estar en ejecución.

---

### **Procedimiento Paso a Paso**

#### **Fase 1: Preparación y Carga de Datos "Sucios" (~30 min)**

1.  Abre DBeaver, conéctate a tu base de datos y abre un nuevo Editor de SQL.
2.  Ejecuta el siguiente script para crear la tabla `cosecha_mensual_crudo` y poblarla con datos que contienen problemas de calidad deliberados.

    ```sql
    -- ===== INICIO DEL ESCENARIO: DATOS CRUDOS DE ANDESHARVEST =====

    DROP TABLE IF EXISTS cosecha_mensual_crudo;

    CREATE TABLE cosecha_mensual_crudo (
        id_registro INT,
        id_empleado VARCHAR(10),
        nombre_empleado VARCHAR(50),
        id_parcela VARCHAR(10),
        kilos_cosechados NUMERIC(5, 2),
        fecha_cosecha DATE
    );

    INSERT INTO cosecha_mensual_crudo VALUES
    (1, 'E-045', 'Ana Solis', 'P-07B', 15.20, '2024-06-01'),      -- Válido
    (2, 'E-012', 'Carlos Rojas', ' P-03A ', 22.50, '2024-06-01'), -- Problema: Espacios en parcela
    (3, NULL, 'Empleado Nuevo', 'P-01A', 18.10, '2024-06-02'),    -- Problema: id_empleado NULO
    (4, 'E-022', 'David Luna', 'p-07b', 25.00, '2024-06-02'),      -- Problema: Inconsistencia en parcela (minúscula)
    (5, 'E-045', 'Ana Solis', 'P-07B', 15.20, '2024-06-01'),      -- Problema: Registro DUPLICADO
    (6, 'E-077', 'Laura Paz', 'P-02B', -5.00, '2024-06-03'),       -- Problema: Kilos inválidos (negativo)
    (7, 'E-012', 'carlos rojas', 'P-03A', 19.80, '2024-06-03'),    -- Problema: Inconsistencia en nombre (minúscula)
    (8, 'E-099', 'Jose Salas', 'P-05C', 500.55, '2024-06-04');     -- Problema: Kilos outlier (posible error de tipeo)

    -- ===== FIN DEL ESCENARIO =====
    ```
3.  Ejecuta `SELECT * FROM cosecha_mensual_crudo;` para familiarizarte con la tabla y sus problemas.

---

#### **Fase 2: Perfilado y Diagnóstico (~45 min)**

Tu primera tarea como analista es **cuantificar los problemas**. Escribe y ejecuta las siguientes consultas de perfilado y anota los resultados.

1.  **Diagnóstico de Completitud:** ¿Hay registros con `id_empleado` nulo?
    ```sql
    -- Cuenta cuántos registros tienen el id_empleado nulo
    SELECT COUNT(*) FROM cosecha_mensual_crudo WHERE id_empleado IS NULL;
    ```

2.  **Diagnóstico de Validez:** ¿Hay valores ilógicos en `kilos_cosechados`?
    ```sql
    -- Encuentra los valores mínimo y máximo de kilos para detectar outliers
    SELECT MIN(kilos_cosechados), MAX(kilos_cosechados) FROM cosecha_mensual_crudo;
    ```

3.  **Diagnóstico de Consistencia:** ¿Cuántas variantes de `id_parcela` y `nombre_empleado` existen?
    ```sql
    -- Agrupa por id_parcela para ver las diferentes formas en que está escrito
    SELECT id_parcela, COUNT(*) FROM cosecha_mensual_crudo GROUP BY id_parcela;

    -- Agrupa por nombre_empleado para ver inconsistencias de mayúsculas/minúsculas
    SELECT nombre_empleado, COUNT(*) FROM cosecha_mensual_crudo GROUP BY nombre_empleado;
    ```

4.  **Diagnóstico de Unicidad:** ¿Hay registros completamente duplicados?
    ```sql
    -- Agrupa por todas las columnas y cuenta. Los que tengan un conteo > 1 son duplicados.
    SELECT id_registro, id_empleado, fecha_cosecha, COUNT(*)
    FROM cosecha_mensual_crudo
    GROUP BY id_registro, id_empleado, fecha_cosecha
    HAVING COUNT(*) > 1;
    ```

---

#### **Fase 3: Ejecución del Plan de Limpieza (~75 min)**

Ahora, escribe un script SQL que solucione los problemas encontrados. La mejor práctica es crear una nueva tabla limpia en lugar de modificar la original.

1.  **Crear la Tabla Limpia:** Primero, crea la estructura de tu tabla de destino.
    ```sql
    -- Crea una nueva tabla para los datos limpios
    CREATE TABLE cosecha_mensual_limpia AS
    SELECT * FROM cosecha_mensual_crudo WHERE 1=0; -- Copia la estructura, pero no los datos
    ```

2.  **Paso 1: Estandarizar Datos (Consistencia)**
    *   Usa `UPDATE` en la tabla `cosecha_mensual_crudo` para corregir las inconsistencias.
    *   **Acción:** Convierte todos los `id_parcela` a mayúsculas y quítales los espacios.
    *   **Acción:** Estandariza los nombres de los empleados (ej. `INITCAP` para poner la primera letra en mayúscula).

    ```sql
    -- Estandarizar id_parcela (mayúsculas y sin espacios)
    UPDATE cosecha_mensual_crudo SET id_parcela = UPPER(TRIM(id_parcela));

    -- Estandarizar nombre_empleado (primera letra en mayúscula)
    UPDATE cosecha_mensual_crudo SET nombre_empleado = INITCAP(nombre_empleado);
    ```

3.  **Paso 2: Eliminar Duplicados (Unicidad)**
    *   La mejor forma de eliminar duplicados exactos es usando `DELETE` con una subconsulta o una función de ventana. Aquí usaremos un método con `ctid` (específico de PostgreSQL).

    ```sql
    -- Eliminar filas duplicadas, conservando una
    DELETE FROM cosecha_mensual_crudo a
        USING cosecha_mensual_crudo b
    WHERE
        a.ctid < b.ctid
        AND a.id_registro = b.id_registro;
    ```

4.  **Paso 3: Transferir y Filtrar Datos Válidos**
    *   Ahora, inserta los datos desde la tabla cruda a la tabla limpia, pero **filtrando en el proceso** para excluir los datos que no se pueden reparar (los que tienen `NULL`s o valores ilógicos).

    ```sql
    -- Insertar en la tabla limpia solo los registros que cumplen las reglas de negocio
    INSERT INTO cosecha_mensual_limpia
    SELECT *
    FROM cosecha_mensual_crudo
    WHERE
        id_empleado IS NOT NULL                         -- Excluye nulos
        AND kilos_cosechados > 0                        -- Excluye negativos y ceros
        AND kilos_cosechados <= 50;                     -- Excluye outliers (basado en el límite de negocio)
    ```

---

#### **Fase 4: Verificación y Análisis Final (~30 min)**

1.  **Verificación:** Comprueba el contenido de tu nueva tabla limpia.
    ```sql
    -- Revisa el resultado final. Debería estar limpio y consistente.
    SELECT * FROM cosecha_mensual_limpia ORDER BY id_registro;
    ```
    > Deberías ver una tabla con solo 4 filas, todas válidas, consistentes y sin duplicados.

2.  **Análisis Final:** Ahora, con los datos limpios, puedes responder a la pregunta original del gerente.
    ```sql
    -- Generar el Reporte de Productividad solicitado
    SELECT
        id_empleado,
        nombre_empleado,
        SUM(kilos_cosechados) AS total_kilos_mes
    FROM
        cosecha_mensual_limpia
    GROUP BY
        id_empleado,
        nombre_empleado
    ORDER BY
        total_kilos_mes DESC;
    ```
    > Este es el reporte confiable que le entregarías al Gerente de Operaciones.

---

### **Entregable**

*   Un único archivo de texto (`limpieza_datos_andesharvest.sql`) que contenga **todo el script** que utilizaste en las Fases 2, 3 y 4.
*   El script debe estar documentado con comentarios (`--`) explicando qué hace cada sección (Perfilado, Estandarización, Carga Limpia, Análisis Final).
*   Sube el archivo `.sql` a la plataforma del curso.

---

### ** Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Perfilado y Diagnóstico (2 pts)** | No incluye o no ejecuta las consultas de perfilado. | Ejecuta las consultas, pero no demuestra comprensión de los resultados en sus comentarios. | Incluye y ejecuta correctamente las consultas de perfilado, y sus comentarios en el script demuestran que ha entendido los problemas de calidad encontrados. | / 2 |
| **Estandarización y Limpieza (4 pts)** | No logra corregir las inconsistencias o eliminar los duplicados. | Corrige algunos de los problemas (ej. mayúsculas) pero no todos, o la lógica para eliminar duplicados es incorrecta. | Aplica correctamente las funciones `UPDATE`, `TRIM`, `UPPER`/`INITCAP` para estandarizar los datos y utiliza un método válido para eliminar los registros duplicados. | / 4 |
| **Filtrado y Carga (3 pts)** | No logra transferir los datos a la tabla limpia o lo hace sin filtrar. | Transfiere los datos, pero la cláusula `WHERE` es incompleta y permite el paso de datos inválidos (ej. nulos u outliers). | Utiliza una sentencia `INSERT INTO ... SELECT` con una cláusula `WHERE` robusta que filtra correctamente **todos** los tipos de datos inválidos según el caso de estudio. | / 3 |
| **Análisis Final y Calidad del Script (1 pto)** | | El script funciona, pero está desordenado, sin comentarios y no incluye la consulta de análisis final. | El script está limpio, bien documentado, se ejecuta sin errores de principio a fin, e incluye la consulta final que genera el reporte de productividad solicitado. | / 1 |
| **Total**| | | | **/ 10** |
