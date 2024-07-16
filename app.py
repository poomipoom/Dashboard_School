import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Load the school data
df_schools = pd.read_json('data/school_province.json')
df_coordinates = pd.read_csv('data/province_coordinates.csv')

# Calculate total students for each province
df_total_students = df_schools.groupby('schools_province').agg({'totalstd': 'sum'}).reset_index()
df_total_students.rename(columns={'schools_province': 'จังหวัด', 'totalstd': 'Total Students'}, inplace=True)

# Merge the coordinates with the total students data
df_map_data = pd.merge(df_coordinates, df_total_students, on='จังหวัด', how='left')

# Filter out rows with NaN values in Total Students
df_map_data = df_map_data.dropna(subset=['Total Students'])

# Define a dictionary mapping provinces to regions
province_to_region = {
    'ภาคเหนือ': ['เชียงใหม่', 'เชียงราย', 'ลำปาง', 'ลำพูน', 'แม่ฮ่องสอน', 'แพร่', 'น่าน', 'พะเยา', 'ตาก', 'อุตรดิตถ์', 'สุโขทัย'],
    'ภาคตะวันออกเฉียงเหนือ': ['นครราชสีมา', 'ขอนแก่น', 'อุดรธานี', 'อุบลราชธานี', 'บุรีรัมย์', 'สุรินทร์', 'ศรีสะเกษ', 'กาฬสินธุ์', 'มหาสารคาม', 'ร้อยเอ็ด', 'เลย', 'สกลนคร', 'นครพนม', 'มุกดาหาร', 'บึงกาฬ', 'หนองบัวลำภู', 'หนองคาย', 'ชัยภูมิ', 'อำนาจเจริญ', 'ยโสธร'],
    'ภาคกลาง': ['กรุงเทพมหานคร', 'สมุทรปราการ', 'นนทบุรี', 'ปทุมธานี', 'พระนครศรีอยุธยา', 'อ่างทอง', 'ลพบุรี', 'สระบุรี', 'ชัยนาท', 'สิงห์บุรี', 'สมุทรสาคร', 'สมุทรสงคราม', 'นครปฐม', 'กาญจนบุรี', 'สุพรรณบุรี', 'ราชบุรี'],
    'ภาคตะวันออก': ['ชลบุรี', 'ระยอง', 'จันทบุรี', 'ตราด', 'ฉะเชิงเทรา', 'ปราจีนบุรี', 'สระแก้ว'],
    'ภาคใต้': ['ภูเก็ต', 'สงขลา', 'นครศรีธรรมราช', 'สุราษฎร์ธานี', 'กระบี่', 'ตรัง', 'พัทลุง', 'ระนอง', 'พังงา', 'ชุมพร', 'นราธิวาส', 'ปัตตานี', 'ยะลา']
}

# Add a column 'Region' to df_schools
def get_region(province):
    for region, provinces in province_to_region.items():
        if province in provinces:
            return region
    return None

df_schools['Region'] = df_schools['schools_province'].apply(get_region)

# Calculate total students for each region
df_region_total = df_schools.groupby('Region').agg({'totalstd': 'sum'}).reset_index()
df_region_total.rename(columns={'totalstd': 'Total Students'}, inplace=True)

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container([
    html.H1('Graduate Student Data Dashboard', style={
        'backgroundColor': '#2C3E50',
            'padding': '20px',
            'borderRadius': '10px',
            'color': 'white',
            'textAlign': 'center',
            'marginTop': '20px'
        }),
    
    dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': province, 'value': province} for province in df_schools['schools_province'].unique()],
        value='พังงา',
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='gender-bar-chart'), width=6),
        dbc.Col(dcc.Graph(id='gender-pie-chart'), width=6)
    ], style={'marginTop': '20px'}),
    
    dbc.Row([
        dbc.Col(html.Div(id='summary-section', style={
            'backgroundColor': '#2C3E50',
            'padding': '20px',
            'borderRadius': '10px',
            'color': 'white',
            'textAlign': 'center',
            'marginTop': '20px'
        }), width=12)
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    dbc.Row([
        dbc.Col(dcc.Graph(id='province-map'), width=12),
        dbc.Col(dcc.Graph(id='region-pie-chart'), width=12)
    ], style={'marginTop': '20px'}),  
])

# Define the callback to update charts and map based on the selected province
@callback(
    [Output('gender-bar-chart', 'figure'),
     Output('gender-pie-chart', 'figure'),
     Output('province-map', 'figure'),
     Output('region-pie-chart', 'figure'),
     Output('summary-section', 'children')],
    [Input('province-dropdown', 'value')]
)
def update_dashboard(selected_province):
    filtered_df = df_schools[df_schools['schools_province'] == selected_province]
    total_students = filtered_df['totalstd'].sum()
    total_male = filtered_df['totalmale'].sum()
    total_female = filtered_df['totalfemale'].sum()
    
    # Bar chart for total students by gender
    bar_chart = px.bar(
        filtered_df.melt(id_vars='schools_province', value_vars=['totalmale', 'totalfemale', 'totalstd']),
        x='variable',
        y='value',
        labels={'variable': 'Gender', 'value': 'Total Students'},
        title=f'Total Students by Gender in {selected_province}',
        color='variable',
        color_discrete_map={'totalmale': 'blue', 'totalfemale': 'red', 'totalstd': 'black'}
    )

    # Pie chart for gender distribution
    pie_chart = px.pie(
        names=['Male', 'Female'],
        values=[total_male, total_female],
        title=f'Gender Distribution in {selected_province}',
        color_discrete_map={'Male': 'blue', 'Female': 'red'}
    )

    # Create scatter plot traces for different ranges of Total Students
    scatter_data = []

    ranges = [
        (0, 1000, 5, 'Students < 1000'),
        (1000, 2000, 10, 'Students 1000-2000'),
        (2000, 3000, 15, 'Students 2000-3000'),
        (3000, float('inf'), 20, 'Students >= 3000')
    ]

    for min_students, max_students, size, label in ranges:
        range_df = df_map_data[(df_map_data['Total Students'] >= min_students) & (df_map_data['Total Students'] < max_students)]
        scatter_data.append(
            go.Scattermapbox(
                lat=range_df['ละติจูด'],
                lon=range_df['ลองจิจูด'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=size,
                    color='blue',
                    opacity=0.5
                ),
                text=range_df.apply(
                    lambda row: f"{row['จังหวัด']}: {row['Total Students']} students", axis=1
                ),
                hoverinfo='text',
                name=label
            )
        )

    # Create map figure
    map_fig = go.Figure(data=scatter_data)
    
    selected_coords = df_map_data[df_map_data['จังหวัด'] == selected_province]
    if not selected_coords.empty:
        map_fig.add_trace(go.Scattermapbox(
            lat=selected_coords['ละติจูด'],
            lon=selected_coords['ลองจิจูด'],
            mode='markers+text',
            marker=go.scattermapbox.Marker(size=14, color='red'),
            # text=selected_coords.apply(
            #     lambda row: f"{row['จังหวัด']}: {row['Total Students']} students", axis=1
            # ),
            hoverinfo='none',
            name=f"{selected_coords['จังหวัด'].iloc[0]}: {selected_coords['Total Students'].iloc[0]} students"
        ))
        map_fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=5,
            mapbox_center={"lat": selected_coords['ละติจูด'].iloc[0], "lon": selected_coords['ลองจิจูด'].iloc[0]}
        )
    else:
        map_fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=5,
            mapbox_center={"lat": 13.736717, "lon": 100.523186}  # Default to Bangkok if no data
        )

    # Pie chart for total students by region
    region_pie_chart = px.pie(
        df_region_total,
        names='Region',
        values='Total Students',
        title='Total Students by Region'
    )

    summary_section = [
        html.H3(f"Total Students in {selected_province}: {total_students}"),
        html.P(f"Male: {total_male}"),
        html.P(f"Female: {total_female}")
    ]
    
    return bar_chart, pie_chart, map_fig, region_pie_chart, summary_section

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
