from dash import Dash, Input, Output, html, dcc
import pandas as pd
import plotly.express as px
from frontend.layout import create_layout  # Assuming you have a layout.py for layout


def run_dashboard():
    # Initialize the Dash app
    app = Dash(__name__)

    # Define the layout using the function from layout.py
    app.layout = create_layout()

    # Define the CSV file path
    filename = 'data/sensor_data_log.csv'

    # Callback to update dashboard elements
    @app.callback(
        [
            Output('altitude-card', 'children'),
            Output('temperature-card', 'children'),
            Output('rocket-state-card', 'children'),
            Output('launch-status-card', 'children'),
            Output('altitude-chart', 'figure'),
            Output('temperature-chart', 'figure'),
            Output('rocket-state-chart', 'figure'),
            Output('acceleration-chart', 'figure')
        ],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):
        try:
            # Read data from the CSV file
            data = pd.read_csv(filename)

            # Ensure data is sorted by Timestamp and handle parsing errors
            if 'Timestamp' in data.columns:
                # Coerce errors to NaT (Not a Time) for invalid formats
                data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
                # Drop rows where Timestamp conversion failed
                data = data.dropna(subset=['Timestamp'])
                data = data.sort_values(by='Timestamp')

            # Handle empty data cases gracefully
            if data.empty:
                raise ValueError("No valid data available in the CSV file.")

            # Create figures
            altitude_fig = px.line(data, x='Timestamp', y='Altitude', title='Altitude Over Time').update_layout(
                plot_bgcolor='#2a2a4e', paper_bgcolor='#2a2a4e', font=dict(color='white')
            )
            temperature_fig = px.line(data, x='Timestamp', y='Temperature',
                                      title='Temperature Over Time').update_layout(
                plot_bgcolor='#2a2a4e', paper_bgcolor='#2a2a4e', font=dict(color='white')
            )

            # Handle Rocket State counts
            rocket_state_counts = data['Rocket_State'].value_counts().reset_index(name='count')
            rocket_state_counts.rename(columns={'index': 'Rocket_State'}, inplace=True)
            rocket_state_fig = px.bar(rocket_state_counts,
                                      x='Rocket_State', y='count', title='Rocket State Distribution').update_layout(
                plot_bgcolor='#2a2a4e', paper_bgcolor='#2a2a4e', font=dict(color='white')
            )

            acceleration_fig = px.line(data, x='Timestamp', y='Acceleration',
                                       title='Acceleration Over Time').update_layout(
                plot_bgcolor='#2a2a4e', paper_bgcolor='#2a2a4e', font=dict(color='white')
            )

            # Update card values
            altitude_card = [html.H4("Current Altitude"), html.H2(f"{data['Altitude'].iloc[-1]:.2f} m")]
            temperature_card = [html.H4("Current Temperature"), html.H2(f"{data['Temperature'].iloc[-1]:.2f} °C")]
            rocket_state_card = [html.H4("Current Rocket State"), html.H2(data['Rocket_State'].iloc[-1])]
            launch_status_card = [html.H4("Launch Status"), html.H2(data['Launch_Status'].iloc[-1])]

            return altitude_card, temperature_card, rocket_state_card, launch_status_card, altitude_fig, temperature_fig, rocket_state_fig, acceleration_fig

        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return ["No data available"] * 8
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
            return ["No data available"] * 8
        except KeyError as e:
            print(f"Error: Missing expected column {e}")
            return ["Data error"] * 8
        except Exception as e:
            print(f"Error reading or processing data: {e}")
            return ["Error"] * 8  # Return default error values

    # Run the Dash app
    app.run_server(debug=True)
