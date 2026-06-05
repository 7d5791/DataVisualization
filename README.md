# VeReMi Viz - Análisis de Ataques en VANETs

Visualización interactiva de datos para el análisis de ataques de privacidad y seguridad en redes vehiculares (VANETs), utilizando datos procesados del dataset **VeReMi Multiattack** a partir de escenarios de simulación InTAS.

[Visualización](https://raw.githubusercontent.com/7d5791/DataVisualization/main/web/index.html)  
*Captura de la visualización interactiva*

## Descripción del Proyecto

Este proyecto forma parte de la **Parte II** de la asignatura **Visualización de Datos** (M2.859 - UOC). 

El objetivo principal es responder a cuatro preguntas de investigación sobre riesgos de privacidad en redes vehiculares mediante una visualización web interactiva que combina:

- Una **estructura narrativa** guiada por preguntas de investigación.
- Un **explorador interactivo** potente con filtros coordinados.

## Demo en Vivo

Puedes acceder a la visualización directamente aquí:

**→ [Ver Visualización en GitHub Pages](https://7d5791.github.io/DataVisualization/web/index.html)**

## ✨ Características

- Visualización de la **distribución espacial** de mensajes normales y de ataque.
- Exploración de **trayectorias** de vehículos individuales.
- Análisis de la relación entre **latencia, velocidad y tipo de ataque**.
- Filtros interactivos por **escenario** (Highway / Urban), **densidad** y **tipo de ataque**.
- Diseño semántico con colores diferenciados (azul = normal, rojo = ataque).
- Publicación estática en GitHub Pages (sin necesidad de servidor).

## 📁 Estructura del Proyecto

DataVisualization/
├── data/                          # Datos originales y procesamiento
│   ├── main.py
│   └── veremi_multiattack_sample.csv
├── figures/                       # Gráficos estáticos para el informe
│   ├── 01_distribucion_espacial.png
│   ├── 02_ejemplos_trayectorias.png
│   └── ...
├── web/                           # Visualización web interactiva
│   ├── index.html
│   └── sample_data.json
├── README.md
└── LICENSE


## Tecnologías Utilizadas

- **HTML5 + Tailwind CSS** (CDN)
- **Plotly.js** (visualizaciones interactivas)
- **Python** (procesamiento de datos con `pandas`, `numpy` y `seaborn`)
- **GitHub Pages** (publicación)

## Procesamiento de Datos
Los datos fueron procesados mediante el script main.py, que:

Lee los archivos JSON de los escenarios InTAS.
Enriquece los datos con variables como latency, speed_kmh, scenario_type, density y attack_label.
Genera una muestra representativa para uso en web.

## Licencia
Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

Cristhian Iza
Universitat Oberta de Catalunya (UOC)
