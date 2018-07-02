# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from datasets import international_transparency_data,international_transparency_pivot_data,\
    all_kpis,spain_corruption,standard_error,sources
from static_graphs import spain_pie_graph, spain_corruption_graph
import plotly.graph_objs as go

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div(children=[
    html.H1(children='International Transparency Rating'),
    html.Div(children='''International Transparency Rating select a Country.'''),
    dcc.Dropdown(
        id='Country_Dropdown',
        options=[{'label': country, 'value': country}
                 for country in international_transparency_data.Country.values],
        value='',
        multi=True
    ),
    html.Div(id='Historical_Graph_Evolution'),
    html.H4(children='Sources'),
    html.Div(id='Sources_Evolution'),
    html.H4(children='CPI Standard Error'),
    html.Div(id='Standard_Error_Evolution'),
    html.H4(children='International Transaparency Table'),
    html.Div(id='Continents_table'),
    html.H4(children='CPI Rank by Region'),
    html.Div(children='''Choose Regions'''),
    dcc.Checklist(
            id='Regions_Selector',
            options=[{'label': region, 'value': region}
                 for region in international_transparency_pivot_data.Region_Full_Name.values],
            values=[region for region in international_transparency_pivot_data.Region_Full_Name.values],
            labelStyle={'display': 'inline-block'},
            style={'height': 100, 'width':'40%'}),
    html.Div(id='Continents_Scatter_Plot_Evolution'),
    html.H4(children='Spain Corruption Graphs'),
    html.Div('corruption cases by political party'),
    html.Div([spain_pie_graph]),
    html.Div([spain_corruption_graph])
])

@app.callback(
    dash.dependencies.Output('Historical_Graph_Evolution', 'children'),
    [dash.dependencies.Input('Country_Dropdown', 'value')])
def historical_graph(Country_Dropdown):
    Historical_Graph_Evolution = []
    Historical_Graph_Evolution.append(dcc.Graph(
        id='Historical Graph',
        figure={
            'data': [
                {'x': [2011, 2012, 2013, 2014, 2015, 2016, 2017],
                 'y': (international_transparency_data
                      [international_transparency_data['Country'] == country]
                       .values.tolist()[0][::-1][:-3]),
                 'type': 'line','name': country}
                for country in Country_Dropdown],
            'layout': {
                'title': 'CPI Evolution',
                'yaxis': dict(
                    range=[0, 100],
                    dtick=10)}}))
    return Historical_Graph_Evolution


@app.callback(
    dash.dependencies.Output('Standard_Error_Evolution', 'children'),
    [dash.dependencies.Input('Country_Dropdown', 'value')])
def standard_graph(Country_Dropdown):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=standard_error[standard_error['Country'] == country]['year'].tolist(),
                    y=standard_error[standard_error['Country'] == country]['standard_error'].tolist(),
                    name=country)
                for country in Country_Dropdown
            ],
            layout=go.Layout(
                title='CPI Standard Error',
                showlegend=True,
                margin=go.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='standard_error_graph')

@app.callback(
    dash.dependencies.Output('Sources_Evolution', 'children'),
    [dash.dependencies.Input('Country_Dropdown', 'value')])
def sources_graph(Country_Dropdown):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=sources[sources['Country']==country]['year'].tolist(),
                    y=sources[sources['Country']==country]['sources'].tolist(),
                    name=country)
                for country in Country_Dropdown
            ],
            layout=go.Layout(
                title='Sources',
                showlegend=True,
                margin=go.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='sources_error_graph')

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
        style={'overflowY': 'scroll', 'height': 100, 'width':'100%'}
    )

@app.callback(
    dash.dependencies.Output('Continents_table', 'children'),
    [dash.dependencies.Input('Country_Dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value in ('', None):
        return None
    df = (international_transparency_data[international_transparency_data.
          Country.str.contains('|'.join(dropdown_value))])
    return generate_table(df)

@app.callback(
    dash.dependencies.Output('Continents_Scatter_Plot_Evolution', 'children'),
    [dash.dependencies.Input('Regions_Selector', 'values')])
def scatter_plot(Regions_Selector):
    filter_df = international_transparency_pivot_data[
                international_transparency_pivot_data['Region_Full_Name'].isin(Regions_Selector)]
    return  dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure={
                            'data': [
                                go.Scatter(
                                    x=filter_df[filter_df['Region_Full_Name'] == region]['year'],
                                    y=filter_df[filter_df['Region_Full_Name'] == region]['cpi_score'],
                                    text= filter_df[filter_df['Region_Full_Name'] == region]['Country'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.2, 'color': 'white'},
                                    },
                                    name=region
                                ) for region in filter_df.Region_Full_Name.unique()
                            ],
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': 'Year', 'range':sorted([filter_df.year.unique()]),
                               'dtick': 1},
                        yaxis={'range':[0, 100],'dtick':10,'title': 'CPI Ranking'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )})

if __name__ == '__main__':
    app.run_server(debug=True)