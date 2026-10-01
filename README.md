# Tasa de Suicidios en Argentina (2017-204) y San Luis 

### El suicidio ya es la principal causa de muerte entre adolescentes y jóvenes adultos en Argentina  
 
**Fuente Nacional:** SNIC-SAT (Ministerio de Seguridad)
**Fuente Provincia:** Dirección de Estadística y Censos de San Luis
**Etapas completadas:** Python (Pandas/Matplotlib) · Tableau 

## Contexto y Definiciones

Este proyecto de análisis de datos estudia la tasa de suicidios en Argentina abordando el fenómeno en dos escalas geográficas y temporales distintas. A nivel nacional, se presenta una comparativa de la evolución de las tasas en las 24 provincias (23 + CABA) durante el período 2017–2024. A nivel provincial, el foco se centra en la Provincia de San Luis (que registró la segunda tasa más alta del país), detallando la distribución de casos por departamento, grupo etario y sexo para el período 2017–2022.   

El objetivo es aportar un diagnóstico cuantitativo riguroso a una problemática de alta relevancia social, exponiendo y documentando al mismo tiempo las limitaciones estructurales en la disponibilidad de información pública desagregada. 

* **Tasa de suicidios:** Calculada como la cantidad de casos cada 100.000 habitantes, permitiendo una comparación equitativa entre jurisdicciones de distinto tamaño demográfico.

* **Discrepancia de fuentes:** Coexisten los registros de intervenciones policiales (SNIC) y los certificados médicos de defunción (DEIS), con diferencias de hasta un 27%. Este proyecto utiliza el SNIC-SAT por ser la única fuente nacional actualizada hasta 2024.

## Preguntas que responde este análisis 

El flujo de trabajo estadístico y visual responde a las siguientes interrogantes clave:   

* ¿Cuáles son las provincias con mayor tasa de suicidios en 2024 y cómo evolucionó el promedio nacional desde 2017?   
* ¿En qué año se registró el mayor aumento interanual a nivel país?   
* ¿Cómo se distribuyen geográficamente los casos dentro de San Luis por departamento?   
* ¿Qué brechas existen entre varones y mujeres, y qué franjas etarias concentran la mayor cantidad de casos en la provincia? 

## Hallazgos principales

* **Ranking Nacional 2024:** San Luis registró una tasa de 17,5 suicidios cada 100.000 habitantes, ubicándose como la segunda jurisdicción con mayor incidencia del país, superando ampliamente el promedio nacional (9,8).
* **Concentración geográfica en San Luis:** La inmensa mayoría de los casos provinciales (2017-2022) se concentran en los departamentos de Juan Martín de Pueyrredón y General Pedernera.
* **Brecha de sexo y edad:** La distribución demográfica provincial evidencia una disparidad marcada entre géneros (mayor prevalencia en varones) y una concentración de casos en franjas etarias específicas.
* **Limitación estructural de los datos:** Se identificó un vacío estadístico a nivel departamental desde 2023 en San Luis y una anomalía en los registros de 2025 (por cambios metodológicos en los sistemas de carga en Buenos Aires), obligando a limitar el estudio a series históricas estrictamente comparables.

## Datos utilizados | 1. Fuente Nacional (SNIC-SAT)

|Campo|Detalle|
|-|-|
|Fuente original|cloud-snic.minseg.gob.ar → Informes → SAT → SAT_SS|
|Archivo|Informe_Suicidios_2024.pdf|
|Formato|PDF (Transcripción manual a CSV)|
|Frecuencia|Anual|
|Variable clave|Tasa de suicidios cada 100.000 hab. por provincia|
|Cobertura|24 jurisdicciones (2017-2024)|

## Datos utilizados | 2. Fuente Provincial (San Luis)

|Campo|Detalle|
|-|-|
|Fuente original|estadistica.sanluis.gov.ar → Sociedad → Salud|
|Archivo|Suicidios consumados San Luis y total país. Período 2017-2022|
|Formato|Excel (.xls)|
|Frecuencia|Anual|
|Variable clave|Casos absolutos por departamento, sexo y edad|
|Cobertura|9 departamentos de San Luis (2017-2022)|

## Etapa 1 · Python

### Limpieza y Análisis 

**Procesamiento de datos:** 
Construcción del dataset nacional extrayendo valores directamente del PDF oficial (Tabla 4). Lectura y limpieza de la matriz Excel provincial utilizando `pandas`, abordando formatos inconsistentes y unificando nomenclaturas. Se aplicó la función `melt` para transformar las tablas de formato ancho a largo, garantizando una correcta ingesta temporal en bases de datos y herramientas de visualización.

**Cálculo de métricas:** 
Cálculo de variaciones absolutas y relativas interanuales. Generación de categorías de riesgo ("Muy alta", "Alta", "Media") basadas en desvíos matemáticos sobre la línea de referencia del promedio nacional (9,8).

**Prototipado visual:**  
Implementación de `matplotlib` y constructores de leyendas (`mpatches`) para crear gráficos estáticos con lógica condicional de colores (destacando a San Luis en paleta propia y segmentando al resto de provincias según su posición frente al promedio nacional).

### Scripts disponibles

|Archivo|Descripción|
|-|-|
|`02_notebooks/01_construir_dataset_nacional.py`|Construcción manual de tasaas nacionales y formato largo.|
|`02_notebooks/02_limpiar_san_luis.py`|Limpieza y normalización estructural del Excel provincial.|
|`02_notebooks/03_analisis_nacional.py`|Cálculo de rankings, agregaciones y variaciones con pandas.|
|`02_notebooks/04_analisis_sl.py`|Cálculos enfocados en la provincia de San Luis.|
|`02_notebooks\05_g1_visualizaciones.py`|Gráfico de Ranking 2024 (barras horizontales con referencia).|
|`02_notebooks\05_g2_visualizaciones.py`|Gráfico de Evolución temporal top 8 (líneas múltiples).|
|`02_notebooks\05_g3_visualizaciones.py`|Gráfico de Casos acumulados por departamento en San Luis.|
|`02_notebooks\05_g4_visualizaciones.py`|Gráfico de Pirámide poblacional (edad y sexo con ejes invertidos).|
|`02_notebooks\05_g5_visualizaciones.py`|Gráfico de distribución de casos por franja horaria.|
|`02_notebooks\05_g6_visualizaciones.py`|Gráfico de distribución de casos por lugar de hecho.|

## Estructura del repositorio

```
TasaSuicidios_SanLuis/
├── 01_datos/
│   ├── original/
|   |   └── Informe_Suicidios_2024.pdf          ← SNIC sin modificar
│   │   └── suicidios_san_luis_2017_2022.xlsx   ← Dir. Estadística SL sin modificar
│   └── procesados/
│       └── analisis_completo.csv
|       └── sl_casos_mensuales.csv      
|       └── sl_edad_sexo_anual.csv
|       └── sl_horario.csv 
|       └── sl_lugar_hecho.csv
|       └── sl_por_departamento.csv
|       └── sl_villa_mercedes.csv
|       └── sl_zanjitas.csv
|       └── tasas_nacionales_largo.csv
|       └── tasas_nacionales.csv     
├── 02_notebooks/
│   └── 01_construir_dataset_nacional.py
│   └── 02_limpiar_san_luis.py
│   └── 03_analisis_nacional.py
│   └── 04_analisis_sl.py
│   └── 05_g1_visualizaciones.py
│   └── 05_g2_visualizaciones.py
│   └── 05_g3_visualizaciones.py
│   └── 05_g4_visualizaciones.py
│   └── 05_g5_visualizaciones.py
│   └── 05_g6_visualizaciones.py
├── 03_capturas/
│   └── CP01_dataset_nacional.png
│   └── CP02_dataset_sanluis.png
│   └── CP03a_ranking.png
│   └── CP03b_sanluis_depto.png
│   └── CP04_dashboard_tableau.png
├── 04_outputs/
│   └── G1_ranking_provincial.png
│   └── G2_evolucion_top8.png
│   └── G3_sanluis_por_departamento.png
│   └── G4_piramide_edad_sexo.png
│   └── G5_horario_casos.png
│   └── G6_lugar_hecho.png
├── venv/   ← entorno virtual
└── README.md
```

### Visualizaciones

|Gráfico|Tipo|Pregunta que responde|
|-|-|-|
|Ranking 2024|Barras horizontales condicionales|¿Qué provincias tienen mayor tasa?|
|Evolución 2022-2024|Líneas múltiples con marcadores|Cómo evolucionó la tasa en el tiempo?|
|Departamentos San Luis|Barras horizontales|¿Dónde se concentran los casos absolutos?|
|Edad y Sexo SL|Pirámide poblacional|¿Qué grupos etarios se ven más afectados?|

Los gráficos pueden ser generados mediante los scripts de Python mencionados o visualizados mediante Tableau Public en mi perfil.

### Etapa 2 · Tableau

Dashboard interactivo ensamblado bajo el principio de aislamiento de fuentes de datos. Se conectaron los CSV procesados de forma independiente para las vistas nacionales y provinciales, asegurando la integridad metodológica al no cruzar bases con distinto nivel de agregación temporal. Incluye diseño mediante layout containers en formato mosaico y aclaraciones visibles de limitación estadística. Se encuentra publicado en Tableau Public en el siguiente link:   

https://public.tableau.com/app/profile/mayco.luciano.correa/viz/TasadeSuicidios-AnlisisArgentinaySanLuispordepartamentos/Presentacin

## Herramientas utilizadas

![Excel](https://img.shields.io/badge/Microsoft\_Excel-217346?style=flat\&logo=microsoft-excel\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat&logo=tableau&logoColor=white)

\---

*Proyecto de portafolio de análisis de datos · Etapas 1 y 2 completadas*

