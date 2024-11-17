from dash import dcc, html

def create_layout():
    layout = html.Div(style={'backgroundColor': '#2a2a4e', 'color': 'white', 'padding': '10px'}, children=[
        html.H1("Rocket Sensor Data Dashboard", style={'textAlign': 'center', 'color': 'white'}),

        # Live video feed embedded using an iframe
        html.Div(children=[
            html.H2("Live Flight Video", style={'textAlign': 'center', 'color': 'white'}),
            html.Iframe(src="http://localhost:5000/video_feed", style={'width': '100%', 'height': '500px', 'borderRadius': '10px'})
        ], style={'padding': '20px'}),

        # Interval component to update every few seconds
        dcc.Interval(
            id='interval-component',
            interval=1000,  # Update every 1 second
            n_intervals=0
        ),

        # Overview Cards
        html.Div(style={'display': 'flex', 'justifyContent': 'space-around'}, children=[
            html.Div(id='altitude-card', style={'backgroundColor': '#b56576', 'padding': '20px', 'borderRadius': '8px'}),
            html.Div(id='temperature-card', style={'backgroundColor': '#6c757d', 'padding': '20px', 'borderRadius': '8px'}),
            html.Div(id='rocket-state-card', style={'backgroundColor': '#fca311', 'padding': '20px', 'borderRadius': '8px'}),
            html.Div(id='launch-status-card', style={'backgroundColor': '#14213d', 'padding': '20px', 'borderRadius': '8px'})
        ]),

        # Graphs
        html.Div(children=[
            html.Div(children=[dcc.Graph(id='altitude-chart')], style={'width': '48%', 'display': 'inline-block'}),
            html.Div(children=[dcc.Graph(id='temperature-chart')], style={'width': '48%', 'display': 'inline-block'}),
            html.Div(children=[dcc.Graph(id='rocket-state-chart')], style={'width': '48%', 'display': 'inline-block'}),
            html.Div(children=[dcc.Graph(id='acceleration-chart')], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
    return layout
