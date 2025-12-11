-- models/staging/stg_cosecha.sql

SELECT
    id_registro,
    id_empleado,
    -- Estandarizamos el id_parcela a mayúsculas y quitamos el guion
    UPPER(REPLACE(id_parcela, '-', '')) AS id_parcela_std,
    kilos_cosechados,
    fecha_cosecha
FROM
    {{ source('raw_data', 'raw_cosecha') }}
WHERE
    id_empleado IS NOT NULL
    AND kilos_cosechados > 0
    AND kilos_cosechados <= 50 -- Filtramos datos inválidos
