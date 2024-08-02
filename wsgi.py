import os
import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from main_app import app as portal_app

# Get the base directory of the WartemProjectHub
base_dir = os.path.dirname(os.path.abspath(__file__))

# Add the paths to the projects dynamically
projects_dir = os.path.join(base_dir, 'projects')
for project in os.listdir(projects_dir):
    project_path = os.path.join(projects_dir, project)
    if os.path.isdir(project_path):
        sys.path.insert(0, project_path)

# Import the project apps dynamically
project_apps = {}
for project in os.listdir(projects_dir):
    if os.path.isdir(os.path.join(projects_dir, project)):
        try:
            module = __import__(f'{project}.app', fromlist=['app'])
            project_apps[f'/{project}'] = module.app
        except ImportError:
            print(f"Warning: Could not import app from {project}")

# Create the DispatcherMiddleware to route to different projects
application = DispatcherMiddleware(portal_app, project_apps)
