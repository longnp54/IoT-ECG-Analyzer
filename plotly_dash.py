import websocket
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import threading
import json

# Initialize the Dash app
app = Dash(__name__)

# Global variables for data storage
heart_rate = 0.0
r_peaks = []
std_rr = 0.0
condition = "Unknown"
heart_condition_value = 0.0
ecg_signal = []  # Variable to store the ECG signal
last_ecg_signal = []  # Variable to store the previous ECG signal for comparison

# Function to handle incoming WebSocket messages
def on_message(ws, message):
    global heart_rate, r_peaks, std_rr, condition, heart_condition_value, ecg_signal
    try:
        data = json.loads(message)
        if "heart-rate" in data:
            heart_rate = float(data["heart-rate"])
        if "r_peaks" in data:
            r_peaks = data["r_peaks"]
        if "std_rr" in data:
            std_rr = float(data["std_rr"])
        if "HeartCondition" in data:
            condition = data["HeartCondition"]
        if "HeartConditionValue" in data:
            heart_condition_value = float(data["HeartConditionValue"])
        if "ecg-signal" in data:
            ecg_signal = data["ecg-signal"]

        print(f"Heart Rate: {heart_rate:.2f} BPM, Condition: {condition}, R-peaks: {len(r_peaks)}, ECG Signal: {len(ecg_signal)} samples")
    except json.JSONDecodeError:
        print("Error decoding JSON message.")
    except Exception as e:
        print(f"Error processing WebSocket message: {e}")

# Function to start the WebSocket connection
def start_websocket():
    url = "ws://localhost:1880/ws/data"
    ws = websocket.WebSocketApp(url, on_message=lambda ws, msg: (print("Raw message received:", msg), on_message(ws, msg)))
    ws.run_forever()

# Function to run the Dash app
def run_dash_app():
    app.run_server(debug=True, port=8050)

# Run the WebSocket in a separate thread to avoid blocking the Dash app
threading.Thread(target=start_websocket, daemon=True).start()

# Layout of the Dash app
app.layout = html.Div([
    # Header section
    html.Header(
        html.H1("Heart Rate Monitor", style={
            'textAlign': 'center',
            'color': '#2d3e50',
            'font-family': 'Arial, sans-serif',
            'font-size': '40px',
            'marginTop': '30px'
        })
    ),
    # Main content section
    html.Div([
        # Heart rate display
        html.Div(id='heart-rate-display', style={
            'fontSize': '36px',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'color': '#e74c3c',
            'marginTop': '20px'
        }),
        # Statistics cards
        html.Div([
            html.Div(
                [
                    html.P("Heart Condition", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#3498db'}),
                    html.P(id='condition', style={'fontSize': '24px', 'color': '#2d3e50'})
                ],
                style={
                    'width': '30%',
                    'display': 'inline-block',
                    'backgroundColor': '#d6eaf8',
                    'padding': '15px',
                    'margin': '5px',
                    'border': '1px solid #2980b9',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }
            ),
            html.Div(
                [
                    html.P("R-peaks Detected", style={'fontSize': '18px', 'fontWeight': 'bold'}),
                    html.P(id='r-peaks-count', style={'fontSize': '24px', 'color': '#2d3e50'})
                ],
                style={
                    'width': '30%',
                    'display': 'inline-block',
                    'backgroundColor': '#fff',
                    'padding': '15px',
                    'margin': '5px',
                    'border': '1px solid #BDC3C7',
                    'borderRadius': '8px',
                    'textAlign': 'center'
                }
            ),
            html.Div(
                [
                    html.P("Standard Deviation of RR", style={'fontSize': '18px', 'fontWeight': 'bold'}),
                    html.P(id='std-rr', style={'fontSize': '24px', 'color': '#2d3e50'})
                ],
                style={
                    'width': '30%',
                    'display': 'inline-block',
                    'backgroundColor': '#fff',
                    'padding': '15px',
                    'margin': '5px',
                    'border': '1px solid #BDC3C7',
                    'borderRadius': '8px',
                    'textAlign': 'center'
                }
            ),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '30px'}),
        # ECG signal graph
        html.Div([
            dcc.Graph(id='ecg-signal-graph', style={'marginTop': '40px'})
        ]),
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px'}),
    # Interval component for updating the dashboard
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

# Callback to update the dashboard based on data
def update_display(n):
    global heart_rate, r_peaks, std_rr, condition, heart_condition_value, ecg_signal, last_ecg_signal

    # Update only if the ECG signal has changed
    if ecg_signal == last_ecg_signal:
        raise PreventUpdate

    last_ecg_signal = ecg_signal[:]  # Save the new state of the ECG signal

    if not ecg_signal:  # If there is no ECG signal, use a default value to prevent errors
        ecg_signal = [0] * 100  # Default 100 samples of zero

    # Calculate the duration of the ECG signal in seconds
    signal_duration = len(ecg_signal) / 100  # Sampling frequency is 100 Hz

    # Generate time points for the x-axis (in seconds)
    time_points = [i / 100 for i in range(len(ecg_signal))]  # Convert sample index to time

    # Display current heart rate
    heart_rate_display = f"Current Heart Rate: {heart_rate:.2f} BPM"

    # Display statistics
    r_peaks_count = len(r_peaks)
    std_rr_display = f"{std_rr:.2f} ms"
    condition_display = f"{condition}"

    # Create the ECG signal graph with time on the x-axis
    ecg_figure = {
        'data': [
            {'x': time_points, 'y': ecg_signal, 'type': 'line', 'name': 'ECG Signal', 'line': {'color': '#3498db'}},
            {'x': [time_points[i] for i in r_peaks], 'y': [ecg_signal[i] for i in r_peaks], 'mode': 'markers', 'marker': {'color': 'red', 'size': 8}, 'name': 'R-peaks'}
        ],
        'layout': {
            'title': 'ECG Signal',
            'xaxis': {'title': 'Time (s)', 'showgrid': True},
            'yaxis': {'title': 'Amplitude', 'showgrid': True},
            'plot_bgcolor': '#ecf0f1',
            'paper_bgcolor': '#ecf0f1',
            'uirevision': 'graph-update'
        }
    }

    return heart_rate_display, r_peaks_count, std_rr_display, condition_display, ecg_figure

# Register the callback
app.callback(
    [Output('heart-rate-display', 'children'),
     Output('r-peaks-count', 'children'),
     Output('std-rr', 'children'),
     Output('condition', 'children'),
     Output('ecg-signal-graph', 'figure')],
    Input('interval', 'n_intervals')
)(update_display)

# Run the Dash app
if __name__ == '__main__':
    # Run the Dash app in the main thread
    run_dash_app()