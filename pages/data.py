# Importamos las librerías
import streamlit as st
import pandas as pd

# Cargamos los datos por separado
df_impuestos = pd.read_excel("./data/detalle/detalle_impuestos_propios.xlsx")
df_cpd = pd.read_excel("./data/detalle/detalle_centros_datos.xlsx")
df_aceleradoras = pd.read_excel("./data/detalle/detalle_aceleradoras.xlsx")
df_subsidios = pd.read_excel("./data/detalle/detalle_subsidios.xlsx")
df_centros_tecnologicos = pd.read_excel("./data/detalle/detalle_centros_tecnologicos.xlsx")
df_incubadoras = pd.read_excel("./data/detalle/detalle_incubadoras.xlsx")
df_parques_tecnologicos = pd.read_excel("./data/detalle/detalle_parques_tecnologicos.xlsx")


# Creamos un diccionario para mapear tipos de datos con DataFrames
df_map = {
    "Impuestos Propios": df_impuestos,
    "Centros de Datos": df_cpd,
    "Subsidios": df_subsidios,
    "Aceleradoras": df_aceleradoras,
    "Incubadoras": df_incubadoras,
    "Centros Tecnológicos": df_centros_tecnologicos,
    "Parques Tecnológicos": df_parques_tecnologicos,  
}

# Creamos un diccionario que asocia el tipo de datos con las columnas relevantes
columns_map = {
    "Impuestos Propios": ['Nombre de Impuestos'],  
    "Centros de Datos": ['Nombre', 'Tipo', 'Provincia'],
    "Subsidios": ['Título', 'Organismo', 'Sector', 'Ámbito Geográfico', 'Tipo', 'Destinatarios', 'Plazo de solicitud'],
    "Aceleradoras": ['Título', 'URI', 'Descripción', 'Dirección'],
    "Incubadoras": ['Título', 'URI', 'Descripción', 'Dirección'],
    "Centros Tecnológicos": ['Título', 'URI','Dirección'],
    "Parques Tecnológicos":  ['Título', 'URI','Dirección']
 
}

# Mostramos la página en el app
def show_page():
    # Título de la página
    st.title("Datos de España: Comunidades Autónomas")
    st.write("Detalle sólo disponible para variables de impuestos propios, centros de datos, aceleradoras, subsidios, centros tecnológicos, incubadoras y parques tecnológicos")
    
    # Creamos el menu de selección para el tipo de datos que quiere ver el usuario
    tipo_datos = st.selectbox("Selecciona el tipo de datos que quieres ver", df_map.keys())
    
    # Selecciona la comunidad en una lista desplegable
    df_seleccionado = df_map[tipo_datos]
    comunidad_seleccionada = st.selectbox("Selecciona una Comunidad Autónoma para ver detalles", df_seleccionado['Comunidad Autónoma'].unique())
    
    # Filtra los datos según la comunidad seleccionada
    df_filtrado = df_seleccionado[df_seleccionado['Comunidad Autónoma'] == comunidad_seleccionada]
    
    # Filtra las columnas importantes según el tipo de datos
    columnas_relevantes = columns_map[tipo_datos]
    df_filtrado = df_filtrado[columnas_relevantes]
    
   # Muestra el DataFrame filtrado
    st.write(f"Mostrando datos para {comunidad_seleccionada} (Tipo de datos: {tipo_datos})")
    st.dataframe(df_filtrado)
