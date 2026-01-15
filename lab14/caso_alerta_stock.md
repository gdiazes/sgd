### Caso de Estudio Actualizado: "Proyecto Retail - Alerta de Stock con Data Studio"

**El Desafío Técnico:** Procesar gran volumen de datos (Big Data) pero presentarlo en una herramienta web ligera (Data Studio).
**Estrategia:** La inteligencia pesada se queda en el backend (Data Warehouse/BigQuery), Data Studio solo visualiza resultados agregados.

---

### 1. Roles y Responsabilidades Ajustados (Equipo de 5)

1.  **Ana (Product Owner):**
    *   *Cambio:* Ya no necesita instalar software. Su responsabilidad es verificar que el reporte se vea bien en Móvil y Desktop (Data Studio es responsive).
2.  **Carlos (Scrum Master / Data Lead):**
    *   *Cambio:* Gestiona los accesos de Google (IAM) y la facturación si se usa BigQuery.
3.  **David (Data Engineer):**
    *   *Cambio Crítico:* Su prioridad es crear **Vistas Materializadas** o Tablas Agregadas. Data Studio no debe hacer cálculos complejos; David debe entregarlos pre-calculados.
4.  **Beatriz (Data Scientist):**
    *   *Cambio:* Sus predicciones deben escribirse en una tabla accesible por el conector de Google (ej. BigQuery, MySQL en nube o Google Sheets para prototipos rápidos).
5.  **Elena (Data Analyst / BI - Experta en Data Studio):**
    *   *Cambio:* Encargada de la configuración de fuentes de datos, "Data Blending" (mezcla de fuentes) y diseño del lienzo (Canvas).
