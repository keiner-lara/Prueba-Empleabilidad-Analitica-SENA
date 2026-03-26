# Documento Técnico de Código Fuente

## 1. Estructura del Proyecto

```
Prueba-Empleabilidad-Analitica-SENA/
├── Datos.csv                   # Dataset original (2,000,000 filas)
├── Datos_limpio.csv            # Dataset limpio (1,951,391 filas)
├── limpieza.py                 # Pipeline ETL de limpieza y normalización
├── conexion_carga_datos.py     # Carga del dataset limpio a PostgreSQL
├── bbdd.sql                    # Esquema modelo estrella y consultas KPI
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno (DATABASE_URL)
├── portal/
│   ├── index.html              # Portal web de resultados analíticos
│   └── styles.css              # Estilos visuales del portal
├── Dashboards/
│   ├── Dashboard.png           # Captura resumen ejecutivo Power BI
│   ├── Top5.png                # Ranking productos y clientes
│   ├── Tendencia temporal.png  # Análisis de tendencia temporal
│   └── Participación por categoría.png
└── docs/
    ├── diagrams/               # UML y modelo ER en PNG
    └── wireframes/             # Mockups de pantallas del portal
```

---

## 2. Flujo del Sistema (Pipeline ETL)

```
Datos.csv  →  limpieza.py  →  Datos_limpio.csv  →  conexion_carga_datos.py  →  PostgreSQL
                                                                                     ↓
                                                                           Power BI / portal/index.html
```

---

## 3. Fragmento 1 — Limpieza de Texto y Correcciones Ortográficas (`limpieza.py`)

```python
# 3. LIMPIEZA DE TEXTO
# Elimina caracteres especiales no deseados y normaliza espacios en blancos
def limpiar_texto(valor):
    if pd.isna(valor):
        return valor                          # Preserva NaN para manejo posterior
    if isinstance(valor, str):
        # Remueve símbolos que contaminan las categorías (ej: "Yogur@t" → "Yogurt")
        valor = re.sub(r'[@#*$%^&(){}[\]<>~`]', '', valor)
        # Colapsa múltiples espacios a un solo espacio
        valor = re.sub(r'\s+', ' ', valor)
        return valor.strip()
    return valor

# 5. CORRECCIONES ORTOGRÁFICAS
# Diccionario de mapeo: versión incorrecta → versión canónica
# Garantiza unicidad de categorías; sin esto, "Yogur" y "Yogurt" serían segmentos distintos
correcciones_producto = {
    'Yogur': 'Yogurt',
    'Yogurth': 'Yogurt',
    'Gasosa': 'Gaseosa',
    'Mantequila': 'Mantequilla',
    'Galleta': 'Galletas',
    'Chocolates': 'Chocolate',
    'Cafe': 'Café',
    'Te': 'Té',
}

if 'producto' in df.columns:
    df['producto'] = df['producto'].replace(correcciones_producto)
```

**Por qué importa:** Sin este paso, `Yogur`, `Yogurth` y `Yogurtt` aparecerían como 3 productos distintos en el dashboard, inflando artificialmente el catálogo de SKUs y distorsionando los KPIs de ventas por producto.

---

## 4. Fragmento 2 — Mapeo Producto → Tipo de Producto (`limpieza.py`)

```python
# 6. NORMALIZAR TIPO_PRODUCTO SEGÚN PRODUCTO
# Aplica la categoría correcta basándose en el nombre del producto.
# Esto corrige casos donde el mismo producto tenía diferentes "tipo_producto"
# según el registro (ej: "Yogurt" catalogado como "Lácteo" en algunos y "Snack" en otros).
mapeo_tipo_producto = {
    'Leche':        'Lácteo',
    'Queso':        'Lácteo',
    'Mantequilla':  'Lácteo',
    'Yogurt':       'Lácteo',
    'Té':           'Bebida',
    'Café':         'Bebida',
    'Gaseosa':      'Bebida',
    'Chocolate':    'Snack',
    'Galletas':     'Snack',
    'Pan':          'Abarrotes',
    'Cereal':       'Abarrotes',
    'Arepa':        'Alimento Perecedero',
}

if 'producto' in df.columns and 'tipo_producto' in df.columns:
    # .map() aplica el diccionario; .fillna() preserva los valores originales
    # para productos que no estén en el diccionario (safe fallback)
    df['tipo_producto'] = df['producto'].map(mapeo_tipo_producto).fillna(df['tipo_producto'])
```

**Por qué importa:** Garantiza que cada producto pertenezca a exactamente una categoría, condición necesaria para el modelo estrella y para que los filtros de Power BI funcionen correctamente.

---

## 5. Fragmento 3 — Carga a Dimensiones y Hechos en PostgreSQL (`conexion_carga_datos.py`)

```python
# CONFIG: Conecta a la base de datos usando la URL del archivo .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")   # Evitamos hardcodear credenciales
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:               # Transacción atómica: todo o nada

    # --- DIM_REGION ---
    # Extraemos pares únicos ciudad/país para poblar la dimensión de región
    regiones = df[["ciudad", "pais"]].drop_duplicates()
    conn.execute(text("""
        INSERT INTO dim_region (ciudad, pais)
        VALUES (:ciudad, :pais)
        ON CONFLICT (ciudad, pais) DO NOTHING   -- Idempotente: puede re-ejecutarse sin duplicar
    """), regiones.to_dict(orient="records"))

    # Recuperamos los IDs generados automáticamente para hacer el JOIN
    region_map = pd.read_sql("SELECT id_region, ciudad, pais FROM dim_region", conn)
    df = df.merge(region_map, on=["ciudad", "pais"], how="left")

    # --- FACT_VENTAS ---
    # Solo insertamos las columnas de claves foráneas + métricas numéricas
    fact = df[[
        "id_fecha", "id_producto", "id_cliente",
        "cantidad", "precio_unitario",
        "descuento", "costo_envio", "total"
    ]].dropna()   # Descartamos filas donde alguna FK es nula (no se puede cargar al DW)

    conn.execute(text("""
        INSERT INTO fact_ventas (
            id_fecha, id_producto, id_cliente,
            cantidad, precio_unitario, descuento, costo_envio, total
        ) VALUES (
            :id_fecha, :id_producto, :id_cliente,
            :cantidad, :precio_unitario, :descuento, :costo_envio, :total
        )
    """), fact.to_dict(orient="records"))
```

**Por qué importa:** El uso de `ON CONFLICT DO NOTHING` hace que el proceso de carga sea **idempotente**: puede ejecutarse múltiples veces sin corromper ni duplicar la base de datos. El bloque `with engine.begin()` garantiza que si un INSERT falla, toda la transacción hace rollback automático.

---

## 6. Tecnologías Utilizadas

| Tecnología | Versión / Rol | Justificación |
|---|---|---|
| Python 3.x | Motor ETL | Ecosistema de datos maduro, Pandas para 2M+ filas |
| Pandas | Transformaciones | API vectorizada, alto rendimiento sin SQL |
| SQLAlchemy | ORM / Conexión | Abstracción de BD, compatible con múltiples motores |
| PostgreSQL | Data Warehouse | ACID, modelo estrella, consultas OLAP eficientes |
| Power BI | Visualización BI | Dashboards interactivos, conexión directa a PostgreSQL |
| HTML/CSS + Bootstrap 5 | Portal web | Accesible sin instalación, responsive |
| python-dotenv | Seguridad | Credenciales fuera del código fuente |

---

## 7. Resultados Reales del Pipeline ETL

| Métrica | Valor |
|---|---|
| Filas originales | 2,000,000 |
| Filas finales limpias | 1,951,391 |
| Total Sales | $33.83B |
| Avg Ticket | $17.34K |
| Units Sold | 10.73M |
| Países cubiertos | Colombia, Brasil, México |
| Tiempo estimado ETL | ~2–3 min en hardware estándar |
