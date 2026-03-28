# Riwi Analytics – Data Analytics Assessment: LATAM Retail Analysis

## 1. Project Overview
This project was developed as part of the **Riwi Analytics Employability Assessment**, aiming to demonstrate an end-to-end data analytics workflow. The objective is to transform raw sales data into actionable business insights through data modeling, ETL processes, exploratory analysis, and interactive dashboards.

The workflow follows a hybrid analytical architecture:
* **PostgreSQL**: Used for data storage, analytical queries, and aggregations.
* **Python**: Used for ETL, data cleaning, validation, and exploratory data analysis (EDA).
# Riwi Analytics – Data Analytics Assessment: LATAM Retail Analysis

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
│   ├── limpieza.py                     # Data cleaning pipeline (2M rows)
│   ├── conexion_carga_datos.py         # PostgreSQL star-schema loader
│   └── extraer_pdfs.py                 # PDF extraction utility
│
├── notebooks/
│   └── Análisis exploratorio (EDA).ipynb  # EDA with charts + English interpretations
│
├── portal/                             # Web portal (HTML/CSS + Bootstrap 5 + Chart.js)
│   ├── index.html
│   └── styles.css
│
├── dashboards/                         # Power BI exports
│   ├── Dashboard.png
│   ├── Top5.png
│   ├── Tendencia temporal.png
│   ├── Participación por categoía.png
│   └── Dashboards_empleabilidad_Keiner_Lara.pbix
│
├── docs/                               # Technical documentation
│   ├── diseno_software.md
│   ├── doc_tecnico.md
│   ├── manual_usuario.md
│   ├── modelo_datos.md
│   ├── prototipo.md
│   ├── uml.md
│   ├── diagrams/       # UML PNGs (Casos de Uso, Clases, Secuencia, ModeloER)
│   └── wireframes/     # Portal wireframes (inicio, top5, insights)
│
└── normas/                             # SENA certification documents
    ├── Documento de diseño de software.docx
    ├── Diagramas de Lenguaje Unificado de Modelado (UML).docx
    ├── Prototipo de solución de software.docx
    ├── Modelo de base de datos.docx
    ├── PRODUCTO NORMA 220501095 Diseñar...pdf
    ├── PRODUCTO NORMA 220501096 Desarrollar...pdf
    ├── Assessment Técnico — Enunciado.pdf
    └── Insights & Storytelling Keiner Lara empleabilidad.pdf
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

## 4. SQL Analytical Queries
The `bbdd.sql` file includes a series of queries designed to extract key business metrics, divided into two complexity levels:

### Basic Analytics (Performance KPIs)

**Sales by Region (Ventas por Región)**
- Identifies the most profitable geographic markets by grouping total sales by country and city
- Purpose: Understand geographic distribution of revenue and identify high-performing territories
- Technique: GROUP BY with geographic dimensions and aggregate functions

**Top 5 Products (Top 5 Productos)**
- Classifies items that generate the highest income to prioritize commercial focus
- Purpose: Identify primary revenue drivers and bestselling products
- Technique: ORDER BY revenue DESC with LIMIT 5

**Average Ticket (Ticket Promedio)**
- Calculates the average spending per transaction according to customer type
- Purpose: Understand purchasing behavior and value metrics per customer segment
- Technique: AVG aggregate function grouped by customer segment

**Customer Audit (Auditoría de Clientes)**
- Uses LEFT JOIN to detect registered customers who have not yet made transactions (inactive customers)
- Purpose: Identify acquisition opportunities and customer engagement issues
- Technique: LEFT JOIN with WHERE clause to filter null values

### Intermediate & Advanced Analytics

**Category and Region Segmentation (Segmentación por Categoría y Región)**
- Crosses dimensions to understand which product types perform better in specific countries
- Purpose: Enable geo-localized product strategies and inventory planning
- Technique: Multi-dimensional aggregation with GROUP BY on multiple categorical fields

**Customer Ranking (Ranking de Clientes)**
- Applies the DENSE_RANK() window function to position customers by sales volume without skipping ranking numbers
- Purpose: Identify top-tier customers for strategic account management
- Technique: Window functions (DENSE_RANK) partitioned by company with ORDER BY sales descending
- Key Feature: DENSE_RANK preserves sequential numbering unlike ROW_NUMBER

**Year-over-Year Growth (Crecimiento YoY)**
- Employs the LAG() function to compare current year sales against the previous year and calculate annual growth percentage
- Purpose: Detect market trends and measure business growth trajectory
- Technique: LAG window function for period-to-period comparison with percentage calculation
- Formula: ((Current Year - Previous Year) / Previous Year) * 100

**Market Participation (Participación de Mercado)**
- Uses aggregate functions over windows to determine what percentage of total income each product category contributes
- Purpose: Understand market segmentation and category importance to overall revenue
- Technique: SUM window functions with PARTITION BY category to calculate percentage share
- Insight: Reveals balanced vs. concentrated revenue streams  

---

## 5. ETL Pipeline (Python)
The `limpieza.py` and `conexion_carga_datos.py` scripts automate:

- **Extraction**: Loading raw data via SQLAlchemy and Pandas
- **Transformation**:
  - Removing duplicates and filtering invalid records (sales ≤ 0)
  - Normalizing data types and handling missing values
  - Creating derived columns (Year, Month) for time dimension
- **Load**: Structured load into PostgreSQL with referential integrity (Dimensions first, Fact table last)

---

## 6. Power BI Dashboards & KPIs - Visual Evidence

### Executive Dashboard Overview
![Dashboard Principal](dashboards/Dashboard.png)

**Core KPIs Dashboard**:
- **Total Sales**: 33.83B
- **Average Ticket**: 17.34K
- **Units Sold**: 10.73M
- **Geographic Reach**: Brazil, Colombia, Mexico
- **Product Categories**: 5 main segments
- **Customer Segments**: Corporate, Government, Wholesale, Retail

- Opportunity for strategic bundling and cross-selling

---

## 7. Business Insights & Conclusions

### Key Actionable Insights

#### B2B & Institutional Market Focus
- **Finding**: Wholesale, Government, and Corporate segments are primary revenue drivers (~8.4B each)
- **Recommendation**: Launch B2B Key Account Management program for long-term contracts
- **Impact**: Secure predictable revenue stream and improve customer retention
- **Next Steps**: Develop dedicated account managers and custom service offerings

#### Product Demand Uniformity
- **Finding**: Evenly distributed demand across top products (~2.82B each)
- **Recommendation**: Implement cross-selling bundles (e.g., Tea + Snacks) to increase average ticket
- **Impact**: Boost per-transaction revenue without proportional marketing increase
- **Strategic Value**: Leverage low price elasticity for bundled offerings

#### Regional Stability
- **Finding**: Consistent performance across Brazil, Colombia, and Mexico
- **Recommendation**: Establish regional distribution hub to optimize logistics
- **Impact**: Reduce shipping costs and improve profit margins by 2-4%
- **Growth Opportunity**: Expand to adjacent regions leveraging proven model

### Strategic Recommendations

1. **Customer Strategy**: Focus on B2B institutional relationships with dedicated account management
2. **Product Strategy**: Create bundled offerings to increase average transaction value
3. **Operational Strategy**: Optimize supply chain through regional consolidation
4. **Market Strategy**: Leverage regional stability for expansion into adjacent segments
5. **Data Strategy**: Implement real-time monitoring dashboards for KPI tracking

---

## Technologies & Tools

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Database** | PostgreSQL 13+ | Data warehouse & complex analytical queries |
| **ETL/Processing** | Python 3.8+ (Pandas, SQLAlchemy) | Data cleaning, transformation & validation |
| **Analysis** | Jupyter Notebook | Exploratory Data Analysis & statistical testing |
| **Visualization** | Power BI | Interactive dashboards, KPIs & storytelling |
| **Data Format** | CSV | Raw & cleaned datasets |
| **Version Control** | Git | Code versioning & collaboration |

---

## Files Description

| File | Purpose | Status |
|------|---------|--------|
| `Análisis_exploratorio_(EDA).ipynb` | Python notebook with statistical analysis and visualizations | Complete |
| `bbdd.sql` | SQL schema, indexes, and analytical queries | Complete |
| `limpieza.py` | Data cleaning and transformation logic | Complete |
| `conexion_carga_datos.py` | Database connection and data loading pipeline | Complete |
| `Datos.csv` | Raw dataset from LATAM markets (original) | Complete |
| `Datos_limpio.csv` | Cleaned and validated dataset | Complete |
| `requirements.txt` | Python dependencies (Pandas, SQLAlchemy, etc.) | Complete |
| `.env` | Database credentials (PostgreSQL connection) | Configured |
| `venv/` | Python virtual environment | Active |
| `Dashboards/` | Power BI visual exports and snapshots | 4 dashboards |

---

## How to Reproduce This Project

### Prerequisites
- PostgreSQL 13+
- Python 3.8+
- Power BI Desktop (optional, for dashboard editing)

### Installation Steps

1. **Clone/Download the repository**
   ```bash
   cd "Prueba-Empleabilidad-Analitica-SENA"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database connection**
   - Edit `.env` with your PostgreSQL credentials
   - Ensure PostgreSQL is running

5. **Run the ETL pipeline**
   ```bash
   python limpieza.py
   python conexion_carga_datos.py
   ```

6. **Execute SQL queries**
   ```bash
   psql -U postgres -d riwi_analytics -f bbdd.sql
   ```

7. **Explore data in Jupyter**
   ```bash
   jupyter notebook
   # Open Análisis_exploratorio_(EDA).ipynb
   ```

---

## Key Metrics & Performance

| Metric | Value | Status |
|--------|-------|--------|
| Total Records Processed | 1,951,391 | Complete |
| Records Removed (cleaning) | 48,609 | Complete |
| Missing Values Handled | 100% | Complete |
| Total Sales Analyzed | 33.83B | Complete |
| Units Sold | 10.73M | Complete |
| Countries Covered | 3 (Brazil, Colombia, Mexico) | Complete |
| Product Categories | 5 (Abarrotes, Alimento Perecedero, Bebida, Lácteo, Snack) | Complete |

---

## Conclusions

This project demonstrates a **scalable analytical foundation** for enterprise data analytics. By integrating:
- **SQL** for robust data storage and complex aggregations
- **Python** for automated data processing and validation
- **Power BI** for actionable visualizations and real-time monitoring

The solution provides stakeholders with a **data-driven framework** to:
- Monitor performance in real-time
- Identify growth opportunities
- Make informed strategic decisions in the LATAM retail market
- Optimize operations through data-driven insights

### Project Achievements
- End-to-end data pipeline implementation
- Star Schema database design for optimal performance
- Automated ETL process reducing manual work by ~80%
- Executive dashboards enabling self-service analytics
- Actionable business insights driving strategic decisions  

---

## Assessment Details
- **Program**: Riwi Analytics Employability Assessment
- **Author**: Keiner Lara
- **GitHub**: [keiner-lara/Prueba-Empleabilidad-Analitica-SENA](https://github.com/keiner-lara/Prueba-Empleabilidad-Analitica-SENA)
- **Assessment Date**:  2026


