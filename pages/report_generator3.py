# Importamos las librerías
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# Cargamos los datos de la comunidad y el score
df_final = pd.read_excel("./data/df_final.xlsx")
df_score = pd.read_excel("./data/total_score.xlsx")

# Cargamos las plantillas desde archivos de texto
def load_templates():
    try:
        with open('./templates/community_template.txt', 'r', encoding='utf-8') as file:
            template1 = file.read()
        with open('./templates/recomendacion_community_template.txt', 'r', encoding='utf-8') as file:
            template2 = file.read()
        return template1, template2
    except FileNotFoundError:
        st.error("No se pudieron cargar las plantillas.")
        return None, None

# Creamos la función para generar el PDF con Poppins y el logo
def generate_pdf(report_text, community_data):
    pdf = FPDF()
    pdf.add_page()

    # Registrar las fuentes Poppins
    pdf.add_font('Poppins', '', 'Poppins-Regular.ttf', uni=True)
    pdf.add_font('Poppins', 'B', 'Poppins-Bold.ttf', uni=True)

    # Usar la fuente Poppins
    pdf.set_font('Poppins', 'B', 16)

    # Añadir el logo
    logo_path = "./imagenes/3.png" 
    pdf.image(logo_path, x=10, y=8, w=33)

    # Título del informe
    pdf.ln(40)  # Espacio después del logo
    pdf.cell(200, 10, txt=f"Informe de Inversión - {community_data['Comunidad Autónoma']}", ln=True, align='C')

    # Cambiar a la fuente regular
    pdf.set_font('Poppins', '', 12)

    # Establecer márgenes personalizados
    pdf.set_margins(left=15, top=10, right=15)
    pdf.ln(10)

    # Estructurar el reporte en párrafos
    paragraphs = report_text.split("\n\n")  
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln()

    # Guardar el PDF en memoria
    pdf_output = pdf.output(dest='S').encode('latin1')

    return pdf_output

# Función para crear un botón de descarga HTML con CSS personalizado
def download_button_custom(data, filename, label):
    # Convertir el archivo PDF a base64 para permitir la descarga
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" class="download-button">{label}</a>'

    # Añadir el CSS personalizado para el botón
    st.markdown(f"""
        <style>
        .download-button {{
            background-color: #39FF14;
            color: black;
            padding: 10px 20px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            display: inline-block;
        }}
        .download-button:hover {{
            background-color: #32CD32;
        }}
        </style>
        {href}
    """, unsafe_allow_html=True)
    
# Función para formatear números con separadores de miles
def format_number(num):
    return "{:,.0f}".format(num).replace(",", ".")

# Función para generar el informe descriptivo basado en la plantilla community_template
def generar_informe_descriptivo(template1, community_data):
    # Reemplazar los placeholders con los datos reales de la comunidad (df_final)
    informe = template1.replace('{{ Comunidad Autónoma }}', community_data['Comunidad Autónoma'])
    informe = informe.replace('{{ Latitud }}', str(community_data['Latitud']))
    informe = informe.replace('{{ Longitud }}', str(community_data['Longitud']))
    informe = informe.replace('{{ Fibra Hasta La Casa % }}', str(community_data['Fibra Hasta La Casa (%)']))
    informe = informe.replace('{{ Nº Centros de Datos }}', str(community_data['Nº Centros de Datos']))
    informe = informe.replace('{{ Nº Universidades }}', str(community_data['Nº Universidades']))
    informe = informe.replace('{{ Nº de Egresados }}', format_number(community_data['Nº de Egresados']))
    informe = informe.replace('{{ Éxito Universitario % }}', str(community_data['Éxito Universitario (%)']))
    informe = informe.replace('{{ Nº Habitantes }}', format_number(community_data['Nº Habitantes']))
    informe = informe.replace('{{ Costo Laboral Promedio }}', format_number(community_data['Costo Laboral Promedio']))  
    informe = informe.replace('{{ Gasto en I+D % }}', str(community_data['Gasto en I+D (%)']))
    informe = informe.replace('{{ PIB per cápita % }}', str(community_data['PIB per cápita (%)']))
    informe = informe.replace('{{ Nº Aceleradoras }}', str(community_data['Nº Aceleradoras']))
    informe = informe.replace('{{ Nº Incubadoras }}', str(community_data['Nº Incubadoras']))
    informe = informe.replace('{{ Nº Parques Tecnológicos }}', str(community_data['Nº Parques Tecnológicos']))
    informe = informe.replace('{{ Criminalidad % }}', str(community_data['Criminalidad (%)']))
    informe = informe.replace('{{ Servicios de Salud % }}', str(community_data['Servicios de Salud (%)']))
    informe = informe.replace('{{ Asistencia de Eventos % }}', str(community_data['Asistencia de Eventos (%)']))
    informe = informe.replace('{{ Índice de Confianza del Sistema Político }}', str(community_data['Índice de Confianza del Sistema Político']))
    informe = informe.replace('{{ Índice de Confianza Judicial }}', str(community_data['Índice de Confianza Judicial']))
    informe = informe.replace('{{ Calidad de Vida % }}', str(community_data['Calidad de Vida (%)']))
    informe = informe.replace('{{ Índice de Satisfacción del Entorno }}', str(community_data['Índice de Satisfacción del Entorno']))
    informe = informe.replace('{{ Índice de Confianza Empresarial }}', str(community_data['Índice de Confianza Empresarial']))
    informe = informe.replace('{{ Nº Empresas Disueltas }}', str(community_data['Nº Empresas Disueltas']))
    informe = informe.replace('{{ Nº Empresas Constituidas }}', str(community_data['Nº Empresas Constituidas']))
    
    return informe

# Función para generar el informe de recomendación basado en la plantilla recomendacion_community_template
def generar_informe_recomendacion(template2, score_data):
    # Definir umbrales para puntos fuertes y áreas de mejora
    umbral_fuerte = 70  # Valores por encima de este umbral serán considerados puntos fuertes
    umbral_mejora = 40  # Valores por debajo de este umbral serán considerados áreas de mejora

    # Generar dinámicamente los puntos fuertes y áreas de mejora
    puntos_fuertes = []
    areas_mejora = []

    if score_data['Fibra Hasta La Casa (%)'] >= umbral_fuerte:
        puntos_fuertes.append(f"- Fibra Hasta La Casa: {score_data['Fibra Hasta La Casa (%)']}% de cobertura de fibra óptica.")
    if score_data['PIB per cápita (%)'] >= umbral_fuerte:
        puntos_fuertes.append(f"- PIB per cápita: {score_data['PIB per cápita (%)']}.")
    if score_data['Nº Centros de Datos'] >= umbral_fuerte:
        puntos_fuertes.append(f"- Nº Centros de Datos: {score_data['Nº Centros de Datos']}.")
    if score_data['Índice de Confianza Empresarial'] < umbral_mejora:
        areas_mejora.append(f"- Índice de Confianza Empresarial: Actualmente en {score_data['Índice de Confianza Empresarial']}%, lo que podría mejorarse.")
    if score_data['Gasto en I+D (%)'] < umbral_mejora:
        areas_mejora.append(f"- Gasto en I+D: Actualmente en {score_data['Gasto en I+D (%)']}%, se recomienda potenciar la inversión en innovación.")

    # Crear la sección de puntos fuertes y áreas de mejora
    puntos_fuertes_texto = "\n".join(puntos_fuertes) if puntos_fuertes else "Ningún punto fuerte destacado."
    areas_mejora_texto = "\n".join(areas_mejora) if areas_mejora else "No se han identificado áreas significativas de mejora."

    # Reemplazar los placeholders en la plantilla
    informe = template2.replace('{{ Comunidad Autónoma }}', score_data['Comunidad Autónoma'])
    informe = informe.replace('{{ total_score }}', str(score_data['total_score']))
    informe = informe.replace('{{ puntos_fuertes }}', puntos_fuertes_texto)
    informe = informe.replace('{{ areas_mejora }}', areas_mejora_texto)

    return informe


# Función para obtener la comunidad con el mayor puntaje desde el archivo de puntajes y buscar sus datos en df_final
def obtener_comunidad_mejor_puntuada(df_score, df_final):
    comunidad_mejor_puntuada = df_score.sort_values(by='total_score', ascending=False).iloc[0]
    comunidad_nombre = comunidad_mejor_puntuada['Comunidad Autónoma']

    # Buscar los datos detallados en df_final
    comunidad_data = df_final[df_final['Comunidad Autónoma'] == comunidad_nombre].to_dict('records')[0]

    # Devolver la información de la comunidad y el puntaje
    return comunidad_data, comunidad_mejor_puntuada

# Aplicación de Streamlit
def show_page():
    st.title("Recomendación de la Mejor Comunidad Autónoma")

    # Cargar las plantillas
    template1, template2 = load_templates()

    if not template1 or not template2:
        return  # Salir si no se encuentran las plantillas
    
    # Verificar si el cuestionario se ha completado en st.session_state
    if "answers" not in st.session_state or not st.session_state["answers"]:
        st.error("No se ha completado el cuestionario. Por favor, completa primero el formulario en la sección de Comunidad Autónoma.")
        return

    if st.button("Generar Informe"):
        
        # Obtener la comunidad con el mayor puntaje y sus datos
        comunidad_data, score_data = obtener_comunidad_mejor_puntuada(df_score, df_final)
        
        # Generar los dos informes separados
        informe_descriptivo = generar_informe_descriptivo(template1, comunidad_data)
        informe_recomendacion = generar_informe_recomendacion(template2, score_data)
        
        # Mostrar ambos informes en pantalla
        st.text_area("Informe Descriptivo", value=informe_descriptivo, height=400)
        st.text_area("Informe de Recomendación", value=informe_recomendacion, height=200)
        
        # Combinar ambos informes en uno solo si es necesario
        informe_final = informe_descriptivo + "\n\n" + informe_recomendacion
        
        # Generar PDF
        pdf = generate_pdf(informe_final, comunidad_data)
        
        # Botón de descarga personalizado
        download_button_custom(pdf, f"{comunidad_data['Comunidad Autónoma']}_informe_completo.pdf", "Descargar PDF")
        

# Ejecutar la aplicación de Streamlit
if __name__ == '__main__':
    show_page()
