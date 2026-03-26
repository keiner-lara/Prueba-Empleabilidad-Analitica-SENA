-- 1. DIMENSION TABLES

-- DIMENSION: FECHA
CREATE TABLE dim_fecha (
    id_fecha SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    CONSTRAINT uq_dim_fecha_fecha UNIQUE (fecha)
);

-- DIMENSION: REGION
CREATE TABLE dim_region (
    id_region SERIAL PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    CONSTRAINT uq_dim_region_ciudad_pais UNIQUE (ciudad, pais)
);

-- DIMENSION: CLIENTE
CREATE TABLE dim_cliente (
    id_cliente SERIAL PRIMARY KEY,
    tipo_cliente VARCHAR(50) NOT NULL,
    segmento_cliente VARCHAR(50) NOT NULL,
    tipo_venta VARCHAR(50) NOT NULL,
    id_region INT NOT NULL,
    CONSTRAINT uq_dim_cliente UNIQUE (
        tipo_cliente,
        segmento_cliente,
        tipo_venta,
        id_region
    ),
    CONSTRAINT fk_cliente_region
        FOREIGN KEY (id_region)
        REFERENCES dim_region(id_region)
);

-- DIMENSION: PRODUCTO
CREATE TABLE dim_producto (
    id_producto SERIAL PRIMARY KEY,
    producto VARCHAR(100) NOT NULL,
    tipo_producto VARCHAR(100) NOT NULL,
    CONSTRAINT uq_dim_producto UNIQUE (producto, tipo_producto)
);


-- 2. FACT TABLE


CREATE TABLE fact_ventas (
    id_venta SERIAL PRIMARY KEY,
    id_fecha INT NOT NULL,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    cantidad NUMERIC(10,2) NOT NULL,
    precio_unitario NUMERIC(12,2) NOT NULL,
    descuento NUMERIC(5,2) DEFAULT 0,
    costo_envio NUMERIC(12,2) DEFAULT 0,
    total NUMERIC(14,2) NOT NULL,

    CONSTRAINT fk_fact_fecha
        FOREIGN KEY (id_fecha)
        REFERENCES dim_fecha(id_fecha),

    CONSTRAINT fk_fact_producto
        FOREIGN KEY (id_producto)
        REFERENCES dim_producto(id_producto),

    CONSTRAINT fk_fact_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES dim_cliente(id_cliente)
);


-- 3. INDEXES (PERFORMANCE BI)


CREATE INDEX idx_fact_fecha ON fact_ventas(id_fecha);
CREATE INDEX idx_fact_producto ON fact_ventas(id_producto);
CREATE INDEX idx_fact_cliente ON fact_ventas(id_cliente);


-- CONSULTAS SQL BÁSICAS
-- 1️) Total de ventas por región
SELECT
    r.pais,
    r.ciudad,
    SUM(f.total) AS total_sales
FROM fact_ventas f
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
JOIN dim_region r ON c.id_region = r.id_region
GROUP BY r.pais, r.ciudad
ORDER BY total_sales DESC;

-- 2️) Top 5 productos por monto vendido
SELECT
    p.producto,
    SUM(f.total) AS total_sales
FROM fact_ventas f
JOIN dim_producto p ON f.id_producto = p.id_producto
GROUP BY p.producto
ORDER BY total_sales DESC
LIMIT 5;

-- 3)  Ticket promedio por cliente
SELECT
    c.tipo_cliente,
    AVG(f.total) AS avg_ticket
FROM fact_ventas f
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
GROUP BY c.tipo_cliente
ORDER BY avg_ticket DESC;

-- 4) Clientes sin ventas asociadas
SELECT
    c.id_cliente,
    c.tipo_cliente,
    c.segmento_cliente
FROM dim_cliente c
LEFT JOIN fact_ventas f ON c.id_cliente = f.id_cliente
WHERE f.id_cliente IS NULL;


-- CONSULTAS SQL INTERMEDIAS
-- 1) Ventas totales por categoría y región
SELECT
    r.pais,
    p.tipo_producto,
    SUM(f.total) AS total_sales
FROM fact_ventas f
JOIN dim_producto p ON f.id_producto = p.id_producto
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
JOIN dim_region r ON c.id_region = r.id_region
GROUP BY r.pais, p.tipo_producto
ORDER BY total_sales DESC;

-- 2) Ranking de clientes por ventas (DENSE_RANK)
SELECT
    c.tipo_cliente,
    SUM(f.total) AS total_sales,
    DENSE_RANK() OVER (ORDER BY SUM(f.total) DESC) AS sales_rank
FROM fact_ventas f
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
GROUP BY c.tipo_cliente;

-- 3) Comparación de ventas YoY
SELECT
    d.year,
    SUM(f.total) AS total_sales,
    LAG(SUM(f.total)) OVER (ORDER BY d.year) AS prev_year_sales,
    ROUND(
        (SUM(f.total) - LAG(SUM(f.total)) OVER (ORDER BY d.year))
        / LAG(SUM(f.total)) OVER (ORDER BY d.year) * 100, 2
    ) AS yoy_growth_pct
FROM fact_ventas f
JOIN dim_fecha d ON f.id_fecha = d.id_fecha
GROUP BY d.year
ORDER BY d.year;

-- 4) % participación por categoría
SELECT
    p.tipo_producto,
    SUM(f.total) AS total_sales,
    ROUND(
        SUM(f.total) * 100.0 / SUM(SUM(f.total)) OVER (), 2
    ) AS sales_percentage
FROM fact_ventas f
JOIN dim_producto p ON f.id_producto = p.id_producto
GROUP BY p.tipo_producto
ORDER BY sales_percentage DESC;




