import pandas as pd
import re


# 1. CARGAR CSV SUCIO

ruta_csv = "Datos.csv"
df = pd.read_csv(ruta_csv)

print(f"Filas originales: {len(df)}")


# 2. NORMALIZAR NOMBRES DE COLUMNAS

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# 3. LIMPIEZA DE TEXTO

def limpiar_texto(valor):
    if pd.isna(valor):
        return valor
    if isinstance(valor, str):
        valor = re.sub(r'[@#*$%^&(){}[\]<>~`]', '', valor)
        valor = re.sub(r'\s+', ' ', valor)
        return valor.strip()
    return valor

columnas_texto = [
    'producto', 'tipo_producto', 'ciudad',
    'pais', 'tipo_venta', 'tipo_cliente'
]

for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].apply(limpiar_texto)


# 4. NORMALIZAR TEXTO CONSISTENTE
# Basic normalization for text values used in analytics
def normalizar_texto(serie):
    return (
        serie.astype(str)
        .str.strip()
        .str.replace("_", " ", regex=False)
        .str.title()
    )

for col in columnas_texto:
    if col in df.columns:
        df[col] = normalizar_texto(df[col])


# 5. CORRECCIONES ORTOGRÁFICAS
# Fix common misspellings to keep categories consistent
correcciones_producto = {
    'Yogur': 'Yogurt',
    'Yogurth': 'Yogurt',
    'Yogurtt': 'Yogurt',
    'Gasosa': 'Gaseosa',
    'Mantequila': 'Mantequilla',
    'Galleta': 'Galletas',
    'Galletass': 'Galletas',
    'Chocolates': 'Chocolate',
    'Cafe': 'Café',
    'Te': 'Té',
}

correcciones_tipo_producto = {
    'Alimento Percedero': 'Alimento Perecedero',
    'Alimento Perecedro': 'Alimento Perecedero',
    'Lacteo': 'Lácteo',
    'Lacteos': 'Lácteo',
    'Abrrotes': 'Abarrotes',
    'Abarotes': 'Abarrotes',
}

correcciones_tipo_venta = {
    'Tienda Fisica': 'Tienda Física',
    'Distribudor': 'Distribuidor',
    'Call Center': 'Call Center',
}

correcciones_tipo_cliente = {
    'Mayorita': 'Mayorista',
    'Mayorsita': 'Mayorista',
    'Govierno': 'Gobierno',
}

if 'producto' in df.columns:
    df['producto'] = df['producto'].replace(correcciones_producto)
if 'tipo_producto' in df.columns:
    df['tipo_producto'] = df['tipo_producto'].replace(correcciones_tipo_producto)
if 'tipo_venta' in df.columns:
    df['tipo_venta'] = df['tipo_venta'].replace(correcciones_tipo_venta)
if 'tipo_cliente' in df.columns:
    df['tipo_cliente'] = df['tipo_cliente'].replace(correcciones_tipo_cliente)


# 6. NORMALIZAR TIPO_PRODUCTO SEGÚN PRODUCTO
# This enforces a consistent category per product
mapeo_tipo_producto = {
    'Leche': 'Lácteo',
    'Queso': 'Lácteo',
    'Mantequilla': 'Lácteo',
    'Yogurt': 'Lácteo',
    'Té': 'Bebida',
    'Café': 'Bebida',
    'Gaseosa': 'Bebida',
    'Chocolate': 'Snack',
    'Galletas': 'Snack',
    'Pan': 'Abarrotes',
    'Cereal': 'Abarrotes',
    'Arepa': 'Alimento Perecedero',
}

if 'producto' in df.columns and 'tipo_producto' in df.columns:
    df['tipo_producto'] = df['producto'].map(mapeo_tipo_producto).fillna(df['tipo_producto'])


# 7. CONVERTIR TIPOS DE DATOS

columnas_numericas = [
    'cantidad', 'precio_unitario',
    'descuento', 'costo_envio', 'total'
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')


# 8. REGLAS DE NEGOCIO

# Ventas mayores a cero
df = df[df['total'] > 0]

# Eliminar filas sin datos críticos
columnas_criticas = ['fecha', 'producto', 'cantidad', 'precio_unitario']
df = df.dropna(subset=columnas_criticas)


# 9. IMPUTACIÓN LÓGICA DE NUMÉRICOS
# Use business math rules to fill missing values when possible
mask_desc = df['descuento'].isna() & df['total'].notna() & df['cantidad'].notna() & df['precio_unitario'].notna()
df.loc[mask_desc, 'descuento'] = (1 - df['total'] / (df['cantidad'] * df['precio_unitario'])).round(2)

mask_precio = df['precio_unitario'].isna() & df['total'].notna() & df['cantidad'].notna()
df.loc[mask_precio, 'precio_unitario'] = df['total'] / (df['cantidad'] * (1 - df['descuento']))

mask_cantidad = df['cantidad'].isna() & df['total'].notna() & df['precio_unitario'].notna()
df.loc[mask_cantidad, 'cantidad'] = (
    df['total'] / (df['precio_unitario'] * (1 - df['descuento']))
).round(0)

mask_total = df['total'].isna() & df['cantidad'].notna() & df['precio_unitario'].notna()
df.loc[mask_total, 'total'] = df['cantidad'] * df['precio_unitario'] * (1 - df['descuento'])


# 10. ELIMINAR DUPLICADOS

df = df.drop_duplicates()


# 11. CREAR COLUMNAS DERIVADAS

df['year'] = df['fecha'].dt.year
df['month'] = df['fecha'].dt.month
df['year_month'] = df['fecha'].dt.to_period('M').astype(str)

# Segmentación de cliente
def segmentar_cliente(tipo):
    if tipo in ['Corporativo', 'Gobierno']:
        return 'Enterprise'
    elif tipo == 'Mayorista':
        return 'Wholesale'
    else:
        return 'Retail'

df['segmento_cliente'] = df['tipo_cliente'].apply(segmentar_cliente)


# 12. MANEJO DE NULOS

df['descuento'] = df['descuento'].fillna(0)
df['costo_envio'] = df['costo_envio'].fillna(0)
df['tipo_venta'] = df['tipo_venta'].fillna('Desconocido')
df['tipo_cliente'] = df['tipo_cliente'].fillna('Desconocido')
df['ciudad'] = df['ciudad'].fillna('Desconocida')
df['pais'] = df['pais'].fillna('Desconocido')


# 13. ORDEN FINAL DE COLUMNAS

orden_final = [
    'fecha', 'year', 'month', 'year_month',
    'producto', 'tipo_producto',
    'cantidad', 'precio_unitario',
    'descuento', 'costo_envio', 'total',
    'tipo_venta', 'tipo_cliente', 'segmento_cliente',
    'ciudad', 'pais'
]

df = df[orden_final]


# 14. EXPORTAR CSV LIMPIO

df.to_csv("Datos_limpio.csv", index=False, encoding="utf-8-sig")


# 15. RESUMEN

print("=" * 60)
print("DATA CLEANING SUMMARY")
print("=" * 60)
print(f"Filas finales: {len(df)}")
print("\nValores nulos por columna:")
print(df.isnull().sum())
print("\nTipos de datos:")
print(df.dtypes)
print("\nPrimeras 5 filas:")
print(df.head())
print("\nOK Archivo generado: Datos_limpio.csv")

# Extra data quality report for presentation
categoricas = ['producto', 'tipo_producto', 'tipo_venta', 'tipo_cliente', 'ciudad', 'pais']
print("\nValores únicos (columnas categóricas):")
for col in categoricas:
    if col in df.columns:
        print(f"- {col}: {df[col].nunique()} únicos")
