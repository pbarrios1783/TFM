# Importamos las librerías
import streamlit as st
import openai
from fpdf import FPDF
import base64


# Obtenemos la clave de la API de OpenAI desde una variable de entorno
openai.api_key = st.secrets('OPENAI_API_KEY')

if openai.api_key is None:
    st.error("No se encontró la clave de la API de OpenAI. Verifica el archivo .env.")

# Cargamos la plantilla desde un archivo de texto
def load_template():
    try:
        with open('./templates/business_template.txt', 'r', encoding='utf-8') as file:
            template = file.read()
        return template
    except FileNotFoundError:
        st.error("No se pudo cargar la plantilla del informe.")
        return None

# Creamos la función para que GPT ajuste el template basado en las respuestas del modelo de negocio
def ajustar_informe_con_gpt(template, respuestas):
    prompt = f"""
    Aquí tienes una plantilla de informe sobre un modelo de negocio. Ajusta esta plantilla basándote en las respuestas que el usuario ha proporcionado. Puedes agregar o modificar detalles para que el informe sea más relevante según las respuestas.

   
    {template}

    Respuestas del Modelo de Negocio:
    Descripción del Modelo de Negocio: {respuestas[0]}
    Valor Añadido: {respuestas[1]}
    Enfoque Único: {respuestas[2]}
    Tecnologías Clave: {respuestas[3]}
    Estrategia de Crecimiento y Evolución: {respuestas[4]}
    Recursos Tecnológicos: {respuestas[5]}
    Proyección Financiera: {respuestas[6]}

    Genera el informe final basándote en esta plantilla y las respuestas proporcionadas.
    """

    # Llamada a la API de OpenAI para que genere el informe ajustado
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a generar informes de modelos de negocio personalizados basados en plantillas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.3
    )

    return response['choices'][0]['message']['content'].strip()

# Función para generar el PDF con formato
def generar_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()

    # Registrar la fuente Poppins
    pdf.add_font('Poppins', '', 'Poppins-Regular.ttf', uni=True)
    pdf.add_font('Poppins', 'B', 'Poppins-Bold.ttf', uni=True)
    

    # Usar la fuente Poppins en el PDF
    pdf.set_font('Poppins', 'B', 16)

    # Añadimos el logo 
    logo_path = "./imagenes/3.png"  # Ruta del logo
    pdf.image(logo_path, x=10, y=8, w=33)

    # Título del informe
    pdf.ln(40)  # Espacio después del logo
    pdf.cell(200, 10, txt="Modelo de Negocio", ln=True, align='C')

    # Añadir contenido del informe con Poppins regular
    pdf.set_font('Poppins', '', 12)

    # Establecer márgenes personalizados (izquierda, arriba, derecha)
    pdf.set_margins(left=15, top=10, right=15)
    pdf.ln(10)
    pdf.multi_cell(0, 10, report_text)

    # Guardar el PDF en memoria
    pdf_output = pdf.output(dest='S').encode('latin1')

    return pdf_output

# Creamos la función para descargar el PDF con estilo personalizado
def descargar_pdf(pdf_output, filename):
    b64_pdf = base64.b64encode(pdf_output).decode('latin1')

    button_css = """
    <style>
        .download-button {
            background-color: #39FF14;
            color: black;
            padding: 10px 20px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            display: inline-block;
        }
        .download-button:hover {
            background-color: #32CD32;
        }
        .download-button:visited, .download-button:link {
            color: black;
        }
    </style>
    """

    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}" class="download-button">Descargar PDF</a>'
    
    st.markdown(button_css + href, unsafe_allow_html=True)

# Mostramos en la aplicación de Streamlit
def show_page():
    st.title("Modelo de Negocio")

    # Cargar la plantilla
    template = load_template()
    if not template:
        return

    # Verificamos si las respuestas ya están en st.session_state
    if 'business_answers' in st.session_state and isinstance(st.session_state['business_answers'], list):
        respuestas = st.session_state['business_answers']

        if st.button("Generar Informe"):
            # Generar el informe usando GPT
            informe = ajustar_informe_con_gpt(template, respuestas)
            
            # Mostrar el informe generado
            st.text_area("Informe Generado", value=informe, height=400)

            # Generar el PDF con el informe
            pdf_output = generar_pdf(informe)

            # Añadir botón de descarga con estilo
            descargar_pdf(pdf_output, "modelo_negocio.pdf")
    else:
        st.error("No hay respuestas cargadas. Por favor, completa el formulario del modelo de negocio primero.")

## Ejecutar la aplicación de Streamlit
if __name__ == '__main__':
    show_page()
