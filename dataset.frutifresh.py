import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Parámetros de Simulación ---
n_transactions = 1000
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 31)

products = {
    'P01': {'name': 'Detox Verde', 'price': 12.50, 'base_prob': 0.25},
    'P02': {'name': 'Energia Matutina', 'price': 11.00, 'base_prob': 0.35},
    'P03': {'name': 'Trio de Berries', 'price': 14.00, 'base_prob': 0.20},
    'P04': {'name': 'Sol Tropical', 'price': 10.50, 'base_prob': 0.15},
    'P05': {'name': 'Inmune-C Boost', 'price': 13.00, 'base_prob': 0.05}
}

stores = {
    'T01': {'name': 'Centro Financiero', 'prob_mult': {'P01': 1.2, 'P02': 1.1, 'P03': 0.8, 'P04': 0.9, 'P05': 1.0}},
    'T02': {'name': 'Zona Residencial', 'prob_mult': {'P01': 0.8, 'P02': 0.9, 'P03': 1.2, 'P04': 1.1, 'P05': 1.0}}
}

# --- Generación de Datos ---
data = []
time_diff = end_date - start_date

for i in range(n_transactions):
    # ID de Transacción
    transaction_id = 1001 + i

    # Fecha y Hora (con picos a las 8am y 3pm)
    random_seconds = np.random.choice(
        [np.random.normal(8 * 3600, 1.5 * 3600), np.random.normal(15 * 3600, 2 * 3600)],
        p=[0.6, 0.4]
    )
    random_days = np.random.rand() * time_diff.days
    transaction_datetime = start_date + timedelta(days=random_days, seconds=random_seconds)
    transaction_datetime = transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Tienda
    store_id = np.random.choice(list(stores.keys()))

    # Producto (con probabilidades ajustadas por tienda)
    store_probs = [p['base_prob'] * stores[store_id]['prob_mult'][pid] for pid, p in products.items()]
    store_probs_normalized = np.array(store_probs) / np.sum(store_probs)
    product_id = np.random.choice(list(products.keys()), p=store_probs_normalized)
    
    product_name = products[product_id]['name']
    unit_price = products[product_id]['price']

    # Cantidad
    quantity = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])

    data.append([transaction_id, transaction_datetime, product_id, product_name, unit_price, quantity, store_id])

# --- Crear DataFrame y Guardar CSV ---
df = pd.DataFrame(data, columns=[
    'ID_Transaccion', 'Fecha_Hora', 'ID_Producto', 'Nombre_Producto',
    'Precio_Unitario', 'Cantidad', 'ID_Tienda'
])

# Asegurar orden cronológico
df = df.sort_values(by='Fecha_Hora').reset_index(drop=True)

# Guardar el archivo
df.to_csv('ventas_frutifresh_mes1.csv', index=False)

print("Archivo 'ventas_frutifresh_mes1.csv' generado con éxito con 1000 transacciones.")
