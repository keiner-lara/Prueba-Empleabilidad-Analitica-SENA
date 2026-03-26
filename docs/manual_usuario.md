# Manual de Usuario — Portal Analítico de Ventas LATAM

**Proyecto:** Plataforma de Postulación a Empleabilidad  
**Autor:** Keiner Lara | Data Analyst  
**Fecha:** Marzo 2026 | SENA

---

## 1. Requisitos del Sistema

| Componente | Versión mínima |
|---|---|
| Python | 3.8+ |
| PostgreSQL | 13+ |
| Navegador web | Chrome, Firefox, Edge (cualquier versión moderna) |
| Power BI Desktop | Opcional (para explorar el archivo .pbix) |
| RAM recomendada | 8 GB (por el dataset de 2M filas) |

---

## 2. Instalación

### 2.1 Clonar o descomprimir el proyecto
Coloca todos los archivos en una carpeta local, por ejemplo:
```
C:\Proyectos\Prueba Empleabilidad\
```

### 2.2 Instalar dependencias Python
```bash
pip install -r requirements.txt
```

Dependencias incluidas:
- `pandas` — procesamiento de datos
- `sqlalchemy` — conexión a PostgreSQL
- `psycopg2-binary` — driver PostgreSQL
- `python-dotenv` — carga de variables de entorno

### 2.3 Configurar conexión a la base de datos
Edita el archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/empleabilidad
```

### 2.4 Crear el esquema de base de datos
Ejecuta el script SQL incluido:
```bash
psql -U usuario -d empleabilidad -f bbdd.sql
```

---

## 3. Ejecución Paso a Paso

### Paso 1 — Ejecutar limpieza de datos

```bash
python limpieza.py
```

**Salida esperada en consola:**
```
Filas originales: 2000000
============================================================
DATA CLEANING SUMMARY
============================================================
Filas finales: 1951391

Valores nulos por columna:
fecha              0
producto           0
cantidad           0
precio_unitario    0
total              0
dtype: int64

Tipos de datos:
fecha              datetime64[ns]
producto                   object
cantidad                  float64
...

OK Archivo generado: Datos_limpio.csv

Valores únicos (columnas categóricas):
- producto: 12 únicos
- tipo_producto: 5 únicos
- tipo_venta: 4 únicos
- tipo_cliente: 4 únicos
- ciudad: 30 únicos
- pais: 3 únicos
```

**Resultado:** Se genera `Datos_limpio.csv` (1,951,391 filas, UTF-8).

---

### Paso 2 — Cargar datos a PostgreSQL

```bash
python conexion_carga_datos.py
```

**Salida esperada:**
```
Columnas detectadas en el CSV:
Index(['fecha', 'year', 'month', 'year_month', 'producto', 'tipo_producto',
       'cantidad', 'precio_unitario', 'descuento', 'costo_envio', 'total',
       'tipo_venta', 'tipo_cliente', 'segmento_cliente', 'ciudad', 'pais'],
      dtype='object')

ETL COMPLETADO CON ÉXITO
```

**Resultado:** Las 4 tablas del modelo estrella quedan pobladas en PostgreSQL.

---

### Paso 3 — Abrir el portal web

1. Navega a la carpeta `portal/`
2. Abre `index.html` con doble clic (o arrástralo a tu navegador)
3. Verás el portal con:
   - **KPIs principales** ($33.83B, $17.34K, 10.73M, 3 hubs)
   - **Top 5 Productos** con tabla y gráfico de barras interactivo
   - **Insights estratégicos** (3 hallazgos con evidencia, impacto y recomendación)
   - **Galería visual** con las 4 capturas de dashboards de Power BI (clic para ampliar)

---

## 4. Capturas del Portal

### Vista KPIs Principales
*(Ver portal/index.html → Sección inicial con 4 tarjetas de métricas)*

Los KPIs provienen directamente del dataset limpio:
- **$33.83B** — Suma del campo `total` de todos los registros
- **$17.34K** — Promedio de `total` por transacción
- **10.73M** — Suma del campo `cantidad`
- **3 hubs** — Países únicos: Colombia, Brasil, México

### Vista Top 5 Productos
*(Ver portal/index.html → Sección "Top 5 Products")*

Tabla generada con la siguiente consulta SQL:
```sql
SELECT p.producto, SUM(f.total) AS total_ventas
FROM fact_ventas f
JOIN dim_producto p ON f.id_producto = p.id_producto
GROUP BY p.producto
ORDER BY total_ventas DESC
LIMIT 5;
```

### Dashboards de Power BI
*(Ver Dashboards/ → 4 archivos PNG)*

| Captura | Descripción |
|---|---|
| `Dashboard.png` | Resumen ejecutivo: ventas totales, tendencia y KPIs |
| `Top5.png` | Ranking de productos y segmentos de clientes |
| `Tendencia temporal.png` | Comportamiento de ventas a lo largo del tiempo |
| `Participación por categoría.png` | Market share por tipo de producto |

---

## 5. Solución de Problemas Comunes

| Error | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: pandas` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `OperationalError: could not connect` | PostgreSQL no corriendo o .env incorrecto | Verificar servicio PostgreSQL y archivo .env |
| `FileNotFoundError: Datos.csv` | El archivo no está en la raíz del proyecto | Asegúrate de ejecutar el script desde la raíz |
| Portal no muestra imágenes | Rutas relativas incorrectas | Asegúrate de abrir `portal/index.html` desde su carpeta, no desde otra ubicación |
