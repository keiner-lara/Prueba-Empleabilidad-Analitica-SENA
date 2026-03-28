# Riwi Analytics – Data Analytics Assessment: LATAM Retail Analysis

[![App Status](https://img.shields.io/badge/Vercel-Deployed-success?logo=vercel&logoColor=white)](https://prueba-empleabilidad-analitica-sena-ayrc61pon.vercel.app/)
[![Database](https://img.shields.io/badge/DB-PostgreSQL-blue?logo=postgresql&logoColor=white)](bbdd.sql)
[![Code](https://img.shields.io/badge/Code-Python-yellow?logo=python&logoColor=white)](scripts/)

This repository contains a comprehensive technical solution for data analytics assessment, focused on retail market behavior in Latin America. It includes everything from data engineering (ETL) to strategic visualization of findings.

---

### [View Live Application (Vercel)](https://prueba-empleabilidad-analitica-sena-ayrc61pon.vercel.app/)

---

## 1. Project Overview

This project was developed as part of the **Riwi Analytics Employability Assessment**, aiming to demonstrate an end-to-end data analytics workflow. The objective is to transform raw sales data into actionable business insights through data modeling, ETL processes, exploratory analysis, and interactive dashboards.

The workflow follows a hybrid analytical architecture:

* **PostgreSQL**: Used for data storage, analytical queries, and aggregations.
* **Python**: Used for ETL, data cleaning, validation, and exploratory data analysis (EDA).
* **Power BI**: Used for data visualization, dashboards, and storytelling.

---

## 2. Project Structure

The repository is organized to ensure scalability and clarity:

```text
Prueba-Empleabilidad-Analitica-SENA/
├── .gitignore                           # Excludes .env, CSVs, venv, temp files
├── README.md                           # Project documentation (English)
├── bbdd.sql                            # Star schema DDL + 8 analytical queries
├── requirements.txt                    # Python dependencies
├── .env                                # DB credentials (NOT in Git)
│
├── scripts/                            # ETL and utility Python scripts
│   ├── limpieza.py                     # Data cleaning pipeline (2X rows)
│   ├── conexion_carga_datos.py         # PostgreSQL star-schema loader
│   └── extraer_pdfs.py                 # PDF extraction utility
│
├── notebooks/
│   └── Análisis exploratorio (EDA).ipynb  # EDA with charts + English interpretations
│
├── portal/                             # Web portal (HTML/CSS + Bootstrap 5 + Chart.js)
│   ├── index.html
│   └── assets/                         # Dashboard images for deployment
│
├── Dashboards/                         # Power BI exports
│   └── Dashboards_empleabilidad_Keiner_Lara.pbix
│
├── docs/                               # Technical documentation
│   ├── diagrams/       # UML PNGs (Casos de Uso, Clases, Secuencia, ModeloER)
│   └── Code-Photo/     # Professional code screenshots
│
└── normas/                             # SENA certification documents
    ├── Documento de diseño de software.docx
    ├── Diagramas de Lenguaje Unificado de Modelado (UML).docx
    ├── Prototipo de solución de software.docx
    ├── Modelo de base de datos.docx
    ├── Documento técnico de código fuente.docx
    ├── Manual de usuario.docx
    └── Solución de software.docx
```

> **Note:** `Datos.csv` (194 MB) and `Datos_limpio.csv` (238 MB) are excluded from Git (exceed GitHub's 100 MB limit). Run `scripts/limpieza.py` locally to regenerate `Datos_limpio.csv` from the original dataset.

---

## 3. Database Structure (Star Schema)

The analytical model uses a **Star Schema** to optimize performance for BI reporting:

### Dimension Tables

- **dim_fecha**: Time intelligence attributes (Year, Month, Year_Month)
- **dim_producto**: Product names and categories (e.g., Snacks, Beverages, Dairy)
- **dim_region**: Geographical data (City, Country)
- **dim_cliente**: Customer segmentation (Corporate, Government, Wholesale) and sales types

### Fact Table

- **fact_ventas**: Transactional data (quantity, unit price, discounts, shipping costs, revenue)

---

## 4. ETL Pipeline (Python)

The `limpieza.py` and `conexion_carga_datos.py` scripts automate:

- **Extraction**: Loading raw data via SQLAlchemy and Pandas
- **Transformation**:
  - Removing duplicates and filtering invalid records (sales ≤ 0)
  - Normalizing data types and handling missing values
  - Creating derived columns (Year, Month) for time dimension
- **Load**: Structured load into PostgreSQL with referential integrity (Dimensions first, Fact table last)

---

## 5. Visual Intelligence & Insights

The solution includes an interactive portal where global KPIs and strategic findings can be viewed:

- **Total Sales**: 33.83B
- **Average Ticket**: 17.34K
- **Units Sold**: 10.73M

[View all Insights in the Portal](https://prueba-empleabilidad-analitica-sena-ayrc61pon.vercel.app/)

---

## 6. How to Reproduce This Project

### Prerequisites

- PostgreSQL 13+
- Python 3.8+

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure .env**: Add your PostgreSQL credentials.
4. **Run ETL**: `python scripts/limpieza.py` and `python scripts/conexion_carga_datos.py`

---

## Assessment Details

- **Program**: Software development (SENA)
- **Author**: Keiner Lara
- **GitHub**: [keiner-lara](https://github.com/keiner-lara)
- **Date**: 2026
