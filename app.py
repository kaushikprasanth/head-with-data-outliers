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
#Air Quality Data

aqi = requests.get('https://raw.githubusercontent.com/kaushikprasanth/head_with_data_outliers_data/master/Air%20Quality%20Data/Cook_County_AQI.json')
aqi = pd.DataFrame(aqi.json())
aqi['Date'] = pd.to_datetime(aqi['Date'])
aqi['year'], aqi['month'] = aqi['Date'].dt.year, aqi['Date'].dt.month.astype(str)+'/'+aqi['Date'].dt.day.astype(str)
aqi_2020=aqi[(aqi['year'] == 2020) & (aqi['Date'] != "2020-02-29")]
aqi_2019=aqi[(aqi['year'] == 2019) & (aqi['Date'] < "2019-08-29")]

aqi_fig = go.Figure()
aqi_fig.add_trace(go.Scatter( x=list(aqi_2020["month"]), y=list(aqi_2020[" AQI Value"]),mode="lines",name="2020"))
aqi_fig.add_trace(go.Scatter( x=list(aqi_2019["month"]), y=list(aqi_2019[" AQI Value"]),mode="lines",name="2019"))

aqi_fig.update_layout(
    title="Air Quality Index till 8/28 for Cook County",
    shapes=[
        # Phase 1 & 2
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0="3/15",
            y0=0,
            x1="6/3",
            y1=1,
            fillcolor="orange",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # Phase 3
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0="6/3",
            y0=0,
            x1="6/24",
            y1=1,
            fillcolor="yellow",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        
    ]
)
color_discrete_map={'Good':'#32CD32','Moderate':'#FFFF66','Unhealthy for sensitive groups':'#FF8C00','Unhealthy':'#FF4500'}
#Pie Charts
fig_2019 = px.pie(aqi_2019['AQI Category'].value_counts().reset_index(), 
                values='AQI Category', names='index',
                color='index',
                color_discrete_map=color_discrete_map
                )
df_2020_cat = aqi_2020['AQI Category'].value_counts().reset_index()
df_2020_cat = df_2020_cat[df_2020_cat['index'] != '0']
fig_2020 = px.pie(df_2020_cat, 
                    values='AQI Category', 
                    names='index',
                    color='index',
                    color_discrete_map=color_discrete_map
                    )

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
fig.update_layout(
    title="Oil Prices")

air_traffic = requests.get('https://raw.githubusercontent.com/kaushikprasanth/head_with_data_outliers_data/master/Air_Traffic_Passenger_Statistics.json')
_df_air_traffic=pd.DataFrame(json.loads(air_traffic.json()))
_df_air_traffic['Activity Period'] = pd.to_datetime((_df_air_traffic['Activity Period']), format='%Y%m')
air_traffic_plot = px.line(_df_air_traffic, x="Activity Period",  y="Passenger Count", color='GEO Summary',
        title="Domestic and International Air Traffic Passenger Count")

app.layout = html.Div(children=[
    html.H1(children='Head With Data - Team Outliers'),

    html.H3(children='A Visualization of Travel and Pollution Data in 2019 and 2020'),

 dcc.Graph(
        id='aqi-graph',
        figure=aqi_fig
    ),
    html.Div(html.Div([
        html.Div([
            html.H4('2019'),
            dcc.Graph(id='g1', figure=fig_2019)
        ], className="six columns"),

        html.Div([
            html.H4('2020'),
            dcc.Graph(id='g2', figure=fig_2020)
        ], className="six columns"),
    ], className="row")),
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