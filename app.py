import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("empleo_formal.csv")

st.set_page_config(page_title="Empleo Formal Colombia", layout="wide", page_icon="📊")

# Estilo
st.markdown(
    """
    <style>
    body {
        background-color: #141627;
        color: white;
    }
    .stApp {
        background-color: #141627;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Selecciona vista:", ["📘 Contexto del problema", "📊 Barras por Categoría", "📈 Boxplot", "🗺️ Mapa"])

# Vista de contexto
if opcion == "📘 Contexto del problema":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("## Contexto del problema")
        st.markdown("""
        Este dashboard presenta un análisis del empleo formal en diferentes departamentos de Colombia.  
        Permite visualizar el valor promedio registrado por departamento, analizar la distribución por categorías,  
        y explorar la ubicación geográfica de los datos de manera interactiva.
        """)
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=250)

# Gráfico de barras
elif opcion == "📊 Barras por Categoría":
    df_prom = df.groupby("Departamento")["Valor"].mean().reset_index()
    fig = px.bar(df_prom, x="Departamento", y="Valor", title="Promedio del Valor por Departamento", color="Valor", color_continuous_scale="viridis")
    st.plotly_chart(fig, use_container_width=True)

# Boxplot
elif opcion == "📈 Boxplot":
    fig = px.box(df, x="Categoría", y="Valor", title="Distribución de Valor por Categoría", color="Categoría")
    st.plotly_chart(fig, use_container_width=True)

# Mapa
elif opcion == "🗺️ Mapa":
    df_prom = df.groupby("Departamento").agg({
        "Valor": "mean",
        "Latitud": "mean",
        "Longitud": "mean"
    }).reset_index()
    
    fig = px.scatter_mapbox(
        df_prom,
        lat="Latitud",
        lon="Longitud",
        color="Valor",
        size="Valor",
        hover_name="Departamento",
        zoom=4.5,
        height=650,
        center={"lat": 4.5709, "lon": -74.2973},
        mapbox_style="carto-darkmatter",
        title="Promedio del Valor por Departamento"
    )
    st.plotly_chart(fig, use_container_width=True)
