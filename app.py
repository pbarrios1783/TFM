# Importamos las librerias
import streamlit as st
from PIL import Image
from pathlib import Path
import importlib.util
from streamlit_option_menu import option_menu
from gtts import gTTS
import os

# Configuramos el nombre del app y el ícono en la pestaña del navegador
st.set_page_config(
    page_title="INVESTEK",  
    page_icon="imagenes/3.png",  
)

# Agregamos CSS personalizado para el diseño y la identidad visual con Poppins
hide_streamlit_style = """
    <style>
    /* Ocultar la barra lateral superior de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Importar la fuente Poppins desde Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    /* Aplicar la fuente Poppins solo a títulos, subtítulos y párrafos */
    h1, h2, h3, p, div, ol, ul {
        font-family: 'Poppins', sans-serif;
    }

    /* Estilo para las imágenes */
    .stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width:  400px;
        height: 400px;
        object-fit: contain;
    }

    /* Botones personalizados */
    .stButton>button {
        background-color: #39FF14;
        color: black;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        padding: 10px 20px;
        font-size: 8px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }

    /* Estilo para botones al pasar el cursor */
    .stButton>button:hover {
        background-color: #39FF14;
        cursor: pointer;
    }

    /* Ajustes para el sidebar (menú lateral) */
    .sidebar .sidebar-content {
        background-color: #39FF14;
        color: white;
    }
    .sidebar .sidebar-content h1 {
        color: #ffffff;
    }

    /* Enlaces en el sidebar */
    .sidebar .sidebar-content a {
        color: #ffffff;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Agregamos la ruta del archivo SVG local
svg_file_path = "./imagenes/3.svg"

# Mostramos el archivo SVG del logo en la barra lateral utilizando HTML
with st.sidebar:
    # Leer el contenido del archivo SVG
    with open(svg_file_path, "r", encoding="utf-8") as svg_file:
        svg_content = svg_file.read()

    # Mostramos el archivo SVG en la barra lateral con un tamaño personalizado 
    st.markdown(f"""
    <style>
    /* Contenedor general de la barra lateral */
    .sidebar .sidebar-content {{
        width: auto;  /* Ajusta el ancho del container de la barra lateral */
        padding: 0.9px;  /* Reduce el padding del contenedor */
    }}
    
    .logo-container {{
        display: flex;
        justify-content: center;  /* Centra horizontalmente */
        align-items: center;  /* Centra verticalmente */
        margin-bottom: 0.01px;  /* Añade espacio debajo del logo */
    }}

    /* Ajustar el tamaño del logo */
    .logo-container svg {{
        width: 800px;   /* Tamaño máximo del logo */
        height: 310px;
    }}
    
    /* Ajustar el tamaño del menú de navegación */
    .css-1v3fvcr {{
        font-size: 14px;  /* Tamaño de fuente para el menú de navegación */
         padding: 1px;  /* Reduce el padding entre elementos del menú */
    }}
    
    </style>

    <div class="logo-container">
        {svg_content}
    </div>
    """, unsafe_allow_html=True)


    
# Definimos las rutas de los tres generadores de informes
GENERADORES = {
    'Modelo de Negocio': 'pages/report_generator1.py',
    'Competidores en el Sector': 'pages/report_generator2.py',
    'Recomendación de la Mejor Comunidad Autónoma': 'pages/report_generator3.py',
}


# Creamos una función para mostrar la página del Generador de Informes unificado
def show_generador_informes():
    st.title("Generador de Informes")
    
    st.write("Seleccione el tipo de generador de informes que desea usar:")
    
    # Añadimos un contenedor alrededor del selector y el botón de informe para mejorar el diseño
    with st.container():
        # Creamos un selector para que el usuario elija el generador
        seleccion = st.radio("Elige un generador de informes", list(GENERADORES.keys()))
        
        # Hcaemos una separación visual entre el selector y el botón
        st.markdown("<hr>", unsafe_allow_html=True)
    
    # Cargamos y ejecutamos el generador seleccionado
    selected_generator = GENERADORES[seleccion]
    generador_module = load_module(seleccion, selected_generator)
    generador_module.show_page()  

    
# Creamos el menú de navegación en la barra lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Navegación",  # Título del menú
        options=["Portada", "Modelo de Negocio", "Comunidad Autónoma", "Generador de Informes", "Mapa", "Data"],  # Creamos las opciones del menú
        icons=["house", "pencil", "grid", "file-earmark-text", "map", "table"],  # Creamos distinto íconos para cada opción
        menu_icon="cast",  # Ícono para el menú en general
        default_index=0,  # Índice predeterminado
        styles={
           "title": {
                "font-size": "10px",
                 "margin": "0.2px",
           },
            "container": {
                "padding": "2px",  # Espacio adicional en el contenedor
                "background-color": "#f8f9fa", 
            },
            "icon": {
                "color": "#000000",  # Color de los íconos
                "font-size": "16px"  # Tamaño más grande para los íconos 
            },
            "nav-link": {
                "font-size": "12px",  # Tamaño de fuente ligeramente mayor para mejor legibilidad
                "text-align": "left", 
                "margin": "0.5px",  # Margen para mayor espaciado entre los elementos
                "color": "#000000",  # Color del texto normal 
                "background-color": "transparent",  # Fondo de los botones no seleccionados
            },
            "nav-link-selected": {
                "background-color": "#39FF14",  # Color del fondo del botón seleccionado (verde neón)
                "color": "#000000",  # Color del texto del botón seleccionado (negro)
                "font-weight": "bold"  # Opción para resaltar el texto del elemento seleccionado
            },
        }     
    )     

# Creamos una función para cargar los módulos de cada página dinámicamente
def load_module(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Texto
texto_motivacional = """
    España es uno de los países más atractivos para la inversión, con una economía en crecimiento
    y grandes oportunidades en sectores clave como la tecnología, turismo y energía renovable.
    
    ¡Invierta en España y aproveche todas estas oportunidades de crecimiento!
"""

# Función para mostrar la portada
def show_portada():
    # Título principal centrado
    st.title("Descubre el Potencial de España")
    st.write(texto_motivacional)

  # Agreagamos la imagen
    mapa_españa = Image.open("./imagenes/spain.jpg")  # Ruta de la imagen
    st.image(mapa_españa, caption=" ", use_column_width=True)   

# Definimos las páginas disponibles con sus rutas correspondientes
PAGES = {
    'Portada': 'app.py',  
    'Modelo de Negocio': 'pages/modelo_negocios.py',
    'Comunidad Autónoma': 'pages/questionnaire.py',
    'Generador de Informes': None, # El generador de informes tiene un submenu
    'Mapa': 'pages/heatmap.py',
    'Data': 'pages/data.py',
}

# Creamos la lógica para cargar la página seleccionada
if selected == 'Portada':
    show_portada()
elif selected =='Generador de Informes':
    # Llamamos a la funcion que maneja los generadores de informes
    show_generador_informes()
else:
    # Creamos un código para asegurarnos de no sobrescribir variables innecesarias
    if selected == "Comunidad Autónoma" and "answers" not in st.session_state:
        st.session_state["answers"] = {}
    if selected == "Modelo de Negocio" and "business_answers" not in st.session_state:
        st.session_state["business_answers"] = []

    # Cargamos y ejecutamos la página seleccionada dinámicamente
    page_module = load_module(selected, PAGES[selected])
    page_module.show_page()  # Llamamos a la función `show_page` de cada página

# Creamos instrucciones formateadas debajo del menú de navegación
st.sidebar.markdown("""
<div class="instrucciones-box">
<h3>Instrucciones</h3>
<ol>
    <li>Describe tú <strong>Modelo</strong> de negocio tecnológico.</li>
    <li>Completa el <strong>Cuestionario</strong> para obtener recomendaciones.</li>
    <li>Genera y descarga informes personalizados en el<strong> Generador de Informes</strong>.</li>
    <li>Explora los datos en el <strong>Mapa Interactivo</strong> y/o en <strong>Data</strong>.</li>
</ol>
</div>
<style>
    /* Estilo de las instrucciones */
    .instrucciones-box {
        background-color: #f8f9fa;
        padding: 5px;
        border-radius: 8px;
        margin-top: 0.9px
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-size: 12px;  /* Tamaño general para el contenedor */
    }

    /* Reducir el tamaño de las listas dentro de las instrucciones */
    .instrucciones-box ol, .instrucciones-box li {
        font-size: 12px;  /* Tamaño más pequeño para el texto de las listas */
        line-height: 1.4;  /* Ajustar el interlineado para mejorar legibilidad */
    }

    /* Mantener el tamaño del subtítulo */
    .instrucciones-box h3 {
        margin-top: 0;
        margin-bottom: 5px;
        font-size: 15px;  /* Tamaño de fuente para el subtítulo */
    }
</style>
""", unsafe_allow_html=True)


# Creamos el footer de la aplicación
st.markdown("""
    <footer class="footer">  <!-- Añadimos la clase "footer" al HTML -->
        <p>© 2024 Investek. Todos los derechos reservados.</p>
    </footer>

    <style>
        /* Estilo del footer */
        .footer p {
            margin-top: 70px;  /* Añadir las unidades "px" */
            margin-bottom: 10px;
            font-size: 12px;  /* Ajuste de tamaño de fuente */
        }
    </style>
""", unsafe_allow_html=True)
