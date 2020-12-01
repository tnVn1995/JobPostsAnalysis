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
                dbc.Col(
                  [
                     html.H2("What The App Does"),
                     html.P(
                         """Instructions on how to use the app here
                           """),
                           dbc.Button("View details", color="secondary"),
                   ],
                  md=4,
               ),
              dbc.Col(
                 [
                     html.H2("Graph"),
                     dcc.Graph(
                         figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                            ),
                        ]
                     ),
                ]
            )
       ],
className="mt-4",
)

def Homepage():
    layout = html.Div([
    nav, 
    dbc.Row([html.Img(src="/static/job-search-strategies.jpg", 
    style={"width": "100vw", 
            "height": "40vw"})]),
    body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()