from navbar import Navbar

#dash
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

nav = Navbar()

body = dbc.Container([
    html.H3("""
    About Me"""),
    html.Div([
        html.Img(src="assets/static/sf.jpg", 
        style={"border":"1px solid #ddd", "border-radius": "4px", "padding": "5px", "width": "150px"})
    ])
])

description = dbc.Container([html.P("I like creating interactive dashboard embeded with machine learning for educational purposes")])
# description = html.Div[
#     html.P("I like creating interactive dashboard embeded with machine learning for educational purposes")
# ]

def About():
    layout = html.Div([
        nav,
        body,
        description
    ])
    return layout
