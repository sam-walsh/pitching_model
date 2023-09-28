import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc  # Import Bootstrap components
from pybaseball import playerid_reverse_lookup

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Add Bootstrap stylesheet

# Load the data from model_predictions.csv
df = pd.read_csv('pitcher_predictions.csv')
leaderboards = df[['player_name', 'pitcher', 'pitch_type', 'pitch_score_percentile', 'pitches_thrown', 'pitch_usage']]
leaderboards['pitch_score_percentile'] = leaderboards['pitch_score_percentile'].astype(int)

# Create a dropdown to select a pitcher by name
pitcher_dropdown = dcc.Dropdown(
    id='pitcher-dropdown',
    options=[{'label': i, 'value': j} for i, j in zip(leaderboards['player_name'].unique().tolist(), leaderboards['pitcher'].unique().tolist())],
    value=leaderboards['pitcher'][0]
)

# Create a slider to filter leaderboards by number of pitches_thrown
pitches_slider = dcc.Slider(
    id='pitches-slider',
    min=leaderboards['pitches_thrown'].min(),
    max=leaderboards['pitches_thrown'].max(),
    value=200,
    step=None
)

# Create a callback to update the image based on the selected pitcher
@app.callback(
    Output('pitcher-info', 'children'),
    [Input('pitcher-dropdown', 'value')]
)
def update_pitcher_info(value):
    pitcher_info = leaderboards[leaderboards['pitcher'] == value][['pitch_type', 'pitch_score_percentile', 'pitch_usage']]
    pitcher_info = pitcher_info.sort_values('pitch_usage', ascending=False)  # Sort by pitch usage
    pitcher_info['pitch_usage'] = pitcher_info['pitch_usage'].apply(lambda x: f"{x}%")  # Convert pitch usage to percentage after sorting

    # Create a list to hold all the cards
    cards = []

    # Create a card for the selected pitcher
    player_name = leaderboards[leaderboards['pitcher'] == value]['player_name'].values[0]
    first_name, last_name = player_name.split(", ")
    formatted_name = f"{last_name} {first_name}"

    pitch_cards = []

    card = dbc.Card(
        dbc.CardBody(
            [
                html.Div([
                    html.Img(src=f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{value}/headshot/67/current",
                             alt='Player Image', style={'height':'150px', 'width':'100px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                    html.H5(formatted_name, className="card-title", style={'textAlign': 'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
                ], style={'display': 'block', 'textAlign': 'center'})
            ]
        ),
        className="mb-3",
        style={"maxWidth": "200px", 'align': 'center'},
        color="light"
    )
    cards.append(card)

    # Create a card for each pitch
    for index, row in pitcher_info.iterrows():
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(row['pitch_type'], className="card-title", style={'textAlign': 'center'}),
                    html.H1(f"{row['pitch_score_percentile']}", className="card-text", style={'textAlign': 'center'}),
                    html.H5(f"{row['pitch_usage']}", className="card-text", style={'textAlign': 'center'})
                ]
            ),
            className="mb-3",
            style={"width": "150px", "height": "150px"},  # Make the cards square
            color="light"
        )
        # Wrap each card in a dbc.Col component
        pitch_cards.append(card)

    pitch_cards_row = dbc.Row(pitch_cards)
    cards.append(pitch_cards_row)

    return cards

# Create checkboxes for each pitch type
pitch_types = leaderboards['pitch_type'].unique().tolist()
pitch_type_checkboxes = dcc.Checklist(
    id='pitch-type-checkboxes',
    options=[{'label': i, 'value': i} for i in pitch_types],
    value=pitch_types,
    inline=True
)

# Create a callback to filter the leaderboard based on the selected pitch types and number of pitches thrown
@app.callback(
    Output('leaderboard', 'data'),
    [Input('pitch-type-checkboxes', 'value'), Input('pitches-slider', 'value')]
)
def update_leaderboard(selected_pitch_types, pitches_thrown):
    filtered_df = leaderboards[(leaderboards['pitch_type'].isin(selected_pitch_types)) & (leaderboards['pitches_thrown'] >= pitches_thrown)]
    # Sort the filtered dataframe by 'pitch_score_percentile' in descending order
    sorted_df = filtered_df.sort_values('pitch_score_percentile', ascending=False)
    return sorted_df.to_dict('records')

app.layout = html.Div(children=[
    html.H1(children='Pitch Percentiles'),

    html.Div(children='''Select a pitcher:'''),
    pitcher_dropdown,
    html.Div(style={'display': 'flex'}, children=[
        html.Img(id='pitcher-image'),
        html.Div(id='pitcher-info'),  # Add a div to display the pitcher info
    ]),
    html.Br(),

    html.H2(children='Leaderboard'),
    html.Div(children='''Select pitch types:'''),
    pitch_type_checkboxes,

    html.Div(children='''Select minimum number of pitches thrown:'''),
    pitches_slider,

    dash_table.DataTable(
        id='leaderboard',
        columns=[{"name": i, "id": i} for i in leaderboards.columns],
        data=leaderboards.to_dict('records'),
        sort_action='native',  # Enable sorting
        sort_by=[{"column_id": "pitch_score_percentile", "direction": "desc"}],  # Default sorting
        page_size=50,  # Display only 50 results per page
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)


