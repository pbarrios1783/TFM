TFM - Plataforma de Recomendación de Inversión y Modelos de Negocio
Descripción del Proyecto
Este proyecto es una plataforma interactiva diseñada para emprendedores e inversores que buscan tomar decisiones basadas en datos sobre modelos de negocio y oportunidades de inversión en España. La aplicación clasifica los modelos de negocio, genera informes personalizados y recomienda la mejor comunidad autónoma para invertir en función de factores económicos, tecnológicos y sociales.

Características Principales
Clasificación de Modelos de Negocio: El usuario completa un cuestionario con preguntas abiertas sobre su modelo de negocio. A través del uso del modelo preentrenado T5 (de Hugging Face), el sistema clasifica automáticamente el tipo de negocio en categorías como SaaS, Fintech, Healthtech, entre otras.

Recomendación de Comunidad Autónoma: La plataforma presenta un cuestionario dinámico basado en factores clave de inversión (población, infraestructura tecnológica, talento disponible, etc.). En función de las respuestas del usuario, se genera una scorecard que recomienda la comunidad autónoma más adecuada para invertir.

Generación de Informes Personalizados: Se generan informes personalizados en tres áreas: el modelo de negocio, un análisis de competidores en el sector, y una descripción de la situación económica y social de la comunidad autónoma recomendada.

Visualización de Datos Geoespaciales: Los usuarios pueden visualizar información clave de las diferentes comunidades autónomas a través de mapas de calor y gráficos interactivos.

Estructura del Proyecto
El proyecto está organizado en varias carpetas y archivos clave:

app.py: Archivo principal que ejecuta la aplicación a través de Streamlit.
data/: Carpeta que contiene los archivos de datos en formato Excel.
imagenes/: Almacena los recursos gráficos como logos o imágenes utilizadas en los informes.
pages/: Subpáginas de la aplicación, incluyendo la clasificación de modelos de negocio y la generación de informes.
templates/: Plantillas de texto utilizadas para la generación de informes.
Instalación y Ejecución
Requisitos Previos
Asegúrate de tener instalado Python 3.7 o superior. También deberás tener las siguientes bibliotecas de Python instaladas:

streamlit
pandas
matplotlib
openai
torch
transformers
fpdf
Puedes instalar todas las dependencias del proyecto con el siguiente comando:

bash
Copy code
pip install -r requirements.txt
Clonar el Proyecto
Clona este repositorio en tu máquina local utilizando el siguiente comando:

bash
Copy code
git clone https://github.com/tu-usuario/tu-repositorio.git
Configuración del Archivo .env
Este proyecto utiliza un archivo .env para almacenar las claves API y otras variables de entorno importantes. Este archivo no está incluido en el repositorio por motivos de seguridad.

Deberás crear un archivo .env en la raíz del proyecto con el siguiente formato:

bash
Copy code
OPENAI_API_KEY=tu_clave_openai
AWS_ACCESS_KEY_ID=tu_clave_aws
AWS_SECRET_ACCESS_KEY=tu_clave_aws_secreta
Ejecución del Proyecto
Después de configurar el entorno, puedes iniciar la aplicación ejecutando el siguiente comando en la terminal:

bash
Copy code
streamlit run app.py
Futuras Mejoras
Implementar un sistema para que los usuarios puedan ponderar manualmente la importancia de cada factor en el scorecard de recomendaciones.
Ampliar la generación dinámica de informes utilizando OpenAI GPT en más áreas de la plataforma.
Migrar el sistema de almacenamiento de archivos a una base de datos en la nube para permitir una mayor escalabilidad.
Contribuciones
Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

Haz un fork del repositorio.
Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
Haz tus cambios y realiza un commit (git commit -m 'Agrega nueva funcionalidad').
Sube tus cambios al repositorio (git push origin feature/nueva-funcionalidad).
Abre un Pull Request para revisión.
