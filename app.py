import io
from base64 import b64encode

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd
from dash_preprocess import runner

#######################################################
################ B U F F E R ##########################
#######################################################

buffer = io.StringIO()

###################################################################
################ D A T A  P R E P R O C E S S #####################
###################################################################

df_value_counts, df_occ_laika, df_total, df_Duration = runner()

################################################
################ P L O T S #####################
################################################

#First plot = Osallistujamäärät
fig_occ_laika = go.FigureWidget()
fig_occ_laika.add_bar(
    x=df_occ_laika['Kokouspäivä'], 
    y=df_occ_laika['count'], 
    hovertemplate=
    "<b>%{x}</b><br>"+
    "Osallistujamäärä: %{y}"+
    "<extra></extra>")
fig_occ_laika.layout.title = 'Osallistujamäärä per kokous'
fig_occ_laika.write_html(buffer)

#First plot = Osallistumiskerrat
fig_occ = go.FigureWidget()
fig_occ.add_bar(
    x=df_value_counts['nimet'], 
    y=df_value_counts['count'], 
    hovertemplate=
    "<b>%{x}</b><br>"+
    "Osallistumiskerrat: %{y}"+
    "<extra></extra>")
fig_occ.layout.title = 'Osallistumiskerrat per henkilö'
fig_occ.write_html(buffer)

#Second plot = Kokonaisaika palavereissa
fig_total = go.FigureWidget()
fig_total.add_bar(
    x=df_total["Full Name"],
    y=df_total["Duration(total)"], 
    hovertemplate=
    "<b>%{x}</b><br>"+
    "Kokonaisaika: %{y:.0f}min"+
    "<extra></extra>")
fig_total.layout.title = "Kokonaisaika palaverissa per henkilö"
fig_total.write_html(buffer)

#Third plot = Kokouksissa oltu keskiarvo & Pisin kokous
fig_meanmax = go.FigureWidget()
fig_meanmax.add_scatter(
    x=df_Duration['Full Name'], 
    y=df_Duration['Duration(mean)'], 
    name='Keskimäärin',
    hovertemplate=
    "<b>%{x}</b><br>"+
    "Keskiarvo: %{y:.0f}min"+
    "<extra></extra>")

fig_meanmax.add_bar(x=df_Duration['Full Name'], 
    y=df_Duration['Duration(max)'], 
    name='Pisin kokous',
    hovertemplate="<b>%{x}</b><br>"+
    "Pisin kokous: %{y}min"+
    "<extra></extra>")
fig_meanmax.layout.title = 'Pisin aika yhdessä kokouksessa & kokouksissa keskimäärin vietetty aika'
fig_meanmax.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

################################################
################ STYLESHEET ####################
################################################

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

################################################
################# D A S H ######################
################################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Teams Statistics Page v1"
server = app.server

#########################################################
################# D A S H  H T M L ######################
#########################################################


app.layout = html.Div(
    children=[
        #Otsikko!
        html.Div(
            children = [
                html.P(children="🛬", className="header-emoji"),
                html.H1(
                    children="Teams meeting statistics",
                    className='header-title',
                    ),
                html.P(
                    children="Viikkostatuspalaveri - tilastot v. 2021",
                    className='header-description'
                ),
            ],
            className='header',
        ),
        
        #Graphit!
        html.Div(
            children= [
                html.Div(
                    children= dcc.Graph(
                        config = {"displayModeBar": False},
                        id='osallistujakpl',
                        figure= fig_occ_laika
                        ),
                        className='card',
                ),
                html.Div(
                    children= dcc.Graph(
                        config = {"displayModeBar": False},
                        id='osallistumismaarat',
                        figure= fig_occ
                        ),
                        className='card',
                ),
                html.Div(
                    children=
                        dcc.Graph(
                        config = {"displayModeBar": False},
                        id='kokonaisaika',
                        figure= fig_total
                        ),
                        className='card',
                ),
                html.Div(
                    children=
                        dcc.Graph(
                        config = {"displayModeBar": False},
                        id='Durationgraph',
                        figure=fig_meanmax
                        ),
                        className='card',
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            html.A(
                html.Button("Download HTML"), 
                id="download",
                href="data:text/html;base64," + encoded,
                download="teams_stats_graphs.html"
            ),
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=False)
