import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.NavLink import NavLink


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
            dbc.NavItem(dbc.NavLink("Recommendation", href="/recommendation")),
            dbc.NavItem(dbc.NavLink("About", href="/about"))
            ],
          brand="Home",
          brand_href="/home",
          sticky="top",
          color='primary',
          className='navbar',
          dark=True
        )
    return navbar