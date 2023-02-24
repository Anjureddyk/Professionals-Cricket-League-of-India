# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 12:39:18 2023

@author: Anju Reddy K
"""
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Load data
data = pd.read_csv('IPL Matches 2008-2020.csv')

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1('Descriptive analysis on Professional Cricket League of India',style={'text-align': 'center'}),
    dcc.Dropdown(
        id='visualization-dropdown',
        options=[
            {'label': 'Histogram of Result Margins', 'value': 'histogram'},
            {'label': 'Winning Team by City', 'value': 'winner'},
            {'label': 'Player of the Match Counts by Team', 'value': 'player_of_match'},
            {'label': 'Toss Decision by Venue', 'value': 'toss_decision'},
            {'label': 'Result Margins by City', 'value': 'result_margin'},
            {'label': 'Matches played in each city', 'value': 'city'},
            {'label': 'Top 10 Players of the Match', 'value': 'top_players'},
            {'label': 'Most Successful Venue for Team 1', 'value': 'most_successful_venue1'},
            {'label': 'Most Successful Venue for Team 2', 'value': 'most_successful_venue2'},
            {'label': 'Highest result Margins for Each Team', 'value': 'team_results'},
            {'label': 'Matches Won by Each Team', 'value': 'team_wins'},
            {'label': 'Matches Lost by Each Team', 'value': 'team_losses'},
            {'label': 'Matches Tied by Each Team', 'value': 'team_ties'},
            {'label': 'Matches played by city and team', 'value': 'matches_by_city_team'}
        ],
        value='histogram'
    ),
    html.Div(id='visualization')
])

# Define callback for the visualization dropdown
@app.callback(
    dash.dependencies.Output('visualization', 'children'),
    [dash.dependencies.Input('visualization-dropdown', 'value')]
)
def update_visualization(value):
    if value == 'histogram':
        fig = px.histogram(data, x='result_margin')
        return dcc.Graph(figure=fig)
    elif value == 'winner':
        fig = px.scatter(data, x='winner', y='city')
        return dcc.Graph(figure=fig)
    elif value == 'player_of_match':
        batsmen_runs = data.groupby('player_of_match')['player_of_match'].count().reset_index(name='count')
        batsmen_runs = batsmen_runs.sort_values(by='count', ascending=False)[:10]
        fig = px.bar(batsmen_runs, x='player_of_match', y='count')
        return dcc.Graph(figure=fig)
    elif value == 'toss_decision':
        fig = px.scatter(data, x='toss_winner', y='venue', color='toss_decision')
        return dcc.Graph(figure=fig)
    elif value == 'result_margin':
        fig = px.box(data, x='city', y='result_margin')
        return dcc.Graph(figure=fig)
    elif value == 'city':
        fig = px.histogram(data, x='city')
        return dcc.Graph(figure=fig)
    elif value == 'top_players':
        top_players = data.groupby('player_of_match').size().reset_index(name='count')
        top_players = top_players.sort_values(by='count', ascending=False)[:10]
        fig = px.bar(top_players, x='player_of_match', y='count')
        return dcc.Graph(figure=fig)
    elif value == 'most_successful_venue1':
        successful_venue_team1 = data.groupby(['team1', 'venue']).size().reset_index(name='matches')
        successful_venue_team1 = successful_venue_team1.loc[successful_venue_team1['team1'] != 'Rising Pune Supergiant']
        fig = px.bar(successful_venue_team1, x='team1', y='matches', color='venue', title='Most Successful Venue for each team')
        fig.update_layout(xaxis_title='Team', yaxis_title='Matches', legend_title='Venue')
        return dcc.Graph(figure=fig)
    elif value == 'most_successful_venue2':
        successful_venue_team1 = data.groupby(['team2', 'venue']).size().reset_index(name='matches')
        successful_venue_team1 = successful_venue_team1.loc[successful_venue_team1['team2'] != 'Royal Challengers Bangalore']
        fig = px.bar(successful_venue_team1, x='team2', y='matches', color='venue', title='Most Successful Venue for each team')
        fig.update_layout(xaxis_title='Team', yaxis_title='Matches', legend_title='Venue')
        return dcc.Graph(figure=fig)
    elif value == 'team_results':
        team_results = data.groupby('winner')['winner'].count().reset_index(name='matches_won')
        fig = px.bar(team_results, x='winner', y='matches_won')
        return dcc.Graph(figure=fig)
    elif value == 'team_wins':
        team_wins = data.groupby('winner')['winner'].count().reset_index(name='matches_won')
        fig = px.bar(team_wins, x='winner', y='matches_won')
        return dcc.Graph(figure=fig)
    elif value == 'team_losses':
        team_losses = pd.concat([data['team1'], data['team2']], axis=1)
        team_losses['loser'] = np.where(team_losses['team1']==data['winner'], team_losses['team2'], team_losses['team1'])
        team_losses = team_losses.groupby('loser')['loser'].count().reset_index(name='matches_lost')
        fig = px.bar(team_losses, x='loser', y='matches_lost')
        return dcc.Graph(figure=fig)
    elif value == 'team_ties':
    # Create a DataFrame with the teams and winners
        team_ties = pd.concat([data['team1'], data['team2'], data['winner']], axis=1)

    # Create a new column called "loser" that contains the name of the team that lost each match
        team_ties['loser'] = np.where(team_ties['team1'] == team_ties['winner'], team_ties['team2'], team_ties['team1'])

    # Create a new column called "result" that indicates whether the match was a tie or not
        team_ties['result'] = np.where(team_ties['winner'] == 'tie', 'tie', 'no tie')

    # Group the data by the "team" and "result" columns and count the number of occurrences
        team_ties = team_ties.groupby(['team1', 'result'])['result'].count().reset_index(name='count')

    # Filter the data to include only ties
        team_ties = team_ties[team_ties['result'] == 'tie']

    # Rename the "team1" column to "team"
        team_ties = team_ties.rename(columns={'team1': 'team'})

    # Create a bar chart with the team names on the x-axis and the number of ties on the y-axis
        fig = px.bar(team_ties, x='team', y='count')

        return dcc.Graph(figure=fig)
    
    elif value == 'matches_by_city_team':
    # Create a DataFrame with the teams, cities, and match counts
        matches_by_city_team = data.groupby(['city', 'team1'])['team1'].count().reset_index(name='matches')
        matches_by_city_team = pd.concat([matches_by_city_team, data.groupby(['city', 'team2'])['team2'].count().reset_index(name='matches')], ignore_index=True)
        
    # Create a horizontal stacked bar chart with the city on the y-axis, the number of matches on the x-axis, and the team name as the color
        fig = px.bar(matches_by_city_team, x='matches', y='city', color='team1', orientation='h')

        return dcc.Graph(figure=fig)
       
          

if __name__ == '__main__':
    app.run_server(debug=True)

        
