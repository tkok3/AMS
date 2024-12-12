import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Function to calculate selectivity
def selectivity(pMax, perm, x1):
    pMin = -1
    n = 100
    x = [x1, 1 - x1]
    p = np.logspace(pMin, pMax, n)
    a = np.array([x + 1 / p + 1 / (perm - 1) for x in x])
    b = np.array([(4 * perm * x) / ((perm - 1) * p) for x in x])
    return p, 0.5 * p * (a - np.sqrt(a**2 - b))

# Function to create the Plotly graph
def create_graph(pMax, perm, x1):
    p, sl = selectivity(pMax, perm, x1)

    # Create a subplot grid (1 row, 2 columns)
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Permeate concentration", "Selectivity"],
        shared_yaxes=True,
        horizontal_spacing=0.1
    )

    # Plot the first subplot (Permeate concentration)
    fig.add_trace(go.Scatter(x=p, y=sl[0], mode='lines', name='Compound 1'), row=1, col=1)
    fig.update_xaxes(title_text="Pressure ratio [-]", type='log', row=1, col=1)
    fig.update_yaxes(title_text="y [-]", range=[0, 1], row=1, col=1)

    # Plot the second subplot (Selectivity)
    fig.add_trace(go.Scatter(x=p, y=sl[0] / sl[1], mode='lines', name="Selectivity"), row=1, col=2)
    fig.update_xaxes(title_text="Pressure ratio [-]", type='log', row=1, col=2)
    fig.update_yaxes(title_text="Selectivity [-]", type='log', range=[-3, 0], row=1, col=2)

    # Update layout
    fig.update_layout(
        title="Selectivity Graph",
        template='plotly_white',
        title_font=dict(size=30),
        font=dict(size=20),
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50),
    )
    
    return fig

# Initialize Dash app
app = dash.Dash(__name__)

# Initial values
pMax = 4  # Maximum pressure ratio
perm = 300  # Permeability
x1 = 0.01  # Mole fraction of component 1

# Layout for Dash app
app.layout = html.Div([
    # Title
    html.H1("Interactive Selectivity Graph", style={'fontSize': 36, 'textAlign': 'center'}),

    # Graph component
    dcc.Graph(id='graph'),

    # Sliders for x1 and perm
    html.Div([
        html.Label('x1 (Mole fraction of Component 1)', style={'fontSize': 18}),
        dcc.Slider(
            id='x1-slider',
            min=0,
            max=1,
            step=0.01,
            value=x1,
            marks={i/10: f'{i/10:.1f}' for i in range(11)},
            updatemode='drag',
            included=True,
            tooltip={'placement': 'bottom', 'always_visible': True},
        ),
    ]),

    html.Div([
        html.Label('perm (Permeability)', style={'fontSize': 18}),
        dcc.Slider(
            id='perm-slider',
            min=1,
            max=1000,
            step=1,
            value=perm,
            marks={i: str(i) for i in range(1, 1001, 200)},
            updatemode='drag',
            included=True,
            tooltip={'placement': 'bottom', 'always_visible': True},
        ),
    ]),
])

# Callback to update the graph based on slider values
@app.callback(
    Output('graph', 'figure'),
    [Input('x1-slider', 'value'),
     Input('perm-slider', 'value')]
)
def update_graph(x1_val, perm_val):
    fig = create_graph(pMax, perm_val, x1_val)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
