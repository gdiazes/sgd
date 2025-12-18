proyecto_andesharvest/
├── dbt_project.yml          # ⚙️ Configuración principal del proyecto
├── packages.yml             # 📦 Librerías externas (ej. dbt-utils)
├── README.md                # 📄 Documentación del proyecto
├── .gitignore               # 🙈 Archivos a ignorar por git (ej. /target, /logs)
│
├── models/                  # 🧠 EL CORAZÓN DE DBT (Tu código SQL/Jinja)
│   ├── staging/             # 🟡 Capa de limpieza (1:1 con fuentes)
│   │   ├── _sources.yml     #    Definición de fuentes (Postgres tables)
│   │   ├── postgres_app/    #    Carpeta por cada sistema fuente
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_orders.sql
│   │   │   └── src_postgres.yml
│   │   └── google_sheets/
│   │       └── stg_presupuesto.sql
│   │
│   ├── intermediate/        # 🟠 Capa de lógica compleja (Joins, cálculos previos)
│   │   └── sales/
│   │       └── int_orders_with_user_details.sql
│   │
│   └── marts/               # 🟢 Capa final (BI / Reportes / Tableros)
│       ├── core/            #    Entidades principales del negocio
│       │   ├── dim_customers.sql  # Dimensión Clientes
│       │   ├── dim_products.sql   # Dimensión Productos
│       │   └── fct_orders.sql     # Tabla de Hechos (Ventas)
│       └── marketing/       #    Marts específicos por área
│           └── fct_campaign_performance.sql
│
├── seeds/                   # 🌱 Datos estáticos (CSVs pequeños)
│   └── country_codes.csv    #    Se carga a la DB con 'dbt seed'
│
├── snapshots/               # 📸 Historial de cambios (SCD Type 2)
│   └── orders_snapshot.sql
│
├── tests/                   # 🧪 Tests singulares (SQL específico)
│   └── assert_total_payment_is_positive.sql
│
├── macros/                  # 🔧 Funciones reutilizables (Jinja)
│   └── generate_schema_name.sql
│
├── analyses/                # 🔎 Consultas ad-hoc (no crean tablas)
│   └── audit_duplicates.sql
│
└── target/                  # 🚫 (Generado automáticamente, NO tocar)
    └── compiled/            #    SQL compilado
