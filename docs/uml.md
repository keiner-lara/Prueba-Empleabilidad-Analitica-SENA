# Diagramas UML (Guía de Entrega)

## 1. Diagrama de Casos de Uso
**Actores:** Analista de datos, Stakeholder  
**Casos de uso:** Limpiar datos, Cargar a BD, Consultar KPIs, Ver dashboard, Ver portal.

![Diagrama de Casos de Uso](diagrams/uml_Diagrama_Casos_De_Uso.png)

## 2. Diagrama de Clases
Componentes (Clases) sugeridos:
- Limpieza (Python)
- Base de datos (PostgreSQL)
- BI (Power BI)
- Portal Web (HTML/CSS)

![Diagrama de Clases](diagrams/uml_Diagrama_De_Clases.png)

## 3. Diagrama de Secuencia
Flujo de eventos:
1. Cargar datos crudos  
2. Limpiar y validar  
3. Exportar `Datos_limpio.csv`  
4. Cargar a BD  
5. Consultar KPIs  
6. Visualizar y publicar en portal

![Diagrama de Secuencia](diagrams/uml_Diagrama_De_Secuencia.png)

> Nota: Estos diagramas se pueden elaborar en Draw.io o Lucidchart.
