import os
import shutil
import json
import re

def is_valid_project_name(name):
    pattern = r'^[a-zA-Z1-9_ ]{3,}$'
    return bool(re.match(pattern, name))

def create_project():
    # Get the project name from the user
 # Get the project name from the user
    project_name = input("Enter the name of the new project: a-z_ len > 2 ")
    project_name = project_name.lower().strip().replace(" ", "_")
        
    if not is_valid_project_name(project_name):
        print("Invalid project name")
        return

    # Get the display name from the user
    display_name = input("Enter the display name for the project (press Enter to use the project name): ").strip()
    if not display_name:
        display_name = project_name

    # Get the directory of the script being executed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    template_dir = os.path.join(script_dir, 'project_templates')
    projects_dir = os.path.join(script_dir, 'projects')
    new_project_dir = os.path.join(projects_dir, project_name)

    # Check if project already exists
    if os.path.exists(new_project_dir):
        print(f"Error: Project '{project_name}' already exists.")
        return

    try:
        # Create projects directory if it doesn't exist
        os.makedirs(projects_dir, exist_ok=True)

        # Copy template to new project directory
        shutil.copytree(template_dir, new_project_dir)

        # Update project_config.json
        config_path = os.path.join(new_project_dir, 'project_config.json')
        config_data = {
            "project_name": project_name,
            "display_name": display_name,
            "debug": True,
            "port": 5600,
            "secret_key": "default_secret_key_replace_me_in_production"
        }
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        # Update routes.py with the correct project name
        routes_path = os.path.join(new_project_dir, 'routes.py')
        with open(routes_path, 'r') as file:
            content = file.read()
        content = content.replace('PROJECT_NAME', project_name)
        with open(routes_path, 'w') as file:
            file.write(content)
            
        # Create __init__.py file
# Create __init__.py file
        init_content = f"""# {project_name} initialization
from flask import Flask
import os
import json

def create_app():
    app = Flask(__name__)

    # Load configuration from project_config.json
    config_path = os.path.join(os.path.dirname(__file__), 'project_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            app.config.update(config)

    # Ensure project_name and display_name are set
    if 'project_name' not in app.config:
        app.config['project_name'] = os.path.basename(os.path.dirname(__file__))
    if 'display_name' not in app.config:
        app.config['display_name'] = app.config['project_name']

    # ... other configurations ...

    from . import routes
    bp = routes.bp
    bp.name = app.config['project_name']  # Dynamically set the blueprint name
    app.register_blueprint(bp)

    return app
"""
    
        init_path = os.path.join(new_project_dir, '__init__.py')
        with open(init_path, 'w') as init_file:
            init_file.write(init_content.strip())

        print(f"Project '{project_name}' created successfully with display name '{display_name}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")

if __name__ == "__main__":
    create_project()