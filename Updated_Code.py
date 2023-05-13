import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


data = pd.read_csv('IPL Matches 2008-2020.csv')

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1('IPL Data Visualizations'),
    dcc.Dropdown(
        id='visualization-dropdown',
        options=[
            {'label': 'Histogram of Result Margins', 'value': 'histogram'},
            {'label': 'Winning Team by City', 'value': 'winner'},
            {'label': 'Player of the Match Counts by Team', 'value': 'player_of_match'},
            {'label': 'Matches played in each city', 'value': 'city'},
            {'label': 'Toss Decision Distribution', 'value': 'toss_outcomes'},
            {'label': 'Matches played by each team', 'value': 'team'},
            {'label': 'Result Outcomes', 'value': 'result_outcomes'},
            {'label': 'Toss Winners by Team', 'value': 'toss_winners_by_team'},
            {'label': 'Matches played by city and team', 'value': 'matches_by_city_team'},
            {'label': 'Most successful venue for team1', 'value': 'successful_venue1'}
        ],
        value='histogram'
    ),
    html.Button('Shape of the dataset', id='button-shape', n_clicks=0),
    html.Button('First 5 rows', id='button-head', n_clicks=0),
    html.Button('Null values', id='button-null', n_clicks=0),
    html.Button('Categorical and numerical values', id='button-types', n_clicks=0),
    html.Button('Last 5 rows', id='button-tail', n_clicks=0),
    html.Div(id='visualization'),
])

# Define callback for the visualization dropdown
@app.callback(
    dash.dependencies.Output('visualization', 'children'),
    [dash.dependencies.Input('visualization-dropdown', 'value'),
     dash.dependencies.Input('button-shape', 'n_clicks'),
     dash.dependencies.Input('button-head', 'n_clicks'),
     dash.dependencies.Input('button-null', 'n_clicks'),
     dash.dependencies.Input('button-tail', 'n_clicks'),
     dash.dependencies.Input('button-types','n_clicks')]
)
def update_visualization(value, n_clicks_shape, n_clicks_head, n_clicks_null,n_clicks_tail, n_clicks_4):
    if n_clicks_shape > 0:
        return html.Div([
            html.H3('Shape of the Dataset'),
            html.P(str(data.shape))
        ])
    elif n_clicks_head > 0:
        return html.Div([
            html.H3('first rows of the Dataset'),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in data.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(data.iloc[i][col]) for col in data.columns
                    ]) for i in range(min(len(data), 5))
                ])
            ])
        ])
    elif n_clicks_null > 0:
        null_counts = data.isnull().sum()
        null_table = pd.DataFrame({'Column Name': null_counts.index, 'Null Count': null_counts.values})
        return html.Div([        html.H3('Null Values'),        html.Table([            html.Thead(html.Tr([html.Th('Column Name'), html.Th('Null Count')])),
            html.Tbody([                html.Tr([html.Td(null_table.iloc[i]['Column Name']), html.Td(null_table.iloc[i]['Null Count'])])
                for i in range(len(null_table))
            ])
        ])
    ])

    elif n_clicks_tail > 0:
        return html.Div([
            html.H3('Last rows of the dataset'),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in data.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(data.iloc[i][col]) for col in data.columns
                    ]) for i in range(max(len(data) - 5, 0), len(data))
                ])
            ])
        ])

    

    elif n_clicks_4 > 0:
        cat_cols = list(data.select_dtypes(include='object').columns)
        num_cols = list(data.select_dtypes(exclude='object').columns)
        return html.Div([
            html.H3('Categorical and Numerical Variables'),
            html.P(f'The dataset has {len(cat_cols)} categorical variables and {len(num_cols)} numerical variables.')
        ])

    else:
        if value == 'histogram':
            fig = px.histogram(data, x='result_margin', nbins=30, marginal='box')
            return dcc.Graph(figure=fig)
        
        elif value == 'winner':
            win_counts = data['winner'].value_counts()
            fig = px.bar(x=win_counts.index, y=win_counts.values)
            fig.update_layout(title='Winning Team by City', xaxis_title='Team', yaxis_title='Count')
            return dcc.Graph(figure=fig)

        elif value == 'player_of_match':
            fig = px.bar(data, x='player_of_match', y='winner', color='winner', barmode='stack')
            return dcc.Graph(figure=fig)

        elif value == 'city':
            fig = px.histogram(data, x='city', color='winner')
            return dcc.Graph(figure=fig)
        
        elif value == 'toss_outcomes':
            fig = px.pie(data, names='toss_decision', hole=.3)
            return dcc.Graph(figure=fig)
        
        elif value == 'team':
            fig = px.histogram(data, x='winner', color='winner')
            return dcc.Graph(figure=fig)
        
        elif value == 'result_outcomes':
            fig = px.pie(data, names='result', hole=.3)
            return dcc.Graph(figure=fig)
        
        elif value == 'toss_winners_by_team':
            fig = px.bar(data, x='toss_winner', y='winner', color='toss_decision', barmode='group')
            return dcc.Graph(figure=fig)
        
        elif value == 'matches_by_city_team':
            fig = px.scatter(data, x='city', y='winner', color='winner')
            return dcc.Graph(figure=fig)
        
        elif value == 'successful_venue1':
            fig = px.bar(data, x='winner', y='venue', color='city', barmode='group')
            return dcc.Graph(figure=fig)
            
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
