### **Guía de Laboratorio: Diseño del Esquema de Base de Datos para "FrutiFresh Lealtad"**

#### ** Marco Conceptual**

El modelado de datos es el proceso de traducir los requisitos de un negocio en una estructura de base de datos técnica, eficiente y escalable. En este desafío, actuarás como el **Arquitecto de Datos** de la startup "FrutiFresh". Tu tarea es diseñar y crear el esquema físico de la base de datos para su nuevo "Programa de Lealtad", escribiendo el script SQL completo que dará vida al sistema.

#### ** Caso de Estudio: El Lanzamiento del Programa "FrutiFresh Lealtad"**

La CEO de FrutiFresh quiere lanzar un programa de lealtad para fidelizar a sus clientes. El sistema debe permitir registrar a los clientes, llevar un conteo de sus puntos y permitirles canjear esos puntos por productos.

**Requisitos de Negocio (definidos por la CEO):**
1.  **Registro de Clientes:** "Necesitamos una forma de registrar a nuestros clientes. Quiero guardar su nombre, apellido, email y fecha de nacimiento. Cada cliente debe tener un ID único que generaremos nosotros."
2.  **Acumulación de Puntos:** "Por cada sol gastado en nuestras tiendas, el cliente gana 1 punto. Necesitamos registrar cada vez que un cliente acumula puntos en una transacción."
3.  **Canje de Recompensas:** "Tendremos un catálogo de 'recompensas' (ej. 'Jugo Gratis', 'Descuento 50%'). Quiero saber qué cliente canjeó qué recompensa y en qué fecha."
4.  **Reglas de Integridad:**
    *   Un cliente puede realizar muchas transacciones de acumulación de puntos.
    *   Un cliente puede realizar muchos canjes de recompensas.
    *   Una recompensa del catálogo puede ser canjeada por muchos clientes.
    *   **¡Crucial!** No se puede registrar una acumulación de puntos o un canje para un cliente que no existe. Tampoco se puede canjear una recompensa que no está en nuestro catálogo.

#### ** Objetivos del Desafío**

1.  Interpretar un conjunto de requisitos de negocio para diseñar un modelo de datos relacional.
2.  Escribir un script SQL utilizando sentencias `CREATE TABLE` para implementar el modelo físico en PostgreSQL.
3.  Definir correctamente las **Claves Primarias (PRIMARY KEY)** para cada tabla.
4.  Implementar las relaciones lógicas entre las tablas utilizando **Claves Foráneas (FOREIGN KEY)**.
5.  Aplicar `NOT NULL` y `CHECK constraints` para hacer cumplir las reglas de negocio básicas.

#### ** Herramientas y Entorno**
*   Cualquier editor de texto para escribir el script SQL (VS Code, Sublime Text, Bloc de notas).
*   **(Opcional pero recomendado)** Docker, PostgreSQL y DBeaver para probar que el script se ejecuta correctamente.

---

### **Tu Misión: El Diseño del Esquema**

Tu tarea es diseñar la estructura de la base de datos para el programa "FrutiFresh Lealtad". Después de analizar los requisitos, has determinado que necesitas **cuatro tablas principales**:

1.  **Tabla `clientes`**
    *   **Propósito:** Almacenar la información de los miembros del programa de lealtad.
    *   **Columnas sugeridas:** `id_cliente`, `nombre`, `apellido`, `email`, `fecha_nacimiento`.

2.  **Tabla `transacciones_puntos`**
    *   **Propósito:** Registrar cada vez que un cliente gana puntos.
    *   **Columnas sugeridas:** `id_transaccion`, `id_cliente` (para saber quién ganó los puntos), `monto_compra`, `puntos_ganados`, `fecha_transaccion`.

3.  **Tabla `catalogo_recompensas`**
    *   **Propósito:** Mantener la lista de recompensas disponibles para canjear.
    *   **Columnas sugeridas:** `id_recompensa`, `nombre_recompensa`, `puntos_requeridos`.

4.  **Tabla `canjes_recompensas`**
    *   **Propósito:** Registrar cada vez que un cliente usa sus puntos para canjear una recompensa.
    *   **Columnas sugeridas:** `id_canje`, `id_cliente` (quién canjeó), `id_recompensa` (qué canjeó), `fecha_canje`.

**Desafío Clave de Diseño:**
*   Identifica qué columnas deben ser las Claves Primarias de cada tabla.
*   Identifica dónde deben ir las Claves Foráneas para conectar las tablas correctamente y cumplir con las reglas de integridad.
*   Decide qué columnas no pueden ser nulas (`NOT NULL`).
*   Añade al menos una restricción `CHECK` (ej. los puntos o montos no pueden ser negativos).

---

### **Entregable**

*   Un único archivo de texto (`esquema_lealtad_frutifresh.sql`) que contenga tu script completo con las **cuatro sentencias `CREATE TABLE`**.
*   El script debe estar **ordenado lógicamente** (no puedes crear una tabla que hace referencia a otra si esta última aún no existe).
*   Utiliza comentarios en tu script SQL (`-- comentario`) para explicar brevemente el propósito de cada tabla o de una restricción importante.

---

### ** Rúbrica de Evaluación (10 Puntos)**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Creación de Tablas y PK (3 pts)** | El script tiene errores de sintaxis graves. No crea las 4 tablas o las PK están mal definidas/ausentes. | Crea la mayoría de las tablas, pero con errores en la definición de las Claves Primarias o tipos de datos inadecuados. | Las cuatro tablas se crean correctamente con `CREATE TABLE`. Todas las Claves Primarias están definidas de forma correcta y única para cada tabla. | / 3 |
| **Implementación de FK (4 pts)** | No se implementan las Claves Foráneas o las relaciones son incorrectas. | Implementa algunas de las relaciones con FK, pero comete errores en la sintaxis `REFERENCES` o en la lógica de la relación. | Todas las relaciones lógicas (`clientes`->`transacciones`, `clientes`->`canjes`, etc.) se implementan correctamente usando `FOREIGN KEY constraints` en las tablas correctas. | / 4 |
| **Aplicación de Constraints (2 pts)** | No se utilizan `NOT NULL` o `CHECK` constraints. | Se aplican algunos `constraints`, pero de forma inconsistente o sin cumplir todos los requisitos del negocio. | Se aplican correctamente todos los `NOT NULL` constraints necesarios (ej. en nombres, emails) y al menos un `CHECK` constraint lógico (ej. puntos > 0). | / 2 |
| **Calidad y Documentación del Script (1 pto)** | | El script funciona, pero no tiene comentarios y el orden de creación es ilógico o casual. | El script es limpio, está bien organizado (tablas "padre" primero), se puede ejecutar sin errores y está documentado con comentarios que explican el propósito de cada tabla. | / 1 |
| **Total**| | | | **/ 10** |
