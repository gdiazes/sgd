-- models/reporte_productividad_diaria.sql

SELECT
    fecha_cosecha,
    id_empleado,
    SUM(kilos_cosechados) AS total_kilos_dia
FROM
    {{ ref('stg_cosecha') }} -- Hacemos referencia a nuestro modelo de staging, no a la tabla cruda
GROUP BY
    fecha_cosecha,
    id_empleado
ORDER BY
    fecha_cosecha,
    total_kilos_dia DESC
