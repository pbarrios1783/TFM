import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Cargar los datos
@st.cache_data
def load_data():
    try:
        # Cargar los datos
        df = pd.read_excel("./data/df_final.xlsx")
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

df = load_data()

def show_page():
    st.title("Cuestionario de Inversión: Scorecard y Ranking Regional")
    
    if df is None:
        return  # Si no se cargó el archivo correctamente, no continuamos

    # Lista de preguntas del cuestionario con sus variables asociadas
    questions = [
        {"question": "¿Es importante tener una gran y diversa población para su inversión?", "key": "Nº Habitantes"},
        {"question": "¿Considera que un alto PIB per cápita es fundamental para el éxito de su inversión?", "key": "PIB per cápita (%)"},
        {"question": "¿Es crucial contar con una cobertura de fibra óptica para su negocio?", "key": "Fibra Hasta La Casa (%)"},
        {"question": "¿Es esencial tener una cantidad significativa de centros de procesamiento de datos (CPD)?", "key": "Nº Centros de Datos"},
        {"question": "¿Valora la presencia de un alto Nº Universidades en la región?", "key": "Nº Universidades"},
        {"question": "¿Es importante contar con un alto Nº de Egresados tecnológicos?", "key": "Nº de Egresados"},
        {"question": "¿Es esencial la calidad y el rendimiento universitario para su inversión?", "key": "Éxito Universitario (%)"},
        {"question": "¿Es importante tener un costo laboral promedio competitivo?", "key": "Costo Laboral Promedio"},
        {"question": "¿Es clave para su negocio un alto gasto en investigación y desarrollo interno?", "key": "Gasto en I+D (%)"},
        {"question": "¿Valora la presencia de un número significativo de aceleradoras?", "key": "Nº Aceleradoras"},
        {"question": "¿Prefiere invertir en una comunidad con una alta disponibilidad de incubadoras?", "key": "Nº Incubadoras"},
        {"question": "¿Es importante la cantidad de parques tecnológicos en la región?", "key": "Nº Parques Tecnológicos"},
        {"question": "¿Es esencial la presencia de centros tecnológicos en la comunidad?", "key": "Nº Centros Tecnológicos"},
        {"question": "¿Es importante tener subsidios disponibles para la innovación en la comunidad?", "key": "Nº Subsidios"},
        {"question": "¿Prefieres invertir en comunidades autónomas con menos impuestos propios adicionales?", "key": "Nº Impuestos"},
        {"question": "¿Es relevante para su inversión una baja tasa de criminalidad?", "key": "Criminalidad (%)"},
        {"question": "¿Valora servicios de salud de alta calidad en la región?", "key": "Servicios de Salud (%)"},
        {"question": "¿Es importante un alto nivel de asistencia a eventos culturales y recreativos?", "key": "Asistencia de Eventos (%)"},
        {"question": "¿Es clave para su inversión un alto índice de confianza en el sistema político?", "key": "Índice de Confianza del Sistema Político"},
        {"question": "¿Considera fundamental un sistema judicial confiable?", "key": "Índice de Confianza Judicial"},
        {"question": "¿Es relevante una alta tasa de calidad de vida en la comunidad?", "key": "Calidad de Vida (%)"},
        {"question": "¿Valora un alto índice de satisfacción con el entorno en la región?", "key": "Índice de Satisfacción del Entorno"},
        {"question": "¿Es esencial para su negocio un alto índice de confianza empresarial?", "key": "Índice de Confianza Empresarial"},
        {"question": "¿Es importante evitar regiones con un alto número de empresas disueltas?", "key": "Nº Empresas Disueltas"},
        {"question": "¿Prefiere invertir en una comunidad con un alto número de empresas constituidas?", "key": "Nº Empresas Constituidas"},
    ]

    # CSS personalizado para las cartas de preguntas
    st.markdown(
        """
        <style>
        .question-card {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .question-card h3 {
            color: black;
        }
        .question-card p {
            font-size: 18px;
            color: black;
        }
        .stButton>button {
            background-color: #39FF14;
            color: black;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #145a86;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Función para mostrar una tarjeta por cada pregunta con estilo personalizado
    def show_question(index, answers):
        question = questions[index]
        st.markdown(
            f"""
            <div class="question-card">
                <h3>Pregunta {index + 1}</h3>
                <p>{question['question']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        # Opciones de respuesta (Sí o No)
        answer = st.radio("", ("Sí", "No"), key=question["key"])
        
        # Guardamos la respuesta seleccionada
        answers[question["key"]] = answer == "Sí"

    # Función para calcular los pesos basados en las respuestas
    def adjust_weights(responses):
        weights = {
            'Fibra Hasta La Casa (%)': 5,
            'PIB per cápita (%)': 5,
            'Nº Centros de Datos': 5,
            'Nº Universidades': 5,
            'Nº de Egresados': 5,
            'Éxito Universitario (%)': 5,
            'Nº Habitantes': 5,
            'Costo Laboral Promedio': 5,
            'Gasto en I+D (%)': 5,
            'Nº Aceleradoras': 5,
            'Nº Incubadoras': 5,
            'Nº Parques Tecnológicos': 5,
            'Nº Centros Tecnológicos': 5,
            'Nº Subsidios': 5,
            'Nº Impuestos': 5,
            'Criminalidad (%)': 5,
            'Servicios de Salud (%)': 5,
            'Asistencia de Eventos (%)': 5,
            'Índice de Confianza del Sistema Político': 5,
            'Índice de Confianza Judicial': 5,
            'Calidad de Vida (%)': 5,
            'Índice de Satisfacción del Entorno': 5,
            'Índice de Confianza Empresarial': 5,
            'Nº Empresas Disueltas': 5,
            'Nº Empresas Constituidas': 5
        }
        
        for key, value in responses.items():
            if key == "Nº Impuestos" and value:  # Si el inversor prefiere menos impuestos
                weights[key] -= 5  # Damos más importancia a las comunidades con menos impuestos
            elif value:  # Si el inversor responde "Sí" a cualquier otra pregunta
                weights[key] += 5
    
        return weights

    # Función para calcular la scorecard y mostrar los resultados
    def calculate_scorecard(weights):
        
        # Normalizar los datos para que todas las columnas estén en la misma escala (0-100)
        normalized_df = df.copy()
        for column in normalized_df.columns[1:]:
            normalized_df[column] = (normalized_df[column] - normalized_df[column].min()) / (normalized_df[column].max() - normalized_df[column].min()) * 100
        
        # Calcular la puntuación total ponderada para cada comunidad
        score_df = normalized_df.copy()
        score_df['total_score'] = 0
        
        for column in weights:
            score_df['total_score'] += score_df[column] * weights[column] / 100
        
        # Ordenar las comunidades por puntuación total
        score_df = score_df.sort_values(by='total_score', ascending=False)
        
        # Mostrar el DataFrame de puntuación
        score_df = score_df[['Comunidad Autónoma', 'total_score'] + list(weights.keys())]
        
        # Redondear las cifras del df
        score_df[[
'total_score',
'PIB per cápita (%)',
'Gasto en I+D (%)',
'Nº Subsidios',
'Índice de Confianza del Sistema Político',
'Índice de Confianza Judicial',
'Fibra Hasta La Casa (%)',
'Nº Habitantes',
'Nº Centros de Datos',
'Nº Universidades',
'Nº de Egresados',
'Éxito Universitario (%)',
'Nº Aceleradoras',
'Nº Impuestos',
'Costo Laboral Promedio',
'Nº Centros Tecnológicos',
'Nº Incubadoras',
'Nº Parques Tecnológicos',
'Criminalidad (%)',
'Servicios de Salud (%)',
'Asistencia de Eventos (%)',
'Calidad de Vida (%)',
'Índice de Satisfacción del Entorno',
'Índice de Confianza Empresarial',
'Nº Empresas Disueltas',
'Nº Empresas Constituidas',

       ]] = score_df[[
'total_score', 
'PIB per cápita (%)',
'Gasto en I+D (%)',
'Nº Subsidios',
'Índice de Confianza del Sistema Político',
'Índice de Confianza Judicial',
'Fibra Hasta La Casa (%)',
'Nº Habitantes',
'Nº Centros de Datos',
'Nº Universidades',
'Nº de Egresados',
'Éxito Universitario (%)', 
'Nº Aceleradoras',
'Nº Impuestos',
'Costo Laboral Promedio',
'Nº Centros Tecnológicos',
'Nº Incubadoras',
'Nº Parques Tecnológicos',
'Criminalidad (%)',
'Servicios de Salud (%)',
'Asistencia de Eventos (%)',
'Calidad de Vida (%)',
'Índice de Satisfacción del Entorno',
'Índice de Confianza Empresarial',
'Nº Empresas Disueltas',
'Nº Empresas Constituidas',   
    
]].round(0).astype(int)
        
        # Guardar el df
        score_df.to_excel('./data/total_score.xlsx', index=False, engine='openpyxl')  
        
        
        texto = """      
        La puntuación total (total_score) se calcula asignando un peso a cada variable clave según su importancia relativa para la inversión. Estas variables se normalizan para garantizar que todas estén en la misma escala, lo que permite compararlas equitativamente. 
        
        Luego, cada variable se multiplica por su peso y se suma al total, resultando en la puntuación global que refleja la capacidad de una comunidad autónoma para atraer inversiones en tecnología e innovación.
        """
        
        # Mostrar el scorecard en streamlit
        st.write("Scorecard de Comunidades Autónomas para Inversión en Tecnología e Innovación")
        st.dataframe(score_df)
        st.write(texto)
                    
        # Control del índice de la pregunta actual
    if "question_index" not in st.session_state:
        st.session_state["question_index"] = 0

    if "answers" not in st.session_state:
        st.session_state["answers"] = {}

    index = st.session_state["question_index"]
    answers = st.session_state["answers"]
    
    # Si todavía hay preguntas por responder, las mostramos una por una
    if index < len(questions):
        show_question(index, answers)

        # Botón para avanzar a la siguiente pregunta
        if st.button("Siguiente"):
            st.session_state["question_index"] += 1  # Avanzamos a la siguiente pregunta
            st.experimental_rerun()  # Refrescamos la página para cargar la siguiente pregunta
    else:
        # Si ya terminamos el cuestionario, mostramos el botón para calcular la puntuación
        st.success("¡Gracias por completar el cuestionario!")
        
        # Botón para calcular la scorecard
        if st.button("Mostrar Resultados"):
            # Ajustar los pesos basados en las respuestas
            weights = adjust_weights(answers)
            # Calcular y mostrar la scorecard
            calculate_scorecard(weights)

        # Botón para reiniciar el cuestionario
        if st.button("Volver a empezar"):
            st.session_state["question_index"] = 0
            st.session_state["answers"] = {}
            st.experimental_rerun()  # Reinicia la aplicación
            

    
   