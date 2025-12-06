import csv
import random
from datetime import datetime, timedelta

# Rutas de salida (directamente a la carpeta seeds de dbt)
PATH_PRODUCTS = 'dbt/seeds/frutifresh_products.csv'
PATH_SALES = 'dbt/seeds/frutifresh_sales.csv'

def generate_products():
    print(f"Generando {PATH_PRODUCTS}...")
    # Lista de productos base
    # NOTA: El ID 200 está DUPLICADO intencionalmente para fallar el test 'unique'
    products = [
        [100, 'Manzana Royal', 'Frutas', 1.50],
        [101, 'Manzana Verde', 'Frutas', 1.60],
        [102, 'Naranja Jugo', 'Frutas', 0.80],
        [103, 'Mandarina', 'Frutas', 1.00],
        [200, 'Pera de Agua', 'Frutas', 2.00], # <--- ID 200
        [200, 'Platano Seda', 'Frutas', 1.20], # <--- ID 200 (Duplicado!)
        [300, 'Uva Italia', 'Frutas', 3.50],
        [301, 'Uva Red Globe', 'Frutas', 3.80],
        [400, 'Lechuga', 'Verduras', 0.50],
        [401, 'Tomate', 'Verduras', 0.90]
    ]
    
    with open(PATH_PRODUCTS, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id', 'product_name', 'category', 'price'])
        writer.writerows(products)

def generate_sales():
    print(f"Generando {PATH_SALES} con 1000 registros...")
    
    valid_product_ids = [100, 101, 102, 103, 200, 300, 301, 400, 401]
    start_date = datetime(2023, 1, 1)
    
    with open(PATH_SALES, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sale_id', 'product_id', 'quantity', 'sale_date'])
        
        for i in range(1, 1001):
            # Datos normales
            sale_id = i
            product_id = random.choice(valid_product_ids)
            quantity = random.randint(1, 50)
            sale_date = start_date + timedelta(days=random.randint(0, 300))
            
            # --- INYECCIÓN DE ERRORES ---
            
            # Error 1: Sale ID Nulo (en el registro #50)
            # Esto fallará el test 'not_null' en sale_id
            if i == 50:
                sale_id = '' 
            
            # Error 2: Producto Inexistente (en el registro #100 y #500)
            # Esto fallará el test 'relationships' (Integridad referencial)
            # El producto 9999 no existe en la tabla de productos
            if i in [100, 500]:
                product_id = 9999
                
            writer.writerow([sale_id, product_id, quantity, sale_date.strftime('%Y-%m-%d')])

if __name__ == '__main__':
    generate_products()
    generate_sales()
    print("¡Datos generados exitosamente!")
