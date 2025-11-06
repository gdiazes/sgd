### **Guía de Laboratorio 07 (Avanzado): Optimizando el Dashboard de "FrutiFresh"**

#### **Marco Conceptual**

La optimización de consultas no termina con la creación de un índice simple en una columna. Las aplicaciones del mundo real ejecutan una variedad de consultas complejas: búsquedas por múltiples campos, ordenamiento, búsquedas de texto y filtros por rango de fechas. Un Ingeniero de Rendimiento de Datos debe saber elegir la estrategia de indexación correcta para cada escenario. En este laboratorio, analizarás varias consultas lentas del nuevo dashboard de "FrutiFresh" y aplicarás técnicas de indexación avanzada, como **índices compuestos** y **índices en funciones**, para optimizarlas.

#### **Caso de Estudio**

"FrutiFresh" ha lanzado su app de lealtad y está recolectando miles de datos de clientes. El equipo de marketing ha construido un dashboard en Looker Studio para analizar el comportamiento del cliente, pero se quejan de que varios filtros y gráficos son extremadamente lentos y a menudo "dan timeout".

**Reporte de Problemas del Equipo de Marketing:**
1.  **"Filtro de Nombre y Apellido Lento":** "Cuando buscamos un cliente por su nombre Y su apellido exactos, la búsqueda tarda demasiado."
2.  **"Búsqueda por Email Ineficiente":** "Habilitamos una barra de búsqueda para encontrar clientes por su email, pero es muy lenta, incluso si el email está en minúsculas en la base de datos y el usuario escribe en mayúsculas."
3.  **"Gráfico de Registros por Mes se Congela":** "Tenemos un gráfico que muestra cuántos clientes se registraron cada mes. Al cargar, la base de datos parece morir."

Tu misión es tomar el rol de DBA/Ingeniero de Datos, diagnosticar cada uno de estos problemas con `EXPLAIN ANALYZE` y aplicar la estrategia de indexación correcta para solucionarlos.

#### **Objetivos del Laboratorio**

1.  Diagnosticar el rendimiento de consultas con múltiples condiciones en la cláusula `WHERE`.
2.  Implementar un **índice compuesto (multi-columna)** y entender su importancia.
3.  Implementar un **índice funcional (expression index)** para optimizar búsquedas insensibles a mayúsculas/minúsculas.
4.  Comprender cómo los índices pueden acelerar operaciones de agregación (`GROUP BY`) sobre funciones de fecha.

#### **Herramientas y Entorno**
*   PostgreSQL y DBeaver.
  

---

### **Procedimiento del Desafío**

#### **Fase 1: Preparación del Escenario (~30 min)**

1.  Abre DBeaver y un nuevo Editor de SQL.
2.  Ejecuta el siguiente script para crear una tabla `clientes_lealtad` con **1 millón de registros**.

    ```sql
    -- ===== INICIO DEL ESCENARIO: TABLA DE CLIENTES DE FRUTIFRESH =====

    DROP TABLE IF EXISTS clientes_lealtad;

    CREATE TABLE clientes_lealtad (
        id_cliente SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        fecha_registro TIMESTAMP NOT NULL
    );

    -- Insertamos 1 millón de clientes. Puede tardar 1-3 minutos.
    INSERT INTO clientes_lealtad (nombre, apellido, email, fecha_registro)
    SELECT
        'Nombre' || n,
        'Apellido' || (n % 10000), -- Genera apellidos repetidos para que la búsqueda sea selectiva
        'cliente' || n || '@email.com',
        NOW() - (RANDOM() * 365 * 2 || ' days')::interval -- Fechas en los últimos 2 años
    FROM generate_series(1, 1000000) AS n;

    -- Añadimos un cliente específico para nuestras pruebas
    INSERT INTO clientes_lealtad (nombre, apellido, email, fecha_registro)
    VALUES ('Ana', 'Solis', 'ana.solis@email.com', NOW());

    -- ===== FIN DEL ESCENARIO =====
    ```
3.  Verifica el tamaño de la tabla con `SELECT COUNT(*) FROM clientes_lealtad;`.

---

#### **Fase 2: Desafío 1 - El Filtro de Nombre y Apellido (~45 min)**

1.  **Diagnóstico:** Ejecuta el `EXPLAIN ANALYZE` para la consulta que busca por nombre y apellido.
    ```sql
    EXPLAIN ANALYZE SELECT * FROM clientes_lealtad
    WHERE nombre = 'Ana' AND apellido = 'Solis';
    ```
    *   **Observa:** Verás un `Seq Scan`. La base de datos lee el millón de filas. Anota el tiempo de ejecución.

2.  **Solución Incorrecta (Intento 1):** Un desarrollador junior podría pensar en crear dos índices separados. Hagámoslo para ver qué pasa.
    ```sql
    CREATE INDEX idx_clientes_nombre ON clientes_lealtad (nombre);
    CREATE INDEX idx_clientes_apellido ON clientes_lealtad (apellido);
    ```
3.  **Verificación 1:** Vuelve a ejecutar el `EXPLAIN ANALYZE`.
    *   **Observa:** PostgreSQL *podría* usar uno de los índices (probablemente el de apellido, si es más selectivo) o combinarlos con un `Bitmap And`, pero el rendimiento no será óptimo. Compara el tiempo de ejecución. Será mejor, pero no ideal.

4.  **Solución Correcta (Intento 2): El Índice Compuesto**
    *   Un índice compuesto indexa múltiples columnas juntas, en un orden específico. Es perfecto para consultas que filtran por esas mismas columnas.
    *   Primero, limpiemos los índices anteriores: `DROP INDEX idx_clientes_nombre; DROP INDEX idx_clientes_apellido;`
    *   Ahora, crea el índice correcto:
    ```sql
    CREATE INDEX idx_clientes_nombre_apellido ON clientes_lealtad (nombre, apellido);
    ```
5.  **Verificación Final:** Ejecuta el `EXPLAIN ANALYZE` por última vez.
    *   **Observa:** El plan ahora debería usar un `Index Scan` sobre `idx_clientes_nombre_apellido`. El tiempo de ejecución debería ser de **sub-milisegundos**. ¡Problema resuelto!

---

#### **Fase 3: Desafío 2 - La Búsqueda por Email (~45 min)**

1.  **Diagnóstico:** El problema es que los usuarios buscan sin importar mayúsculas/minúsculas. La consulta usa la función `LOWER()`.
    ```sql
    EXPLAIN ANALYZE SELECT * FROM clientes_lealtad
    WHERE LOWER(email) = 'ana.solis@email.com';
    ```
    *   **Observa:** Verás un `Seq Scan`. Un índice normal sobre la columna `email` **no sirve** porque la base de datos tiene que aplicar la función `LOWER()` a cada una del millón de filas antes de poder comparar.

2.  **Solución: El Índice Funcional (Expression Index)**
    *   Podemos crear un índice no sobre la columna en sí, sino sobre el **resultado de una función** aplicada a la columna.
    ```sql
    CREATE INDEX idx_clientes_email_lower ON clientes_lealtad (LOWER(email));
    ```

3.  **Verificación:** Vuelve a ejecutar el `EXPLAIN ANALYZE` de este desafío.
    *   **Observa:** El plan ahora usará un `Index Scan` sobre nuestro nuevo índice `idx_clientes_email_lower`. La consulta será casi instantánea.

---

#### **Fase 4: Desafío 3 - El Gráfico de Registros por Mes (~45 min)**

1.  **Diagnóstico:** La consulta para el gráfico agrupa por mes. La función `DATE_TRUNC('month', ...)` se aplica a cada fila.
    ```sql
    EXPLAIN ANALYZE SELECT DATE_TRUNC('month', fecha_registro)::DATE AS mes, COUNT(*)
    FROM clientes_lealtad
    GROUP BY mes
    ORDER BY mes;
    ```
    *   **Observa:** Verás un `Seq Scan`. La base de datos debe leer el millón de fechas, truncar cada una, y luego agruparlas.

2.  **Solución:** Al igual que en el desafío anterior, podemos crear un índice sobre la expresión que usamos para agrupar.
    ```sql
    CREATE INDEX idx_clientes_fecha_registro_month ON clientes_lealtad (DATE_TRUNC('month', fecha_registro));
    ```

3.  **Verificación:** Ejecuta el `EXPLAIN ANALYZE` de nuevo.
    *   **Observa:** El plan de ejecución cambiará. En lugar de un `Seq Scan` seguido de un `GroupAggregate`, PostgreSQL puede usar una estrategia mucho más rápida que lee los datos ya agrupados directamente desde el índice (`Index Only Scan` o similar), evitando leer la tabla principal por completo. La mejora en el rendimiento será muy significativa.

---

### **Entregable**

Un único archivo de texto (`reporte_optimizacion_avanzado.txt`) que contenga:
1.  **Para cada uno de los 3 desafíos:**
    *   El `EXPLAIN ANALYZE` inicial (el del problema).
    *   El comando `CREATE INDEX` que usaste como solución.
    *   El `EXPLAIN ANALYZE` final (el que demuestra la mejora).
    *   Una línea resumiendo el cambio en el tiempo de ejecución.
2.  **Una sección final de "Conclusiones"** donde expliques brevemente en tus propias palabras la diferencia entre un índice simple, un índice compuesto y un índice funcional.

---

### **Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Resolución del Índice Compuesto (3 pts)** | No resuelve el problema o usa solo índices simples. | Resuelve el problema con índices simples, pero no implementa el índice compuesto. | Diagnostica, implementa correctamente el **índice compuesto** y verifica la mejora con `EXPLAIN ANALYZE`. | / 3 |
| **Resolución del Índice Funcional (Email) (3 pts)** | No logra optimizar la consulta con `LOWER()`. | Intenta crear un índice normal sobre `email`, lo cual no resuelve el problema. | Diagnostica, implementa correctamente el **índice funcional** sobre `LOWER(email)` y verifica la mejora. | / 3 |
| **Resolución del Índice Funcional (Fecha) (3 pts)** | No logra optimizar la consulta con `GROUP BY`. | Intenta crear un índice normal sobre `fecha_registro`, lo cual tiene un impacto limitado. | Diagnostica, implementa correctamente el **índice funcional** sobre `DATE_TRUNC()` y verifica la mejora significativa en la agregación. | / 3 |
| **Análisis y Conclusiones (1 pto)** | | El reporte está incompleto o las conclusiones son incorrectas/inexistentes. | El reporte está completo, bien estructurado y la sección de **Conclusiones** explica de forma clara y correcta los diferentes tipos de índices utilizados. | / 1 |
| **Total**| | | | **/ 10** |
