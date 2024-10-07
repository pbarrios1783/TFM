# TFM - Inversión Tecnológica en España

## Descripción del Proyecto
Este proyecto es una plataforma interactiva diseñada para emprendedores e inversores que buscan tomar decisiones basadas en datos sobre modelos de negocio y oportunidades de inversión en España. La aplicación clasifica los modelos de negocio, genera informes personalizados y recomienda la mejor comunidad autónoma para invertir en función de factores económicos, tecnológicos y sociales.

## Características Principales
### 1. Clasificación de Modelos de Negocio: 
El usuario completa un cuestionario con preguntas abiertas sobre su modelo de negocio. A través del uso del modelo preentrenado T5 (de Hugging Face), el sistema clasifica automáticamente el tipo de negocio en categorías como SaaS, Fintech, Healthtech, entre otras.

### 2. Recomendación de Comunidad Autónoma: 
La plataforma presenta un cuestionario dinámico basado en factores clave de inversión (población, infraestructura tecnológica, talento disponible, etc.). En función de las respuestas del usuario, se genera una scorecard que recomienda la comunidad autónoma más adecuada para invertir.

### 3. Generación de Informes Personalizados: 
Se generan informes personalizados en tres áreas: el modelo de negocio, un análisis de competidores en el sector, y una descripción de la situación económica y social de la comunidad autónoma recomendada.

### 4. Visualización de Datos Geoespaciales: 
Los usuarios pueden visualizar información clave de las diferentes comunidades autónomas a través de mapas de calor y gráficos interactivos.

## Estructura del Proyecto
El proyecto está organizado en varias carpetas y archivos clave:

- `app.py`: Archivo principal que ejecuta la aplicación a través de Streamlit.
- `data/`: Carpeta que contiene los archivos de datos en formato Excel.
- `imagenes/`: Almacena los recursos gráficos como logos o imágenes utilizadas en los informes.
- `pages/`: Subpáginas de la aplicación, incluyendo la clasificación de modelos de negocio y la generación de informes.
- `templates/`: Plantillas de texto utilizadas para la generación de informes.

## Instalación y Ejecución
### Requisitos Previos
Asegúrate de tener instalado Python 3.7 o superior. También deberás tener las siguientes bibliotecas de Python instaladas:

- `streamlit`
- `pandas`
- `matplotlib`
- `openai`
- `torch`
- `transformers`
- `fpdf`
  
Puedes instalar todas las dependencias del proyecto con el siguiente comando:
![image](https://github.com/user-attachments/assets/9606b6a9-35ed-4dd6-bfd2-ca65efd55a29)


## Clonar el Proyecto
Clona este repositorio en tu máquina local utilizando el siguiente comando:
![image](https://github.com/user-attachments/assets/e11f2f61-d2e2-473e-a390-f6c7af3705cf)

## Configuración del Archivo `.env`
Este proyecto utiliza un archivo ``.env` para almacenar las claves API y otras variables de entorno importantes. Este archivo no está incluido en el repositorio por motivos de seguridad.

Deberás crear un archivo `.env` en la raíz del proyecto con el siguiente formato:
![image](https://github.com/user-attachments/assets/634d5372-38ed-41a8-95dd-c996bb5a113f)

## Ejecución del Proyecto
Después de configurar el entorno, puedes iniciar la aplicación ejecutando el siguiente comando en la terminal:
![image](https://github.com/user-attachments/assets/e49cf970-6123-4097-973a-acb84a9ddd87)

## Futuras Mejoras
* Implementar un sistema para que los usuarios puedan ponderar manualmente la importancia de cada factor en el scorecard de recomendaciones.
* Ampliar la generación dinámica de informes utilizando OpenAI GPT en más áreas de la plataforma.
* Migrar el sistema de almacenamiento de archivos a una base de datos en la nube para permitir una mayor escalabilidad.

## Licencia
Este proyecto está bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Puedes ver más detalles en el archivo `LICENSE`.
