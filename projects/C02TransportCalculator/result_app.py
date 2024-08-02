import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import render_template

# Use the current directory to reference the CSV file
file_path = os.path.join(os.path.dirname(__file__), 'carbon-footprint-travel-mode.csv')

def generate_plot(distance):
    df = pd.read_csv(file_path)
    emissions_column = 'Emissions per km'
    df['Total emissions'] = df[emissions_column] * float(distance)
    
    df_sorted = df.sort_values('Total emissions', ascending=False)
    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted['Numbered Entity'] = (df_sorted.index + 1).astype(str) + '. ' + df_sorted['Entity']
    
    plt.figure(figsize=(15, 10))
    bars = plt.barh(df_sorted['Numbered Entity'], df_sorted['Total emissions'], color='#4285F4')
    plt.title(f'CO2 Emissions for {distance} km by Transport Type', fontsize=18)
    plt.xlabel('CO2 Emissions (g)', fontsize=16)
    plt.ylabel('Transport Mode', fontsize=16)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add value labels to the end of each bar
    for i, v in enumerate(df_sorted['Total emissions']):
        plt.text(v, i, f' {v:.2f}', va='center', fontsize=10)
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    
    return df_sorted, plot_data

def show_result(distance):
    df_sorted, plot_data = generate_plot(distance)
    
    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted['No.'] = range(1, len(df_sorted) + 1)
    
    columns_order = ['No.', 'Entity', 'Emissions per km', 'Total emissions']
    df_sorted = df_sorted[columns_order]
    
    # Format numeric columns
    df_sorted['Emissions per km'] = df_sorted['Emissions per km'].map('{:.2f}'.format)
    df_sorted['Total emissions'] = df_sorted['Total emissions'].map('{:.2f}'.format)
    
    # Convert to HTML with custom classes and styles
    table_html = df_sorted.to_html(
        classes='table table-striped table-hover emissions-table',
        index=False,
        escape=False,
        formatters={
            'Emissions per km': lambda x: f'<div class="text-right">{x}</div>',
            'Total emissions': lambda x: f'<div class="text-right">{x}</div>'
        }
    )
    
    return render_template('result.html', 
                           table_data=table_html, 
                           plot_url=plot_data, 
                           distance=distance)