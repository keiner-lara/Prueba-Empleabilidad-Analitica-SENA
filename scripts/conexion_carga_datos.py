import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


# CONFIG

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


# LOAD CSV

df = pd.read_csv("Datos_limpio.csv")

print("Columnas detectadas en el CSV:")
print(df.columns)


# DATA PREP

df.columns = df.columns.str.lower()
df["fecha"] = pd.to_datetime(df["fecha"])

df = df.dropna(subset=[
    "fecha", "producto", "tipo_producto",
    "tipo_cliente", "segmento_cliente",
    "tipo_venta", "ciudad", "pais", "total"
])


# ETL

with engine.begin() as conn:


    # DIM_REGION
   
    regiones = df[["ciudad", "pais"]].drop_duplicates()

    conn.execute(text("""
        INSERT INTO dim_region (ciudad, pais)
        VALUES (:ciudad, :pais)
        ON CONFLICT (ciudad, pais) DO NOTHING
    """), regiones.to_dict(orient="records"))

    region_map = pd.read_sql(
        "SELECT id_region, ciudad, pais FROM dim_region", conn
    )

    df = df.merge(region_map, on=["ciudad", "pais"], how="left")

    
    # DIM_CLIENTE
    
    clientes = df[[
        "tipo_cliente",
        "segmento_cliente",
        "tipo_venta",
        "id_region"
    ]].drop_duplicates()

    conn.execute(text("""
        INSERT INTO dim_cliente (
            tipo_cliente,
            segmento_cliente,
            tipo_venta,
            id_region
        )
        VALUES (
            :tipo_cliente,
            :segmento_cliente,
            :tipo_venta,
            :id_region
        )
        ON CONFLICT (
            tipo_cliente,
            segmento_cliente,
            tipo_venta,
            id_region
        ) DO NOTHING
    """), clientes.to_dict(orient="records"))

    cliente_map = pd.read_sql("""
        SELECT id_cliente, tipo_cliente, segmento_cliente, tipo_venta, id_region
        FROM dim_cliente
    """, conn)

    df = df.merge(
        cliente_map,
        on=["tipo_cliente", "segmento_cliente", "tipo_venta", "id_region"],
        how="left"
    )

    
    # DIM_PRODUCTO
    
    productos = df[["producto", "tipo_producto"]].drop_duplicates()

    conn.execute(text("""
        INSERT INTO dim_producto (producto, tipo_producto)
        VALUES (:producto, :tipo_producto)
        ON CONFLICT (producto, tipo_producto) DO NOTHING
    """), productos.to_dict(orient="records"))

    producto_map = pd.read_sql("""
        SELECT id_producto, producto, tipo_producto FROM dim_producto
    """, conn)

    df = df.merge(
        producto_map,
        on=["producto", "tipo_producto"],
        how="left"
    )

    
    # DIM_FECHA
    
    fechas = df[["fecha", "year", "month", "year_month"]].drop_duplicates()

    conn.execute(text("""
        INSERT INTO dim_fecha (fecha, year, month, year_month)
        VALUES (:fecha, :year, :month, :year_month)
        ON CONFLICT (fecha) DO NOTHING
    """), fechas.to_dict(orient="records"))

    fecha_map = pd.read_sql(
        "SELECT id_fecha, fecha FROM dim_fecha", conn
    )

  
    fecha_map["fecha"] = pd.to_datetime(fecha_map["fecha"])

    df = df.merge(fecha_map, on="fecha", how="left")

   
    # FACT_VENTAS
   
    fact = df[[
        "id_fecha",
        "id_producto",
        "id_cliente",
        "cantidad",
        "precio_unitario",
        "descuento",
        "costo_envio",
        "total"
    ]].dropna()

    conn.execute(text("""
        INSERT INTO fact_ventas (
            id_fecha,
            id_producto,
            id_cliente,
            cantidad,
            precio_unitario,
            descuento,
            costo_envio,
            total
        )
        VALUES (
            :id_fecha,
            :id_producto,
            :id_cliente,
            :cantidad,
            :precio_unitario,
            :descuento,
            :costo_envio,
            :total
        )
    """), fact.to_dict(orient="records"))

print("ETL COMPLETADO CON ÉXITO")
