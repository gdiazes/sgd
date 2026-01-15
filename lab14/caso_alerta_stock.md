
# PROYECTO HIDRA: Centralización de Retail Analytics
**Metodología:** Scrum para DataOps
**Equipo:** 5 Integrantes
**Tech Stack:** Python, Google Sheets API, Google Looker Studio.

---

## 1. El Escenario (Contexto del Proyecto)
La empresa "ModaFast" tiene **50 tiendas**. Cada gerente reporta sus ventas y stock diariamente en archivos aislados (simulados). La dirección necesita un **Dashboard Centralizado** que se actualice automáticamente, limpie los errores humanos y prediga roturas de **stock**.

### El Equipo Scrum (Roles Adaptados)
1.  **Ana (Product Owner):** Define las reglas de negocio (ej. "¿Qué hacemos con ventas negativas?"). Valida el Dashboard final.
2.  **Carlos (Scrum Master / Lead):** Gestiona los bloqueos técnicos (APIs, permisos) y facilita las ceremonias.
3.  **David (Data Engineer):** Construye el "Robot" (Script Python) que unifica los 50 archivos en una fuente maestra.
4.  **Beatriz (Data Scientist):** Implementa lógica de limpieza avanzada y detección de anomalías en el código Python.
5.  **Elena (Data Analyst / BI):** Diseña la experiencia visual en Looker Studio y optimiza el rendimiento del reporte.

---

## 2. Fase de Preparación: Generación de Datos (Sprint 0)

Antes de analizar, necesitamos datos. Como estamos en fase de desarrollo, utilizaremos un script para simular el caos de las 50 tiendas (datos sucios, errores de tipeo, diferentes volúmenes).

**Instrucciones para el Data Engineer (David):**
Ejecuta este script en tu entorno local para generar la "Materia Prima".

```python
import pandas as pd
import random
import os
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
NUM_TIENDAS = 50
DIAS_HISTORIA = 30
OUTPUT_FOLDER = "datos_crudos_tiendas"

# Catálogo simulado
PRODUCTOS = ['Zapatilla Air', 'Bota Montaña', 'Sandalia Playa', 'Zapato Formal', 'Tenis Running']
PRECIOS = {'Zapatilla Air': 120, 'Bota Montaña': 150, 'Sandalia Playa': 30, 'Zapato Formal': 90, 'Tenis Running': 80}

# Crear carpeta de salida
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def generar_datos_tienda(id_tienda):
    data = []
    fecha_base = datetime.today()
    
    for dia in range(DIAS_HISTORIA):
        fecha = fecha_base - timedelta(days=dia)
        # Simulamos volumen de ventas aleatorio
        num_ventas = random.randint(0, 20)
        
        for _ in range(num_ventas):
            producto = random.choice(PRODUCTOS)
            cantidad = random.randint(1, 3)
            precio = PRECIOS[producto]
            
            # --- GENERADOR DE CAOS (Errores Humanos Simulados) ---
            # 1. Error de tipeo en el producto (Suciedad para el Data Scientist)
            if random.random() < 0.02: # 2% de probabilidad
                producto = "Zapa_Air_ERROR_TYPO" 
            
            # 2. Venta negativa (Error de dedo del gerente)
            if random.random() < 0.01: 
                cantidad = -1 
            
            # 3. Comentarios
            nota = "Todo OK" if random.random() > 0.1 else "URGENTE: Falta stock"
            
            data.append([fecha.strftime("%Y-%m-%d"), f"Tienda_{id_tienda}", producto, cantidad, precio, nota])

    # Crear DataFrame y guardar CSV individual
    df = pd.DataFrame(data, columns=['Fecha', 'ID_Tienda', 'Producto', 'Cantidad', 'Precio_Unitario', 'Notas'])
    nombre_archivo = f"{OUTPUT_FOLDER}/Reporte_Tienda_{id_tienda}.csv"
    df.to_csv(nombre_archivo, index=False)
    print(f"Generado: {nombre_archivo}")

# Ejecución
print("--- 🔨 GENERANDO ENTORNO DE DATOS DE 50 TIENDAS ---")
for i in range(1, NUM_TIENDAS + 1):
    generar_datos_tienda(i)
print(f"---  Proceso Terminado. Verifica la carpeta /{OUTPUT_FOLDER} ---")
```

---

## 3. Guía Paso a Paso del Sprint (Duración: 2 Semanas)

### Paso 1: Sprint Planning (Lunes, Semana 1)
**Sprint Goal:** "Automatizar la ingesta de las 50 tiendas, sanear los datos erróneos y publicar un Dashboard consolidado en Looker Studio".

**Estrategia de Arquitectura:**
*   **Incorrecto:** Conectar Looker Studio a los 50 CSVs individuales (Lento, propenso a fallos).
*   **Correcto:** Python lee 50 CSVs $\rightarrow$ Limpia y Une $\rightarrow$ Genera 1 archivo `MASTER_DATA.csv` (o sube a Google Sheet Maestro) $\rightarrow$ Looker Studio lee el Maestro.

**Backlog de Tareas (Asignación):**

| ID | Rol | Tarea | Descripción Técnica |
| :--- | :--- | :--- | :--- |
| **T-01** | **DE** | **Pipeline ETL (Unificación).** | Crear script `etl_processor.py` que itere sobre la carpeta, lea los 50 CSVs y cree un solo DataFrame. |
| **T-02** | **DS** | **Reglas de Calidad (Sanitización).** | Definir función Python para: 1) Convertir cantidades negativas a positivas (`abs()`). 2) Corregir "Zapa_Air_ERROR_TYPO" a "Zapatilla Air". |
| **T-03** | **DE** | **Automatización de Salida.** | El script debe exportar el resultado limpio a un `MASTER_CLEAN.csv` (o subirlo a Google Sheets vía API si hay credenciales). |
| **T-04** | **PO** | **Validación de Negocio.** | Definir rangos de alerta (ej. "¿Si una tienda vende 0 en 3 días, es alarma?"). |
| **T-05** | **BI** | **Configuración de Fuente de Datos.** | Conectar Looker Studio al `MASTER_CLEAN.csv`. Configurar tipos de datos (Fecha, Geo, Moneda). |
| **T-06** | **BI** | **Diseño de Dashboard.** | Crear filtros por Tienda y Gráficos de Tendencia Temporal. |

---

### Paso 2: Desarrollo y Daily Scrums (La Ejecución)

Durante los días de desarrollo, el equipo se enfrenta a la realidad de los datos generados.

**Día 3 - Problema de "Datos Sucios":**
*   **Beatriz (DS):** "El generador creó productos con nombres raros. Looker Studio va a mostrar eso feo."
*   **Solución (Pair Programming DE + DS):** Integran un diccionario de mapeo en el script ETL:
    ```python
    # Snippet de limpieza para la Tarea T-02
    mapping = {"Zapa_Air_ERROR_TYPO": "Zapatilla Air"}
    df['Producto'] = df['Producto'].replace(mapping)
    df['Cantidad'] = df['Cantidad'].abs() # Corregir negativos
    ```

**Día 7 - Optimización de Looker Studio:**
*   **Elena (BI):** "El reporte carga rápido porque ahora leo de un solo archivo maestro, no de 50. Voy a agregar un campo calculado para 'Ingresos Totales' (`Cantidad * Precio`)."
*   **Carlos (SM):** "Asegúrate de que el formato de fecha sea compatible. Looker prefiere `YYYYMMDD` o `YYYY-MM-DD`."

---

### Paso 3: Sprint Review (La Demo)

El equipo presenta el resultado a los Stakeholders (Gerentes Regionales simulados).

1.  **Elena proyecta Looker Studio:**
    *   Muestra un mapa de calor con las ventas de las 50 tiendas.
    *   Usa un filtro desplegable para seleccionar "Tienda_12".
    *   El gráfico se actualiza en < 2 segundos.
2.  **David explica el proceso:** "Ya no dependemos de abrir 50 Excels. El robot corre cada mañana y genera la vista limpia."
3.  **Ana (PO) destaca la calidad:** "Notarán que no hay ventas negativas en el reporte, el sistema las ha corregido automáticamente."

---

## 4. Definición de "Done" (DoD)

Para que una historia de usuario se considere terminada en este proyecto:

1.  **Código:** El script ETL está versionado en Git y comentado.
2.  **Calidad de Datos:** No existen valores `Null` en columnas críticas (Fecha, ID_Tienda, Producto). No hay cantidades negativas.
3.  **Visualización:**
    *   El Dashboard en Looker Studio carga en menos de 5 segundos.
    *   Los filtros funcionan correctamente (cross-filtering).
    *   Tiene fecha de "Última Actualización" visible.
4.  **Acceso:** El reporte es accesible mediante enlace compartido (permisos de lectura configurados).

---

## 5. Script de Procesamiento (La Solución Técnica)

Este es el script que David (DE) y Beatriz (DS) deberían producir al final del Sprint para cumplir con el objetivo.

```python
import pandas as pd
import glob
import os

# Configuración
INPUT_FOLDER = "datos_crudos_tiendas"
OUTPUT_FILE = "MASTER_CLEAN_DATA.csv"

def procesar_datos():
    print("--- 🚀 Iniciando ETL de Consolidación ---")
    
    # 1. Extracción (Leer todos los CSVs)
    archivos = glob.glob(f"{INPUT_FOLDER}/*.csv")
    lista_dfs = []
    
    for archivo in archivos:
        try:
            df_temp = pd.read_csv(archivo)
            lista_dfs.append(df_temp)
        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")
    
    if not lista_dfs:
        print("No se encontraron archivos.")
        return

    # Unir todo en un gran DataFrame
    df_master = pd.concat(lista_dfs, ignore_index=True)
    print(f"📊 Datos crudos unificados: {len(df_master)} filas.")

    # 2. Transformación y Limpieza (Lógica de Beatriz)
    # A. Corregir nombres de productos (Mapping)
    diccionario_correccion = {
        "Zapa_Air_ERROR_TYPO": "Zapatilla Air"
    }
    df_master['Producto'] = df_master['Producto'].replace(diccionario_correccion)
    
    # B. Corregir negativos (Regla de negocio de Ana)
    errores_negativos = df_master[df_master['Cantidad'] < 0].shape[0]
    if errores_negativos > 0:
        print(f" Corrigiendo {errores_negativos} registros con ventas negativas.")
        df_master['Cantidad'] = df_master['Cantidad'].abs()

    # C. Crear columna de Ingresos (Pre-cálculo para ayudar a Looker Studio)
    df_master['Ingresos_Totales'] = df_master['Cantidad'] * df_master['Precio_Unitario']

    # 3. Carga (Generar el Maestro para Looker Studio)
    df_master.to_csv(OUTPUT_FILE, index=False)
    print(f" EXITO: Archivo maestro generado: {OUTPUT_FILE}")
    print(" Ahora conecta Looker Studio a este archivo CSV.")

if __name__ == "__main__":
    procesar_datos()
```

