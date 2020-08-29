import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets,title='Head With Data - Team Outliers')
server = app.server

#Oil Data Prep
brent = requests.get('https://pkgstore.datahub.io/core/oil-prices/brent-daily_json/data/11a834b4b126dcc4601b562966cadf3a/brent-daily_json.json')
df_brent=pd.DataFrame(brent.json())
wti = requests.get('https://pkgstore.datahub.io/core/oil-prices/wti-daily_json/data/9b7deec86cf68066ac3b523b2478f1df/wti-daily_json.json')
df_wti=pd.DataFrame(wti.json())
df_wti.rename(columns={'Price':'Wti_Price'},inplace=True)
_df_brent = df_brent[df_brent['Date'] >= '2019-01-01']
_df_wti = df_wti[df_wti['Date'] >= '2019-01-01']
a = _df_wti.merge(_df_brent, on='Date',how='left')

random_x = np.array(a['Date'])
random_y0 =np.array(a['Price'])
random_y1 =np.array(a['Wti_Price'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                    mode='lines',
                    name='Brent Oil Price'))
fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                    mode='lines',
                    name='WTI Oil Price'))

air_traffic = requests.get('https://raw.githubusercontent.com/kaushikprasanth/head_with_data_outliers_data/master/Air_Traffic_Passenger_Statistics.json')
_df_air_traffic=pd.DataFrame(json.loads(air_traffic.json()))
_df_air_traffic['Activity Period'] = pd.to_datetime((_df_air_traffic['Activity Period']), format='%Y%m')
air_traffic_plot = px.line(_df_air_traffic, x="Activity Period",  y="Passenger Count", color='GEO Summary',
        title="Domestic and International Air Traffic Passenger Count")

app.layout = html.Div(children=[
    html.H1(children='Head With Data - Team Outliers'),

    html.H3(children='A Visualization of Travel and Pollution in COVID Days'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
       dcc.Graph(
        id='air-traffic-graph',
        figure=air_traffic_plot
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)