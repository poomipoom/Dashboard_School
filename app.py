from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load the school data
df_schools = pd.read_json('https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json')

# Data for province coordinates
data_coordinates = {
    'จังหวัด': [
        'อำนาจเจริญ', 'อ่างทอง', 'กรุงเทพมหานคร', 'บึงกาฬ', 'บุรีรัมย์', 'ฉะเชิงเทรา',
        'ชัยนาท', 'ชัยภูมิ', 'จันทบุรี', 'เชียงใหม่', 'เชียงราย', 'ชลบุรี',
        'ชุมพร', 'กาฬสินธุ์', 'กำแพงเพชร', 'กาญจนบุรี', 'ขอนแก่น', 'กระบี่',
        'ลำปาง', 'ลำพูน', 'เลย', 'ลพบุรี', 'แม่ฮ่องสอน', 'มหาสารคาม',
        'มุกดาหาร', 'นครนายก', 'นครปฐม', 'นครพนม', 'นครราชสีมา', 'นครสวรรค์',
        'นราธิวาส', 'น่าน', 'นราธิวาส', 'หนองบัวลำภู', 'หนองคาย', 'นนทบุรี',
        'ปทุมธานี', 'ปัตตานี', 'พัทยา', 'พังงา', 'พัทลุง', 'พะเยา',
        'เพชรบูรณ์', 'เพชรบุรี', 'พิจิตร', 'พิษณุโลก', 'พระนครศรีอยุธยา', 'แพร่',
        'ภูเก็ต', 'ปราจีนบุรี', 'ประจวบคีรีขันธ์', 'ระนอง', 'ราชบุรี', 'ระยอง',
        'ร้อยเอ็ด', 'สระแก้ว', 'สกลนคร', 'สมุทรปราการ', 'สมุทรสาคร', 'สมุทรสงคราม',
        'สระบุรี', 'สตูล', 'ศรีสะเกษ', 'สิงห์บุรี', 'สงขลา', 'สุโขทัย', 'สุพรรณบุรี',
        'สุราษฎร์ธานี', 'สุรินทร์', 'ตาก', 'ตรัง', 'ตราด', 'อุบลราชธานี', 'อุดรธานี',
        'อุทัยธานี', 'อุตรดิตถ์', 'ยะลา', 'ยโสธร'
    ],
    'ละติจูด': [
        15.8656783, 14.5896054, 13.7563309, 18.3609104, 14.9951003, 13.6904194,
        15.1851971, 16.0074974, 12.6112485, 18.7883439, 19.9104798, 13.3611431,
        10.4930496, 16.438508, 16.4827798, 14.1011393, 16.4321938, 8.0862997,
        18.2855395, 18.5744606, 17.4860232, 14.7995081, 19.3020296, 16.0132015,
        16.5435914, 14.2069466, 13.8140293, 17.392039, 14.9738493, 15.6987382,
        8.4324831, 18.793, 6.4254607, 17.2218247, 17.8782803, 13.8591084,
        14.0208391, 6.7618308, 12.9235557, 8.4501414, 7.6166823, 19.2154367,
        16.301669, 12.9649215, 16.2740876, 16.8211238, 14.3692325, 18.1445774,
        7.8804479, 14.0420699, 11.7938389, 9.9528702, 13.5282893, 12.6813957,
        16.0538196, 13.824038, 17.1664211, 13.5990961, 13.5475216, 13.4098217,
        14.5289154, 6.6238158, 15.1186009, 14.8936253, 7.1897659, 43.6485556,
        14.4744892, 9.1341949, 37.0358271, 45.0299646, 7.5644833, 12.2427563,
        15.2448453, 17.3646969, 15.3835001, 17.6200886, 44.0579117, 15.792641
    ],
    'ลองจิจูด': [
        104.6257774, 100.455052, 100.5017651, 103.6464463, 103.1115915, 101.0779596,
        100.125125, 101.6129172, 102.1037806, 98.9853008, 99.840576, 100.9846717,
        99.1800199, 103.5060994, 99.5226618, 99.4179431, 102.8236214, 98.9062835,
        99.5127895, 99.0087221, 101.7223002, 100.6533706, 97.9654368, 103.1615169,
        104.7024121, 101.2130511, 100.0372929, 104.7695508, 102.083652, 100.11996,
        99.9599033, 100.786, 101.8253143, 102.4260368, 102.7412638, 100.5216508,
        100.5250276, 101.3232549, 100.8824551, 98.5255317, 100.0740231, 100.2023692,
        101.1192804, 99.6425883, 100.3346991, 100.2658516, 100.5876634, 100.1402831,
        98.3922504, 101.6600874, 99.7957564, 98.6084641, 99.8134211, 101.2816261,
        103.6520036, 102.0645839, 104.1486055, 100.5998319, 100.2743956, 100.0022645,
        100.9101421, 100.0673744, 104.3220095, 100.3967314, 100.5953813, -79.3746639,
        100.1177128, 99.3334198, -95.6276367, -93.1049815, 99.6239334, 102.5174734,
        104.8472995, 102.8158924, 100.0245527, 100.0992942, -123.1653848, 104.1452827
    ]
}

# Create DataFrame for province coordinates
df_coordinates = pd.DataFrame(data_coordinates)

# Create the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1(children='Student Data Dashboard', style={'textAlign': 'center', 'color': '#003366'}),

    html.Div([
        dcc.Dropdown(
            id='dropdown-selection',
            options=[{'label': province, 'value': province} for province in df_schools['schools_province'].unique()],
            value=df_schools['schools_province'].iloc[0],  # Default value
            style={'width': '50%', 'margin': 'auto'}
        ),
    ], style={'textAlign': 'center', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='scatter-map')
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
])

# Define callback to update graphs based on dropdown selection
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-map', 'figure')],
    [Input('dropdown-selection', 'value')]
)
def update_graphs(selected_province):
    dff = df_schools[df_schools['schools_province'] == selected_province]

    # Bar chart for total students by gender
    bar_fig = px.bar(
        dff,
        x=['totalmale', 'totalfemale'],
        y='totalstd',
        labels={'x': 'Gender', 'y': 'Total Students'},
        title=f'Total Students by Gender in {selected_province}'
    )

    # Pie chart for gender distribution
    pie_fig = px.pie(
        values=[dff['totalmale'].sum(), dff['totalfemale'].sum()],
        names=['Male', 'Female'],
        title=f'Gender Distribution in {selected_province}'
    )

    # Scatter map for province coordinates
    scatter_fig = px.scatter_mapbox(df_coordinates, lat="ละติจูด", lon="ลองจิจูด", hover_name="จังหวัด",
                                    hover_data=["จังหวัด"], zoom=5)

    # Highlight selected province with red color and larger size
    selected_province_data = df_coordinates[df_coordinates['จังหวัด'] == selected_province]
    selected_province_lat = selected_province_data['ละติจูด'].iloc[0]
    selected_province_lon = selected_province_data['ลองจิจูด'].iloc[0]

    scatter_fig.add_trace(
        go.Scattermapbox(
            lat=[selected_province_lat],
            lon=[selected_province_lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=12,
                color='red'
            ),
            hoverinfo='skip'
        )
    )

    scatter_fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom = 10,
        mapbox_center={"lat": selected_province_lat, "lon": selected_province_lon},
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return bar_fig, pie_fig, scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
