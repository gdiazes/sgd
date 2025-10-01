### **Guía de Laboratorio 02**

#### **Guía de Laboratorio 02: Creando el Primer Dashboard Ejecutivo para FrutiFresh**

*   **Marco Conceptual:**
    Las empresas modernas no consumen datos en tablas estáticas, sino a través de dashboards interactivos. Looker Studio es una herramienta líder de Business Intelligence (BI) que permite conectar diversas fuentes de datos y crear reportes visuales. En este laboratorio, actuarás como Analista de BI para "FrutiFresh". Tu misión es transformar el CSV de ventas crudas en un dashboard ejecutivo que permita a la CEO explorar los datos y entender el rendimiento del negocio de un vistazo.

*   **Caso de Estudio:**
    La CEO de "FrutiFresh" está impresionada con el análisis inicial, pero lo encuentra estático. Su nueva petición es: **"Necesito un dashboard interactivo que pueda consultar todos los días. Quiero ver nuestras métricas clave de un vistazo, poder filtrar por tienda y ver gráficamente cuáles son nuestros productos estrella. ¡Quiero jugar con los datos!"**

*   **Objetivos del Laboratorio:**
    1.  Conectar una fuente de datos (Google Sheets) a Looker Studio.
    2.  Crear tarjetas de resultados (Scorecards) para visualizar KPIs operacionales.
    3.  Construir gráficos de barras y circulares para el análisis estratégico.
    4.  Implementar controles de filtro para hacer el dashboard interactivo.
    5.  Diseñar un reporte limpio y profesional que cuente una historia.

*   **Herramientas y Datos:**
    *   **Software:** Una cuenta de Google (para acceder a Google Sheets y Looker Studio).
    *   **Dataset:** `ventas_frutifresh_mes1.csv`.

---

### **Procedimiento Detallado Paso a Paso**

#### **Fase 1: Preparación de la Fuente de Datos**

Looker Studio funciona mejor cuando la fuente de datos está limpia y preparada.

1.  **Carga los Datos a Google Sheets:**
    *   Crea una nueva hoja de cálculo en Google Sheets y nómbrala **"Fuente de Datos - FrutiFresh"**.
    *   Importa el archivo `ventas_frutifresh_mes1.csv` en la primera hoja.
    *   **Paso Crítico:** Crea la columna `Ingreso_Transaccion`. En la celda `H1` escribe el título y en la `H2` la fórmula `=E2*F2`. Arrastra la fórmula hasta el final.
    *   **Verificación:** Asegúrate de que las cabeceras de las columnas (`A1` a `H1`) sean claras y no tengan espacios extra.

#### **Fase 2: Conexión y Configuración en Looker Studio**

1.  **Accede a Looker Studio:**
    *   Ve a [lookerstudio.google.com](https://lookerstudio.google.com/) e inicia sesión con tu cuenta de Google.

2.  **Crea un Nuevo Reporte:**
    *   Haz clic en **"Informe vacío"** o en el botón grande con un "+".

3.  **Conecta tu Fuente de Datos:**
    *   Looker Studio te pedirá que añadas datos al informe. En el panel de conectores, selecciona **"Hojas de cálculo de Google"**.
    *   Busca y selecciona el archivo **"Fuente de Datos - FrutiFresh"** que acabas de crear.
    *   Asegúrate de que la opción **"Usar la primera fila como encabezados"** esté marcada.
    *   Haz clic en el botón **"Añadir"** en la esquina inferior derecha. Te aparecerá un aviso, haz clic en **"Añadir al informe"**.

4.  **Verifica los Tipos de Datos:**
    *   Serás llevado al editor del informe. A la derecha, verás el panel de "Datos" con todas las columnas de tu hoja.
    *   Looker Studio es bueno detectando tipos, pero siempre hay que verificar. Asegúrate de que:
        *   `Precio_Unitario` e `Ingreso_Transaccion` tengan el tipo `Number` o `Currency`.
        *   `Fecha_Hora` tenga el tipo `Date & Time`.
        *   `Cantidad` sea de tipo `Number`.
    > ![Placeholder para Imagen 2.1: Captura de pantalla del panel de Datos en Looker Studio, mostrando los campos y sus tipos de datos (Fecha, Texto, Número).]

#### **Fase 3: Construcción del Dashboard Operacional**

Vamos a construir la sección de KPIs (Indicadores Clave de Rendimiento).

1.  **Añade un Título:**
    *   Usa la herramienta de "Texto" (icono `A`) para añadir un título en la parte superior del lienzo: **"Dashboard Ejecutivo - FrutiFresh Mes 1"**.

2.  **Crea Tarjetas de Resultados (Scorecards):**
    *   Ve a "Añadir un gráfico" -> "Tarjeta de resultados".
    *   **KPI 1: Ingresos Totales:**
        *   Coloca la tarjeta en el dashboard. Por defecto, mostrará "Record Count".
        *   En el panel de configuración de la derecha, arrastra el campo `Ingreso_Transaccion` al área de "Métrica". Asegúrate de que la agregación sea `SUM`.
        *   En la pestaña "Estilo", puedes cambiar el tamaño de la fuente y añadir un borde.
    *   **KPI 2: Cantidad Total de Productos Vendidos:**
        *   Copia y pega la tarjeta anterior.
        *   En la nueva tarjeta, cambia la "Métrica" a `Cantidad`.
    *   **KPI 3: Número de Transacciones:**
        *   Copia y pega de nuevo.
        *   Cambia la "Métrica" a `ID_Transaccion`. Cambia la agregación a `COUNT_DISTINCT` para asegurarte de contar cada transacción una sola vez.

    > ![Placeholder para Imagen 2.2: Captura de pantalla del dashboard con las tres tarjetas de resultados (KPIs) alineadas en la parte superior.]

#### **Fase 4: Construcción de Visualizaciones Estratégicas**

Ahora, vamos a responder las preguntas estratégicas con gráficos.

1.  **Crea un Gráfico de Barras - Ingresos por Producto:**
    *   Ve a "Añadir un gráfico" -> "Gráfico de barras".
    *   Colócalo en el lienzo.
    *   **Configuración:**
        *   **Dimensión:** `Nombre_Producto`
        *   **Métrica:** `Ingreso_Transaccion` (con agregación `SUM`)
        *   **Orden:** `Ingreso_Transaccion` (descendente).
    *   ¡Ahora puedes ver visualmente qué producto genera más ingresos!

2.  **Crea un Gráfico Circular - Unidades Vendidas por Producto:**
    *   Ve a "Añadir un gráfico" -> "Gráfico circular".
    *   Colócalo al lado del gráfico de barras.
    *   **Configuración:**
        *   **Dimensión:** `Nombre_Producto`
        *   **Métrica:** `Cantidad` (con agregación `SUM`)
    *   Este gráfico te mostrará la proporción de unidades vendidas por cada producto. Compara este resultado con el gráfico de barras. ¿El producto más vendido es el más rentable?

3.  **Crea una Serie Temporal - Ventas a lo Largo del Tiempo:**
    *   Ve a "Añadir un gráfico" -> "Serie temporal".
    *   Colócalo debajo de los KPIs.
    *   **Configuración:**
        *   **Dimensión de Tiempo:** `Fecha_Hora` (Puedes hacer clic en el lápiz y cambiar el tipo a "Fecha" para agrupar por día).
        *   **Métrica:** `Ingreso_Transaccion` (con agregación `SUM`)
    *   Este gráfico te mostrará las tendencias de ventas diarias a lo largo del mes.

    > ![Placeholder para Imagen 2.3: Captura de pantalla del dashboard completo, mostrando el título, los KPIs y los tres gráficos (barras, circular y serie temporal).]

#### **Fase 5: Añadiendo Interactividad**

Esta es la parte que le encantará a la CEO.

1.  **Añade un Control de Filtro por Tienda:**
    *   Ve a "Añadir un control" -> "Lista desplegable".
    *   Colócalo en una esquina superior del dashboard.
    *   **Configuración:**
        *   **Campo de control:** `ID_Tienda`
    *   Ahora, sal del modo "Edición" y entra en el modo **"Ver"** (botón en la esquina superior derecha).
    *   Haz clic en el filtro. Selecciona `T01`. ¡Observa cómo todo el dashboard se actualiza para mostrar solo los datos de esa tienda! Selecciona `T02` y verás cómo cambian de nuevo los datos.

---

### **Entregable**

1.  En la esquina superior derecha de tu dashboard en Looker Studio, haz clic en el botón **"Compartir"**.
2.  Cambia la configuración de acceso del enlace de "Restringido" a **"Cualquier persona con el enlace puede ver"**.
3.  Copia el enlace.
4.  **Entrega el enlace a tu dashboard de Looker Studio** en la plataforma del curso. El instructor podrá acceder a tu reporte interactivo y evaluarlo.

---
