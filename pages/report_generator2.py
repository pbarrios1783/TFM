# Importamos las librerías
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# Cargamos el DataFrame de negocios en España
def cargar_negocios_similares():
    try:
        df = pd.read_excel('./data/df_sintetico.xlsx')          
        return df
    except FileNotFoundError:
        st.error("No se pudo encontrar el archivo.")
        return None

# Creamos una función para filtrar los negocios similares por sector
def filtrar_negocios_similares(df, sector):
    return df[df['Sector'] == sector].head(10)  # Filtramos por sector y seleccionamos los 10 primeros

# Creamos una función para generar el informe de negocios similares
def generar_informe_negocios_similares(negocios_df):
    template = """
    A continuación, se muestran algunas empresas que tienen un modelo de negocio similar al tuyo:

    1. Nombre: {{empresa_1}}
       - Descripción: {{descripcion_1}}
   
   2. Nombre: {{empresa_2}}
       - Descripción: {{descripcion_2}}
   
   3. Nombre: {{empresa_3}}
       - Descripción: {{descripcion_3}}       
   
   4. Nombre: {{empresa_4}}
       - Descripción: {{descripcion_4}}       
   
   5. Nombre: {{empresa_5}}
       - Descripción: {{descripcion_5}}       
   
   6. Nombre: {{empresa_6}}
       - Descripción: {{descripcion_6}}       
   
   7. Nombre: {{empresa_7}}
       - Descripción: {{descripcion_7}}       
   
   8. Nombre: {{empresa_8}}
       - Descripción: {{descripcion_8}}  
       
   9. Nombre: {{empresa_9}}
       - Descripción: {{descripcion_9}}       
  
  10. Nombre: {{empresa_10}}
       - Descripción: {{descripcion_10}}

    Estas empresas operan en el mismo sector y podrían ser relevantes para tu red de contactos o estrategias de colaboración.
    """

    # Reemplazar los placeholders con los datos del DataFrame hasta 10 empresas
    informe = template.replace('{{empresa_1}}', negocios_df.iloc[0]['Nombre empresa'])
    informe = informe.replace('{{descripcion_1}}', f"Ubicada en {negocios_df.iloc[0]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[0]['Sector']}.")
    
    informe = informe.replace('{{empresa_2}}', negocios_df.iloc[1]['Nombre empresa'])
    informe = informe.replace('{{descripcion_2}}', f"Ubicada en {negocios_df.iloc[1]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[1]['Sector']}.")
    
    informe = informe.replace('{{empresa_3}}', negocios_df.iloc[2]['Nombre empresa'])
    informe = informe.replace('{{descripcion_3}}', f"Ubicada en {negocios_df.iloc[2]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[2]['Sector']}.")
    
    informe = informe.replace('{{empresa_4}}', negocios_df.iloc[3]['Nombre empresa'])
    informe = informe.replace('{{descripcion_4}}', f"Ubicada en {negocios_df.iloc[3]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[3]['Sector']}.")
    
    informe = informe.replace('{{empresa_5}}', negocios_df.iloc[4]['Nombre empresa'])
    informe = informe.replace('{{descripcion_5}}', f"Ubicada en {negocios_df.iloc[4]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[4]['Sector']}.")
    
    informe = informe.replace('{{empresa_6}}', negocios_df.iloc[5]['Nombre empresa'])
    informe = informe.replace('{{descripcion_6}}', f"Ubicada en {negocios_df.iloc[5]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[5]['Sector']}.")
    
    informe = informe.replace('{{empresa_7}}', negocios_df.iloc[6]['Nombre empresa'])
    informe = informe.replace('{{descripcion_7}}', f"Ubicada en {negocios_df.iloc[6]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[6]['Sector']}.")
    
    informe = informe.replace('{{empresa_8}}', negocios_df.iloc[7]['Nombre empresa'])
    informe = informe.replace('{{descripcion_8}}', f"Ubicada en {negocios_df.iloc[7]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[7]['Sector']}.")
    
    informe = informe.replace('{{empresa_9}}', negocios_df.iloc[8]['Nombre empresa'])
    informe = informe.replace('{{descripcion_9}}', f"Ubicada en {negocios_df.iloc[8]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[8]['Sector']}.")
    
    informe = informe.replace('{{empresa_10}}', negocios_df.iloc[9]['Nombre empresa'])
    informe = informe.replace('{{descripcion_10}}', f"Ubicada en {negocios_df.iloc[9]['Comunidad Autónoma']}, opera en el sector {negocios_df.iloc[9]['Sector']}.")
    
    return informe
    

# Creamos la función para generar el PDF con Poppins y logo
def generar_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()

    # Registrar la fuente Poppins
    pdf.add_font('Poppins', '', 'Poppins-Regular.ttf', uni=True)
    pdf.add_font('Poppins', 'B', 'Poppins-Bold.ttf', uni=True)

    # Usar la fuente Poppins en el PDF
    pdf.set_font('Poppins', 'B', 16)

    # Añadir el logo
    logo_path = "./imagenes/3.png"  # Ruta del logo
    pdf.image(logo_path, x=10, y=8, w=33)

    # Título del informe
    pdf.ln(40)  # Espacio después del logo
    pdf.cell(200, 10, txt="Competidores en Tu Sector", ln=True, align='C')

    # Añadir contenido del informe con Poppins regular
    pdf.set_font('Poppins', '', 12)

    # Establecer márgenes personalizados
    pdf.set_margins(left=15, top=10, right=15)
    pdf.ln(10)
    pdf.multi_cell(0, 10, report_text)

    # Guardar el PDF en memoria
    pdf_output = pdf.output(dest='S').encode('latin1')

    return pdf_output

# Creamos una función para descargar el PDF con estilo personalizado
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

# Aplicación de Streamlit para mostrar los negocios similares
def show_page():
    st.title("Competidores en Tu Sector")

    # Cargar los negocios similares desde el archivo 
    df_negocios = cargar_negocios_similares()
    if df_negocios is None:
        return  # Si no se carga el archivo, detener la ejecución

    # Verificar si el sector ya está en st.session_state
    if 'sector_clasificado' in st.session_state:
        # Obtener el sector desde st.session_state
        sector_clasificado = st.session_state['sector_clasificado']

        st.write(f"Generando informe para el sector: **{sector_clasificado}**")

        if st.button("Generar Informe"):
            # Filtrar los negocios similares
            negocios_similares = filtrar_negocios_similares(df_negocios, sector_clasificado)

            # Generar el informe
            informe = generar_informe_negocios_similares(negocios_similares)

            # Mostrar el informe
            st.text_area("Informe Generado", value=informe, height=300)

            # Generar el PDF
            pdf_output = generar_pdf(informe)

            # Botón para descargar el PDF
            descargar_pdf(pdf_output, "Competidores en Tu Sector.pdf")
    else:
        st.error("No se ha clasificado un sector. Por favor, completa primero el formulario de clasificación de modelo de negocio.")

# Ejecutar la aplicación de Streamlit
if __name__ == '__main__':
    show_page()
