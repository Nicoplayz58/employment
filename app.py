from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# Cargar datos
df = pd.read_csv("empleo_formal.csv")

# App
app = Dash(__name__,suppress_callback_exceptions=True)
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

# Layout principal
app.layout = html.Div([
    html.H1("Dashboard Empleo Formal", style={"textAlign": "center", "color": "white"}),

    dcc.Tabs(id="tabs", value="dashboard", children=[
        dcc.Tab(label="📘 Contexto del problema", value="contexto",
                style={"backgroundColor": "#2c2e4a", "color": "white"},
                selected_style={"backgroundColor": "#4c4f75", "color": "white"}),

        dcc.Tab(label="📊 Dashboard", value="dashboard",
                style={"backgroundColor": "#2c2e4a", "color": "white"},
                selected_style={"backgroundColor": "#4c4f75", "color": "white"})
    ]),

    html.Div(id="contenido")
], style={"backgroundColor": "#141627", "padding": "20px", "fontFamily": "Arial"})


@app.callback(
    Output("contenido", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "contexto":
        return html.Div([
            html.Div([
                html.Div([
                    html.H2("Contexto del problema", style={"color": "white", "marginBottom": "20px"}),
                    html.P(
                        "Este dashboard presenta un análisis del empleo formal en diferentes departamentos de Colombia. "
                        "Permite visualizar el valor promedio registrado por departamento, analizar la distribución por categorías, "
                        "y explorar la ubicación geográfica de los datos de manera interactiva. "
                        "La finalidad es facilitar la comprensión de patrones y diferencias entre regiones.",
                        style={"color": "white", "fontSize": "16px", "textAlign": "justify", "lineHeight": "1.7"}
                    )
                ], style={"width": "60%", "padding": "30px"}),
        
                html.Div([
                    html.Img(
                        src="https://cdn-icons-png.flaticon.com/512/1995/1995574.png",
                        style={
                            "width": "100%",
                            "maxWidth": "250px",
                            "margin": "auto",
                            "display": "block",
                            "filter": "drop-shadow(0 0 15px #00ffff)"
                        }
                    )
                ], style={"width": "40%", "display": "flex", "justifyContent": "center", "alignItems": "center"})
            ], style={
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "center",
                "justifyContent": "center",
                "maxWidth": "1000px",
                "margin": "auto",
                "minHeight": "65vh"  # <- clave para centrar respecto al contenido principal
            })
        ])

     
    elif tab == "dashboard":
        return html.Div([
            html.Div([
                html.Label("Selecciona vista:", style={"color": "white", "fontSize": "18px", "marginBottom": "10px"}),
                dcc.RadioItems(
                    id="tipo_grafico",
                    options=[
                        {"label": "📊 Barras por Categoría", "value": "barras"},
                        {"label": "📈 Boxplot por Categoría", "value": "box"},
                        {"label": "🗺️ Mapa Colombia", "value": "mapa"}
                    ],
                    value="barras",
                    labelStyle={"display": "block", "marginBottom": "10px", "cursor": "pointer"},
                    inputStyle={"marginRight": "10px", "accentColor": "#00FFFF"}
                )
            ], style={"width": "20%", "padding": "20px", "display": "flex", "flexDirection": "column", "justifyContent": "center"}),

            html.Div([
                dcc.Graph(id="grafico")
            ], style={"width": "80%"})
        ], style={"display": "flex", "flexDirection": "row", "alignItems": "center"})


@app.callback(
    Output("grafico", "figure"),
    Input("tipo_grafico", "value")
)
def actualizar_grafico(tipo):
    if tipo is None:
        raise PreventUpdate

    if tipo == "barras":
        df_promedio = df.groupby("Departamento")["Valor"].mean().reset_index()
        fig = px.bar(df_promedio, x="Departamento", y="Valor",
                     title="Promedio del Valor por Departamento",
                     color="Valor", color_continuous_scale="viridis")

    elif tipo == "box":
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
            zoom=5,
            height=650,
            center={"lat": 5.5, "lon": -74.0},
            mapbox_style="carto-darkmatter",
            title="Promedio del Valor por Departamento"
        )

    fig.update_layout(paper_bgcolor="#141627", plot_bgcolor="#141627", font_color="white")
    return fig


if __name__ == '__main__':
    app.run(debug=True)

