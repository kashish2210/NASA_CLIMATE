from django.shortcuts import render

import json
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go

def home(request):
    # Your original climate data source
    climate_data = [
        {'location': 'New York City, USA', 'date': '2023-09-10', 'temperature': 22.5, 'precipitation': 0.2},
        {'location': 'London, UK', 'date': '2023-09-10', 'temperature': 18.3, 'precipitation': 3.1},
        {'location': 'Tokyo, Japan', 'date': '2023-09-10', 'temperature': 27.8, 'precipitation': 0.0}
    ]

    # Extract data for the graphs
    locations = [entry['location'] for entry in climate_data]
    temperatures = [entry['temperature'] for entry in climate_data]
    precipitations = [entry['precipitation'] for entry in climate_data]

    # Create temperature vs location bar graph
    temp_bar = go.Bar(
        x=locations,
        y=temperatures,
        name='Temperature (°C)',
        marker=dict(color='orange')
    )

    # Create precipitation vs location bar graph
    precip_bar = go.Bar(
        x=locations,
        y=precipitations,
        name='Precipitation (mm)',
        marker=dict(color='blue')
    )

    # Create a 3D scatter plot of temperature and precipitation vs location
    scatter_3d = go.Scatter3d(
        x=locations,
        y=temperatures,
        z=precipitations,
        mode='markers',
        marker=dict(size=10, color=precipitations, colorscale='Viridis'),
        name='3D Visualization'
    )

    # Layout for 2D and 3D graphs
    layout = go.Layout(
        title='Climate Data Visualization',
        xaxis=dict(title='Location'),
        yaxis=dict(title='Temperature (°C) / Precipitation (mm)')
    )

    layout_3d = go.Layout(
        title='3D Climate Data Visualization',
        scene=dict(
            xaxis_title='Location',
            yaxis_title='Temperature (°C)',
            zaxis_title='Precipitation (mm)'
        )
    )

    # Generate the plotly figure and convert to HTML
    plot_div = plot({'data': [temp_bar, precip_bar], 'layout': layout}, output_type='div')
    plot_3d_div = plot({'data': [scatter_3d], 'layout': layout_3d}, output_type='div')

    context = {
        'climate_data': climate_data,  # Your original context for the table
        'plot_div': plot_div,          # 2D plot
        'plot_3d_div': plot_3d_div,    # 3D plot
    }

    return render(request, 'home.html', context)

def anim(request):
    # Fetch climate data from your data source (replace with your actual data)
    climate_data = [
        {'location': 'New York City, USA', 'date': '2023-09-10', 'temperature': 22.5, 'precipitation': 0.2},
    ]

    # Pass the data to the template
    context = {'climate_data': climate_data}
    return render(request, 'anim.html', context)

def water(request):
    return render(request, 'water.html')

def solar(request):
    return render(request, 'solar.html')