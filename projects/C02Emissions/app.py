import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import importlib  # Add this import
from flask import Flask, render_template, request

app = Flask(__name__)

# Define the path to the CSV file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'carbon-footprint-travel-mode.csv')

def generate_plot(distance):
    """Generate a bar plot based on the distance and return the plot data."""
    df = pd.read_csv(file_path)
    emissions_column = 'Transport emissions per kilometer travelled'
    df['Total emissions'] = df[emissions_column] * distance
    
    # Sort the dataframe by Total emissions
    df_sorted = df.sort_values('Total emissions', ascending=False)
    
    # Create a bar plot
    plt.figure(figsize=(15, 8))  # Increased figure size
    plt.bar(df_sorted['Entity'], df_sorted['Total emissions'])
    plt.title(f'CO2 Emissions for {distance} km by transport type', fontsize=18)
    plt.xlabel('Transport Mode', fontsize=16)
    plt.ylabel('CO2 Emissions (g)', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=14)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    # Save plot to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300)  # Increased DPI for better quality
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    
    return df_sorted, plot_data

@app.route('/')
def home():
    projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projects')
    projects = [
        {"name": project, "url": f"/{project}"}
        for project in os.listdir(projects_dir)
        if os.path.isdir(os.path.join(projects_dir, project))
    ]
    return render_template('home.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

# Dynamically import and register project routes
projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projects')
for project in os.listdir(projects_dir):
    project_path = os.path.join(projects_dir, project)
    if os.path.isdir(project_path):
        try:
            module = importlib.import_module(f'projects.{project}.routes')
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp, url_prefix=f'/{project}')
        except ImportError as e:
            print(f"Could not import routes for project: {project}. Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)