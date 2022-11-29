# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

listings = pd.read_csv("listings.csv")
nb = pd.read_csv("neighbourhoods.csv")

merged = listings.merge(nb, on="neighbourhood", suffixes=("_ls", "_nb"))

# graph 3
fig1 = px.histogram(merged, x="neighbourhood", color="neighbourhood", title="Neighbourhood", barmode="group")

def function(x):
    if x < 500:
        return "Less than 500"
    elif x >= 500 and x < 1000:
        return "Less than 1000"
    elif x >= 1000 and x < 2000:
        return "Less than 2000"
    elif x >= 2000 and x < 4000:
        return "Less than 4000"
    else:
        return "More than 4000"
merged["priceByCond"]=merged['price'].apply(function)

df1 = merged['priceByCond'].value_counts().to_frame().reset_index()

# graph 1
fig2 = px.pie(df1, values='priceByCond', names='index', title="Accommodation price", hole=.3)

# graph 2
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
fig3 = go.Figure(data=[go.Pie(labels=merged["neighbourhood_group_nb"].value_counts().index,
                              values=merged["neighbourhood_group_nb"].value_counts().values)])
fig3.update_traces(hoverinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))


# display of graphs
app.layout = html.Div(children=[
    html.H1(children='Hong Kong Airbnb Viz'),
    
    html.Div(children=[
        # graph 1
        dcc.Graph(
            id='graph1',
            style={'display': 'inline-block'},
            figure=fig2
        ),
        # graph 2
        dcc.Graph(
            id='graph2',
            style={'display': 'inline-block'},
            figure=fig3
        ),
    ]),

    # graph 3
    html.Div([
        # html.Div(children='''
        #     Graph 3 - Neighbourhood
        # '''),
        dcc.Graph(
            id='graph3',
            figure=fig1
        ),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)