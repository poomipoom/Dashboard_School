from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Load the data
df = pd.read_json('https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json')

# Create the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Student Data Dashboard', style={'textAlign': 'center', 'color': '#003366'}),
    
    html.Div([
        dcc.Dropdown(
            id='dropdown-selection',
            options=[{'label': province, 'value': province} for province in df['schools_province'].unique()],
            value=df['schools_province'].iloc[0],  # Default value
            style={'width': '50%', 'margin': 'auto'}
        ),
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='line-chart')
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('line-chart', 'figure')],
    [Input('dropdown-selection', 'value')]
)
def update_graphs(selected_province):
    dff = df[df['schools_province'] == selected_province]
    
    # Bar chart for total students by gender
    bar_fig = px.bar(
        dff, 
        x=['totalmale', 'totalfemale'], 
        y='totalstd', 
        labels={'x':'Gender', 'y':'Total Students'},
        title=f'Total Students by Gender in {selected_province}'
    )
    
    # Pie chart for gender distribution
    pie_fig = px.pie(
        values=[dff['totalmale'].sum(), dff['totalfemale'].sum()], 
        names=['Male', 'Female'],
        title=f'Gender Distribution in {selected_province}'
    )
    
    # Line chart for comparison of male and female students
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=dff['schools_province'], y=dff['totalmale'], mode='lines+markers', name='Male Students'))
    line_fig.add_trace(go.Scatter(x=dff['schools_province'], y=dff['totalfemale'], mode='lines+markers', name='Female Students'))
    line_fig.update_layout(
        title=f'Comparison of Male and Female Students in {selected_province}',
        xaxis_title='Province',
        yaxis_title='Number of Students'
    )
    
    return bar_fig, pie_fig, line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
