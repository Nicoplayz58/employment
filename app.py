from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("empleo_formal.csv")

# App
app = Dash(__name__)
server = app.server
app.title = "Empleo Formal Colombia"

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                background-color: #141627;
                color: white;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }
            * {
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


app.layout = html.Div([
    html.H1("Dashboard Empleo Formal", style={"textAlign": "center", "color": "white"}),

    html.Div([
        html.Label("Selecciona tipo de gráfico:", style={"color": "white"}),
        dcc.Dropdown(
            id="tipo_grafico",
            options=[
                {"label": "Barras por Categoría", "value": "barras"},
                {"label": "Boxplot por Categoría", "value": "box"},
                {"label": "Mapa Colombia", "value": "mapa"}
            ],
            value="barras"
        )
    ], style={"width": "50%", "margin": "auto"}),

    dcc.Graph(id="grafico")
], style={"backgroundColor": "#141627", "padding": "20px", "fontFamily": "Arial"})

@app.callback(
    Output("grafico", "figure"),
    Input("tipo_grafico", "value")
)
def actualizar_grafico(tipo):
    if tipo == "barras":
        # Promedio del Valor por Departamento
        df_promedio = df.groupby("Departamento")["Valor"].mean().reset_index()
        fig = px.bar(df_promedio, x="Departamento", y="Valor", 
                     title="Promedio del Valor por Departamento", 
                     color="Valor", color_continuous_scale="viridis")
        
    elif tipo == "box":
        # Distribución por Categoría
        fig = px.box(df, x="Categoría", y="Valor", 
                     title="Distribución de Valor por Categoría", 
                     color="Categoría")
        
    else:
        df_promedio = df.groupby("Departamento").agg({
            "Valor": "mean",
            "Latitud": "mean",
            "Longitud": "mean"
        }).reset_index()

        fig = px.scatter_mapbox(
            df_promedio,
            lat="Latitud",
            lon="Longitud",
            color="Valor",
            size="Valor",
            hover_name="Departamento",
            zoom=4.5,
            center={"lat": 4.5709, "lon": -74.2973},
            mapbox_style="carto-darkmatter",
            title="Promedio del Valor por Departamento"
        )

    fig.update_layout(paper_bgcolor="#141627", plot_bgcolor="#141627", font_color="white")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
