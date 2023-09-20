import dash
from dash import dcc, html
import dash_table
import pandas as pd

app = dash.Dash(__name__)

# Load the data from model_predictions.csv
df = pd.read_csv('pitcher_predictions.csv')
leaderboards = df[['player_name', 'team', 'pitch_type', 'pitch_score_percentile', 'pitches_thrown']]
leaderboards['pitch_score_percentile'] = leaderboards['pitch_score_percentile'].astype(int)

# Create a slider for the leaderboard for pitches_thrown with the default setting 200
slider = dcc.Slider(
    id='pitches-thrown-slider',
    min=leaderboards['pitches_thrown'].min(),
    max=leaderboards['pitches_thrown'].max(),
    value=200,
)

# Define a callback to update the leaderboard based on the slider value
@app.callback(
    dash.dependencies.Output('leaderboard', 'data'),
    [dash.dependencies.Input('pitches-thrown-slider', 'value')]
)
def update_leaderboard(value):
    filtered_df = leaderboards[leaderboards['pitches_thrown'] >= value]
    return filtered_df.to_dict('records')

app.layout = html.Div(children=[
    html.H1(children='Pitch Percentiles'),

    html.Div(children='''Select minimum number of pitches thrown:'''),

    slider,

    dash_table.DataTable(
        id='leaderboard',
        columns=[{"name": i, "id": i} for i in leaderboards.columns],
        data=leaderboards.to_dict('records'),
        sort_action='native',  # Enable sorting
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)