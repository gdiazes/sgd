
### **Guía de Laboratorio 03 (Versión con Looker Studio): Dashboard de Calidad de Datos para "YapeGO"**

*   **Marco Conceptual:**
    El Gobierno de Datos no es solo responsabilidad de los ingenieros; los analistas juegan un rol crucial como la "primera línea de defensa". Su trabajo es utilizar herramientas de Business Intelligence para crear "Dashboards de Calidad de Datos" (Data Quality Dashboards). Estos reportes no miden el rendimiento del negocio (KPIs de ventas), sino la "salud" de los datos mismos. Permiten cuantificar el impacto de los problemas de calidad y priorizar los esfuerzos de corrección del equipo de ingeniería.

*   **Caso de Estudio:**
    Eres el Analista de Datos principal en la startup "YapeGO". El equipo de producto te ha alertado sobre posibles inconsistencias en los datos de la nueva funcionalidad "Recargas de Celular". Antes de que el equipo de ingeniería invierta tiempo en solucionarlo, la CEO (Data Owner) te pide un reporte visual y cuantitativo para entender la magnitud del problema.

    **Tu Misión:**
    Construir un dashboard en Looker Studio que responda a tres preguntas clave sobre la calidad de los datos de recargas:
    1.  **Impacto de las "Transacciones Fantasma":** ¿Qué porcentaje de nuestras transacciones y de nuestro dinero recaudado está asociado a un `numero_celular` desconocido (`NULL`)?
    2.  **Fragmentación de "Operadores":** ¿Cuántos operadores diferentes tenemos registrados? ¿Cuáles son los válidos y cuáles son "ruido"?
    3.  **Análisis de "Montos Inválidos":** ¿Qué porcentaje de las transacciones se ha realizado con montos que no ofrecemos (fuera de S/ 5, 10, 15, 20)?

*   **Objetivos del Desafío:**
    1.  Utilizar Looker Studio para conectarse a un conjunto de datos con problemas de calidad.
    2.  Crear campos calculados (`CASE`) para clasificar los datos en "Válidos" e "Inválidos" según las reglas de negocio.
    3.  Usar tablas y gráficos para cuantificar el número y el impacto monetario de los datos de baja calidad.
    4.  Diseñar un dashboard claro y conciso que comunique eficazmente los problemas de calidad de datos a una audiencia de negocio.

*   **Herramientas y Datos:**
    *   **Software:** Una cuenta de Google (para Google Sheets y Looker Studio).
    *   **Dataset:** `recargas_yapego_sucio.csv`. [**📥 Descarga el archivo aquí**](https://gist.githubusercontent.com/braulio-arteaga/9f38c3327d420f865f576e3381e4b868/raw/c26b7189f783109a962a938c4710178fc3ef995a/recargas_yapego_sucio.csv).
        *(Este CSV contiene 1000 registros con los problemas de calidad descritos en el caso)*.

*   **Procedimiento y Tareas a Desarrollar:**

    **Fase 1: Preparación y Conexión (~30 min)**
    1.  **Carga los Datos a Google Sheets:**
        *   Crea una nueva hoja de cálculo en Google Sheets y nómbrala **"Fuente - Recargas YapeGO"**.
        *   Importa el archivo `recargas_yapego_sucio.csv`.
    2.  **Conecta Looker Studio:**
        *   Crea un nuevo informe en Looker Studio.
        *   Conecta la hoja de cálculo que acabas de crear como tu fuente de datos.
        *   Verifica que los tipos de datos sean correctos (especialmente `monto` como Moneda y `fecha_hora` como Fecha y Hora).

    **Fase 2: Creación de Campos Calculados para Auditoría (~60 min)**
    Esta es la fase más importante. Crearemos nuevas dimensiones que nos permitirán clasificar cada registro.

    1.  **Campo 1: `Estado_Numero_Celular`**
        *   En el panel de "Datos", haz clic en "Añadir un campo".
        *   **Nombre:** `Estado_Numero_Celular`
        *   **Fórmula:**
            ```sql
            CASE
                WHEN numero_celular IS NULL THEN "Inválido (Nulo)"
                ELSE "Válido"
            END
            ```
        *   Haz clic en "Guardar".

    2.  **Campo 2: `Estado_Operador`**
        *   Añade otro campo.
        *   **Nombre:** `Estado_Operador`
        *   **Fórmula:**
            ```sql
            CASE
                WHEN UPPER(operador) IN ("CLARO", "MOVISTAR", "ENTEL", "BITEL") THEN "Válido"
                ELSE "Inválido"
            END
            ```
        > *Nota: Usamos `UPPER()` para manejar casos como 'movistar' en minúsculas y considerarlo válido.*

    3.  **Campo 3: `Estado_Monto`**
        *   Añade un tercer campo.
        *   **Nombre:** `Estado_Monto`
        *   **Fórmula:**
            ```sql
            CASE
                WHEN monto IN (5, 10, 15, 20) THEN "Válido"
                ELSE "Inválido"
            END
            ```

    **Fase 3: Construcción del Dashboard de Calidad de Datos (~90 min)**
    Ahora, usa tus nuevos campos para construir las visualizaciones.

    1.  **Título del Dashboard:** "Reporte de Calidad de Datos - Recargas de Celular".

    2.  **Sección 1: Análisis de "Transacciones Fantasma"**
        *   **Gráfico Circular:**
            *   **Dimensión:** `Estado_Numero_Celular`
            *   **Métrica:** `Record Count` (Conteo de registros)
            *   **Título del Gráfico:** "% de Transacciones por Validez de Celular"
        *   **Tabla:**
            *   **Dimensión:** `Estado_Numero_Celular`
            *   **Métrica 1:** `Record Count`
            *   **Métrica 2:** `monto` (con agregación `SUM`)
            *   **Título de la Tabla:** "Impacto Total de Celulares Nulos"
        > *Insight esperado: Verás qué porcentaje de transacciones son "fantasma" y cuánto dinero representan.*

    3.  **Sección 2: Análisis de "Operadores"**
        *   **Tabla:**
            *   **Dimensión:** `operador`
            *   **Dimensión 2 (opcional):** `Estado_Operador`
            *   **Métrica:** `Record Count`
            *   **Orden:** `Record Count` (descendente)
            *   **Título de la Tabla:** "Distribución de Operadores Registrados"
        > *Insight esperado: Podrás ver la lista completa de todos los valores únicos de operadores, identificando fácilmente los válidos y los que son "ruido".*

    4.  **Sección 3: Análisis de "Montos Inválidos"**
        *   **Gráfico de Barras:**
            *   **Dimensión:** `Estado_Monto`
            *   **Métrica:** `Record Count`
            *   **Título del Gráfico:** "Conteo de Transacciones por Validez de Monto"
        *   **Tarjeta de Resultados (Scorecard):**
            *   **Métrica:** `monto` (con agregación `SUM`)
            *   **Añade un Filtro a este gráfico:** En la configuración de la tarjeta, baja hasta "Filtro" -> "Añadir un filtro". Crea un filtro donde `Estado_Monto` sea exactamente `Inválido`.
            *   **Título de la Tarjeta:** "Suma Total de Montos Inválidos"
        > *Insight esperado: Cuantificarás cuántas transacciones tienen montos erróneos y cuánto dinero está involucrado en esas transacciones.*

    5.  **Sección 4: Resumen Ejecutivo (Texto)**
        *   Añade un cuadro de texto en la parte superior del dashboard con 3 puntos clave que resuman tus hallazgos para la CEO.
        *   **Ejemplo:**
            > **Resumen Ejecutivo:**
            > 1.  El **XX%** de nuestras transacciones de recarga no tienen un número de celular asociado, representando **S/ YYY** en ingresos no atribuibles.
            > 2.  Hemos detectado **ZZ** operadores inválidos, siendo los más comunes 'AT&T' y 'Verizon'.
            > 3.  El **WW%** de las recargas se realizaron con montos no ofrecidos, lo que indica un posible error en la app.

*   **Entregable:**
    *   El **enlace público (solo vista)** a tu dashboard de Looker Studio. Asegúrate de que el dashboard sea claro, profesional y responda a las tres preguntas del caso de estudio.

*   **Rúbrica de Evaluación (10 Puntos):**

| Criterio | **Inaceptable (0-1 pts)** | **Mejorable (2 pts)** | **Satisfactorio (3-4 pts)** | Puntos |
| :--- | :--- | :--- | :--- | :--- |
| **Campos Calculados (4 pts)** | No crea los campos calculados o la lógica es incorrecta. | Crea algunos de los campos, pero con errores lógicos que afectan el análisis (ej. no usa `UPPER` para operadores). | Crea los **tres** campos calculados (`Estado_Numero_Celular`, `Estado_Operador`, `Estado_Monto`) con la lógica `CASE` correcta y funcional para la auditoría. | / 4 |
| **Visualización de Calidad (4 pts)** | Los gráficos son confusos, no responden a las preguntas del caso o están mal configurados. | Crea algunas visualizaciones, pero no logran cuantificar claramente el impacto de los problemas de calidad (ej. falta el impacto monetario). | Utiliza una combinación efectiva de gráficos y tablas para **cuantificar y visualizar claramente** el impacto de cada uno de los tres problemas de calidad de datos, tanto en número de registros como en monto. | / 4 |
| **Comunicación y Diseño (2 pts)** | El dashboard es desordenado y no comunica los hallazgos. | El dashboard es funcional, pero carece de títulos, etiquetas claras o un resumen ejecutivo que explique los resultados a una audiencia de negocio. | El dashboard está bien diseñado, es fácil de leer y el **Resumen Ejecutivo** sintetiza de forma clara y cuantitativa los principales problemas de calidad de datos encontrados. | / 2 |
| **Total** | | | | **/ 10** |
