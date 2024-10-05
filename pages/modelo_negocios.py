import streamlit as st
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch
import re
import pandas as pd
from wordcloud import STOPWORDS
from safetensors.torch import load_file
import os
import boto3
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar cliente de S3
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.getenv('AWS_DEFAULT_REGION'))

# Nombre del bucket y nombre del archivo
BUCKET_NAME = 'tfm-modelo'
FILE_KEY = 'model/'
LOCAL_MODEL_PATH = 'model/'

# Crear la carpeta local si no existe
if not os.path.exists(LOCAL_MODEL_PATH):
    os.makedirs(LOCAL_MODEL_PATH)

# Función para descargar todos los archivos de la carpeta 'model/' desde S3
def download_files_from_s3(folder_name):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            file_key = obj['Key']  # Nombre completo del archivo en S3 (incluye la carpeta)
            file_name = file_key.split('/')[-1]  # Nombre del archivo
            if file_name:  # Ignorar las "carpetas vacías" en S3
                local_file_path = os.path.join(LOCAL_MODEL_PATH, file_name)
                # Verificar si el archivo ya existe localmente
                if not os.path.exists(local_file_path):
                    s3.download_file(BUCKET_NAME, file_key, local_file_path)

# Descargar todos los archivos de la carpeta 'model/'
download_files_from_s3(LOCAL_MODEL_PATH)

# Cargar el modelo y el tokenizer
@st.cache_resource
def load_model():
    model_path = LOCAL_MODEL_PATH
    safetensors_file = os.path.join(model_path, "model.safetensors")

    # Verificar si el archivo model.safetensors existe localmente
    if not os.path.exists(safetensors_file):
        st.error(f"El archivo '{safetensors_file}' no se encontró. Asegúrate de que el archivo se haya descargado correctamente.")
        return None, None

    try:
        # Cargar el tokenizer y el modelo usando los archivos descargados
        st.write("Cargando el tokenizer y el modelo...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        state_dict = load_file(safetensors_file)
        model = T5ForConditionalGeneration.from_pretrained(model_path, state_dict=state_dict)
        st.success("Modelo y tokenizer cargados correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        return None, None

    return tokenizer, model


# Definir la función principal de la página
def show_page():
    st.title("Clasificador de Modelos de Negocio")
    
    # Asegurarnos de que 'business_answers' es una lista y no un diccionario
    if 'business_answers' not in st.session_state:
        st.session_state['business_answers'] = []  # Inicializamos como lista

    # Lista de modelos de negocio
    BUSINESS_MODELS = [
        "Software as a Service (SaaS)", "Software as a Service",
        "Inteligencia Artificial y Aprendizaje Automático", "Artificial Intelligence and Machine Learning",
        "Internet de las Cosas (IoT)", "Internet of Things",
        "Ciberseguridad", "Cybersecurity",
        "Fintech", 
        "Healthtech", 
        "E-commerce y Retail Tech", "E-commerce",
        "Edtech", 
        "Blockchain y Criptomonedas", "Blockchain and Cryptocurrencies",
        "Realidad Virtual y Aumentada", "Virtual Reality and Augmented Reality",
        "Robótica y Automatización", "Robotics and Automation",
        "Cleantech y Energía Sostenible", "Cleantech and Sustainable Energy"
    ]

    # Preguntas para el usuario
    QUESTIONS = [
        "¿Cuál es el valor añadido de tu proyecto? ¿Qué problema o necesidad del mercado tecnológico está abordando tu empresa?",
        "¿Cómo describirías al usuario o cliente ideal que se beneficiaría más de tu solución?",
        "En tu opinión, ¿qué hace que tu enfoque sea único en comparación con otras soluciones disponibles en el mercado?",
        "¿Qué desarrollos tecnológicos recientes han influido más en la evolución de tu producto o servicio?",
        "¿De qué manera tu empresa está contribuyendo a un futuro más sostenible o ético en el sector tecnológico?",
        "¿Cuáles son los mayores desafíos que has enfrentado hasta ahora en el desarrollo y crecimiento de tu empresa?",
        "¿Qué tipo de infraestructura o recursos tecnológicos son cruciales para el funcionamiento de tu solución?",
        "¿Cómo ves que tu producto o servicio evolucionará en los próximos 3-5 años en respuesta a las tendencias del mercado?",
        "¿Qué papel juegan los datos y la analítica en tu modelo de negocio y en la toma de decisiones de tu empresa?",
        "¿Qué ingresos tienes previsto para los 3 primeros años? ¿En qué transforma tu propuesta el modelo de negocio de tus clientes?"
    ]

    # Preprocesamiento del texto
    def preprocess_text(text):
        text = re.sub(r'[^\w\s]', '', text)
        words = text.lower().split()
        stop_words = set(STOPWORDS)
        words = [word for word in words if word not in stop_words]
        return ' '.join(words)

  
    # Función para clasificar el modelo de negocio
    def classify_business(text, tokenizer, model, business_models):
        preprocessed_text = preprocess_text(text)
        inputs = tokenizer(f"Classify the business type: {preprocessed_text}", return_tensors="pt", max_length=512, truncation=True)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50, num_return_sequences=5, num_beams=5)

        # Decodificar las predicciones
        decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

        # Mostrar salida cruda para depuración
        st.write(f"Salida del modelo: {decoded_outputs}")

        # Crear lista de modelos con probabilidades
        predicted_models = []
        probability = 1.0  # Iniciar con probabilidad de 1.0
        decay_rate = 0.02  # Definir tasa de decrecimiento

        for decoded_output in decoded_outputs:
            model_name = decoded_output.strip()  # Limpiar el espacio en blanco adicional
            if model_name in business_models:
                predicted_models.append((model_name, probability))
                probability = max(probability - decay_rate, 0)  # Reducir la probabilidad para cada modelo sucesivo

        if len(predicted_models) == 0:
            st.error("No se encontraron predicciones válidas.")
            return []

        # Ordenar por probabilidad y obtener las 5 mejores predicciones
        top_5_predictions = sorted(predicted_models, key=lambda x: x[1], reverse=True)[:5]

        return top_5_predictions

    # Función para mostrar los resultados en una tabla
    def display_classification_table(predictions):
        # Crear un DataFrame a partir de las predicciones
        df = pd.DataFrame(predictions, columns=["Modelo de Negocio", "Probabilidad"])
        # Mostrar la tabla usando Streamlit
        st.table(df)

    # Cargar el modelo y el tokenizer
    tokenizer, model = load_model()

    if tokenizer is None or model is None:
        st.stop()

    if 'step' not in st.session_state:
        st.session_state.step = 0

    # Proceso de preguntas
    if st.session_state.step < len(QUESTIONS):
        st.subheader(f"Pregunta {st.session_state.step + 1} de {len(QUESTIONS)}")
        st.write(QUESTIONS[st.session_state.step])
        user_input = st.text_area("Su respuesta:", height=100, key=f"input_{st.session_state.step}")

        if st.button("Siguiente", key=f"next_{st.session_state.step}"):
            if user_input:
                # Guardar respuestas como una lista
                st.session_state['business_answers'].append(user_input)
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("Por favor, responda la pregunta antes de continuar.")

    # Resumen de respuestas y clasificación
    elif st.session_state.step == len(QUESTIONS):
        st.subheader("Resumen de sus respuestas:")
        for q, a in zip(QUESTIONS, st.session_state['business_answers']):
            st.write(f"**{q}**")
            st.write(a)
            st.write("---")

        if st.button("Clasificar Modelo de Negocio"):
            full_text = " ".join(st.session_state['business_answers'])
            with st.spinner("Clasificando..."):
                try:
                    predictions = classify_business(full_text, tokenizer, model, BUSINESS_MODELS)
                    st.success("Clasificación completada. Aquí están los modelos de negocio más probables:")
                    
                    # Mostrar las 5 predicciones principales en una tabla
                    display_classification_table(predictions)
                    
                    # Almacenar el sector clasificado en st.session_state
                    sector_clasificado = predictions[0][0]  # Tomar la primera predicción
                    st.session_state['sector_clasificado'] = sector_clasificado
                    
                    # Mostrar el sector clasificado
                    st.write(f"Tu modelo de negocio ha sido clasificado como: **{sector_clasificado}**")
                
                except Exception as e:
                    st.error(f"Error al clasificar el modelo de negocio: {e}")

    else:
        st.subheader("Clasificación completada")

    # Mostrar botón para avanzar a la página de generación del informe
    if st.button("Guardar Modelo de Negocio"):
        st.success("Modelo de negocio guardado con éxito. Ve a la página de generación de informes.")
    
    # Botón para reiniciar el cuestionario
    if st.button("Volver a empezar"):
        # Reiniciar todas las variables relevantes en session_state
        st.session_state["step"] = 0
        st.session_state["business_answers"] = []
        st.session_state["sector_clasificado"] = None
        st.experimental_rerun()  # Reinicia la aplicación

