import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [  
        dbc.Row(
            [
                html.Div([
                html.H2("What The App Does", style={'text-align':'center'}),
                html.P("""IInstructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                eeenstructions on how to use the app here"""),
                html.Br(),
                html.P("""IInstructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                eeenstructions on how to use the app here"""),
                html.Br(),
                html.P("""IInstructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                eeenstructions on how to use the app here"""),
                html.Br(),
                html.P("""IInstructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                Instructions on how to use the app hereInstructions on how to use the app her
                eeenstructions on how to use the app here"""),
                dbc.Button("View details", color="secondary"),
            ], style={"align":"center"})
            ]
            )
       ],
className="mt-4",
)

def Homepage():
    layout = html.Div([
    nav, 
    dbc.Row([html.Img(src="assets/static/job-search.jpg", 
    style={"width": "100vw", 
            "height": "40vw"})]),
    body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()