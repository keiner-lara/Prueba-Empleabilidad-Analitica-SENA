# Documento de Diseño de Software

## 1. Introducción
Este documento describe el diseño de la solución analítica para la plataforma de empleabilidad basada en datos de ventas LATAM. El objetivo es mostrar el enfoque completo de análisis, desde el ETL hasta la visualización y el portal web.

## 2. Problema a Resolver
La organización requiere transformar un dataset de ventas de 2,000,000 filas con inconsistencias en información confiable para la toma de decisiones. El proceso debe garantizar calidad de datos, modelado analítico y visualización clara.

## 3. Objetivos del Sistema
- Limpiar y normalizar datos de ventas.
- Construir un modelo estrella para análisis.
- Generar insights accionables.
- Presentar resultados en dashboards y un portal web.

## 4. Actores / Usuarios
- Analista de datos: ejecuta ETL y valida resultados.
- Stakeholder de negocio: consume dashboards y portal web.

## 5. Requisitos
### Funcionales
- Limpieza automática de datos.
- Generación de dataset limpio.
- Carga a base de datos con modelo estrella.
- Consultas SQL para KPIs.
- Portal web con KPIs, Top 5 y insights.

### No Funcionales
- Reproducible en ambiente local.
- Rendimiento aceptable para 2M filas.
- Código documentado y mantenible.

## 6. Arquitectura
1. **Ingesta:** `Datos.csv`
2. **ETL:** `limpieza.py` (Python + Pandas)
3. **Modelo Analítico:** PostgreSQL (estrella)
4. **BI:** Power BI
5. **Presentación:** `portal/index.html`

## 6.1 Métricas Reales del Proyecto
- Filas limpias: **1,951,391**
- Total Sales: **$33.83B**
- Avg Ticket: **$17.34K**
- Units Sold: **10.73M**
- Países: **Colombia, Brasil, México**

## 7. Módulos
- Limpieza y normalización de datos
- Carga a base de datos
- Consultas SQL analíticas
- Visualización BI
- Portal web de resultados

## 8. Tecnologías
- Python, Pandas
- PostgreSQL
- Power BI
- HTML/CSS + Bootstrap

## 9. Justificación Técnica

La arquitectura híbrida propuesta —Python como motor ETL, PostgreSQL como repositorio analítico, Power BI como capa de visualización empresarial y HTML/CSS como portal de publicación— fue seleccionada por su equilibrio entre rendimiento, reproducibilidad y adopción en la industria. Python con Pandas permite procesar datasets de más de 2 millones de filas con pipelines explícitos, trazables y fácilmente auditables, donde cada transformación queda documentada como un paso numerado en el código fuente.

El modelo de datos estrella implementado en PostgreSQL garantiza que las consultas analíticas sean eficientes incluso a gran escala. La separación en tablas de dimensión (`dim_fecha`, `dim_producto`, `dim_region`, `dim_cliente`) y una tabla de hechos central (`fact_ventas`) sigue el estándar Kimball para Data Warehousing, lo cual facilita la agregación por múltiples ejes sin redundancia. Este diseño es extensible: agregar nuevas dimensiones (por ejemplo, `dim_canal`) no requiere modificar el esquema de hechos.

La decisión de exponer los resultados a través de un portal web estático (HTML/CSS + Bootstrap) responde a la necesidad de democratizar el acceso a los insights sin requerir herramientas especializadas por parte del usuario final. El portal complementa el dashboard de Power BI al ofrecer los KPIs clave, el ranking de productos y los hallazgos estratégicos en un formato universalmente accesible desde cualquier navegador, sin instalación adicional.

## 10. Métricas de Calidad de Datos (Antes vs Después)

| Métrica | Dataset Original | Dataset Limpio |
|---|---|---|
| Total de filas | 2,000,000 | 1,951,391 |
| Filas eliminadas | — | 48,609 (~2.4%) |
| Columnas con nulos críticos | 4 | 0 |
| Errores ortográficos en categorías | 15+ variantes | 0 |
| Tipos de datos incorrectos | 3 columnas numéricas como texto | 0 |
| Columnas derivadas añadidas | 0 | 3 (year, month, year_month, segmento_cliente) |
| Filas duplicadas removidas | — | Eliminadas con `drop_duplicates()` |
