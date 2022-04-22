# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import sys
sys.path.append('/Users/samrelins/Documents/LIDA/transport_proj/src')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from journey_time_helpers import *
import pandas as pd

bradford_lsoas = FULL_JT_DATA.LA_Name == "Bradford"
lsoa_data = (FULL_JT_DATA[bradford_lsoas][["LSOA_code", "LSOA_name"]]
             .sort_values(by="LSOA_name"))
lsoa_options = [{"label": data[1]["LSOA_name"], "value": data[1]["LSOA_code"]}

 for data in lsoa_data.iterrows()]

def generate_table(lsoa_codes):
    if lsoa_codes == []:
        return "Select LSOA(s) to view stats"
    dataframe = build_accessibility_table(lsoa_codes, agg_method="mean")
    return html.Table([
        html.Thead([
            html.Tr(
                [html.Th(""), html.Th("")] +
                [html.Th(col[0]) for col in dataframe.columns]
            )
        ]),
        html.Thead([
            html.Tr(
                [html.Th(""), html.Th("")] +
                [html.Th(col[1]) for col in dataframe.columns]
            )
        ]),
        html.Thead([
            html.Tr(
                [html.Th("Service"), html.Th("Mode")] +
                [html.Th("") for col in dataframe.columns]
            )
        ]),
        html.Tbody([
            html.Tr(
                [html.Th(dataframe.index[i][0]) if i%4 == 0 else html.Th("")] +
                [html.Th(dataframe.index[i][1])] +
                [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
            ) for i in range(len(dataframe))
        ])
    ])


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="lsoas",
        options = lsoa_options,
        multi=True,
        value=["E01010612"]
    ),
    html.Div(id="jt_table")
])

@app.callback(
    Output("jt_table", "children"),
    Input("lsoas", "value"))
def update_table(lsoas):
    print(lsoas)
    return generate_table(lsoas)

if __name__ == '__main__':
    app.run_server(debug=True)
