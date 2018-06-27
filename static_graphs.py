import dash_core_components as dcc
import plotly.graph_objs as go
from datasets import spain_corruption

def pie_chart_labels(dataframe, key):
    results = dataframe.groupby([key]).count().to_records()
    labels = []
    for label in results:
        political_party = label[0]
        number_of_political_parties = label[0].split(',')
        number_of_occurencies = label[1]
        if len(number_of_political_parties)>1:
            labels.append('More than 1 political parties')
        elif number_of_occurencies<8:
            labels.append('Others')
        else:
            labels.append(political_party)
    return labels

def pie_chart_values(dataframe,key):
    results = [result[1] for result in dataframe.groupby([key]).count().to_records()]
    return results

def pie_graph(labels, values):
    return dcc.Graph(id='Corruption by political party',
              figure={
                  'data': [go.Pie(labels=labels, values=values, hole= .4,)]})

parties_labels = pie_chart_labels(dataframe=spain_corruption, key='partido')
parties_values = pie_chart_values(dataframe=spain_corruption, key='partido')
spain_pie_graph = pie_graph(labels=parties_labels, values=parties_values)

def get_years(year):
    if year[0]=='\t':
        return year[1:5]
    else:
        return year[0:4]

def spain_corruption_evolution():
    spain_corruption_filter_data = spain_corruption[(spain_corruption['year']>=2000)
                                                    & (spain_corruption['year']<=2011)]
    yvalues=[records[1] for records in spain_corruption_filter_data.groupby(['year']).count().to_records()]
    xvalues = [records[0] for records in spain_corruption_filter_data.groupby(['year']).count().to_records()]
    return dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=xvalues,
                            y=yvalues,
                            marker=go.Marker(
                                color='rgb(55, 83, 109)'
                            ),
                        )
                    ],
                    layout=go.Layout(
                        title='Corruption Cases per Year',
                        showlegend=False,
                        margin=go.Margin(l=40, r=0, t=40, b=30)
                    )
                ),
                style={'height': 300},
                id='my-graph')

spain_corruption_graph = spain_corruption_evolution()