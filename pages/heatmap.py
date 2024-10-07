# Importamos las librerías
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd  

# Cargamos los datos
df = pd.read_excel("./data/df_final.xlsx")

# Cargamos el file geojson
df_comunidades = gpd.read_file("./data/georef-spain-comunidad-autonoma.geojson")

# Agreagamos esta línea de código para mantener los datos numéricos para el HeatMap, sin formatear
# (el formateo se hará solo en los tooltips para la visualización)
def format_number(num):
    return "{:,.0f}".format(num).replace(",", ".")

# Mostramos la página en el app
def show_page():
    # Creamos el título de la página
    st.title("Datos de España: Comunidades Autónomas")
    
    # Seleccionamos la variable para el mapa de calor
    variable = st.selectbox('Seleccione una variable', df.columns[1:])
     
    # Creamos el mapa interactivo
    m = folium.Map(location=[40.416775, -3.703790], zoom_start=6)
    
    # Añadimos una capa de mapa de calor basada en la variable seleccionada con tooltips
    heat_data = [[row['Latitud'], row['Longitud'], row[variable]] for index, row in df.iterrows()]
    heat_layer = HeatMap(heat_data).add_to(m)
    
    # Añadimos comunidades autónomas al mapa
    folium.GeoJson(
       df_comunidades,
       name="comunidades",
       # Tooltip para indicar el nombre de la comunidad
       tooltip=folium.GeoJsonTooltip(fields=['acom_name'], labels=False, sticky=True)
    ).add_to(m)
    
    # Añadimos los marcadores con tooltips, aplicando el formateo solo en la visualización
    for i, row in df.iterrows():
        tooltip_text = f"{row['Comunidad Autónoma']}: {format_number(row[variable])}"
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            tooltip=tooltip_text
        ).add_to(m)
    

    # Mostramos el mapa en Streamlit usando st_folium
    st_folium(m, width=700, height=500)

