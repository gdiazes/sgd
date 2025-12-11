
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Generando 1 millón de registros de cosecha... Esto puede tardar unos minutos.")
num_rows = 1_000_000
error_rate = 0.15 # 15% de errores

# Datos base
employees = [f'E-{i:03d}' for i in range(1, 101)]
parcels = [f'P-{i:02d}{c}' for i in range(1, 11) for c in ['A', 'B']] # P-01A, P-01B, etc.

# Generación de datos base
data = {
    'id_empleado': np.random.choice(employees, size=num_rows),
    'id_parcela': np.random.choice(parcels, size=num_rows),
    'kilos_cosechados': np.random.uniform(10, 40, size=num_rows).round(2),
    'fecha_cosecha': [datetime(2024, 6, 1) + timedelta(days=np.random.randint(0, 29)) for _ in range(num_rows)]
}
df = pd.DataFrame(data)

# Introducción de errores (15%)
num_errors = int(num_rows * error_rate)
error_indices = np.random.choice(df.index, size=num_errors, replace=False)

for i in error_indices:
    error_type = np.random.choice(['null_id', 'bad_format', 'negative_kilos', 'outlier_kilos'])
    if error_type == 'null_id':
        df.loc[i, 'id_empleado'] = None
    elif error_type == 'bad_format':
        df.loc[i, 'id_parcela'] = df.loc[i, 'id_parcela'].lower().replace('-', '') # ej. p01a
    elif error_type == 'negative_kilos':
        df.loc[i, 'kilos_cosechados'] = -10.0
    elif error_type == 'outlier_kilos':
        df.loc[i, 'kilos_cosechados'] = np.random.uniform(100, 500)

# Crear carpeta si no existe y guardar
output_dir = 'dbt_project/seeds'
import os
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, 'raw_cosecha.csv'), index_label='id_registro')
print(f"Archivo 'raw_cosecha.csv' con {num_rows} registros y ~{error_rate:.0%} de errores generado en la carpeta 'dbt_project/seeds/'.")
