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
    emissions_column = 'Transport emissions per kilometer travelled'
    df['Total emissions'] = df[emissions_column] * float(distance)
    
    df_sorted = df.sort_values('Total emissions', ascending=False)
    
    plt.figure(figsize=(15, 8))
    plt.bar(df_sorted['Entity'], df_sorted['Total emissions'])
    plt.title(f'CO2 Emissions for {distance} km by transport type', fontsize=18)
    plt.xlabel('Transport Mode', fontsize=16)
    plt.ylabel('CO2 Emissions (g)', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=14)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    
    return df_sorted, plot_data

def show_result(distance):
    df_sorted, plot_data = generate_plot(distance)
    
    # Apply custom styling to the DataFrame HTML
    styled_df = df_sorted.style.set_table_attributes('class="table table-striped emissions-table"')
    styled_df = styled_df.set_properties(**{
        'class': 'entity-column',
        'title': lambda x: x
    }, subset=['Entity'])
    styled_df = styled_df.set_properties(**{
        'class': 'total-emissions-column',
        'title': lambda x: f"{x:.2f}"
    }, subset=['Total emissions'])
    
    # Format the 'Total emissions' column to display 2 decimal places
    styled_df = styled_df.format({'Total emissions': '{:.2f}'})
    
    table_html = styled_df.to_html(classes='table table-striped emissions-table', index=False)
    
    return render_template('result.html', table_data=table_html, plot_url=plot_data, distance=distance)